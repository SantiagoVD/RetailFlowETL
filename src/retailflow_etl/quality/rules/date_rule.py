"""Date validity rule."""

import pandas as pd

from retailflow_etl.quality.rules.base_rule import BaseRule


class DateRule(BaseRule):
    name = "date"

    def validate(self, frame: pd.DataFrame):
        self.config["_frame"] = frame
        column_value = self.config.get("column")
        if not isinstance(column_value, str) or column_value not in frame:
            return []
        column = column_value
        parsed = pd.to_datetime(frame[column], errors="coerce")
        mask = parsed.isna()
        return [self.error(i, column, frame.loc[i, column], "INVALID_DATE", f"{column} is not a valid date") for i in frame.index[mask]]
