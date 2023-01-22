"""
IDEAS:
    - monthly summary
    - add sum of new spaces to summary
    - tweet about proposals that have lots of discussion on twitter
    - consider adding cashtags to tweets?
PROBLEMS:
    - has_already_tweeted_prop filter will prevent high activity / contested tweets for props that
      were tweeted about at creation time
"""

import os
import base64
from hashlib import sha256

import flask

from govbot import proposal_filters as pf
from govbot import firestore
from govbot import snapshot
from govbot.twitter import GovTweeter


def webhook_entry(req):
    """Entrypoint for the webhook based cloud function"""
    if sha256(req.json.get("secret").encode("utf-8")) != os.environ["SNAPSHOT_SECRET"]:
        return flask.Response(status=401)

    proposal_id = req.json["id"].split("proposal/")[1]
    proposal = snapshot.get_proposal(proposal_id)
    gov_tweeter = GovTweeter()

    filters = [
        pf.has_blocked_words,
        pf.is_non_member_author,
        pf.is_blocked_space,
        pf.has_recently_tweeted_space,
        pf.has_already_tweeted_prop,
    ]

    for fil in filters:
        if fil(proposal) == True:
            break
    else:
        # Only tweet new proposals from top spaces (for now) to avoid spam
        if len(snapshot.get_space_follows(proposal.space.id)) > 1000:
            gov_tweeter.update_twitter_status(gov_tweeter.new_proposal_status(proposal))

    return flask.Response(status=200)


def cron_entry(event=None, context=None):
    """Entrypoint for the pub-sub based cloud function"""
    if not event:
        return

    message = base64.b64decode(event["data"])

    if message == b"check_special":
        contested_cron()
        high_activity_cron()
    elif message == b"summary":
        gov_tweeter = GovTweeter()
        gov_tweeter.update_twitter_status(gov_tweeter.weekly_summary_status())


def contested_cron():
    gov_tweeter = GovTweeter()

    ending_proposals = snapshot.get_ending_proposals()
    filters = [
        pf.has_blocked_words,
        pf.is_blocked_space,
        pf.is_low_follower_space,
        pf.is_not_contested_proposal,
        pf.has_recently_tweeted_space,
        pf.has_already_tweeted_prop,
    ]

    filtered_proposals = pf.apply_filters(filters, ending_proposals)
    for prop in filtered_proposals:
        if not firestore.has_contested_tweet(prop.id):
            status = gov_tweeter.contested_proposal_status(prop)
            gov_tweeter.update_twitter_status(status)
            firestore.store_contested_proposal_tweet(prop.id)


def high_activity_cron():
    gov_tweeter = GovTweeter()

    ending_proposals = snapshot.get_ending_proposals()
    filters = [
        pf.has_blocked_words,
        pf.is_blocked_space,
        pf.is_low_follower_space,
        pf.is_low_activity_proposal,
        pf.has_recently_tweeted_space,
        pf.has_already_tweeted_prop,
    ]

    filtered_proposals = pf.apply_filters(filters, ending_proposals)
    for prop in filtered_proposals:
        status = gov_tweeter.high_activity_proposal_status(prop)
        gov_tweeter.update_twitter_status(status)


def _dev_get_new():
    from collections import namedtuple

    Req = namedtuple("request", "json")

    new_proposals = snapshot.get_latest_proposals()
    for proposal in new_proposals:
        req = Req(json={"id": f"proposal/{proposal.id}"})
        webhook_entry(req)


if __name__ == "__main__":
    _dev_get_new()
    # contested_cron()
    # high_activity_cron()
    # print(snapshot.get_week_summary())
