import pandas as pd

from retailflow_etl.gold.gold_service import GoldService
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_gold_service_calculates_sales_measures():
    frame = pd.DataFrame({"sale_id": ["A"], "sale_date": ["2026-01-01"], "customer_id": ["C1"], "product_id": ["P1"], "store_id": ["S1"], "payment_id": ["M1"], "quantity": [2], "unit_price": [10.0], "discount_percentage": [10.0]})
    repo = InMemoryS3Repository()
    keys = GoldService(repo, PathBuilder()).process(frame, "sales", "RUN-1", pd.Timestamp("2026-01-01", tz="UTC"))
    output = next(ParquetWriter().from_bytes(repo.get_object(key)) for key in keys if "fact_sales" in key)
    assert output.loc[0, "gross_amount"] == 20
    assert output.loc[0, "discount_amount"] == 2
    assert output.loc[0, "net_amount"] == 18
