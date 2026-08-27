"""Datatype rule."""

import pandas as pd

from retailflow_etl.models.validation_error import ValidationError
from retailflow_etl.quality.rules.base_rule import BaseRule


class DatatypeRule(BaseRule):
    name = "datatype"

    def validate(self, frame: pd.DataFrame):
        self.config["_frame"] = frame
        errors: list[ValidationError] = []
        for column, expected in self.config.get("columns", {}).items():
            if column not in frame:
                continue
            converted = pd.to_numeric(frame[column], errors="coerce") if expected == "numeric" else frame[column]
            mask = converted.isna() & frame[column].notna()
            errors.extend(self.error(i, column, frame.loc[i, column], "INVALID_DATATYPE", f"Expected {expected}") for i in frame.index[mask])
        return errors
