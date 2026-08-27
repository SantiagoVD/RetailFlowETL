# Testing strategy

Unit tests use small dataframes and fake repositories; no unit test calls AWS. Integration tests use `InMemoryS3Repository` to exercise event parsing, all layers, invalid-row quarantine, failure visibility and checksum idempotency. Coverage is measured with pytest-cov. SAM validation/build are infrastructure checks rather than AWS deployments.
