import pandas as pd

from retailflow_etl.quality.rules.date_rule import DateRule


def test_date_rule_rejects_invalid_date():
    errors = DateRule(column="event_date", record_id="id").validate(pd.DataFrame({"id": ["A"], "event_date": ["2026-99-01"]}))
    assert errors[0].error_code == "INVALID_DATE"
