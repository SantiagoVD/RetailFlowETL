"""Generate coherent local RetailFlow datasets without external APIs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_datasets(sales_count: int) -> dict[str, pd.DataFrame]:
    customers = pd.DataFrame([
        {"customer_id": f"C{i:03d}", "first_name": name, "last_name": "Customer", "email": f"customer{i}@example.com", "city": city, "region": "Central", "registration_date": "2026-01-05", "segment": segment}
        for i, (name, city, segment) in enumerate([("Ana", "Lima", "VIP"), ("Bruno", "Cusco", "PREMIUM"), ("Carla", "Lima", "STANDARD"), ("Diego", "Arequipa", "STANDARD"), ("Elena", "Trujillo", "PREMIUM")], 1)
    ])
    products = pd.DataFrame([
        {"product_id": f"P{i:03d}", "product_name": name, "category": category, "brand": "RetailFlow", "unit_cost": cost, "unit_price": price, "active": True}
        for i, (name, category, cost, price) in enumerate([("Coffee", "Grocery", 4.0, 8.5), ("Tea", "Grocery", 3.0, 7.0), ("Notebook", "Stationery", 2.0, 5.5), ("Backpack", "Accessories", 18.0, 35.0), ("Bottle", "Home", 6.0, 14.0)], 1)
    ])
    stores = pd.DataFrame([
        {"store_id": f"S{i:03d}", "store_name": name, "city": city, "region": "Central", "opening_date": "2024-01-15", "active": True}
        for i, (name, city) in enumerate([("Lima Centro", "Lima"), ("Cusco Plaza", "Cusco"), ("Arequipa Mall", "Arequipa")], 1)
    ])
    dates = pd.date_range("2026-08-01", periods=27, freq="D")
    products_by_sale = [8.5, 7.0, 5.5, 35.0, 14.0]
    sales = pd.DataFrame({
        "sale_id": [f"SA{i:06d}" for i in range(1, sales_count + 1)],
        "sale_date": [dates[i % len(dates)].strftime("%Y-%m-%d") for i in range(sales_count)],
        "customer_id": [f"C{(i % 5) + 1:03d}" for i in range(sales_count)],
        "product_id": [f"P{(i % 5) + 1:03d}" for i in range(sales_count)],
        "store_id": [f"S{(i % 3) + 1:03d}" for i in range(sales_count)],
        "payment_id": [f"PAY{i:06d}" for i in range(1, sales_count + 1)],
        "quantity": [(i % 4) + 1 for i in range(sales_count)],
        "unit_price": [products_by_sale[i % 5] for i in range(sales_count)],
        "discount_percentage": [0 if i % 4 else 10 for i in range(sales_count)],
    })
    payments = pd.DataFrame({
        "payment_id": sales["payment_id"], "sale_id": sales["sale_id"],
        "payment_method": [["CARD", "CASH", "TRANSFER", "DIGITAL_WALLET"][i % 4] for i in range(sales_count)],
        "payment_status": "PAID", "payment_date": sales["sale_date"],
        "amount": sales["quantity"] * sales["unit_price"] * (1 - sales["discount_percentage"] / 100),
    })
    inventory = pd.DataFrame([
        {"inventory_id": f"INV{i:04d}", "store_id": f"S{(i % 3) + 1:03d}", "product_id": f"P{(i % 5) + 1:03d}", "stock_quantity": (i * 7) % 80, "minimum_stock": 20, "snapshot_date": "2026-08-27"}
        for i in range(1, 16)
    ])
    return {"sales": sales, "customers": customers, "products": products, "stores": stores, "payments": payments, "inventory": inventory}


def write_datasets(root: Path, sales_count: int = 1000) -> None:
    data = build_datasets(sales_count)
    for dataset, frame in data.items():
        path = root / "valid" / dataset
        path.mkdir(parents=True, exist_ok=True)
        if dataset == "payments":
            frame.to_json(path / "payments.json", orient="records", indent=2)
        elif dataset == "inventory":
            frame.to_excel(path / "inventory.xlsx", index=False)
        else:
            filename = "sales_2026_08_27.csv" if dataset == "sales" else f"{dataset}.csv"
            frame.to_csv(path / filename, index=False)
    invalid_sales = data["sales"].head(4).copy()
    invalid_sales.loc[0, "quantity"] = -1
    invalid_sales.loc[1, "sale_date"] = "not-a-date"
    invalid_sales.loc[2, "sale_id"] = invalid_sales.loc[0, "sale_id"]
    invalid_sales.loc[3, "discount_percentage"] = 120
    invalid_root = root / "invalid"
    (invalid_root / "sales").mkdir(parents=True, exist_ok=True)
    invalid_sales.to_csv(invalid_root / "sales" / "sales_invalid_values.csv", index=False)
    invalid_sales.head(1).assign(quantity=None).to_csv(invalid_root / "sales" / "sales_nulls.csv", index=False)
    invalid_sales.head(2).assign(sale_id="SA_DUPLICATE").to_csv(invalid_root / "sales" / "sales_duplicates.csv", index=False)
    invalid_sales.head(1).assign(sale_date="2026-99-99").to_csv(invalid_root / "sales" / "sales_invalid_dates.csv", index=False)
    (invalid_root / "customers").mkdir(parents=True, exist_ok=True)
    data["customers"].head(1).assign(email="invalid-email").to_csv(invalid_root / "customers" / "customers_invalid.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sales-count", type=int, default=1000, choices=[1000, 10000, 50000, 100000])
    parser.add_argument("--output", type=Path, default=Path("sample_data"))
    args = parser.parse_args()
    write_datasets(args.output, args.sales_count)
