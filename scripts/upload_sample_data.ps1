param([string]$Bucket, [string]$Profile = 'default', [string]$Region = 'us-east-1')
$ErrorActionPreference = 'Stop'
if (-not $Bucket) { throw 'Pass -Bucket with the deployed bucket name.' }
aws s3 cp sample_data/valid/ "s3://$Bucket/input/" --recursive --profile $Profile --region $Region
