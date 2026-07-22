param(
    [string]$TargetDir = "",
    [switch]$Force = $false
)

$skillFile = Join-Path $PSScriptRoot "SKILL.md"

if (-not (Test-Path $skillFile)) {
    Write-Error "SKILL.md not found next to this script. Run install.ps1 from the repo root."
    exit 1
}

# Detect target directory
if (-not $TargetDir) {
    $candidates = @(
        "$env:USERPROFILE\.claude\skills",
        "$env:USERPROFILE\.config\opencode\skills",
        "$env:USERPROFILE\.claude\skills\ecc",
        "$env:USERPROFILE\.local\share\claude\skills"
    )
    foreach ($dir in $candidates) {
        if (Test-Path $dir) {
            $TargetDir = $dir
            break
        }
    }
}

if (-not $TargetDir) {
    # Default to ECC skills dir
    $TargetDir = "$env:USERPROFILE\.claude\skills"
}

# Create target if missing
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    Write-Host "Created $TargetDir" -ForegroundColor Yellow
}

$targetPath = Join-Path $TargetDir "deal-inspector-SKILL.md"

if ((Test-Path $targetPath) -and -not $Force) {
    $response = Read-Host "$targetPath already exists. Overwrite? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "Install cancelled." -ForegroundColor Red
        exit 1
    }
}

Copy-Item -Path $skillFile -Destination $targetPath -Force
Write-Host "Installed Deal Inspector to $targetPath" -ForegroundColor Green
Write-Host ""
Write-Host "Load it in Claude Code:  /skill deal-inspector" -ForegroundColor Cyan
