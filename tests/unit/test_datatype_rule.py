import pandas as pd

from retailflow_etl.quality.rules.datatype_rule import DatatypeRule


def test_datatype_rule_rejects_non_numeric():
    errors = DatatypeRule(columns={"amount": "numeric"}, record_id="id").validate(pd.DataFrame({"id": ["A"], "amount": ["bad"]}))
    assert errors[0].error_code == "INVALID_DATATYPE"
