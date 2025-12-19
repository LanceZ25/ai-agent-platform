param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev","test","prod")]
    [string]$env
)

$rgMap = @{
    dev = "rg-ai-core"
    test = "rg-ai-core-test"
    prod = "rg-ai-core-prod"
}

$rg = $rgMap[$env]
$paramFile = "..\infra\params\$env.json"
$templateFile = "..\infra\core\main.bicep"

Write-Host "=== WHAT-IF Preview for $env ===" -ForegroundColor Cyan

az deployment group what-if `
    --resource-group $rg `
    --template-file $templateFile `
    --parameters $paramFile

Write-Host "`n✅ WHAT-IF preview complete for $env environment." -ForegroundColor Green
