[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$failures = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()

$forbiddenExtensions = @('.iso', '.ova', '.ovf', '.vdi', '.vmdk', '.qcow2', '.pcap', '.pcapng', '.pfx', '.p12', '.pem', '.key')
$files = Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Force |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' }

foreach ($file in $files) {
    if ($forbiddenExtensions -contains $file.Extension.ToLowerInvariant()) {
        $failures.Add("Forbidden artifact: $($file.FullName.Substring($repoRoot.Length + 1))")
    }
    if ($file.Length -gt 10MB) {
        $warnings.Add("Large file requires review: $($file.FullName.Substring($repoRoot.Length + 1))")
    }
}

$textExtensions = @('.md', '.txt', '.json', '.xml', '.yml', '.yaml', '.ps1', '.sh', '.conf', '.ini')
$patterns = @(
    @{ Name = 'Private key'; Regex = '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----' },
    @{ Name = 'AWS access key shape'; Regex = 'AKIA[0-9A-Z]{16}' },
    @{ Name = 'GitHub token shape'; Regex = 'gh[pousr]_[A-Za-z0-9_]{20,}' },
    @{ Name = 'Generic assigned secret'; Regex = '(?i)(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*["''][^"'']{6,}["'']' }
)

foreach ($file in $files | Where-Object {
    $textExtensions -contains $_.Extension.ToLowerInvariant() -and $_.FullName -ne $PSCommandPath
}) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    foreach ($pattern in $patterns) {
        if ($content -match $pattern.Regex) {
            $failures.Add("$($pattern.Name) pattern: $($file.FullName.Substring($repoRoot.Length + 1))")
        }
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot 'README.md'))) {
    $failures.Add('README.md is missing')
}
if (-not (Test-Path -LiteralPath (Join-Path $repoRoot 'SECURITY.md'))) {
    $failures.Add('SECURITY.md is missing')
}

foreach ($warning in $warnings) { Write-Warning $warning }
if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ -ErrorAction Continue }
    throw "Repository validation failed with $($failures.Count) issue(s)."
}

Write-Host "Repository validation passed for $($files.Count) files." -ForegroundColor Green
Write-Host 'Manual review of screenshots and Git history is still required.' -ForegroundColor Yellow
