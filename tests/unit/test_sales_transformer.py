import pandas as pd

from retailflow_etl.silver.transformers.sales_transformer import SalesTransformer


def test_sales_transformer_normalizes_types_and_deduplicates():
    frame = pd.DataFrame({"sale_id": [" A ", " A "], "sale_date": ["2026-01-01", "2026-01-01"], "quantity": ["2", "2"], "unit_price": ["5", "5"], "discount_percentage": ["10", "10"]})
    result = SalesTransformer().transform(frame)
    assert len(result) == 1
    assert result.iloc[0]["sale_id"] == "A"
    assert result.iloc[0]["quantity"] == 2
