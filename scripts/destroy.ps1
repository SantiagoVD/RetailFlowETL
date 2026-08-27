param(
    [string]$Profile = 'default',
    [string]$Region = 'us-east-1',
    [string]$StackName = 'retailflow-serverless-etl',
    [switch]$EmptyBucket
)
$ErrorActionPreference = 'Stop'
$confirmation = Read-Host "Type DESTROY to delete stack '$StackName'"
if ($confirmation -ne 'DESTROY') { Write-Output 'Cancelled.'; exit 0 }
if ($EmptyBucket) {
    $bucket = aws cloudformation describe-stacks --stack-name $StackName --query "Stacks[0].Outputs[?OutputKey=='DataBucketName'].OutputValue" --output text --profile $Profile --region $Region
    if ($bucket -and $bucket -ne 'None') { aws s3 rm "s3://$bucket" --recursive --profile $Profile --region $Region }
}
sam delete --stack-name $StackName --profile $Profile --region $Region --no-prompts
