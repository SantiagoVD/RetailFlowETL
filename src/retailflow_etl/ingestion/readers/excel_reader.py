"""Excel reader using openpyxl through pandas."""

import io

import pandas as pd

from retailflow_etl.ingestion.readers.base_reader import BaseReader


class ExcelReader(BaseReader):
    def read(self, payload: bytes) -> pd.DataFrame:
        return pd.read_excel(io.BytesIO(payload), engine="openpyxl")
