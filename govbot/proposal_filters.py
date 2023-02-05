import json
import typing
from datetime import datetime, timedelta
from pkg_resources import resource_filename
from itertools import filterfalse

from govbot import snapshot, firestore, twitter
from govbot.snapshot_schema import snapshot_schema as ss


def apply_filters(filters: typing.List[typing.Callable], proposals: typing.List[ss.Proposal]):
    """Filter a list of proposals using the provided filters

    Note: Filter using low cost and highly restrictive filters first for best performance
    """
    for fil in filters:
        # If the filter returns false for the proposal, the proposal will be included
        proposals = filterfalse(fil, proposals)  # type: ignore
    return proposals


def has_recently_tweeted_space(proposal: ss.Proposal) -> bool:
    """Check if a tweet about a proposal from this space has been sent in the last day"""
    space_name = twitter._get_space_name(proposal)

    govTweeter = twitter.GovTweeter()
    return govTweeter.has_recently_tweeted(space_name, timedelta(days=1))


def has_already_tweeted_prop(proposal: ss.Proposal) -> bool:
    # TODO: Store tweets in Firestore, query from that
    govTweeter = twitter.GovTweeter()
    return govTweeter.has_recently_tweeted(proposal.title, timedelta(days=10))


def is_old_proposal(proposal):
    """Where 'old' is defined as a proposal created more than 15 minutes ago"""
    return (datetime.now() - datetime.fromtimestamp(proposal.created)).seconds > 9000


def is_not_contested_proposal(proposal: ss.Proposal) -> bool:
    """Returns whether the provided proposal is contested

    A proposal is considered contested when it is close to being tied
    """
    results = snapshot.get_proposal_results(proposal)
    if results is None:
        return True

    vote_sum = sum(results.values())
    if vote_sum == 0.0:
        return True

    if len(results.keys()) == 1:
        # Edge case where all of the proposal choices are the same string
        return True

    result_percentages = sorted([votes / vote_sum for votes in results.values()])
    if result_percentages[-1] - result_percentages[-2] < 0.1:
        return False
    return True


def is_low_activity_proposal(proposal: ss.Proposal) -> bool:
    """Fewer voters than an interesting proposal might have

    Obviously not useful for new proposals

    This considers whether the proposal has:
        - more than 10 voters
        - more than X% above avg activity for proposals in the space
    """
    num_votes = proposal.votes
    if num_votes < 10:
        return True

    avg_voters = firestore.get_avg_space_voters(proposal.space.id)
    return num_votes < avg_voters * 1.5


def is_blocked_space(proposal: ss.Proposal) -> bool:
    """Any space that isn't in the allowed_spaces json is considered blocked

    The list of allowed spaces is all spaces with more than 3 proposals and >10 avg voters
    """
    with open(resource_filename("govbot", "allowed_spaces.json"), "r") as fi:
        allowed_spaces = json.load(fi)

    # https://raw.githubusercontent.com/snapshot-labs/snapshot-spaces/master/spaces/verified.json
    with open(resource_filename("govbot", "verified_spaces.json"), "r") as fi:
        verified_spaces = json.load(fi)
        blocked_spaces = [s for s, v in verified_spaces.items() if v == -1]

    return proposal.space.id not in allowed_spaces or proposal.space.id in blocked_spaces


def is_non_member_author(proposal: ss.Proposal) -> bool:
    return proposal.author not in proposal.space.members


def is_low_follower_space(proposal: ss.Proposal) -> bool:
    return proposal.space.followers_count < 100


def has_blocked_words(proposal: ss.Proposal) -> bool:
    """A crude attempt to avoid tweeting about dev/spam proposals"""
    return True if "TEST" in proposal.title.upper() else False
