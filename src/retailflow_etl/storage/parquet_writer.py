"""Parquet serialization using PyArrow."""

import io
from typing import Any

import pandas as pd

from retailflow_etl.common.exceptions import StorageException


class ParquetWriter:
    """Serialize data frames to portable Parquet bytes."""

    def to_bytes(self, frame: pd.DataFrame) -> bytes:
        try:
            buffer = io.BytesIO()
            frame.to_parquet(buffer, engine="pyarrow", index=False)
            return buffer.getvalue()
        except Exception as exc:
            raise StorageException("PyArrow is required to write Parquet") from exc

    def from_bytes(self, payload: bytes) -> pd.DataFrame:
        try:
            return pd.read_parquet(io.BytesIO(payload), engine="pyarrow")
        except Exception as exc:
            raise StorageException("Could not read Parquet payload") from exc

    def write(self, repository: Any, key: str, frame: pd.DataFrame) -> None:
        repository.put_object(key, self.to_bytes(frame), "application/octet-stream")
