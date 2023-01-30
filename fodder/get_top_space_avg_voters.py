import json
import typing
import statistics

from sgqlc.operation import Operation

from govbot import snapshot, firestore
from govbot.snapshot_schema import snapshot_schema as ss


def get_space_proposals(space_id: str, proposal_fields: list) -> typing.List[ss.Proposal]:
    def get_proposal_page(page_size: int, skip: int):
        op = Operation(ss.Query, name="getSpaceProposals")
        op_proposal = op.proposals(first=page_size, skip=skip, where={"space": space_id})
        op_proposal.__fields__(*proposal_fields)
        return snapshot.run_operation(op).proposals

    return snapshot.get_paginated(get_proposal_page, 1000)


if __name__ == "__main__":
    spaces = snapshot.get_spaces()
    filtered_spaces = [s for s in spaces if s.proposals_count > 3]
    for space in filtered_spaces:
        print(space.proposals_count, "proposals")

        proposals = get_space_proposals(space.id, ["id", "votes"])
        prop_votes = [p.votes for p in proposals]

        avg_num_votes = statistics.median(prop_votes)
        stdev_num_votes = statistics.pstdev(prop_votes)

        if avg_num_votes != 0.0:
            # stored_num_votes = firestore.get_avg_space_voters(space.id)
            print(space.id, avg_num_votes)
            firestore.store_space_avg_voters(space.id, avg_num_votes)
