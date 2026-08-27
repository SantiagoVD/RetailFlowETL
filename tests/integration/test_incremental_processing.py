import pandas as pd

from retailflow_etl.application.etl_service import EtlService
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_different_content_with_same_name_is_processed_again(quality_config):
    repo = InMemoryS3Repository()
    event = {"Records": [{"s3": {"bucket": {"name": repo.bucket}, "object": {"key": "input/sales/same.csv"}}}]}
    def payload(quantity):
        return pd.DataFrame({"sale_id": [f"A{quantity}"], "sale_date": ["2026-01-01"], "customer_id": ["C1"], "product_id": ["P1"], "store_id": ["S1"], "payment_id": ["M1"], "quantity": [quantity], "unit_price": [2], "discount_percentage": [0]}).to_csv(index=False).encode()
    service = EtlService(repo, quality_config)
    repo.put_object("input/sales/same.csv", payload(1))
    assert service.process_event(event).status == "SUCCESS"
    repo.put_object("input/sales/same.csv", payload(2))
    assert service.process_event(event).status == "SUCCESS"
