import pandas as pd

from retailflow_etl.application.etl_service import EtlService
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_complete_pipeline_writes_all_expected_layers(quality_config):
    repo = InMemoryS3Repository()
    frame = pd.DataFrame({"sale_id": ["A", "B"], "sale_date": ["2026-01-01", "2026-01-02"], "customer_id": ["C1", "C2"], "product_id": ["P1", "P2"], "store_id": ["S1", "S1"], "payment_id": ["M1", "M2"], "quantity": [1, 2], "unit_price": [2, 3], "discount_percentage": [0, 10]})
    repo.put_object("input/sales/sales.csv", frame.to_csv(index=False).encode())
    event = {"Records": [{"s3": {"bucket": {"name": repo.bucket}, "object": {"key": "input/sales/sales.csv"}}}]}
    result = EtlService(repo, quality_config).process_event(event)
    parquet_keys = [key for key in repo.objects if key.endswith(".parquet")]
    assert result.status == "SUCCESS"
    assert len(parquet_keys) >= 4
    assert all(len(ParquetWriter().from_bytes(repo.get_object(key))) > 0 for key in parquet_keys)
