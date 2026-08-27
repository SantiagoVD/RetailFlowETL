param([string]$Event = 'events/s3_sales_event.json')
$ErrorActionPreference = 'Stop'
sam build --template-file template.yaml
sam local invoke RetailFlowFunction --event $Event
