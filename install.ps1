[CmdletBinding()]
param(
    [string]$TargetDir = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.claude/skills'),
    [switch]$Force
)
$ErrorActionPreference = 'Stop'

function Assert-SafePath([string]$Path) {
    $current = [IO.Path]::GetFullPath($Path)
    while ($current) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Linked paths are not supported: $current"
            }
        }
        $parent = [IO.Directory]::GetParent($current)
        if ($null -eq $parent) { break }
        $current = $parent.FullName
    }
}

try {
    if ([string]::IsNullOrWhiteSpace($TargetDir)) { throw 'TargetDir must name a skills directory.' }
    $root = [IO.Path]::GetFullPath($TargetDir)
    $destination = Join-Path $root 'deal-inspector'
    $marker = Join-Path $destination '.deal-inspector-owned'
    Assert-SafePath $destination
    foreach ($name in @('SKILL.md', 'LICENSE')) {
        if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $name) -PathType Leaf)) {
            throw "$name is missing beside the installer."
        }
    }
    if (Test-Path -LiteralPath $destination) {
        if (-not (Test-Path -LiteralPath $destination -PathType Container)) { throw 'Install destination is not a directory.' }
        Assert-SafePath $marker
        if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) { throw 'Existing directory has no Deal Inspector ownership marker; refusing to overwrite it.' }
        $lines = @(Get-Content -LiteralPath $marker)
        if ($lines.Count -ne 3 -or $lines[0] -cne 'deal-inspector-v2' -or
            $lines[1] -cnotmatch '^[a-f0-9]{64}  SKILL\.md$' -or
            $lines[2] -cnotmatch '^[a-f0-9]{64}  LICENSE$') { throw 'Invalid ownership marker.' }
        foreach ($name in @('SKILL.md', 'LICENSE')) {
            $owned = Join-Path $destination $name
            Assert-SafePath $owned
            if ((Test-Path -LiteralPath $owned) -and -not (Test-Path -LiteralPath $owned -PathType Leaf)) { throw "Owned path is not a file: $name" }
        }
        if (-not $Force) { throw 'Already installed. Use -Force to replace the two owned files; local edits will be overwritten.' }
    }
    New-Item -ItemType Directory -Path $destination -Force | Out-Null
    $stage = Join-Path $destination ('.install.' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $stage | Out-Null
    try {
        $manifest = @('deal-inspector-v2')
        foreach ($name in @('SKILL.md', 'LICENSE')) {
            Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination (Join-Path $stage $name)
            $hash = (Get-FileHash -LiteralPath (Join-Path $stage $name) -Algorithm SHA256).Hash.ToLowerInvariant()
            $manifest += "$hash  $name"
        }
        [IO.File]::WriteAllText((Join-Path $stage '.deal-inspector-owned'), ($manifest -join "`n") + "`n", [Text.UTF8Encoding]::new($false))
        # Replace path entries rather than writing through a possible hard link.
        foreach ($name in @('SKILL.md', 'LICENSE', '.deal-inspector-owned')) {
            $owned = Join-Path $destination $name
            if (Test-Path -LiteralPath $owned) { Remove-Item -LiteralPath $owned -Force }
            Move-Item -LiteralPath (Join-Path $stage $name) -Destination $owned -Force
        }
    } finally {
        foreach ($name in @('SKILL.md', 'LICENSE', '.deal-inspector-owned')) {
            $stagedFile = Join-Path $stage $name
            if (Test-Path -LiteralPath $stagedFile -PathType Leaf) { Remove-Item -LiteralPath $stagedFile -Force }
        }
        # Dot-prefixed staging paths are hidden on Unix; -Force permits only this checked, empty path.
        if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Force }
    }
    Write-Host "Installed Deal Inspector in $destination"
    Write-Host 'Start a new Claude Code session and invoke /deal-inspector.'
    Write-Host 'An old deal-inspector-SKILL.md file is left untouched. Use uninstall.ps1 -Legacy -Force with the same TargetDir to remove it explicitly.'
} catch {
    Write-Error ("{0} (line {1})" -f $_.Exception.Message, $_.InvocationInfo.ScriptLineNumber) -ErrorAction Continue
    exit 1
}

