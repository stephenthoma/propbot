"""
IDEAS:
    - high activity proposal alert tweet. when # voters is X std deviations above average
    - consider adding cashtags to tweets?
    - make a mapping of space name to project twitter @
    - make a mapping of string to project twitter @ -- eg "Convex Finance" gets replaced with @convexfinance
PROBLEMS:
    - has_already_tweeted_prop filter will prevent high activity / contested tweets for props that
      were tweeted about at creation time
"""

import json
import base64
from datetime import datetime

from govbot import proposal_filters as pf
from govbot import firestore
from govbot import snapshot
from govbot.twitter import GovTweeter


def webhook_entry(req):
    """Entrypoint for the webhook based cloud function"""
    prop_id = req.json["id"].split("proposal/")[1]
    prop = snapshot.get_proposal(prop_id)
    if is_valid_proposal(prop):
        gov_tweeter = GovTweeter()
        gov_tweeter.tweet_proposal(prop)

    filters = [
        pf.is_old_proposal,
        pf.has_blocked_words,
        pf.is_blocked_space,
        pf.is_low_follower_space,
        pf.has_recently_tweeted_space,
        pf.has_already_tweeted_prop,
    ]
    proposals = pf.apply_filters(filters, [prop])

    return {"status": "success"}


def cron_entry(event=None, context=None):
    """Entrypoint for the pub-sub based cloud function"""
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


def dev_get_new():
    gov_tweeter = GovTweeter()
    new_proposals = snapshot.get_latest_proposals()
    filters = [
        # pf.is_old_proposal,
        pf.has_blocked_words,
        pf.is_blocked_space,
        pf.is_low_follower_space,
        pf.has_recently_tweeted_space,
        pf.has_already_tweeted_prop,
    ]
    proposals = pf.apply_filters(filters, new_proposals)

    for prop in proposals:
        status = gov_tweeter.new_proposal_status(prop)
        gov_tweeter.update_twitter_status(status)


if __name__ == "__main__":
    # cron_entry()
    # dev_get_new()
    high_activity_cron()
    # gov_tweeter = GovTweeter()
    # print(snapshot.get_week_summary())
