import os
import base64
from hashlib import sha256

import flask

from govbot import proposal_filters as pf
from govbot import firestore
from govbot import snapshot
from govbot import logger
from govbot.twitter import GovTweeter, enqueue_status_update_tweets


def reply_tweet_entry(req):
    if req.json.get("secret") != os.environ["APP_SECRET"]:
        logger.send_msg(
            severity="ERROR",
            message="Received unauthorized secret",
            received_secret=req.json.get("secret"),
        )
        return flask.Response(status=401)

    proposal_id = req.json["proposal_id"]
    tweet_str_func_name = req.json["func_name"]
    in_reply_to_status_id = req.json["in_reply_to_status_id"]

    proposal = snapshot.get_proposal(proposal_id)

    gov_tweeter = GovTweeter()
    status = getattr(gov_tweeter, tweet_str_func_name)(proposal)
    if status is not None:
        gov_tweeter.update_twitter_status(
            status, in_reply_to_status_id, auto_populate_reply_metadata=True
        )

    return flask.Response(status=200)


def webhook_entry(req):
    """Entrypoint for the webhook based cloud function"""
    secret = sha256(req.json.get("secret").encode("utf-8")).hexdigest()
    if secret != os.environ["SNAPSHOT_SECRET"]:
        logger.send_msg(
            severity="ERROR",
            message="Received unauthorized secret",
            received_secret=req.json.get("secret"),
        )
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
        if proposal.space.followers_count > 1000:
            status = gov_tweeter.update_twitter_status(gov_tweeter.new_proposal_status(proposal))
            if status:
                enqueue_status_update_tweets(status.id, proposal)

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
