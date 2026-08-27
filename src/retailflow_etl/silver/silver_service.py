"""Silver transformation and writer."""

from datetime import datetime
from typing import Any

import pandas as pd

from retailflow_etl.silver.transformers.customer_transformer import CustomerTransformer
from retailflow_etl.silver.transformers.inventory_transformer import InventoryTransformer
from retailflow_etl.silver.transformers.payment_transformer import PaymentTransformer
from retailflow_etl.silver.transformers.product_transformer import ProductTransformer
from retailflow_etl.silver.transformers.sales_transformer import SalesTransformer
from retailflow_etl.silver.transformers.store_transformer import StoreTransformer
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder


class SilverService:
    def __init__(self, repository: Any, paths: PathBuilder) -> None:
        self.repository = repository
        self.paths = paths
        self.parquet = ParquetWriter()
        self.transformers = {"sales": SalesTransformer(), "customers": CustomerTransformer(), "products": ProductTransformer(), "stores": StoreTransformer(), "payments": PaymentTransformer(), "inventory": InventoryTransformer()}

    def process(self, frame: pd.DataFrame, dataset: str, run_id: str, event_time: datetime) -> tuple[pd.DataFrame, str]:
        transformed = self.transformers[dataset].transform(frame)
        key = self.paths.data_key("silver", dataset, run_id, event_time)
        self.repository.put_object(key, self.parquet.to_bytes(transformed), "application/octet-stream")
        return transformed, key
