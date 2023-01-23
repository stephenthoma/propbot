import os
import datetime
from typing import Optional

import tweepy
from tweepy.models import Status
import pytz

from govbot import snapshot, queue
from govbot.snapshot_schema import snapshot_schema as ss


def enqueue_status_update_tweets(in_reply_to_status_id: str, proposal: ss.Proposal):
    payload = {
        "proposal_id": proposal.id,
        "func_name": "vote_update_status",
        "in_reply_to_status_id": in_reply_to_status_id,
    }
    proposal_half_complete_secs = int((proposal.end - proposal.start) / 2)
    proposal_complete_secs = int(proposal.end - proposal.start)

    queue.enqueue_task("followup-tweet-queue", payload, proposal_half_complete_secs)
    queue.enqueue_task("followup-tweet-queue", payload, proposal_complete_secs)


class GovTweeter:
    def __init__(self):
        self.is_production = os.environ["GOVBOT_PRODUCTION"] == "true"
        self.api = self._get_tweepy_api()

    def _get_tweepy_api(self):
        CONSUMER_KEY = os.environ["CONSUMER_KEY"]
        CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
        ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
        ACCESS_SECRET = os.environ["ACCESS_SECRET"]

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        return tweepy.API(auth)

    def vote_update_status(self, proposal: ss.Proposal) -> str:
        """Create a string for a reply tweet updating on the proposal's votes"""
        results = snapshot.get_proposal_results(proposal)
        # TODO: make it pretty
        return str(results)

    def new_proposal_status(self, proposal: ss.Proposal) -> str:
        """Create a string for a tweet about a new proposal"""
        end_date_str = _get_human_time(proposal.end)
        url = snapshot.get_proposal_url(proposal)
        name = _get_space_name(proposal)

        return f'⚡️ {name} proposal: "{proposal.title}"\n\nVoting ends {end_date_str}\n{url}'

    def contested_proposal_status(self, proposal: ss.Proposal) -> str:
        """Create a string for a tweet about a contested proposal"""
        end_date_str = _get_human_time(proposal.end)
        url = snapshot.get_proposal_url(proposal)
        name = _get_space_name(proposal)

        return f'⚔️ [contested] {name} proposal: "{proposal.title}"\n\nVoting ends soon {end_date_str}\n{url}'

    def high_activity_proposal_status(self, proposal: ss.Proposal) -> str:
        """Create a string for a tweet about a contested proposal"""
        end_date_str = _get_human_time(proposal.end)
        url = snapshot.get_proposal_url(proposal)
        name = _get_space_name(proposal)

        return f'🔥 [high activity] {name} proposal: "{proposal.title}"\n\nVoting ends {end_date_str}\n{url}'

    def weekly_summary_status(self) -> str:
        stats = snapshot.get_week_summary()

        return (
            f'📈 [weekly summary]\n- {stats["num_proposals"]:,} new proposals'
            f'\n- {stats["num_votes"]:,} votes cast\n\n'
            f"Fastest growing spaces:\n"
            f'- {stats["top_growth_spaces"][0][0]}: +{stats["top_growth_spaces"][0][1]:,} followers\n'
            f'- {stats["top_growth_spaces"][1][0]}: +{stats["top_growth_spaces"][1][1]:,} followers\n'
            f'- {stats["top_growth_spaces"][2][0]}: +{stats["top_growth_spaces"][2][1]:,} followers'
        )

    def update_twitter_status(
        self,
        status: str,
        in_reply_to_status_id: Optional[str] = None,
        auto_populate_reply_metadata: Optional[bool] = False,
    ) -> Optional[Status]:
        if self.is_production:
            return self.api.update_status(
                status,
                in_reply_to_status_id=in_reply_to_status_id,
                auto_populate_reply_metadata=auto_populate_reply_metadata,
            )

    def has_recently_tweeted(self, search_str: str, cutoff_delta: datetime.timedelta) -> bool:
        cutoff_time = pytz.utc.localize(datetime.datetime.now() - cutoff_delta)

        tweets = self.api.user_timeline(count=25)
        if tweets[-1].created_at > cutoff_time:
            # TODO: Improve this retrieval logic lol
            tweets = self.api.user_timeline(count=100)
            assert tweets[-1].created_at <= cutoff_time

        included_tweets = [t for t in tweets if t.created_at >= cutoff_time]
        filtered_tweets = [t for t in included_tweets if search_str in t.text]
        return len(filtered_tweets) > 0


def _get_human_time(unix_time: int) -> str:
    return datetime.datetime.fromtimestamp(unix_time).strftime("%H:%M %b %d %Y")


def _get_space_name(proposal: ss.Proposal) -> str:
    if proposal.space.twitter:
        return f"@{proposal.space.twitter}"
    else:
        return proposal.space.name
