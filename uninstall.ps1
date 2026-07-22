param()

$candidates = @(
    "$env:USERPROFILE\.claude\skills\deal-inspector-SKILL.md",
    "$env:USERPROFILE\.config\opencode\skills\deal-inspector-SKILL.md",
    "$env:USERPROFILE\.local\share\claude\skills\deal-inspector-SKILL.md"
)

$found = $false
foreach ($path in $candidates) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Force
        Write-Host "Removed $path" -ForegroundColor Yellow
        $found = $true
    }
}

if (-not $found) {
    Write-Host "Deal Inspector is not installed." -ForegroundColor Red
} else {
    Write-Host "Deal Inspector uninstalled." -ForegroundColor Green
}
