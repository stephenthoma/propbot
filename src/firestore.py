import os

from google.cloud import firestore

GCP_PROJECT = os.environ["GCP_PROJECT"]

CONTESTED_COLLECTION = "contested_tweets"
AVG_SPACE_COLLECTION = "avg_space_voters"


def get_avg_space_voters(space_id: str) -> int:
    """Retrieve previously computed average voters for a space"""
    db = firestore.Client(project=GCP_PROJECT)
    doc_ref = db.collection(AVG_SPACE_COLLECTION).document(space_id)
    return doc_ref.get().to_dict()["avg_voters"]


def store_space_avg_voters(space_id: str, avg_voters: int):
    """Store average voters for a space"""
    db = firestore.Client(project=GCP_PROJECT)
    doc_ref = db.collection(AVG_SPACE_COLLECTION).document(space_id)
    doc_ref.set({"avg_voters": avg_voters})


def has_contested_tweet(proposal_id: str):
    """Check if Firestore contains a record of the given proposal having been tweeted"""
    proposal_ids = get_contested_tweet_proposals()
    return proposal_id in proposal_ids


def get_contested_tweet_proposals() -> list:
    """Retrieve all proposal ids from the contested_tweets collection"""
    db = firestore.Client(project=GCP_PROJECT)
    doc_ref = db.collection(CONTESTED_COLLECTION).document("proposals")
    return doc_ref.get().to_dict()["ids"]


def add_contested_tweet_proposal(proposal_id: str):
    current_ids = get_contested_tweet_proposals()
    update_ids = current_ids + [proposal_id]

    db = firestore.Client(project=GCP_PROJECT)
    doc_ref = db.collection(CONTESTED_COLLECTION).document("proposals")
    doc_ref.set({"ids": update_ids})
