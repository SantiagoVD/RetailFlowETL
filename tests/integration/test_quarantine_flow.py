import pandas as pd

from retailflow_etl.quality.quality_service import QualityService
from retailflow_etl.quality.quarantine_service import QuarantineService
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_invalid_rows_are_written_to_quarantine(quality_config):
    repo = InMemoryS3Repository()
    frame = pd.DataFrame({"sale_id": ["A"], "sale_date": ["bad"], "quantity": [-1], "unit_price": [2]})
    quality = QualityService(quality_config).validate(frame, "sales")
    key = QuarantineService(repo, PathBuilder()).write(quality, "sales", "RUN-1", "bad.csv", pd.Timestamp("2026-01-01", tz="UTC"))
    output = ParquetWriter().from_bytes(repo.get_object(key))
    assert output.loc[0, "_error_codes"]
    assert "_error_messages" in output
