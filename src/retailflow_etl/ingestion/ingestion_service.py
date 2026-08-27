"""Input extraction service."""

from typing import Any

import pandas as pd

from retailflow_etl.common.exceptions import IngestionException
from retailflow_etl.ingestion.file_reader_factory import FileReaderFactory
from retailflow_etl.models.s3_event import S3InputEvent


class IngestionService:
    def __init__(self, repository: Any) -> None:
        self.repository = repository

    def extract(self, source: S3InputEvent) -> pd.DataFrame:
        try:
            payload = self.repository.get_object(source.key)
            return FileReaderFactory.create(source.dataset.extension).read(payload)
        except Exception as exc:
            if isinstance(exc, IngestionException):
                raise
            raise IngestionException(f"Could not extract {source.key}") from exc
