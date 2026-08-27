"""DimCustomer builder."""

import hashlib

import pandas as pd


class DimCustomerBuilder:
    def build(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        result["customer_key"] = result["customer_id"].map(lambda x: "C_" + hashlib.sha256(str(x).encode()).hexdigest()[:12])
        return result[["customer_key", "customer_id", "first_name", "last_name", "email", "city", "region", "registration_date", "segment"]]
