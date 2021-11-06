"""
IDEAS:
    - weekly summary of # proposals accepted + denied, # voters overall. most active spaces?
    - high activity proposal alert tweet. when # voters is X std deviations above average
    - need to make an allowlist of spaces so i can more confidently turn on auto tweets
    - consider adding cashtags to tweets?
    - make a mapping of space name to project twitter @
    - make a mapping of string to project twitter @ -- eg "Convex Finance" gets replaced with @convexfinance
    - add circuit breaker to prevent @ tagging a project more than once a day
"""

import json
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
        govTweeter = GovTweeter()
        govTweeter.tweet_proposal(prop)

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
    """Entrypoint for the pub-sub based cloud function

    This cloud function will be triggered on a schedule. We will assume that it runs every 15 min.
    without fail. This lets us ignore any proposals that were created more than 15 min. ago.
    """
    print(event, context)
    govTweeter = GovTweeter()

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
            status = govTweeter.contested_proposal_status(prop)
            govTweeter.update_twitter_status(status)
            firestore.store_contested_proposal_tweet(prop.id)


def dev_get_new():
    govTweeter = GovTweeter()
    new_proposals = snapshot.get_latest_proposals()
    filters = [
        pf.is_old_proposal,
        pf.has_blocked_words,
        pf.is_blocked_space,
        pf.is_low_follower_space,
        pf.has_recently_tweeted_space,
        pf.has_already_tweeted_prop,
    ]
    proposals = pf.apply_filters(filters, new_proposals)

    for prop in proposals:
        status = govTweeter.new_proposal_status(prop)
        govTweeter.update_twitter_status(status)


if __name__ == "__main__":
    # cron_entry()
    dev_get_new()
