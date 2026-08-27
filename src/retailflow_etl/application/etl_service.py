"""End-to-end ETL orchestrator."""

from datetime import datetime, timezone
from typing import Any

from retailflow_etl.bronze.bronze_service import BronzeService
from retailflow_etl.gold.gold_service import GoldService
from retailflow_etl.ingestion.ingestion_service import IngestionService
from retailflow_etl.metadata.checksum_service import ChecksumService
from retailflow_etl.metadata.metadata_service import MetadataService
from retailflow_etl.models.processing_result import ProcessingResult
from retailflow_etl.models.s3_event import S3InputEvent
from retailflow_etl.monitoring.audit_service import AuditService
from retailflow_etl.quality.quality_service import QualityService
from retailflow_etl.quality.quarantine_service import QuarantineService
from retailflow_etl.silver.silver_service import SilverService
from retailflow_etl.storage.path_builder import PathBuilder


class EtlService:
    def __init__(self, repository: Any, quality_config: dict[str, Any], paths: PathBuilder | None = None, logger: Any | None = None) -> None:
        self.repository = repository
        self.paths = paths or PathBuilder()
        self.ingestion = IngestionService(repository)
        self.bronze = BronzeService(repository, self.paths)
        self.quality = QualityService(quality_config)
        self.quarantine = QuarantineService(repository, self.paths)
        self.silver = SilverService(repository, self.paths)
        self.gold = GoldService(repository, self.paths)
        self.metadata = MetadataService(repository, self.paths)
        self.logger = logger
        self.audit = AuditService(logger) if logger is not None else None

    def process_event(self, event: dict[str, Any]) -> ProcessingResult:
        source = S3InputEvent.from_event(event)
        payload = self.repository.get_object(source.key)
        checksum = ChecksumService.calculate(payload)
        processed = self.metadata.processed_record(source.dataset.name, checksum)
        if processed is not None:
            run = self.metadata.new_run(source.dataset.name, source.dataset.file_name, source.upload_id)
            run.original_run_id = processed.get("run_id")
            self.metadata.finish(run, "SKIPPED")
            result = ProcessingResult("SKIPPED", run.run_id, source.dataset.name, original_run_id=run.original_run_id)
            return result
        run = self.metadata.new_run(source.dataset.name, source.dataset.file_name, source.upload_id)
        result = ProcessingResult("STARTED", run.run_id, source.dataset.name)
        try:
            frame = self.ingestion.extract(source)
            result.records_received = len(frame)
            run.records_received = len(frame)
            result.bronze_key = self.bronze.process(frame, source.dataset.name, source.key, source.dataset.file_name, run.run_id, datetime.now(timezone.utc))
            run.bronze_key = result.bronze_key
            self._audit(run.run_id, source.dataset.name, "BRONZE", len(frame))
            quality = self.quality.validate(frame, source.dataset.name)
            result.records_valid = len(quality.valid)
            result.records_rejected = len(quality.rejected)
            run.records_valid = result.records_valid
            run.records_rejected = result.records_rejected
            result.quarantine_key = self.quarantine.write(quality, source.dataset.name, run.run_id, source.dataset.file_name, datetime.now(timezone.utc))
            run.quarantine_key = result.quarantine_key
            self._audit(run.run_id, source.dataset.name, "QUALITY", len(quality.valid))
            if not quality.valid.empty:
                _, result.silver_key = self.silver.process(quality.valid, source.dataset.name, run.run_id, datetime.now(timezone.utc))
                result.gold_keys = self.gold.process(quality.valid, source.dataset.name, run.run_id, datetime.now(timezone.utc))
                run.silver_key = result.silver_key
                run.gold_keys = result.gold_keys
                self._audit(run.run_id, source.dataset.name, "GOLD", len(quality.valid))
            self.metadata.finish(run, "SUCCESS")
            self.metadata.mark_processed(run, checksum)
            result.status = "SUCCESS"
            return result
        except Exception as exc:
            self.metadata.finish(run, "FAILED", str(exc))
            self.logger.exception("pipeline failed", extra={"run_id": run.run_id, "dataset": source.dataset.name, "stage": "PIPELINE", "status": "FAILED"}) if self.logger else None
            result.status = "FAILED"
            result.error_message = str(exc)
            raise

    def _audit(self, run_id: str, dataset: str, stage: str, records: int) -> None:
        if self.audit:
            self.audit.record(run_id, dataset, stage, "SUCCESS", records)
