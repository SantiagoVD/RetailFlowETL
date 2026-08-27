"""CSV reader."""

import io

import pandas as pd

from retailflow_etl.ingestion.readers.base_reader import BaseReader


class CsvReader(BaseReader):
    def read(self, payload: bytes) -> pd.DataFrame:
        return pd.read_csv(io.BytesIO(payload))
