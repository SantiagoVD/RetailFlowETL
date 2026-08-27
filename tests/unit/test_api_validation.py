import pytest

from retailflow_api.common.exceptions import ApiError
from retailflow_api.uploads.validation import UploadRequest, build_object_key, validate_upload_request


def test_upload_validation_builds_a_safe_dataset_key():
    request = validate_upload_request(
        {
            "dataset": "sales",
            "file_name": "sales_august.xlsx",
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
    )
    assert request == UploadRequest("sales", "sales_august.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert build_object_key("input", request, "UPLOAD-123") == "input/sales/UPLOAD-123/sales_august.xlsx"


@pytest.mark.parametrize(
    "payload",
    [
        {"dataset": "unknown", "file_name": "sales.csv", "content_type": "text/csv"},
        {"dataset": "sales", "file_name": "../sales.csv", "content_type": "text/csv"},
        {"dataset": "sales", "file_name": "sales.exe", "content_type": "text/csv"},
        {"dataset": "sales", "file_name": "sales.csv", "content_type": "application/json"},
    ],
)
def test_upload_validation_rejects_unsafe_or_incompatible_requests(payload):
    with pytest.raises(ApiError):
        validate_upload_request(payload)
