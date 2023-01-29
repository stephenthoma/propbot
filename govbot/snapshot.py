import json
import datetime
from typing import Callable, Optional, List, Dict
from collections import Counter

import requests
from sgqlc.operation import Operation
from govbot.snapshot_schema import snapshot_schema as ss

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORE_API = "https://score.snapshot.org/api/scores"

PROPOSAL_FIELDS = [
    "id",
    "title",
    "start",
    "created",
    "end",
    "snapshot",
    "strategies",
    "network",
    "state",
    "author",
    "choices",
]
PROPOSAL_SPACE_FIELDS = [
    "id",
    "name",
    "members",
    "twitter",
]


def get_proposal_results(proposal: ss.Proposal) -> Optional[Dict[str, float]]:
    """Calculate the results of a proposal by retrieving all votes, then requesting scores

    Returns:
        dict: The keys are the proposal choices, values are the sum of votes for each choice
    """
    votes = get_votes(proposal.id)
    if votes is None:
        return None

    scores = get_scores(proposal, [v.voter for v in votes])
    if scores is None:
        return None

    # Votes have a choice int that is 1-indexed map to the choices list from the proposal
    choice_map = {i + 1: choice for i, choice in enumerate(proposal.choices)}

    results = {choice: 0.0 for choice in proposal.choices}
    try:
        for vote in votes:
            choice = choice_map[vote.choice]
            # Not sure why scores is an array here?
            results[choice] += scores[0][vote.voter]
    except:
        return None

    return results


def get_scores(proposal: ss.Proposal, addresses: List[str]):
    """Retrieve the vote balance for a list of voter addresses"""
    params = {
        "space": proposal.space.id,
        "network": proposal.network,
        "snapshot": int(proposal.snapshot),
        "strategies": [s.__to_json_value__() for s in proposal.strategies],
        "addresses": addresses,
    }

    res_json = requests.post(SNAPSHOT_SCORE_API, json={"params": params}).json()

    if "error" in res_json:
        print("Error:", json.dumps(res_json["error"]))
        return None
    else:
        return res_json["result"]["scores"]


def get_votes(proposal_id: str) -> list[ss.Vote]:
    op = Operation(ss.Query)
    op_votes = op.votes(where={"proposal": proposal_id})
    op_votes.__fields__("choice", "voter")
    return run_operation(op).votes


def get_ending_proposals() -> list[ss.Proposal]:
    op = Operation(ss.Query, name="getEndingProposals")
    day_after_tomorrow = int((datetime.datetime.now() + datetime.timedelta(days=2)).timestamp())

    op_proposals = op.proposals(
        first=100,
        where={"state": "active", "end_lte": day_after_tomorrow},
        order_by="end",
        order_direction="asc",
    )
    op_proposals.__fields__(*PROPOSAL_FIELDS)
    op_proposals.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposals


def get_proposal(proposal_id: str) -> ss.Proposal:
    op = Operation(ss.Query, name="getProposal")
    op_proposal = op.proposal(id=proposal_id)
    op_proposal.__fields__(*PROPOSAL_FIELDS)
    op_proposal.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    op_proposal.strategies().__fields__("name", "params")
    return run_operation(op).proposal


def get_latest_proposals() -> list[ss.Proposal]:
    op = Operation(ss.Query, name="getProposals")
    op_proposals = op.proposals(
        first=25, where={"state": "open"}, order_by="created", order_direction="desc"
    )
    op_proposals.__fields__(*PROPOSAL_FIELDS)
    op_proposals.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposals


def get_paginated(fetch_func: Callable, page_size: int) -> list:
    skip = 0
    results = []
    while True:
        page = fetch_func(page_size, skip)
        if not page or len(page) == 0:
            break

        skip += page_size
        results.extend(page)

    return results


def get_space_follows(space_id: str) -> list[ss.Follow]:
    def get_follows_page(page_size: int, skip: int):
        op = Operation(ss.Query, name="getSpaceFollows")
        op_follows = op.follows(first=page_size, skip=skip, where={"space": space_id})
        op_follows.follower()
        return run_operation(op).follows

    return get_paginated(get_follows_page, 1000)


def get_spaces():
    def get_space_page(page_size: int, skip: int):
        op = Operation(ss.Query, name="getSpaces")
        op_space = op.spaces(first=page_size, skip=skip)
        op_space.id()
        return run_operation(op).spaces

    return get_paginated(get_space_page, 100)


def get_week_summary() -> dict:
    """Get a summary of activity on the snapshot platform from the last week"""
    a_week_ago = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())
    op = Operation(ss.Query)

    op_proposals: typing.Any = op.proposals(where={"created_gte": a_week_ago}, first=10e5)
    op_proposals.id()

    op_follows = op.follows(where={"created_gte": a_week_ago}, first=10e5)
    op_follows.space().id()
    op_follows.space().name()

    res = run_operation(op)

    counts = Counter([f.space.name for f in res.follows])
    return {
        "num_votes": get_count_weeks_votes(),
        "num_proposals": len(res.proposals),
        "top_growth_spaces": counts.most_common(3),
    }


def get_count_weeks_votes() -> int:
    """The API caps results at 100,000. So split into multiple queries and sum"""

    def get_votes_from_timespan(start, end):
        start_stamp = int(start.timestamp())
        end_stamp = int(end.timestamp())
        op = Operation(ss.Query)
        op_vote = op.votes(where={"created_gte": start_stamp, "created_lte": end_stamp}, first=10e4)
        op_vote.id()
        res = run_operation(op)
        return res.votes

    vote_sum = 0
    end_time = datetime.datetime.now()
    for day_offset in range(1, 8):
        start_time = end_time - datetime.timedelta(days=day_offset)
        days_votes = len(get_votes_from_timespan(start_time, end_time))
        if days_votes == 10e4:
            print("Warning: Vote retrieval likely hit API limit")

        vote_sum += days_votes
        end_time = start_time

    return vote_sum


def get_proposal_url(proposal: ss.Proposal) -> str:
    """Get the URL of the proposal on the Snapshot website"""
    return f"https://snapshot.org/#/{proposal.space.id}/proposal/{proposal.id}"


def run_operation(op, variables: Optional[dict] = None):
    return op + run_query(str(op), SNAPSHOT_GRAPH_URL, variables)


def run_query(
    query: str, url: str, headers: Optional[dict] = None, variables: Optional[dict] = None
) -> dict:
    """Sends a GraphQL query"""
    res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    try:
        res.raise_for_status()
    except requests.HTTPError as err:
        print("Error: Got bad status code in GraphQL query response:", res.text)
        raise err

    return res.json()
