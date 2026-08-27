$ErrorActionPreference = 'Stop'
sam validate --template-file template.yaml
sam build --template-file template.yaml
