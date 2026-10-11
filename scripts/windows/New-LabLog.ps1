[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Za-z0-9-]+$')]
    [string]$Id,

    [datetime]$Date = (Get-Date)
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$template = Join-Path $repoRoot 'templates\daily-lab-log.md'
$directory = Join-Path $repoRoot ('evidence\{0:yyyy}\{0:MM}' -f $Date)
$output = Join-Path $directory ('{0:yyyy-MM-dd}_{1}_lab-log.md' -f $Date, $Id)

if (Test-Path -LiteralPath $output) {
    throw "A log already exists at $output"
}

New-Item -ItemType Directory -Path $directory -Force | Out-Null
$content = (Get-Content -LiteralPath $template -Raw).Replace('YYYY-MM-DD', $Date.ToString('yyyy-MM-dd'))
Set-Content -LiteralPath $output -Value $content -Encoding utf8
Write-Output $output
