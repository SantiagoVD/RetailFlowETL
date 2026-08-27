"""Config-driven quality engine."""

from typing import Any

import pandas as pd

from retailflow_etl.quality.quality_result import QualityResult
from retailflow_etl.quality.rules.base_rule import BaseRule
from retailflow_etl.quality.rules.business_rule import BusinessRule
from retailflow_etl.quality.rules.datatype_rule import DatatypeRule
from retailflow_etl.quality.rules.date_rule import DateRule
from retailflow_etl.quality.rules.duplicate_rule import DuplicateRule
from retailflow_etl.quality.rules.null_rule import NullRule
from retailflow_etl.quality.rules.range_rule import RangeRule

RULE_TYPES: dict[str, type[BaseRule]] = {
    "null": NullRule,
    "duplicate": DuplicateRule,
    "datatype": DatatypeRule,
    "range": RangeRule,
    "date": DateRule,
    "business": BusinessRule,
}


class QualityService:
    def __init__(self, configuration: dict[str, Any]) -> None:
        self.configuration = configuration

    def validate(self, frame: pd.DataFrame, dataset: str) -> QualityResult:
        errors = []
        primary = self._primary_column(dataset, frame)
        for rule_config in self.configuration.get("datasets", {}).get(dataset, []):
            rule_type = rule_config.get("type")
            rule_class = RULE_TYPES.get(rule_type)
            if rule_class is not None:
                configured = dict(rule_config)
                configured["record_id"] = primary or ""
                errors.extend(rule_class(**configured).validate(frame))
        rejected_indexes = {error.row_index for error in errors}
        rejected_mask = frame[primary].astype(str).isin(rejected_indexes) if primary else pd.Series(False, index=frame.index)
        if errors:
            rejected_mask = frame.index.isin(rejected_indexes)
        rejected = frame.loc[rejected_mask].copy()
        valid = frame.loc[~rejected_mask].copy()
        return QualityResult(valid=valid, rejected=rejected, errors=errors)

    @staticmethod
    def _primary_column(dataset: str, frame: pd.DataFrame) -> str | None:
        preferred = {"sales": "sale_id", "customers": "customer_id", "products": "product_id", "stores": "store_id", "payments": "payment_id", "inventory": "inventory_id"}.get(dataset)
        return preferred if preferred in frame.columns else (str(frame.columns[0]) if len(frame.columns) else None)
