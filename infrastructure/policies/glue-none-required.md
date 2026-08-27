# Architecture decision

AWS Glue is intentionally not required. This portfolio pipeline is bounded to small and medium files and runs in one Lambda to minimize operational cost and infrastructure. Larger workloads would require a separate architecture review.
