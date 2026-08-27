"""Numeric range rule."""

import pandas as pd

from retailflow_etl.quality.rules.base_rule import BaseRule


class RangeRule(BaseRule):
    name = "range"

    def validate(self, frame: pd.DataFrame):
        self.config["_frame"] = frame
        column_value = self.config.get("column")
        if not isinstance(column_value, str) or column_value not in frame:
            return []
        column = column_value
        values = pd.to_numeric(frame[column], errors="coerce")
        mask = values.isna() | values.lt(self.config.get("min", float("-inf"))) | values.gt(self.config.get("max", float("inf")))
        mask &= frame[column].notna()
        return [self.error(i, column, frame.loc[i, column], "OUT_OF_RANGE", f"{column} is outside allowed range") for i in frame.index[mask]]
