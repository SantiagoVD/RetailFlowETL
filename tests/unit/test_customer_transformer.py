import pandas as pd

from retailflow_etl.silver.transformers.customer_transformer import CustomerTransformer


def test_customer_transformer_normalizes_names_and_email():
    frame = pd.DataFrame({"customer_id": ["C1"], "first_name": [" ana "], "last_name": ["LOPEZ"], "email": ["A@EXAMPLE.COM"], "city": [" lima "], "region": ["central"], "registration_date": ["2026-01-01"], "segment": ["premium"]})
    result = CustomerTransformer().transform(frame)
    assert result.iloc[0]["first_name"] == "Ana"
    assert result.iloc[0]["email"] == "a@example.com"
    assert result.iloc[0]["segment"] == "PREMIUM"
