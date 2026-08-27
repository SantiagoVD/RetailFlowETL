"""Store Silver transformation."""

import pandas as pd

from retailflow_etl.silver.transformers.base_transformer import BaseTransformer


class StoreTransformer(BaseTransformer):
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.title_case(self.clean_strings(frame), ["store_name", "city", "region"])
        result["opening_date"] = pd.to_datetime(result["opening_date"]).dt.strftime("%Y-%m-%d")
        result["active"] = result["active"].map({True: True, False: False, "true": True, "false": False, "TRUE": True, "FALSE": False}).fillna(False)
        return result.drop_duplicates(subset=["store_id"])
