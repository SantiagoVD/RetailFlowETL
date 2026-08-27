"""DimProduct builder."""

import hashlib

import pandas as pd


class DimProductBuilder:
    def build(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result["product_key"] = result["product_id"].map(lambda x: "P_" + hashlib.sha256(str(x).encode()).hexdigest()[:12])
        return result[["product_key", "product_id", "product_name", "category", "brand", "unit_cost", "unit_price", "active"]]
