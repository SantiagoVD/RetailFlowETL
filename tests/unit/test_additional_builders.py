import pandas as pd

from retailflow_etl.gold.builders.dim_customer_builder import DimCustomerBuilder
from retailflow_etl.gold.builders.dim_payment_method_builder import DimPaymentMethodBuilder
from retailflow_etl.gold.builders.dim_product_builder import DimProductBuilder
from retailflow_etl.gold.builders.dim_store_builder import DimStoreBuilder
from retailflow_etl.gold.builders.fact_inventory_builder import FactInventoryBuilder
from retailflow_etl.gold.gold_service import GoldService
from retailflow_etl.storage.path_builder import PathBuilder
from retailflow_etl.storage.s3_repository import InMemoryS3Repository


def test_dimension_builders_create_deterministic_keys():
    customer = pd.DataFrame({"customer_id": ["C1"], "first_name": ["Ana"], "last_name": ["Test"], "email": ["a@x.com"], "city": ["Lima"], "region": ["Central"], "registration_date": ["2026-01-01"], "segment": ["VIP"]})
    product = pd.DataFrame({"product_id": ["P1"], "product_name": ["Coffee"], "category": ["Grocery"], "brand": ["RF"], "unit_cost": [2], "unit_price": [4], "active": [True]})
    store = pd.DataFrame({"store_id": ["S1"], "store_name": ["Main"], "city": ["Lima"], "region": ["Central"], "opening_date": ["2024-01-01"], "active": [True]})
    assert DimCustomerBuilder().build(customer).loc[0, "customer_key"].startswith("C_")
    assert DimProductBuilder().build(product).loc[0, "product_key"].startswith("P_")
    assert DimStoreBuilder().build(store).loc[0, "store_key"].startswith("S_")
    assert DimPaymentMethodBuilder().build(pd.DataFrame({"payment_method": ["CARD"]})).loc[0, "payment_method_key"].startswith("M_")


def test_inventory_fact_assigns_stock_status():
    frame = pd.DataFrame({"inventory_id": ["I1", "I2", "I3"], "store_id": ["S1"] * 3, "product_id": ["P1"] * 3, "stock_quantity": [0, 2, 20], "minimum_stock": [5, 5, 5], "snapshot_date": ["2026-08-27"] * 3})
    output = FactInventoryBuilder().build(frame)
    assert list(output["stock_status"]) == ["OUT_OF_STOCK", "LOW_STOCK", "OK"]


def test_gold_service_supports_all_dataset_outputs():
    timestamp = pd.Timestamp("2026-08-27", tz="UTC")
    cases = {
        "customers": pd.DataFrame({"customer_id": ["C1"], "first_name": ["A"], "last_name": ["B"], "email": ["a@b.com"], "city": ["Lima"], "region": ["Central"], "registration_date": ["2026-01-01"], "segment": ["VIP"]}),
        "products": pd.DataFrame({"product_id": ["P1"], "product_name": ["Coffee"], "category": ["Grocery"], "brand": ["RF"], "unit_cost": [1], "unit_price": [2], "active": [True]}),
        "stores": pd.DataFrame({"store_id": ["S1"], "store_name": ["Main"], "city": ["Lima"], "region": ["Central"], "opening_date": ["2024-01-01"], "active": [True]}),
        "payments": pd.DataFrame({"payment_id": ["M1"], "sale_id": ["A"], "payment_method": ["CARD"], "payment_status": ["PAID"], "payment_date": ["2026-01-01"], "amount": [2]}),
        "inventory": pd.DataFrame({"inventory_id": ["I1"], "store_id": ["S1"], "product_id": ["P1"], "stock_quantity": [1], "minimum_stock": [2], "snapshot_date": ["2026-08-27"]}),
    }
    for dataset, frame in cases.items():
        repository = InMemoryS3Repository()
        assert GoldService(repository, PathBuilder()).process(frame, dataset, "RUN-1", timestamp)
