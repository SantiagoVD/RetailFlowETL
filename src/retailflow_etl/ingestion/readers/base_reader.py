"""Reader interface."""

from abc import ABC, abstractmethod

import pandas as pd


class BaseReader(ABC):
    """Convert an input byte payload into a tabular data frame."""

    @abstractmethod
    def read(self, payload: bytes) -> pd.DataFrame:
        """Read bytes into a data frame."""
