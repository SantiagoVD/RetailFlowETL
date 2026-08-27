"""Bronze Parquet writer."""

from datetime import datetime
from typing import Any

import pandas as pd

from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder


class BronzeWriter:
    def __init__(self, repository: Any, paths: PathBuilder) -> None:
        self.repository = repository
        self.paths = paths
        self.parquet = ParquetWriter()

    def write(self, frame: pd.DataFrame, dataset: str, source_key: str, file_name: str, run_id: str, event_time: datetime) -> str:
        enriched = frame.copy()
        enriched["_ingestion_timestamp"] = datetime.now().astimezone().isoformat()
        enriched["_source_file"] = file_name
        enriched["_source_key"] = source_key
        enriched["_dataset"] = dataset
        enriched["_run_id"] = run_id
        key = self.paths.data_key("bronze", dataset, run_id, event_time)
        self.repository.put_object(key, self.parquet.to_bytes(enriched), "application/octet-stream")
        return key
