"""Required-value rule."""

import pandas as pd

from retailflow_etl.quality.rules.base_rule import BaseRule


class NullRule(BaseRule):
    name = "null"

    def validate(self, frame: pd.DataFrame):
        self.config["_frame"] = frame
        errors = []
        for column in self.config.get("columns", []):
            if column not in frame:
                continue
            for index in frame.index[frame[column].isna() | frame[column].astype(str).str.strip().eq("")]:
                errors.append(self.error(index, column, frame.loc[index, column], "NULL_VALUE", f"{column} is required"))
        return errors
