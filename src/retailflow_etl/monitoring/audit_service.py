"""Audit event helper."""

from typing import Any


class AuditService:
    def __init__(self, logger: Any) -> None:
        self.logger = logger

    def record(self, run_id: str, dataset: str, stage: str, status: str, records: int = 0) -> None:
        self.logger.info("stage completed", extra={"run_id": run_id, "dataset": dataset, "stage": stage, "status": status, "records": records})
