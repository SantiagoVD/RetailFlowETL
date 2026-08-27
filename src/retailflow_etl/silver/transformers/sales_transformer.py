"""Sales Silver transformation."""

import pandas as pd

from retailflow_etl.silver.transformers.base_transformer import BaseTransformer


class SalesTransformer(BaseTransformer):
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        result = self.clean_strings(frame)
        result = self.title_case(result, ["sale_date"])
        result["sale_date"] = pd.to_datetime(result["sale_date"]).dt.strftime("%Y-%m-%d")
        for column in ["quantity", "unit_price", "discount_percentage"]:
            result[column] = pd.to_numeric(result[column])
        return result.drop_duplicates(subset=["sale_id"])
