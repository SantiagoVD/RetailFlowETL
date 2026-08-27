import pandas as pd

from retailflow_etl.gold.gold_service import GoldService
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_silver_to_gold_creates_fact_and_date_outputs():
    repo = InMemoryS3Repository()
    frame = pd.DataFrame({"sale_id": ["A"], "sale_date": ["2026-01-01"], "customer_id": ["C1"], "product_id": ["P1"], "store_id": ["S1"], "payment_id": ["M1"], "quantity": [1], "unit_price": [2], "discount_percentage": [0]})
    keys = GoldService(repo, PathBuilder()).process(frame, "sales", "RUN-1", pd.Timestamp("2026-01-01", tz="UTC"))
    assert len(keys) == 2
    assert all(repo.object_exists(key) for key in keys)
