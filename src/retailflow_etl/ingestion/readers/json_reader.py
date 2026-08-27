"""JSON reader supporting an object list or a single object."""

import io

import pandas as pd

from retailflow_etl.ingestion.readers.base_reader import BaseReader


class JsonReader(BaseReader):
    def read(self, payload: bytes) -> pd.DataFrame:
        return pd.read_json(io.BytesIO(payload))
