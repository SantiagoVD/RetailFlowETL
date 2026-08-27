"""DimPaymentMethod builder."""

import hashlib

import pandas as pd


class DimPaymentMethodBuilder:
    def build(self, frame: pd.DataFrame) -> pd.DataFrame:
        methods = frame[["payment_method"]].drop_duplicates().copy()
        methods["payment_method_key"] = methods["payment_method"].map(lambda x: "M_" + hashlib.sha256(str(x).encode()).hexdigest()[:12])
        return methods[["payment_method_key", "payment_method"]].reset_index(drop=True)
