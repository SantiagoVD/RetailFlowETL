"""AWS Lambda entry point for the operations API."""

from typing import Any

from retailflow_api.application.api_service import ApiService
from retailflow_api.config.settings import ApiSettings
from retailflow_api.storage.s3_gateway import S3Gateway


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    del context
    settings = ApiSettings.from_env()
    return ApiService(S3Gateway(settings), settings).handle(event)


handler = lambda_handler
