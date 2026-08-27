import pandas as pd

from retailflow_etl.quality.rules.null_rule import NullRule


def test_null_rule_reports_empty_values():
    errors = NullRule(columns=["id"], record_id="id").validate(pd.DataFrame({"id": ["A", None, ""]}))
    assert len(errors) == 2
    assert all(error.error_code == "NULL_VALUE" for error in errors)
