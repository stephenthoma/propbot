import json

from govbot import snapshot, firestore


spaceProposalsQuery = """
query Proposals($id: String) {
  proposals( where: {space: $id} ) { id }
}
"""


with open("./all_spaces.json", "r") as spacefi:
    space_json = json.load(spacefi)["data"]

for space in space_json["spaces"]:

    vars = {"id": space["id"]}
    res = snapshot.run_query(spaceProposalsQuery, snapshot.SNAPSHOT_GRAPH_URL, variables=vars)
    proposals = res["data"]["proposals"]
    if len(proposals) < 3:
        continue

    prop_votes = [len(snapshot.get_votes(p["id"])) for p in proposals]
    avg_votes = sum(prop_votes) / len(prop_votes)
    if avg_votes != 0.0:
        print(space["id"], avg_votes)
        firestore.store_space_avg_voters(space["id"], avg_votes)
        firestore.get_avg_space_voters(space["id"])
