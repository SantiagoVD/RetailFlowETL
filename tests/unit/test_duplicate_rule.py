import pandas as pd

from retailflow_etl.quality.rules.duplicate_rule import DuplicateRule


def test_duplicate_rule_keeps_first_occurrence():
    errors = DuplicateRule(columns=["id"], record_id="id").validate(pd.DataFrame({"id": ["A", "A", "B"]}))
    assert [error.record_id for error in errors] == ["A"]
