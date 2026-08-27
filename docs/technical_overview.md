# Technical overview

`etl_handler.py` parses the event and constructs the service graph. `EtlService` owns the sequence and delegates to cohesive services. `S3Repository` is the only production boto3 boundary. `ParquetWriter` centralizes PyArrow serialization. Rules are classes configured through YAML; transformers and builders are one responsibility per dataset concern.

The in-memory repository is deliberately limited to tests and local logic checks. Production uses S3 with the same interface. All outputs are partitioned by event date and run id for traceability.
