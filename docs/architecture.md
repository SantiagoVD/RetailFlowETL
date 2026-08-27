# AWS architecture

CloudFormation provisions one encrypted private S3 bucket, one Lambda function, one Lambda dependency layer, one least-privilege role and one CloudWatch log group. The bucket notification has an `input/` prefix filter. This is the critical recursion control: Bronze, Silver, Gold, Quarantine and metadata writes cannot trigger the function.

```mermaid
flowchart LR
  S3[S3 bucket input/] -->|ObjectCreated prefix filter| L[Single Lambda]
  L --> S3
  L --> CW[CloudWatch Logs]
  L -. role .-> IAM[IAM least privilege]
```
