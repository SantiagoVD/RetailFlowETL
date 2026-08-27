"""Inventory Silver transformation."""

import pandas as pd

from retailflow_etl.silver.transformers.base_transformer import BaseTransformer


class InventoryTransformer(BaseTransformer):
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.clean_strings(frame)
        result["snapshot_date"] = pd.to_datetime(result["snapshot_date"]).dt.strftime("%Y-%m-%d")
        result["stock_quantity"] = pd.to_numeric(result["stock_quantity"])
        result["minimum_stock"] = pd.to_numeric(result["minimum_stock"])
        return result.drop_duplicates(subset=["inventory_id"])
