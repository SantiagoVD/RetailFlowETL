# Security notes

- The bucket blocks public access and uses S3-managed encryption.
- The Lambda role grants read access only to `input/` and read/write access only to ETL output prefixes.
- The S3 notification filters on `input/`, preventing output recursion.
- Credentials are supplied by the AWS CLI profile or execution role; none are stored in this repository.
- Production deployments should supply a unique bucket name and review the generated CloudFormation change set.
