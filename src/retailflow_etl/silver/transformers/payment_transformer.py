"""Payment Silver transformation."""

import pandas as pd

from retailflow_etl.silver.transformers.base_transformer import BaseTransformer


class PaymentTransformer(BaseTransformer):
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.clean_strings(frame)
        result["payment_method"] = result["payment_method"].str.upper()
        result["payment_status"] = result["payment_status"].str.upper()
        result["payment_date"] = pd.to_datetime(result["payment_date"]).dt.strftime("%Y-%m-%d")
        result["amount"] = pd.to_numeric(result["amount"])
        return result.drop_duplicates(subset=["payment_id"])
