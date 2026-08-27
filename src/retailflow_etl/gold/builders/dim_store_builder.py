"""DimStore builder."""

import hashlib

import pandas as pd


class DimStoreBuilder:
    def build(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result["store_key"] = result["store_id"].map(lambda x: "S_" + hashlib.sha256(str(x).encode()).hexdigest()[:12])
        return result[["store_key", "store_id", "store_name", "city", "region", "opening_date", "active"]]
