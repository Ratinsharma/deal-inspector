[CmdletBinding()]
param(
    [string]$TargetDir = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.claude/skills'),
    [switch]$Force,
    [switch]$Legacy
)
$ErrorActionPreference = 'Stop'

function Assert-SafePath([string]$Path) {
    $current = [IO.Path]::GetFullPath($Path)
    while ($current) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked paths are not supported: $current" }
        }
        $parent = [IO.Directory]::GetParent($current)
        if ($null -eq $parent) { break }
        $current = $parent.FullName
    }
}

try {
    if ([string]::IsNullOrWhiteSpace($TargetDir)) { throw 'TargetDir must name a skills directory.' }
    $root = [IO.Path]::GetFullPath($TargetDir)
    if ($Legacy) {
        $legacyPath = Join-Path $root 'deal-inspector-SKILL.md'
        Assert-SafePath $legacyPath
        if (-not (Test-Path -LiteralPath $legacyPath)) { Write-Host 'Legacy file is not installed in the selected directory.'; exit 0 }
        if (-not (Test-Path -LiteralPath $legacyPath -PathType Leaf)) { throw 'Legacy path is not a file.' }
        if (-not $Force) { throw 'Legacy ownership cannot be verified. Use -Legacy -Force to explicitly remove only deal-inspector-SKILL.md.' }
        Remove-Item -LiteralPath $legacyPath -Force
        Write-Host "Removed legacy file: $legacyPath"
        exit 0
    }
    $destination = Join-Path $root 'deal-inspector'
    Assert-SafePath $destination
    if (-not (Test-Path -LiteralPath $destination)) { Write-Host 'Deal Inspector is not installed in the selected directory.'; exit 0 }
    if (-not (Test-Path -LiteralPath $destination -PathType Container)) { throw 'Install destination is not a directory.' }
    $marker = Join-Path $destination '.deal-inspector-owned'
    Assert-SafePath $marker
    if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) { throw 'No ownership marker; refusing to remove files.' }
    $lines = @(Get-Content -LiteralPath $marker)
    if ($lines.Count -ne 3 -or $lines[0] -cne 'deal-inspector-v2' -or
        $lines[1] -cnotmatch '^[a-f0-9]{64}  SKILL\.md$' -or
        $lines[2] -cnotmatch '^[a-f0-9]{64}  LICENSE$') { throw 'Invalid ownership marker.' }
    $ownedPaths = @()
    for ($index = 1; $index -le 2; $index++) {
        $name = if ($index -eq 1) { 'SKILL.md' } else { 'LICENSE' }
        $owned = Join-Path $destination $name
        Assert-SafePath $owned
        if (Test-Path -LiteralPath $owned) {
            if (-not (Test-Path -LiteralPath $owned -PathType Leaf)) { throw "Owned path is not a file: $name" }
            $hash = (Get-FileHash -LiteralPath $owned -Algorithm SHA256).Hash.ToLowerInvariant()
            if (-not $Force -and $hash -cne $lines[$index].Substring(0, 64)) { throw "$name has local changes. Use -Force to remove the owned files anyway." }
            $ownedPaths += $owned
        }
    }
    # All resolved paths and hashes were checked before any file is removed.
    foreach ($owned in $ownedPaths) { Remove-Item -LiteralPath $owned -Force }
    Remove-Item -LiteralPath $marker -Force
    if (@(Get-ChildItem -LiteralPath $destination -Force).Count -eq 0) {
        Remove-Item -LiteralPath $destination
    } else { Write-Host 'Other files remain in the installation folder and were preserved.' }
    Write-Host "Uninstalled Deal Inspector from $destination"
} catch {
    Write-Error ("{0} (line {1})" -f $_.Exception.Message, $_.InvocationInfo.ScriptLineNumber) -ErrorAction Continue
    exit 1
}
