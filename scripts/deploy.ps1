param(
    [string]$Profile = 'default',
    [string]$Region = 'us-east-1',
    [string]$StackName = 'retailflow-serverless-etl',
    [string]$Environment = 'dev',
    [string]$BucketName = ''
)
$ErrorActionPreference = 'Stop'
sam build --template-file template.yaml --use-container
$deployArgs = @('--stack-name', $StackName, '--region', $Region, '--profile', $Profile, '--capabilities', 'CAPABILITY_IAM', '--no-confirm-changeset', '--no-fail-on-empty-changeset', '--parameter-overrides', "Environment=$Environment")
if ($BucketName) { $deployArgs += "BucketName=$BucketName" }
sam deploy @deployArgs
