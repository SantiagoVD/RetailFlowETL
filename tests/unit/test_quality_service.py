import pandas as pd

from retailflow_etl.quality.quality_service import QualityService


def test_quality_splits_valid_and_invalid_rows(quality_config):
    frame = pd.DataFrame({"sale_id": ["A", "A", "C"], "sale_date": ["2026-01-01", "bad", "2026-01-02"], "quantity": [1, 2, -1], "unit_price": [2, 2, 2]})
    result = QualityService(quality_config).validate(frame, "sales")
    assert len(result.valid) == 1
    assert len(result.rejected) == 2
    assert {error.error_code for error in result.errors} >= {"DUPLICATE_VALUE", "INVALID_DATE", "OUT_OF_RANGE"}
