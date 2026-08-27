import pandas as pd

from retailflow_etl.bronze.bronze_service import BronzeService
from retailflow_etl.silver.silver_service import SilverService
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_bronze_to_silver_preserves_lineage_and_normalizes():
    repo = InMemoryS3Repository()
    frame = pd.DataFrame({"sale_id": [" A "], "sale_date": ["2026-01-01"], "quantity": [1], "unit_price": [2], "discount_percentage": [0]})
    path = PathBuilder()
    BronzeService(repo, path).process(frame, "sales", "input/sales/a.csv", "a.csv", "RUN-1", pd.Timestamp("2026-01-01", tz="UTC"))
    result, key = SilverService(repo, path).process(frame, "sales", "RUN-1", pd.Timestamp("2026-01-01", tz="UTC"))
    assert result.loc[0, "sale_id"] == "A"
    assert repo.object_exists(key)
