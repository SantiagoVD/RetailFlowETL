"""AWS Lambda entry point kept intentionally thin."""

from typing import Any

from retailflow_etl.application.etl_service import EtlService
from retailflow_etl.config.settings import Settings
from retailflow_etl.monitoring.logger import get_logger
from retailflow_etl.storage.s3_repository import S3Repository


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    del context
    settings = Settings.from_env()
    logger = get_logger(level=settings.log_level)
    service = EtlService(S3Repository(settings.bucket), settings.data_quality, logger=logger)
    result = service.process_event(event)
    logger.info("pipeline completed", extra={"run_id": result.run_id, "dataset": result.dataset, "stage": "PIPELINE", "status": result.status, "records": result.records_valid})
    return {"statusCode": 200, "body": result.as_dict()}


handler = lambda_handler
