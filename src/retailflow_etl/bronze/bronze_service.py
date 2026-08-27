"""Bronze layer service."""

from datetime import datetime
from typing import Any

import pandas as pd

from retailflow_etl.bronze.bronze_writer import BronzeWriter
from retailflow_etl.storage.path_builder import PathBuilder


class BronzeService:
    def __init__(self, repository: Any, paths: PathBuilder) -> None:
        self.writer = BronzeWriter(repository, paths)

    def process(self, frame: pd.DataFrame, dataset: str, source_key: str, file_name: str, run_id: str, event_time: datetime) -> str:
        return self.writer.write(frame, dataset, source_key, file_name, run_id, event_time)
