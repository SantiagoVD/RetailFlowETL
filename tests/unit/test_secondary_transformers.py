import pandas as pd

from retailflow_etl.silver.transformers.inventory_transformer import InventoryTransformer
from retailflow_etl.silver.transformers.payment_transformer import PaymentTransformer
from retailflow_etl.silver.transformers.product_transformer import ProductTransformer
from retailflow_etl.silver.transformers.store_transformer import StoreTransformer


def test_product_transformer_normalizes_numeric_and_boolean_values():
    frame = pd.DataFrame({"product_id": ["P1"], "product_name": [" notebook "], "category": ["stationery"], "brand": ["brand"], "unit_cost": ["2"], "unit_price": ["5"], "active": ["TRUE"]})
    output = ProductTransformer().transform(frame)
    assert output.loc[0, "product_name"] == "Notebook"
    assert output.loc[0, "unit_price"] == 5
    assert bool(output.loc[0, "active"])


def test_store_transformer_normalizes_location_and_date():
    frame = pd.DataFrame({"store_id": ["S1"], "store_name": [" lima centro "], "city": ["lima"], "region": ["central"], "opening_date": ["2024-01-01"], "active": ["true"]})
    output = StoreTransformer().transform(frame)
    assert output.loc[0, "store_name"] == "Lima Centro"
    assert output.loc[0, "opening_date"] == "2024-01-01"


def test_payment_transformer_normalizes_categories():
    frame = pd.DataFrame({"payment_id": ["M1"], "sale_id": ["A"], "payment_method": [" card "], "payment_status": ["paid"], "payment_date": ["2026-01-01"], "amount": ["2.5"]})
    output = PaymentTransformer().transform(frame)
    assert output.loc[0, "payment_method"] == "CARD"
    assert output.loc[0, "amount"] == 2.5


def test_inventory_transformer_converts_values():
    frame = pd.DataFrame({"inventory_id": ["I1"], "store_id": ["S1"], "product_id": ["P1"], "stock_quantity": ["2"], "minimum_stock": ["5"], "snapshot_date": ["2026-08-27"]})
    output = InventoryTransformer().transform(frame)
    assert output.loc[0, "stock_quantity"] == 2
