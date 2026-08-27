import json
from unittest.mock import MagicMock

from retailflow_api.application.api_service import ApiService
from retailflow_api.config.settings import ApiSettings


def settings():
    return ApiSettings("bucket", "input", "metadata", "gold", "quarantine", 300, 300, 10_000_000, "http://localhost:5173")


def response_body(response):
    return json.loads(response["body"])


def test_post_upload_returns_presigned_post_contract():
    gateway = MagicMock()
    gateway.generate_upload_post.return_value = {"url": "https://s3.example", "fields": {"key": "input/sales/UPLOAD-1/sales.csv"}}
    response = ApiService(gateway, settings()).handle(
        {
            "requestContext": {"http": {"method": "POST"}},
            "rawPath": "/uploads",
            "body": json.dumps({"dataset": "sales", "file_name": "sales.csv", "content_type": "text/csv"}),
        }
    )
    body = response_body(response)
    assert response["statusCode"] == 201
    assert body["upload_id"].startswith("UPLOAD-")
    assert body["object_key"].startswith("input/sales/")
    assert body["upload_url"] == "https://s3.example"
    gateway.generate_upload_post.assert_called_once()


def test_upload_status_exposes_skipped_run_and_original_run():
    gateway = MagicMock()
    gateway.find_latest_run_by_upload.return_value = {
        "upload_id": "UPLOAD-123",
        "run_id": "RUN-skip",
        "original_run_id": "RUN-original",
        "dataset": "sales",
        "status": "SKIPPED",
    }
    response = ApiService(gateway, settings()).handle(
        {"requestContext": {"http": {"method": "GET"}}, "rawPath": "/uploads/UPLOAD-123"}
    )
    assert response_body(response)["status"] == "SKIPPED"
    assert response_body(response)["original_run_id"] == "RUN-original"


def test_run_result_is_limited_by_api_contract():
    gateway = MagicMock()
    gateway.get_run.return_value = {"run_id": "RUN-1", "dataset": "sales", "status": "SUCCESS", "gold_keys": ["gold/fact_sales.parquet"]}
    gateway.gold_preview.return_value = {"run_id": "RUN-1", "preview_count": 100, "rows": []}
    response = ApiService(gateway, settings()).handle(
        {"requestContext": {"http": {"method": "GET"}}, "rawPath": "/runs/RUN-1/result", "queryStringParameters": {"limit": "500"}}
    )
    assert response["statusCode"] == 200
    gateway.gold_preview.assert_called_once_with(gateway.get_run.return_value, 100)
