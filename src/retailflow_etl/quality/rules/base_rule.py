"""Base data-quality rule."""

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from retailflow_etl.models.validation_error import ValidationError


class BaseRule(ABC):
    name = "base"

    def __init__(self, **config: Any) -> None:
        self.config = config

    @abstractmethod
    def validate(self, frame: pd.DataFrame) -> list[ValidationError]:
        """Return one structured error per violated row."""

    def error(self, index: Any, column: str, value: Any, code: str, message: str) -> ValidationError:
        record_column = self.config.get("record_id", "")
        record_id = str(frame_value(self.config.get("_frame"), index, record_column) if record_column else index)
        return ValidationError(record_id, self.name, column, value, code, message, index)


def frame_value(frame: pd.DataFrame | None, index: Any, column: str) -> Any:
    if frame is None or column not in frame.columns:
        return index
    return frame.loc[index, column]
