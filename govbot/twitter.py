import os
from datetime import datetime

import tweepy

from govbot import snapshot


class GovTweeter:
    def __init__(self):
        is_production = os.environ["GOVBOT_PRODUCTION"] == "true"
        self.api = self._get_tweepy_api() if is_production else TweepyAPIMock()

    def new_proposal_status(self, prop: dict) -> str:
        """Create a string for a tweet about a new proposal"""
        end_date_str = get_human_time(prop["end"])
        url = snapshot.get_proposal_url(prop["space"]["id"], prop["id"])
        name = get_space_name(prop)

        return f"⚡️ {name} proposal: \"{prop['title']}\"\n\nVoting ends {end_date_str}\n{url}"

    def contested_proposal_status(self, prop: dict) -> str:
        """Create a string for a tweet about a contested proposal"""
        end_date_str = get_human_time(prop["end"])
        url = snapshot.get_proposal_url(prop["space"]["id"], prop["id"])
        name = get_space_name(prop)

        return f"⚔️ [contested] {name} proposal: \"{prop['title']}\"\n\nVoting ends soon {end_date_str}\n{url}"

    def _get_tweepy_api(self):
        CONSUMER_KEY = os.environ["CONSUMER_KEY"]
        CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
        ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
        ACCESS_SECRET = os.environ["ACCESS_SECRET"]

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        return tweepy.API(auth)

    def update_twitter_status(self, status: str) -> dict:
        """Post a tweet"""
        result = self.api.update_status(status)
        return result


def get_human_time(unix_time) -> str:
    return datetime.fromtimestamp(unix_time).strftime("%H:%M %b %d %Y")


def get_space_name(proposal) -> str:
    # if proposal["space"]["twitter"]:
    #     return f"@{proposal['space']['twitter']}"
    # else:
    return proposal["space"]["name"]


class TweepyAPIMock:
    """Used to mock the Tweepy API instance in development. Prints to stdout instead of tweeting"""

    def update_status(self, status):
        print("[ DEBUG ]\n", status, "\n[ DEBUG ]")
