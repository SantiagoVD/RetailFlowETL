"""Base Silver transformer."""

from abc import ABC, abstractmethod

import pandas as pd


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Normalize a valid dataset."""

    @staticmethod
    def clean_strings(frame: pd.DataFrame) -> pd.DataFrame:
        result = frame.copy()
        for column in result.select_dtypes(include=["object"]).columns:
            result[column] = result[column].map(lambda value: value.strip() if isinstance(value, str) else value)
        return result

    @staticmethod
    def title_case(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        result = frame.copy()
        for column in columns:
            if column in result:
                result[column] = result[column].map(lambda value: value.title() if isinstance(value, str) else value)
        return result
