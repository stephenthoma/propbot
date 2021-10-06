"""This cloud function will be triggered on a schedule. We will assume that it runs every 15 min.
without fail. This lets us ignore any proposals that were created more than 15 min. ago.
"""

import requests
import time
from datetime import datetime

import tweepy

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"

TW_SECRETS = {
    "consumer_key": "wLid5ZXYbm0Ux4e7gdnLeMpRe",
    "consumer_secret": "oJghmQYDE9NBTlD4xo2mSS9FYkrjEE75R4Jvb6hC4Hj4pabNtA",
    "access_token": "1444758939854204930-k0ezp3yNL3tRcwszFyriWQvA5TANKr",
    "access_secret": "bQmg95bfVyQPqfNcsMGNWTn0kVaiDWPvy73ibMeS9Yfqg",
}

BLOCKLIST = ["upsidedao.eth"]


def get_proposals():
    """Retrieve proposals, then filter out any that don't meet criteria to be posted"""
    with open("./queries/getProposals.graphql", "r") as fi:
        query = fi.read()

    # Retrieve the 25 most recent proposals
    proposals = run_query(query, SNAPSHOT_GRAPH_URL)["data"]["proposals"]

    # Filter out spaces with too few members
    proposals = [p for p in proposals if is_valid_proposal(p)]

    return proposals


def get_proposal(id):
    with open("./queries/getProposal.graphql", "r") as fi:
        query = fi.read()

    return run_query(query, SNAPSHOT_GRAPH_URL, variables={"id": id})["data"]["proposal"]


def is_valid_proposal(proposal):
    """Return True if a proposal meets all criteria, False otherwise

    Current criteria:
        - XXX newer than 15 minutes (frequency that the cron runs)
        - more than 10 members in the space
    """
    # Must be older than 15 minutes
    # now = datetime.now()
    # if (now - datetime.fromtimestamp(proposal["created"])).seconds > 9000:
    #     return False

    # Must have more than X members in the space
    if len(proposal["space"]["members"]) < 10:
        return False

    if proposal["space"]["id"] in BLOCKLIST:
        return False

    return True


def run_query(query, url, headers=None, variables=None):
    """Sends a GraphQL query"""
    res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    res.raise_for_status()
    return res.json()


def format_proposal_status(prop):
    # URLs should be in the following format:
    # https://snapshot.org/#/sushigov.eth/proposal/QmNT8bY7aJRFUMtfbFp9m7JHcUgEVCNZzWE67Crr9oAVrA
    end_date_str = datetime.fromtimestamp(prop["end"]).strftime("%H:%M %b %d %Y")
    url = f"https://snapshot.org/#/{prop['space']['id']}/proposal/{prop['id']}"
    name = f"@{prop['space']['twitter']}" if prop["space"]["twitter"] else prop["space"]["name"]

    str = f"⚡️ {name} proposal: \"{prop['title']}\"\n\nVoting ends {end_date_str}\n{url}"
    return str


def update_twitter_status(status, api):
    result = api.update_status(status)
    return result


def get_tweepy_api():
    auth = tweepy.OAuthHandler(TW_SECRETS["consumer_key"], TW_SECRETS["consumer_secret"])
    auth.set_access_token(TW_SECRETS["access_token"], TW_SECRETS["access_secret"])
    return tweepy.API(auth)


def webhook_entry(req):
    prop_id = req.json.id.split("proposal/")
    prop = get_proposal(prop_id)
    if is_valid_proposal(prop):
        status = format_proposal_status(prop)
        update_twitter_status(status, api)


def main(event=None, context=None):
    proposals = get_proposals()
    if len(proposals) == 0:
        print("No valid proposals found to post")
        return
    else:
        print(f"Found {len(proposals)} proposals")

    api = get_tweepy_api()
    for prop in proposals:
        status = format_proposal_status(prop)
        update_twitter_status(status, api)


if __name__ == "__main__":
    proposals = get_proposals()
    api = get_tweepy_api()
    for prop in proposals:
        status = format_proposal_status(prop)
        print(status)
