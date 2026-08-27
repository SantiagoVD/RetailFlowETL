"""Product Silver transformation."""

import pandas as pd

from retailflow_etl.silver.transformers.base_transformer import BaseTransformer


class ProductTransformer(BaseTransformer):
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.clean_strings(frame)
        result = self.title_case(result, ["product_name", "category", "brand"])
        result["unit_cost"] = pd.to_numeric(result["unit_cost"])
        result["unit_price"] = pd.to_numeric(result["unit_price"])
        result["active"] = result["active"].map({True: True, False: False, "true": True, "false": False, "TRUE": True, "FALSE": False}).fillna(False)
        return result.drop_duplicates(subset=["product_id"])
