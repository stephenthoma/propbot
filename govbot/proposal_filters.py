import typing
from datetime import datetime, timedelta

from govbot import snapshot, firestore, twitter

BLOCKLIST = ["upsidedao.eth", "compgov.eth"]


def apply_filters(filters: typing.List[typing.Callable], proposals):
    """Filter a list of proposals using the provided filters

    Note: Low cost  nd/or highly restrictive filters should be put earlier in the list
    """
    for fil in filters:
        proposals = filter(fil, proposals)
    return proposals


def has_recently_tweeted_space(proposal: dict) -> bool:
    cutoff_delta = timedelta(days=1)
    space_name = twitter.get_space_name(proposal)

    govTweeter = twitter.GovTweeter()
    return not govTweeter.has_recently_tweeted(space_name, cutoff_delta)


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
        - more than a std. deviation from avg activity for proposals in the space
    """
    if len(snapshot.get_votes(proposal["id"])) < 10:
        return False

    return True


def is_allowed_space(proposal):
    if proposal["space"]["id"] not in BLOCKLIST:
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
