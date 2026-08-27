"""FactInventory builder."""

import hashlib

import pandas as pd


def _key(prefix: str, value: object) -> str:
    return prefix + hashlib.sha256(str(value).encode()).hexdigest()[:12]


class FactInventoryBuilder:
    def build(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result["date_key"] = pd.to_datetime(result["snapshot_date"]).dt.strftime("%Y%m%d").astype(int)
        result["store_key"] = result["store_id"].map(lambda x: _key("S_", x))
        result["product_key"] = result["product_id"].map(lambda x: _key("P_", x))
        result["stock_status"] = result.apply(lambda row: "OUT_OF_STOCK" if row.stock_quantity == 0 else ("LOW_STOCK" if row.stock_quantity < row.minimum_stock else "OK"), axis=1)
        return result[["inventory_id", "date_key", "store_key", "product_key", "stock_quantity", "minimum_stock", "stock_status"]]
