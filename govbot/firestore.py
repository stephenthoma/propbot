import os

from google.cloud import firestore

from govbot import logger

GCP_PROJECT = os.environ["GCP_PROJECT"]

CONTESTED_COLLECTION = "contested_tweets"
AVG_SPACE_COLLECTION = "avg_space_voters"


def get_avg_space_voters(space_id: str) -> float:
    """Retrieve previously computed average voters for a space

    NOTE: If a record isn't found for a space, returns a very high average to
    exclude the space from high activity consideration
    """
    db = firestore.Client(project=GCP_PROJECT)
    doc_val = db.collection(AVG_SPACE_COLLECTION).document(space_id).get()
    if doc_val.exists is True:
        return doc_val.to_dict()["avg_voters"]
    else:
        logger.send_msg(
            f"Did not have average space voters stored for {space_id}", severity="WARNING"
        )
        return 10000.0


def store_space_avg_voters(space_id: str, avg_voters: float):
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


def store_contested_proposal_tweet(proposal_id: str):
    current_ids = get_contested_tweet_proposals()
    update_ids = current_ids + [proposal_id]

    db = firestore.Client(project=GCP_PROJECT)
    doc_ref = db.collection(CONTESTED_COLLECTION).document("proposals")
    doc_ref.set({"ids": update_ids})
