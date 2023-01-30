import datetime
from typing import Callable, Optional, Dict, Any
from collections import Counter

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from sgqlc.operation import Operation
from govbot.snapshot_schema import snapshot_schema as ss
from govbot import logger

SNAPSHOT_GRAPH_URL = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORE_API = "https://score.snapshot.org/api/scores"

PROPOSAL_FIELDS = [
    "author",
    "choices",
    "created",
    "end",
    "id",
    "network",
    "scores",
    "scores_total",
    "snapshot",
    "start",
    "state",
    "strategies",
    "title",
    "votes",
]
PROPOSAL_SPACE_FIELDS = [
    "followers_count",
    "id",
    "members",
    "name",
    "twitter",
]


def get_proposal_results(proposal: ss.Proposal) -> Optional[Dict[str, float]]:
    """Calculate the results of a proposal by retrieving all votes, then requesting scores

    Returns:
        dict: The keys are the proposal choices, values are the sum of vote scores for each choice
    """
    if proposal.votes == 0:
        return None

    results = dict(zip(proposal.choices, proposal.scores))
    return results


def get_ending_proposals() -> list[ss.Proposal]:
    op = Operation(ss.Query, name="getEndingProposals")
    day_after_tomorrow = int((datetime.datetime.now() + datetime.timedelta(days=2)).timestamp())

    op_proposals: Any = op.proposals(
        first=100,
        where={"state": "active", "end_lte": day_after_tomorrow},
        order_by="end",
        order_direction="asc",
    )
    op_proposals.__fields__(*PROPOSAL_FIELDS)
    op_proposals.space.__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposals


def get_proposal(proposal_id: str) -> ss.Proposal:
    op = Operation(ss.Query, name="getProposal")
    op_proposal: Any = op.proposal(id=proposal_id)
    op_proposal.__fields__(*PROPOSAL_FIELDS)
    op_proposal.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    op_proposal.strategies().__fields__("name", "params")
    return run_operation(op).proposal


def get_latest_proposals() -> list[ss.Proposal]:
    op = Operation(ss.Query, name="getProposals")
    op_proposals: Any = op.proposals(
        first=25, where={"state": "open"}, order_by="created", order_direction="desc"
    )
    op_proposals.__fields__(*PROPOSAL_FIELDS)
    op_proposals.space().__fields__(*PROPOSAL_SPACE_FIELDS)
    return run_operation(op).proposals


def get_spaces():
    def get_space_page(page_size: int, skip: int):
        op = Operation(ss.Query, name="getSpaces")
        op_space = op.spaces(first=page_size, skip=skip)
        op_space.__fields__("id")
        return run_operation(op).spaces

    return get_paginated(get_space_page, 100)


def get_week_summary() -> dict:
    """Get a summary of activity on the snapshot platform from the last week"""
    a_week_ago = int((datetime.datetime.now() - datetime.timedelta(days=7)).timestamp())

    def get_new_proposals(page_size: int, skip: int):
        op = Operation(ss.Query)
        op_proposals: Any = op.proposals(
            first=page_size, skip=skip, where={"created_gte": a_week_ago}
        )
        op_proposals.id()
        return run_operation(op).proposals

    def get_new_follows(page_size: int, skip: int):
        op = Operation(ss.Query)
        op_follows: Any = op.follows(first=page_size, skip=skip, where={"created_gte": a_week_ago})
        op_follows.space().__fields__("id", "name")
        return run_operation(op).follows

    proposals_res = get_paginated(get_new_proposals, 1000)
    follows_res = get_paginated(get_new_follows, 1000)

    counts = Counter([f.space.name for f in follows_res])
    return {
        "num_votes": get_count_weeks_votes(),
        "num_proposals": len(proposals_res),
        "top_growth_spaces": counts.most_common(3),
    }


def get_votes_from_timespan(start, end):
    start_stamp = int(start.timestamp())
    end_stamp = int(end.timestamp())
    page_size = 1000
    skip = 0
    votes = []

    while True:
        op = Operation(ss.Query)
        op_vote = op.votes(
            first=page_size,
            skip=skip,
            where={"created_gte": start_stamp, "created_lte": end_stamp},
        )
        op_vote.__fields__("id")
        page = run_operation(op)

        if not page or "errors" in page or not page.votes or len(page.votes) == 0:
            if "errors" in page:
                logger.send_msg(
                    "Error while fetching votes from timespan",
                    severity="WARNING",
                    error_message=page["errors"],
                )
            break

        skip += page_size
        votes.extend(page.votes)
    return votes


def subdivide_date_range(start_time, end_time, count) -> list:
    res = []

    diff = (end_time - start_time) // count
    for idx in range(0, count):
        res.append((start_time + idx * diff))

    return res


def get_count_weeks_votes() -> int:
    """The API caps results at 5000 per time range. So split into multiple queries and sum"""

    vote_sum = 0
    week_end_time = datetime.datetime.now()
    week_start_time = week_end_time - datetime.timedelta(days=7)
    time_chunks = subdivide_date_range(week_start_time, week_end_time, 21)
    for i, start_time in enumerate(time_chunks[:-1]):
        end_time = time_chunks[i + 1]
        days_votes = len(get_votes_from_timespan(start_time, end_time))

        vote_sum += days_votes
        end_time = start_time

    return vote_sum


def get_proposal_url(proposal: ss.Proposal) -> str:
    """Get the URL of the proposal on the Snapshot website"""
    return f"https://snapshot.org/#/{proposal.space.id}/proposal/{proposal.id}"


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


def run_operation(op, variables: Optional[dict] = None):
    return op + run_query(str(op), SNAPSHOT_GRAPH_URL, variables)


def run_query(
    query: str, url: str, headers: Optional[dict] = None, variables: Optional[dict] = None
) -> dict:

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["OPTIONS", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)

    res = session.post(url, json={"query": query, "variables": variables}, headers=headers)

    try:
        res.raise_for_status()
    except requests.HTTPError as err:
        logger.send_msg(
            severity="ERROR",
            message="Got bad status code in GraphQL query response",
            error_message=res.text,
        )
        raise err

    return res.json()
