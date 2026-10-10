# Ambient Odyssey — one-time initial GitHub repository upload.
# Before running: create a PRIVATE, completely empty repo named Ambient-Odyssey
# under the GitHub account alsynth at https://github.com/new
# (do not initialize it with a GitHub README/.gitignore/license).
# Extract the entire GitHub-ready archive to a normal folder first.
# Run this script in PowerShell from its extracted folder.
param(
    [string]$RepositoryUrl = 'https://github.com/alsynth/Ambient-Odyssey.git'
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
function Invoke-Git {
    & git @args
    if ($LASTEXITCODE -ne 0) { throw "Git command failed (exit $LASTEXITCODE): git $($args -join ' ')" }
}
function Require-Tool([string]$tool, [string]$message) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) { throw $message }
}
Require-Tool git 'Git is not installed. Install Git for Windows, then reopen PowerShell.'
& git lfs version
if ($LASTEXITCODE -ne 0) { throw 'Git LFS is required. Install Git LFS, then rerun this script.' }
$treePack = Join-Path $PSScriptRoot 'release_030\overrides\config\tanshugetrees\custom_packs\#main.zip'
if (-not (Test-Path -LiteralPath $treePack -PathType Leaf)) { throw "Required Tans Huge Trees asset missing. Extract the full GitHub-ready repository ZIP again." }
$expectedBytes = 73500294
$actualBytes = (Get-Item -LiteralPath $treePack).Length
if ($actualBytes -ne $expectedBytes) { throw "Custom worldgen asset size mismatch ($actualBytes vs $expectedBytes)." }
$expectedSha = '0c20b47a6377230e10c53fe36f30efa6c14fd8576928640e7c8af8580122ab89'
$actualSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $treePack).Hash.ToLowerInvariant()
if ($actualSha -ne $expectedSha) { throw 'Custom worldgen asset SHA-256 mismatch.' }
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.git'))) {
    Invoke-Git init -b main
}
Invoke-Git lfs install
Invoke-Git add --all
$expectedPath = 'release_030/overrides/config/tanshugetrees/custom_packs/#main.zip'
$lfsOutput = (& git lfs ls-files) -join "`n"
if ($LASTEXITCODE -ne 0 -or $lfsOutput -notmatch [regex]::Escape($expectedPath)) {
    throw 'Custom worldgen asset was not staged with Git LFS. Do NOT commit until this is fixed.'
}
$headSha = (& git rev-parse --verify HEAD 2>$null)
if ($LASTEXITCODE -ne 0) {
    Invoke-Git commit -m 'Initialize Ambient Odyssey Test 5 Audit1 source and Test 6 handoff'
} else {
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 1) { Invoke-Git commit -m 'Prepare Ambient Odyssey Test 5 Audit1 GitHub handoff' }
}
$existingRemote = (& git remote get-url origin 2>$null)
if ($LASTEXITCODE -ne 0) {
    Invoke-Git remote add origin $RepositoryUrl
} elseif ($existingRemote -ne $RepositoryUrl) {
    throw "origin points to $existingRemote instead of $RepositoryUrl. Resolve that before pushing."
}
Write-Host "`nPushing the repository (including its Git LFS worldgen asset) to $RepositoryUrl" -ForegroundColor Cyan
Invoke-Git push -u origin main
Write-Host "`nSuccess! GitHub repository: $($RepositoryUrl -replace '\.git$','')" -ForegroundColor Green
