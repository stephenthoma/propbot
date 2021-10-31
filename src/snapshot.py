import json

import requests

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORE_API = "https://score.snapshot.org/api/scores"


def is_contested_proposal(id: str) -> bool:
    """Returns whether the provided proposal is contested

    A proposal is considered contested when:
        - [TODO] it will end soon
        - it is close to being tied, +-20%
    """
    prop = get_proposal(id)
    votes = get_votes(id)
    addresses = [v["voter"] for v in votes]
    scores = get_scores(
        prop["space"]["id"], prop["strategies"], prop["network"], prop["snapshot"], addresses
    )

    # Votes have a choice int that is 1-indexed map to the choices list from the proposal
    choice_map = {i + 1: choice for i, choice in enumerate(prop["choices"])}

    # Initialize results dict
    results = {choice: 0.0 for choice in prop["choices"]}
    for vote in votes:
        choice = choice_map[vote["choice"]]
        # Not sure why scores is an array here?
        results[choice] += scores[0][vote["voter"]]

    vote_sum = sum(results.values())
    if vote_sum == 0.0:
        return False  # Return early to avoid division by zero

    result_percentages = {choice: votes / vote_sum for choice, votes in results.items()}
    tied_percentage = 1 / len(results)

    # Arbitrarily grab a result percentage and check how close to the percentage that would be a
    # tie (for the number of choices this proposal has. eg 0.5 for 2 choices, 0.3 for 3 etc)
    # If the resulting percentage is within 20% of a tie, we say it's contested
    print(len(scores[0]))
    print(results)
    print(result_percentages)
    print(list(result_percentages.values())[0] - tied_percentage)
    if abs(list(result_percentages.values())[0] - tied_percentage) < 0.2:
        return True

    return False


def get_scores(space_id: str, strategies: list, network: str, snapshot: int, addresses: list):
    params = {
        "space": space_id,
        "network": network,
        "snapshot": snapshot,
        "strategies": strategies,
        "addresses": addresses,
    }
    res = requests.post(SNAPSHOT_SCORE_API, json={"params": params})
    return res.json()["result"]["scores"]


def get_votes(proposal_id: str) -> list:
    """Get a list of all votes for a given proposal_id"""
    with open("./queries/getVotes.graphql", "r") as fi:
        query = fi.read()

    votes = run_query(query, SNAPSHOT_GRAPH_URL, variables={"id": proposal_id})
    return votes["data"]["votes"]


def get_proposals() -> dict:
    """Retrieve proposals, then filter out any that don't meet criteria to be posted"""
    with open("./queries/getProposals.graphql", "r") as fi:
        query = fi.read()

    # Retrieve the 25 most recent proposals
    proposals = run_query(query, SNAPSHOT_GRAPH_URL)["data"]["proposals"]

    return proposals


def get_proposal(id: str) -> dict:
    """Retrieve a single proposal with the id passed in"""
    with open("./queries/getProposal.graphql", "r") as fi:
        query = fi.read()

    return run_query(query, SNAPSHOT_GRAPH_URL, variables={"id": id})["data"]["proposal"]


def run_query(query: str, url: str, headers: dict = None, variables: dict = None) -> dict:
    """Sends a GraphQL query"""
    res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    try:
        res.raise_for_status()
    except requests.HTTPError as err:
        print(res.text)
        raise err

    return res.json()


if __name__ == "__main__":

    is_contested_proposal("QmWqj4HqaY5eFQAKJjTc1BJDXy4HQuTJcGf62qvyRpjFfq")
