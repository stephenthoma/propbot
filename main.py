import json
from datetime import datetime

import snapshot
from twitter import GovTweeter

BLOCKLIST = ["upsidedao.eth"]


def is_valid_proposal(proposal: dict) -> bool:
    """Return True if a proposal meets all criteria, False otherwise

    Current criteria:
        - XXX newer than 15 minutes (frequency that the cron runs)
        - more than 10 members in the space
    """
    with open("./explore.json", "r") as explore_fi:
        explore = json.load(explore_fi)
    # Must be older than 15 minutes
    now = datetime.now()
    if (now - datetime.fromtimestamp(proposal["created"])).seconds > 9000:
        return False

    # Must have more than X members in the space
    # if len(proposal["space"]["members"]) < 2:
    # return False

    if explore["spaces"].get(proposal["space"]["id"], {}).get("followers", 0) < 10:
        return False

    if proposal["space"]["id"] in BLOCKLIST:
        return False

    # Try to ignore test proposals
    if "TEST" in proposal["title"].upper():
        print("Ignoring proposal with test in title", prop)
        return False

    return True


def webhook_entry(req):
    """Entrypoint for the webhook based cloud function"""
    prop_id = req.json["id"].split("proposal/")[1]
    prop = snapshot.get_proposal(prop_id)
    if is_valid_proposal(prop):
        govTweeter = GovTweeter()
        govTweeter.tweet_proposal(prop)

    return {"status": "success"}


def main(event=None, context=None):
    """Entrypoint for the pub-sub based cloud function

    This cloud function will be triggered on a schedule. We will assume that it runs every 15 min.
    without fail. This lets us ignore any proposals that were created more than 15 min. ago.
    """
    proposals = snapshot.get_proposals()

    if len(proposals) == 0:
        print("No valid proposals found to post")
        return
    else:
        print(f"Found {len(proposals)} proposals")

    govTweeter = GovTweeter()
    for prop in proposals:
        if is_valid_proposal(prop):
            govTweeter.tweet_proposal(prop)


if __name__ == "__main__":
    """Used for development"""
    proposals = snapshot.get_proposals()
    govTweeter = GovTweeter()
    for prop in proposals:
        if is_valid_proposal(prop):
            govTweeter.tweet_proposal(prop)
