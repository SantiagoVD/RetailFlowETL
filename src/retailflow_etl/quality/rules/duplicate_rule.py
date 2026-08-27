"""Duplicate-key rule."""

import pandas as pd

from retailflow_etl.quality.rules.base_rule import BaseRule


class DuplicateRule(BaseRule):
    name = "duplicate"

    def validate(self, frame: pd.DataFrame):
        self.config["_frame"] = frame
        columns = self.config.get("columns", [])
        if not columns or any(column not in frame for column in columns):
            return []
        mask = frame.duplicated(columns, keep="first")
        return [self.error(index, ",".join(columns), frame.loc[index, columns].to_dict(), "DUPLICATE_VALUE", "Duplicate business key") for index in frame.index[mask]]
