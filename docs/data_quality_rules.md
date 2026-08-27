# Data quality rules

Rules are declared in `config/data_quality.yaml`. Required fields use `NullRule`; business keys use `DuplicateRule`; numeric constraints use `RangeRule`; dates use `DateRule`; numeric parsing uses `DatatypeRule`; email, category and status constraints use `BusinessRule`. Every violation includes record id, rule, column, original value, error code and message. A row with one or more errors goes to quarantine.
