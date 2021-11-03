import json
import typing
from datetime import datetime, timedelta
from pkg_resources import resource_filename

from govbot import snapshot, firestore, twitter


def apply_filters(filters: typing.List[typing.Callable], proposals):
    """Filter a list of proposals using the provided filters

    Note: Low cost  nd/or highly restrictive filters should be put earlier in the list
    """
    for fil in filters:
        proposals = filter(fil, proposals)
    return proposals


def has_recently_tweeted_space(proposal: dict) -> bool:
    space_name = twitter.get_space_name(proposal)

    govTweeter = twitter.GovTweeter()
    return not govTweeter.has_recently_tweeted(space_name, timedelta(days=1))


def has_already_tweeted_prop(proposal: dict) -> bool:
    govTweeter = twitter.GovTweeter()
    return not govTweeter.has_recently_tweeted(proposal["title"], timedelta(days=10))


def is_new_proposal(proposal):
    """Where old == created more than 15 minutes ago"""
    if (datetime.now() - datetime.fromtimestamp(proposal["created"])).seconds < 9000:
        return True


def is_contested_proposal(proposal: dict) -> bool:
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
    if abs(list(result_percentages.values())[0] - tied_percentage) < 0.2 * tied_percentage:
        return True

    return False


def is_high_activity_proposal(proposal: dict) -> bool:
    """More voters than usual

    This considers whether the proposal has:
        - more than an arbitrary threshold of voters (currently 10)
        - more than 30% above avg activity for proposals in the space
    """
    num_votes = len(snapshot.get_votes(proposal["id"]))
    if num_votes < 10:
        return False

    avg_voters = firestore.get_avg_space_voters(proposal["space"]["id"])
    if num_votes < avg_voters * 1.3:
        return False

    return True


def is_allowed_space(proposal):
    """The list of allowed spaces is all spaces with more than 3 proposals + >10 avg voters"""
    with open(resource_filename("govbot", "allowed_spaces.json"), "r") as fi:
        spaces = json.load(fi)

    if proposal["space"]["id"] in spaces:
        return True


def is_popular_space(proposal):
    """Check if thet proposal's space has more than 100 followers"""
    if len(snapshot.get_space_followers(proposal["space"]["id"])) > 10:
        return True


def has_blocked_words(proposal):
    """A crude attempt to avoid tweeting about test proposals"""
    if "TEST" in proposal["title"].upper():
        print("Ignoring proposal with test in title", proposal["title"])
        return False

    return True
