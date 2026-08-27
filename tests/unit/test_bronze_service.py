from datetime import datetime, timezone

import pandas as pd

from retailflow_etl.bronze.bronze_service import BronzeService
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_bronze_preserves_data_and_adds_lineage():
    repo = InMemoryS3Repository()
    key = BronzeService(repo, PathBuilder()).process(pd.DataFrame({"id": [1]}), "sales", "input/sales/a.csv", "a.csv", "RUN-1", datetime.now(timezone.utc))
    result = ParquetWriter().from_bytes(repo.get_object(key))
    assert result.loc[0, "id"] == 1
    assert result.loc[0, "_dataset"] == "sales"
    assert result.loc[0, "_run_id"] == "RUN-1"
