param(
    [Parameter(Mandatory = $true)] [string]$Profile,
    [Parameter(Mandatory = $true)] [string]$Region,
    [string]$StackName = "retailflow-web-api",
    [ValidateSet("dev", "prod")] [string]$Environment = "dev",
    [Parameter(Mandatory = $true)] [string]$BucketName,
    [string]$AllowedOrigin = "http://localhost:5173"
)

$ErrorActionPreference = "Stop"
$env:__SAM_CLI_APP_DIR = $env:TEMP
$env:SAM_CLI_TELEMETRY = "0"

sam build --template-file template-api.yaml --use-container
if ($LASTEXITCODE -ne 0) { throw "sam build failed with exit code $LASTEXITCODE" }

sam deploy `
    --template-file .aws-sam/build/template.yaml `
    --stack-name $StackName `
    --region $Region `
    --profile $Profile `
    --capabilities CAPABILITY_IAM `
    --resolve-s3 `
    --no-confirm-changeset `
    --no-fail-on-empty-changeset `
    --parameter-overrides "Environment=$Environment" "BucketName=$BucketName" "AllowedOrigin=$AllowedOrigin"
if ($LASTEXITCODE -ne 0) { throw "sam deploy failed with exit code $LASTEXITCODE" }
