import requests

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"


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
