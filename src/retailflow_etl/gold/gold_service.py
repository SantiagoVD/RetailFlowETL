"""Gold dimensional outputs."""

from datetime import datetime
from typing import Any

import pandas as pd

from retailflow_etl.gold.builders.dim_customer_builder import DimCustomerBuilder
from retailflow_etl.gold.builders.dim_date_builder import DimDateBuilder
from retailflow_etl.gold.builders.dim_payment_method_builder import DimPaymentMethodBuilder
from retailflow_etl.gold.builders.dim_product_builder import DimProductBuilder
from retailflow_etl.gold.builders.dim_store_builder import DimStoreBuilder
from retailflow_etl.gold.builders.fact_inventory_builder import FactInventoryBuilder
from retailflow_etl.gold.builders.fact_sales_builder import FactSalesBuilder
from retailflow_etl.storage.parquet_writer import ParquetWriter
from retailflow_etl.storage.path_builder import PathBuilder


class GoldService:
    def __init__(self, repository: Any, paths: PathBuilder) -> None:
        self.repository = repository
        self.paths = paths
        self.parquet = ParquetWriter()

    def process(self, frame: pd.DataFrame, dataset: str, run_id: str, event_time: datetime) -> list[str]:
        outputs: dict[str, pd.DataFrame] = {}
        if dataset == "sales":
            outputs = {"fact_sales": FactSalesBuilder().build(frame), "dim_date": DimDateBuilder().build(frame)}
        elif dataset == "inventory":
            outputs = {"fact_inventory": FactInventoryBuilder().build(frame), "dim_date": DimDateBuilder().build(frame, "snapshot_date")}
        elif dataset == "customers":
            outputs = {"dim_customer": DimCustomerBuilder().build(frame)}
        elif dataset == "products":
            outputs = {"dim_product": DimProductBuilder().build(frame)}
        elif dataset == "stores":
            outputs = {"dim_store": DimStoreBuilder().build(frame)}
        elif dataset == "payments":
            outputs = {"dim_payment_method": DimPaymentMethodBuilder().build(frame)}
        keys = []
        for entity, output in outputs.items():
            key = self.paths.gold_key(entity, run_id, event_time)
            self.repository.put_object(key, self.parquet.to_bytes(output), "application/octet-stream")
            keys.append(key)
        return keys
