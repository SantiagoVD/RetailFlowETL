# Cost control

The design uses one on-demand Lambda, one S3 bucket, a short CloudWatch retention period and no provisioned concurrency or permanently running compute. Keep sample files small, use lifecycle rules for old Parquet in real environments, set a budget alert, and destroy development stacks after testing. The Lambda memory/timeout are sized for small and medium files; distributed processing is a separate future decision.
