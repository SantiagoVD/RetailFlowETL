"""Configurable business rule."""

import pandas as pd

from retailflow_etl.quality.rules.base_rule import BaseRule


class BusinessRule(BaseRule):
    name = "business"

    def validate(self, frame: pd.DataFrame):
        self.config["_frame"] = frame
        column_value = self.config.get("column")
        if not isinstance(column_value, str) or column_value not in frame:
            return []
        column = column_value
        values = frame[column]
        check = self.config.get("check")
        present = values.notna() & values.astype(str).str.strip().ne("")
        if check == "email":
            mask = present & ~values.astype(str).str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", na=False)
        elif check == "in":
            mask = present & ~values.isin(self.config.get("values", []))
        else:
            mask = pd.Series(False, index=frame.index)
        return [self.error(i, column, frame.loc[i, column], "BUSINESS_RULE_FAILED", f"{column} failed business validation") for i in frame.index[mask]]
