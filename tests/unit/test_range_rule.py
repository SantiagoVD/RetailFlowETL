import pandas as pd

from retailflow_etl.quality.rules.range_rule import RangeRule


def test_range_rule_rejects_negative_value():
    errors = RangeRule(column="amount", min=0, record_id="id").validate(pd.DataFrame({"id": ["A"], "amount": [-1]}))
    assert errors[0].error_code == "OUT_OF_RANGE"
