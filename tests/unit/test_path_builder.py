from datetime import datetime, timezone

from retailflow_etl.storage.path_builder import PathBuilder


def test_path_builder_partitions_outputs():
    builder = PathBuilder()
    key = builder.data_key("silver", "sales", "RUN-1", datetime(2026, 8, 27, tzinfo=timezone.utc))
    assert key == "silver/sales/year=2026/month=08/day=27/run_id=RUN-1/sales.parquet"
    assert builder.processed_key("sales", "abc") == "metadata/processed/sales/abc.json"
