import json
import typing
from datetime import datetime, timedelta
from pkg_resources import resource_filename

from govbot import snapshot, firestore, twitter
from govbot.snapshot_schema import snapshot_schema as ss


def apply_filters(filters: typing.List[typing.Callable], proposals):
    """Filter a list of proposals using the provided filters

    Note: Filter using low cost and highly restrictive filters first for best performance
    """
    for fil in filters:
        # Invert the filter to exclude proposals that did not meet the filter criteria
        proposals = filter(lambda p: not fil(p), proposals)
    return proposals


def has_recently_tweeted_space(proposal: ss.Proposal) -> bool:
    """Check if a tweet about a proposal from this space has been sent in the last day"""
    space_name = twitter.get_space_name(proposal)

    govTweeter = twitter.GovTweeter()
    return govTweeter.has_recently_tweeted(space_name, timedelta(days=1))


def has_already_tweeted_prop(proposal: ss.Proposal) -> bool:
    # TODO: Store tweets in Firestore, query from that
    govTweeter = twitter.GovTweeter()
    return govTweeter.has_recently_tweeted(proposal.title, timedelta(days=10))


def is_old_proposal(proposal):
    """Where old == created more than 15 minutes ago"""
    return (datetime.now() - datetime.fromtimestamp(proposal.created)).seconds > 9000


def is_not_contested_proposal(proposal: ss.Proposal) -> bool:
    """Returns whether the provided proposal is contested

    A proposal is considered contested when it is close to being tied
    """
    results = snapshot.get_proposal_results(proposal)
    if results is None:
        return False

    tied_percentage = 1 / len(results)

    vote_sum = sum(results.values())
    if vote_sum == 0.0:
        return False

    result_percentages = {choice: votes / vote_sum for choice, votes in results.items()}

    # Arbitrarily grab a result percentage and check how close to the percentage that would be a
    # tie (for the number of choices this proposal has. eg 0.5 for 2 choices, 0.3 for 3 etc)
    # If the resulting percentage is within 20% of a tie it is considered contested
    return not abs(list(result_percentages.values())[0] - tied_percentage) < 0.2 * tied_percentage


def is_low_activity_proposal(proposal: ss.Proposal) -> bool:
    """Fewer voters than an interesting proposal might have

    Obviously not useful for new proposals

    This considers whether the proposal has:
        - more than 10 voters
        - more than 30% above avg activity for proposals in the space
    """
    num_votes = len(snapshot.get_votes(proposal.id))
    if num_votes < 10:
        return False

    avg_voters = firestore.get_avg_space_voters(proposal.space.id)
    return num_votes < avg_voters * 1.3


def is_blocked_space(proposal: ss.Proposal) -> bool:
    """Any space that isn't in the allowed_spaces json is considered blocked

    The list of allowed spaces is all spaces with more than 3 proposals + >10 avg voters
    """
    with open(resource_filename("govbot", "allowed_spaces.json"), "r") as fi:
        spaces = json.load(fi)

    return proposal.space.id not in spaces


def is_low_follower_space(proposal: ss.Proposal) -> bool:
    return len(snapshot.get_space_follows(proposal.space.id)) < 100


def has_blocked_words(proposal: ss.Proposal) -> bool:
    """A crude attempt to avoid tweeting about dev/spam proposals"""
    if "TEST" in proposal.title.upper():
        print("Ignoring proposal with test in title:", proposal.title)
        return True

    return False
