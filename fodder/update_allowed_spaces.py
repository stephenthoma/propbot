import json

from govbot import snapshot, firestore

if __name__ == "__main__":
    allowed_spaces = []
    spaces = snapshot.get_spaces()
    filtered_spaces = [s for s in spaces if s.proposals_count > 3]
    for space in filtered_spaces:

        stored_num_votes = firestore.get_avg_space_voters(space.id)
        if stored_num_votes > 10 and stored_num_votes != 10000.0:
            print(space.id, space.proposals_count, stored_num_votes)
            allowed_spaces.append(space.id)

    with open("../govbot/allowed_spaces.json", "w+") as outfi:
        json.dump(allowed_spaces, outfi)
