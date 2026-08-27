"""Customer Silver transformation."""

import pandas as pd

from retailflow_etl.silver.transformers.base_transformer import BaseTransformer


class CustomerTransformer(BaseTransformer):
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.clean_strings(frame)
        result = self.title_case(result, ["first_name", "last_name", "city", "region"])
        result["email"] = result["email"].str.lower()
        result["registration_date"] = pd.to_datetime(result["registration_date"]).dt.strftime("%Y-%m-%d")
        result["segment"] = result["segment"].str.upper()
        return result.drop_duplicates(subset=["customer_id"])
