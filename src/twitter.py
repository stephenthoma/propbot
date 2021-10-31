import os
from datetime import datetime

import tweepy


class GovTweeter:
    def __init__(self):
        is_production = os.environ["GOVBOT_PRODUCTION"] == "true"

        consumer_key = os.environ["CONSUMER_KEY"]
        consumer_secret = os.environ["CONSUMER_SECRET"]
        access_token = os.environ["ACCESS_TOKEN"]
        access_secret = os.environ["ACCESS_SECRET"]

        self.api = self.get_tweepy_api() if is_production else TweepyAPIMock()

    def tweet_proposal(self, prop: dict):
        formatted_prop = self.format_proposal_status(prop)
        self.update_twitter_status(formatted_prop)

    def format_proposal_status(self, prop: dict) -> str:
        """The propbot tweets about governance proposals in a specific format. This function takes
        a proposal object returned by the Snapshot GraphQL API and returns a properly formatted str

        Args:
            prop (dict): Snapshot proposal (see the query to reference expected keys)

        Returns:
            str: The tweet ready to be tweeted
        """
        # URLs should be in the following format:
        # https://snapshot.org/#/sushigov.eth/proposal/QmNT8bY7aJRFUMtfbFp9m7JHcUgEVCNZzWE67Crr9oAVrA
        end_date_str = datetime.fromtimestamp(prop["end"]).strftime("%H:%M %b %d %Y")
        url = f"https://snapshot.org/#/{prop['space']['id']}/proposal/{prop['id']}"
        name = f"@{prop['space']['twitter']}" if prop["space"]["twitter"] else prop["space"]["name"]

        str = f"⚡️ {name} proposal: \"{prop['title']}\"\n\nVoting ends {end_date_str}\n{url}"
        return str

    def get_tweepy_api(self):
        auth = tweepy.OAuthHandler(self.SECRETS["consumer_key"], self.SECRETS["consumer_secret"])
        auth.set_access_token(self.SECRETS["access_token"], self.SECRETS["access_secret"])
        return tweepy.API(auth)

    def update_twitter_status(self, status: str) -> dict:
        """Equivalent to posting a tweet"""
        result = self.api.update_status(status)
        return result


class TweepyAPIMock:
    """Used to mock the Tweepy API instance in development. Prints to stdout intsead of tweeting"""

    def update_status(self, status):
        print("[ DEBUG ]\n", status, "\n[ DEBUG ]")
