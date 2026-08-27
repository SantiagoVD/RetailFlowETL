import pandas as pd

from retailflow_etl.quality.rules.business_rule import BusinessRule


def test_business_rule_validates_allowed_values_and_email():
    status_errors = BusinessRule(column="status", check="in", values=["PAID"], record_id="id").validate(pd.DataFrame({"id": ["A"], "status": ["UNKNOWN"]}))
    email_errors = BusinessRule(column="email", check="email", record_id="id").validate(pd.DataFrame({"id": ["A"], "email": ["bad"]}))
    assert status_errors[0].error_code == "BUSINESS_RULE_FAILED"
    assert email_errors[0].column == "email"
