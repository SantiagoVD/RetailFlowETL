$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath '.aws-sam') { Remove-Item -LiteralPath '.aws-sam' -Recurse -Force }
Get-ChildItem -Path . -Recurse -Filter '__pycache__' -Directory | Remove-Item -Recurse -Force
