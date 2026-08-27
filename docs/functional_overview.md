# Functional overview

RetailFlow receives daily retail extracts from sales, customer, product, store, payment and inventory systems. A file arrival starts one traceable processing run. The business outcome is a clean set of analytics-ready facts and dimensions, while questionable rows remain queryable in quarantine instead of disappearing.

The system supports incremental delivery: every source object is identified by its content checksum. Repeated S3 notifications do not duplicate output after a successful run.
