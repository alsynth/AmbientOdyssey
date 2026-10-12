param([string]$Profile, [string]$InstancesRoot = (Join-Path $env:USERPROFILE 'curseforge\minecraft\Instances'))
$ErrorActionPreference = 'Stop'
$instances = [IO.Path]::GetFullPath($InstancesRoot).TrimEnd('\')
if (-not $Profile) {
    Add-Type -AssemblyName System.Windows.Forms
    $picker = New-Object System.Windows.Forms.FolderBrowserDialog
    $picker.Description = 'Select the CurseForge Minecraft profile you want to update. Close Minecraft first.'
    $picker.SelectedPath = $instances
    if ($picker.ShowDialog() -ne 'OK') { exit 0 }
    $Profile = $picker.SelectedPath
}
$target = [IO.Path]::GetFullPath($Profile).TrimEnd('\')
if (-not $target.StartsWith($instances + '\', [StringComparison]::OrdinalIgnoreCase) -or
    [IO.Path]::GetDirectoryName($target) -ne $instances) {
    throw 'Choose one profile directly inside the CurseForge Minecraft Instances folder.'
}
$mods = Join-Path $target 'mods'
if (-not (Test-Path -LiteralPath $mods -PathType Container)) { throw 'This profile has no mods folder.' }
foreach ($directory in @($target, $mods, (Join-Path $target 'config'))) {
    if ((Test-Path -LiteralPath $directory) -and
            ((Get-Item -LiteralPath $directory).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw 'Linked profile/config/mod folders are not supported by this updater.'
    }
}
$required = @('betterinventory-neoforge-1.21.1-1.3.2.jar', 'questlog-neoforge-1.21.1-3.4.1.jar', 'Apotheosis-1.21.1-8.9.0.jar')
foreach ($name in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $mods $name))) { throw "Expected installed mod missing: $name" }
}
$jars = @('ao-affix-trims-0.1.1-experimental.jar', 'ao-questlog-betterinventory-0.1.5.jar')
$hashes = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'SHA256.json') -Raw | ConvertFrom-Json
foreach ($name in $jars) {
    $source = Join-Path $PSScriptRoot ('mods\' + $name)
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { $actualHash = [BitConverter]::ToString($hasher.ComputeHash([IO.File]::ReadAllBytes($source))).Replace('-', '') }
    finally { $hasher.Dispose() }
    if ($actualHash -ne $hashes.$name) { throw "Update JAR failed checksum: $name" }
}
$old = @(Get-ChildItem -LiteralPath $mods -File | Where-Object {
    $_.Name -like 'ao-affix-trims-*.jar' -or $_.Name -like 'ao-questlog-betterinventory-*.jar'
})
$backup = Join-Path $target ('AO-update-backups\trims-questlog-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
$configDir = Join-Path $target 'config'
$config = Join-Path $configDir 'questlog-client.toml'
$hadConfig = Test-Path -LiteralPath $config
foreach ($file in $old) { Copy-Item -LiteralPath $file.FullName -Destination $backup }
if ($hadConfig) { Copy-Item -LiteralPath $config -Destination (Join-Path $backup 'questlog-client.toml') }
# All removal paths are verified absolute, direct children of this profile's mods folder.
foreach ($file in $old) {
    if ([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($file.FullName)) -ne $mods) { throw 'Unsafe addon path.' }
}
try {
    foreach ($file in $old) { Remove-Item -LiteralPath $file.FullName -Force }
    foreach ($name in $jars) { Copy-Item -LiteralPath (Join-Path $PSScriptRoot ('mods\' + $name)) -Destination $mods }
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    $text = if ($hadConfig) { Get-Content -LiteralPath $config -Raw } else { '' }
    $button = [regex]'(?ms)^\[button\]\s*\r?\n.*?(?=^\[|\z)'
    if ($button.IsMatch($text)) {
        $section = $button.Match($text).Value
        if ($section -match '(?m)^enabled\s*=') {
            $updated = [regex]::Replace($section, '(?m)^enabled\s*=\s*(true|false)[^\r\n]*', 'enabled = false')
        } else { $updated = $section.TrimEnd() + "`r`nenabled = false`r`n" }
        $text = $text.Replace($section, $updated)
    } else { $text = $text.TrimEnd() + "`r`n[button]`r`nenabled = false`r`nshowBadge = true`r`n" }
    [IO.File]::WriteAllText($config, $text, [Text.UTF8Encoding]::new($false))
    Write-Host "Updated: $target" -ForegroundColor Green
    Write-Host 'Start this profile normally. Q should be immediately right of Settings; newly found affixed armor gets cosmetic trims.'
    Write-Host "Backup: $backup"
} catch {
    foreach ($name in $jars) {
        $added = Join-Path $mods $name
        if (Test-Path -LiteralPath $added) { Remove-Item -LiteralPath $added -Force }
    }
    foreach ($file in $old) { Copy-Item -LiteralPath (Join-Path $backup $file.Name) -Destination $mods -Force }
    if ($hadConfig) { Copy-Item -LiteralPath (Join-Path $backup 'questlog-client.toml') -Destination $config -Force }
    throw
}
