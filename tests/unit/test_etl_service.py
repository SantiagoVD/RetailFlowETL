import pandas as pd

from retailflow_etl.application.etl_service import EtlService
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_etl_service_processes_and_skips_same_checksum(quality_config):
    repository = InMemoryS3Repository()
    repository.put_object("input/sales/sales.csv", pd.DataFrame({"sale_id": ["A"], "sale_date": ["2026-01-01"], "customer_id": ["C1"], "product_id": ["P1"], "store_id": ["S1"], "payment_id": ["M1"], "quantity": [2], "unit_price": [10], "discount_percentage": [5]}).to_csv(index=False).encode())
    event = {"Records": [{"s3": {"bucket": {"name": repository.bucket}, "object": {"key": "input/sales/sales.csv"}}}]}
    service = EtlService(repository, quality_config)
    first = service.process_event(event)
    second = service.process_event(event)
    assert first.status == "SUCCESS"
    assert second.status == "SKIPPED"
    assert repository.read_json(f"metadata/runs/{first.run_id}.json")["bronze_key"] == first.bronze_key
    skipped = repository.read_json(f"metadata/runs/{second.run_id}.json")
    assert skipped["status"] == "SKIPPED"
    assert skipped["original_run_id"] == first.run_id
    assert any(key.startswith("gold/") for key in repository.objects)


def test_etl_persists_upload_id(quality_config):
    repository = InMemoryS3Repository()
    repository.put_object("input/sales/UPLOAD-123/sales.csv", b"sale_id,sale_date,customer_id,product_id,store_id,payment_id,quantity,unit_price,discount_percentage\nA,2026-01-01,C1,P1,S1,M1,1,10,0\n")
    event = {"Records": [{"s3": {"bucket": {"name": repository.bucket}, "object": {"key": "input/sales/UPLOAD-123/sales.csv"}}}]}
    result = EtlService(repository, quality_config).process_event(event)
    run = repository.read_json(f"metadata/runs/{result.run_id}.json")
    assert run["upload_id"] == "UPLOAD-123"
