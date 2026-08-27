"""S3-backed metadata and idempotency service."""

from time import perf_counter
from typing import Any
from uuid import uuid4

from retailflow_etl.common.datetime_utils import isoformat, utc_now
from retailflow_etl.metadata.pipeline_run import PipelineRun
from retailflow_etl.storage.path_builder import PathBuilder


class MetadataService:
    def __init__(self, repository: Any, paths: PathBuilder) -> None:
        self.repository = repository
        self.paths = paths
        self._started: dict[str, float] = {}

    def new_run(self, dataset: str, source_file: str, upload_id: str | None = None) -> PipelineRun:
        run_id = f"RUN-{uuid4()}"
        now = utc_now()
        self._started[run_id] = perf_counter()
        run = PipelineRun(run_id=run_id, dataset=dataset, source_file=source_file, start_time=isoformat(now), upload_id=upload_id)
        self.save_run(run)
        return run

    def is_processed(self, dataset: str, checksum: str) -> bool:
        return self.processed_record(dataset, checksum) is not None

    def processed_record(self, dataset: str, checksum: str) -> dict[str, Any] | None:
        key = self.paths.processed_key(dataset, checksum)
        if not self.repository.object_exists(key):
            return None
        try:
            record = self.repository.read_json(key)
            return record if record.get("status") == "SUCCESS" else None
        except Exception:
            return None

    def save_run(self, run: PipelineRun) -> None:
        self.repository.write_json(self.paths.run_key(run.run_id), run.as_dict())

    def finish(self, run: PipelineRun, status: str, error_message: str | None = None) -> PipelineRun:
        run.status = status
        run.end_time = isoformat(utc_now())
        run.duration_ms = round((perf_counter() - self._started.get(run.run_id, perf_counter())) * 1000)
        run.error_message = error_message
        self.save_run(run)
        return run

    def mark_processed(self, run: PipelineRun, checksum: str) -> None:
        body = {
            "run_id": run.run_id,
            "dataset": run.dataset,
            "file_name": run.source_file,
            "upload_id": run.upload_id,
            "source_key": run.source_file,
            "checksum": checksum,
            "processed_at": run.end_time,
            "records_received": run.records_received,
            "records_valid": run.records_valid,
            "records_rejected": run.records_rejected,
            "status": run.status,
        }
        self.repository.write_json(self.paths.processed_key(run.dataset, checksum), body)
