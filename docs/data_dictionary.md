# Data dictionary

Sales: `sale_id` key, `sale_date` date, customer/product/store/payment references, `quantity` and `unit_price` numeric, `discount_percentage` 0-100.

Customers: `customer_id` key, names/email/location strings, `registration_date` date, `segment` STANDARD/PREMIUM/VIP.

Products: `product_id` key, descriptive strings, `unit_cost` and `unit_price` non-negative, `active` boolean.

Stores: `store_id` key, name/location strings, `opening_date` date, `active` boolean.

Payments: `payment_id` key, `sale_id` reference, method CASH/CARD/TRANSFER/DIGITAL_WALLET, status PAID/PENDING/REFUNDED, date and non-negative amount.

Inventory: `inventory_id` key, store/product references, non-negative stock and minimum stock, snapshot date.
