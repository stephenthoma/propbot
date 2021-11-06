import datetime
import typing
import json
from pkg_resources import resource_filename
from collections import defaultdict, Counter

import requests
from sgqlc.operation import Operation

from snapshot_schema import snapshot_schema as ss

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORE_API = "https://score.snapshot.org/api/scores"

PROPOSAL_FIELDS = [
    "id",
    "title",
    "start",
    "created",
    "end",
    "snapshot",
    "network",
    "state",
    "author",
    "choices",
]
PROPOSAL_SPACE_FIELDS = [
    "id",
    "name",
    "twitter",
]


def get_proposal_results(proposal: dict) -> typing.Optional[typing.Dict[str, float]]:
    """Calculate the results of a proposal by retrieving all votes, then requesting scores

    Returns:
        dict: The keys are the proposal choices, values are the sum of votes for each choice
    """
    votes = get_votes(proposal["id"])
    voter_addresses = [v["voter"] for v in votes]
    scores = get_scores(
        proposal["space"]["id"],
        proposal["strategies"],
        proposal["network"],
        int(proposal["snapshot"]),
        voter_addresses,
    )

    if scores is None:
        return None

    # Votes have a choice int that is 1-indexed map to the choices list from the proposal
    choice_map = {i + 1: choice for i, choice in enumerate(proposal["choices"])}

    results = {choice: 0.0 for choice in proposal["choices"]}
    try:
        for vote in votes:
            choice = choice_map[vote["choice"]]
            # Not sure why scores is an array here?
            results[choice] += scores[0][vote["voter"]]
    except:
        return None

    return results


def get_scores(space_id: str, strategies: list, network: str, snapshot: int, addresses: list):
    """Retrieve the vote balance for a list of voter addresses"""
    params = {
        "space": space_id,
        "network": network,
        "snapshot": snapshot,
        "strategies": strategies,
        "addresses": addresses,
    }

    res_json = requests.post(SNAPSHOT_SCORE_API, json={"params": params}).json()

    if "error" in res_json:
        print("Error:", res_json["error"]["data"]["reason"])
        return None
    else:
        return res_json["result"]["scores"]


def get_votes(proposal_id: str) -> list[ss.Vote]:
    op = Operation(ss.Query)
    op_votes = op.votes(where={"proposal": proposal_id}, first=10000)
    op_votes.__fields__("choice", "voter")
    return run_operation(op).votes


def get_ending_proposals() -> list[ss.Proposal]:
    op = Operation(ss.Query, name="getEndingProposals")
    op_proposals = op.proposals(
        first=50, where={"state": "active"}, order_by="end", order_direction="asc"
    )
    op_proposals.__fields__(*PROPOSAL_FIELDS)
    op_proposals.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposals


def get_proposal(proposal_id: str) -> ss.Proposal:
    op = Operation(ss.Query, name="getProposal")
    op_proposal = op.proposal(id=proposal_id)
    op_proposal.__fields__(*PROPOSAL_FIELDS)
    op_proposal.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposal


def get_latest_proposals() -> list[ss.Proposal]:
    op = Operation(ss.Query, name="getProposals")
    op_proposals = op.proposals(
        first=25, where={"state": "open"}, order_by="created", order_direction="desc"
    )
    op_proposals.__fields__(*PROPOSAL_FIELDS)
    op_proposals.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposals


def get_space_follows(space_id: str) -> list[ss.Follow]:
    op = Operation(ss.Query, name="getSpaceFollows")
    op_follows = op.follows(where={"space": space_id})
    op_follows.follower()
    return run_operation(op)


def get_week_summary() -> dict:
    """Get a summary of activity on the snapshot platform from the last week"""
    a_week_ago = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())
    op = Operation(ss.Query)
    op_votes = op.votes(where={"created_gte": a_week_ago}, first=10e5)
    op_votes.id()

    op_proposals = op.proposals(where={"created_gte": a_week_ago}, first=10e5)
    op_proposals.id()

    op_follows = op.follows(where={"created_gte": a_week_ago}, first=10e5)
    op_follows.space().id()
    op_follows.space().name()

    res = run_operation(op)

    counts = Counter([f.space.name for f in res.follows])
    return {
        "num_votes": len(res.votes),
        "num_proposals": len(res.proposals),
        "top_growth_spaces": counts.most_common(3),
    }


def get_proposal_url(space_id: str, proposal_id: str) -> str:
    """Get the URL of the proposal on the Snapshot website"""
    return f"https://snapshot.org/#/{space_id}/proposal/{proposal_id}"


def run_operation(op, variables: dict = None):
    return op + run_query(str(op), SNAPSHOT_GRAPH_URL, variables)


def run_query(query: str, url: str, headers: dict = None, variables: dict = None) -> dict:
    """Sends a GraphQL query"""
    res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    try:
        res.raise_for_status()
    except requests.HTTPError as err:
        print("Error: Got bad status code in GraphQL query response:", res.text)
        raise err

    return res.json()
