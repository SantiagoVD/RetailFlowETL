"""Quarantine invalid records without dropping traceability."""

from datetime import datetime
from typing import Any

from retailflow_etl.quality.quality_result import QualityResult
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder


class QuarantineService:
    def __init__(self, repository: Any, paths: PathBuilder) -> None:
        self.repository = repository
        self.paths = paths
        self.parquet = ParquetWriter()

    def write(self, result: QualityResult, dataset: str, run_id: str, source_file: str, event_time: datetime) -> str | None:
        if result.rejected.empty:
            return None
        errors_by_id: dict[str, list[str]] = {}
        messages_by_id: dict[str, list[str]] = {}
        for error in result.errors:
            error_id = str(error.row_index if error.row_index is not None else error.record_id)
            errors_by_id.setdefault(error_id, []).append(error.error_code)
            messages_by_id.setdefault(error_id, []).append(error.error_message)
        output = result.rejected.copy()
        ids = output.index.astype(str)
        output["_error_codes"] = ids.map(lambda x: ";".join(errors_by_id.get(str(x), ["QUALITY_ERROR"])))
        output["_error_messages"] = ids.map(lambda x: ";".join(messages_by_id.get(str(x), ["Record failed data quality"])))
        output["_rejected_at"] = datetime.now().astimezone().isoformat()
        output["_run_id"] = run_id
        output["_source_file"] = source_file
        key = self.paths.quarantine_key(dataset, run_id, event_time)
        self.repository.put_object(key, self.parquet.to_bytes(output), "application/octet-stream")
        return key
