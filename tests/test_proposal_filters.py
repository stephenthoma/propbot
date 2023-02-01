import json
from unittest.mock import MagicMock

import pytest

from govbot import proposal_filters
from govbot import snapshot_schema as ss


@pytest.fixture(scope="module")
def test_proposals():
    with open("proposal_list.json") as f:
        return json.load(f)


def always_true_filter(proposal: ss.Proposal) -> bool:
    return True


def always_false_filter(proposal: ss.Proposal) -> bool:
    return False


class TestApplyFilters:
    def test_apply_with_true_filter(self, test_proposals):
        filters = [always_true_filter, always_false_filter]
        proposals = test_proposals[:2]
        result = proposal_filters.apply_filters(filters, proposals)
        assert list(result) == []

    def test_apply_with_all_false_filter(self, test_proposals):
        filters = [always_false_filter, always_false_filter]
        proposals = test_proposals[:2]
        result = proposal_filters.apply_filters(filters, proposals)
        assert list(result) == test_proposals[:2]


def test_is_blocked_space():
    prop = MagicMock()
    prop.space.id = "tbcc.eth"
    assert proposal_filters.is_blocked_space(prop) == True

    prop.space.id = "bitembassy.eth"
    assert proposal_filters.is_blocked_space(prop) == False
