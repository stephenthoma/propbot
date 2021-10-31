import typing
import json

import requests

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORE_API = "https://score.snapshot.org/api/scores"


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


def get_votes(proposal_id: str) -> list:
    """Get a list of all votes for a given proposal_id"""
    with open("./queries/getVotes.graphql", "r") as fi:
        query = fi.read()

    votes = run_query(query, SNAPSHOT_GRAPH_URL, variables={"id": proposal_id})
    return votes["data"]["votes"]


def get_latest_proposals() -> dict:
    with open("./queries/getProposals.graphql", "r") as fi:
        query = fi.read()

    # Retrieve the last 25 proposals
    proposals = run_query(query, SNAPSHOT_GRAPH_URL)["data"]["proposals"]

    return proposals


def get_ending_proposals() -> dict:
    with open("./queries/getEndingProposals.graphql", "r") as fi:
        query = fi.read()

    proposals = run_query(query, SNAPSHOT_GRAPH_URL)["data"]["proposals"]

    return proposals


def get_proposal(id: str) -> dict:
    """Retrieve a single proposal with the id passed in"""
    with open("./queries/getProposal.graphql", "r") as fi:
        query = fi.read()

    return run_query(query, SNAPSHOT_GRAPH_URL, variables={"id": id})["data"]["proposal"]


def get_proposal_url(space_id: str, proposal_id: str) -> str:
    """Get the URL of the proposal on the Snapshot website"""
    return f"https://snapshot.org/#/{space_id}/proposal/{proposal_id}"


def get_space_followers(space_id: str) -> list:
    """Retrieve list of follower ids for a space"""
    with open("./queries/getSpaceFollowers.graphql", "r") as fi:
        query = fi.read()

    return run_query(query, SNAPSHOT_GRAPH_URL, variables={"id": space_id})["data"]["follows"]


def run_query(query: str, url: str, headers: dict = None, variables: dict = None) -> dict:
    """Sends a GraphQL query"""
    res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    try:
        res.raise_for_status()
    except requests.HTTPError as err:
        print(res.text)
        raise err

    return res.json()
