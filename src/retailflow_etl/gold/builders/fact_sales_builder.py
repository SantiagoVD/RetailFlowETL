"""FactSales builder."""

import hashlib

import pandas as pd


def _key(prefix: str, value: object) -> str:
    return prefix + hashlib.sha256(str(value).encode()).hexdigest()[:12]


class FactSalesBuilder:
    def build(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result["date_key"] = pd.to_datetime(result["sale_date"]).dt.strftime("%Y%m%d").astype(int)
        result["customer_key"] = result["customer_id"].map(lambda x: _key("C_", x))
        result["product_key"] = result["product_id"].map(lambda x: _key("P_", x))
        result["store_key"] = result["store_id"].map(lambda x: _key("S_", x))
        result["payment_method_key"] = result["payment_id"].map(lambda x: _key("M_", x))
        result["gross_amount"] = result["quantity"] * result["unit_price"]
        result["discount_amount"] = result["gross_amount"] * result["discount_percentage"] / 100
        result["net_amount"] = result["gross_amount"] - result["discount_amount"]
        return result[["sale_id", "date_key", "customer_key", "product_key", "store_key", "payment_method_key", "quantity", "unit_price", "discount_percentage", "gross_amount", "discount_amount", "net_amount"]]
