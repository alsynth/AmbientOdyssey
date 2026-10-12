param([string]$Profile)
$ErrorActionPreference = 'Stop'
if (-not $Profile) {
    Add-Type -AssemblyName System.Windows.Forms
    $picker = New-Object System.Windows.Forms.FolderBrowserDialog
    $picker.Description = 'Close Minecraft, then select your Ambient Odyssey profile.'
    $picker.SelectedPath = Join-Path $env:USERPROFILE 'curseforge\minecraft\Instances'
    if ($picker.ShowDialog() -ne 'OK') { exit 0 }
    $Profile = $picker.SelectedPath
}
$target = [IO.Path]::GetFullPath($Profile)
if (-not (Test-Path -LiteralPath (Join-Path $target 'mods') -PathType Container)) { throw 'Choose a Minecraft profile with a mods folder.' }
foreach ($name in @('LegendaryTooltips-1.21.1-neoforge-1.5.5.jar','EquipmentCompare-1.21.1-neoforge-1.3.13.jar','worldweaver-21.0.26.jar','SimplyTooltips-neoforge-0.1.5.jar')) {
    if (-not (Test-Path -LiteralPath (Join-Path $target ('mods\' + $name)))) { throw "Expected mod missing: $name" }
}
$changes = @(
    @('legendarytooltips.toml','client.visual_options','render_item_model','"NONE"'),
    @('legendarytooltips.toml','client.visual_options','enable_tooltip_scrolling','"NEVER"'),
    @('legendarytooltips.toml','client.visual_options','max_tooltip_width','0'),
    @('legendarytooltips.toml','client.visual_options','max_tooltip_height','0'),
    @('legendarytooltips.toml','client.definitions','blacklist','["*"]'),
    @('equipmentcompare.toml','client.visual_options','max_comparisons','1'),
    @('equipmentcompare.toml','client.control_options','strict','true'),
    @('equipmentcompare.toml','client.control_options','blacklist','["*"]'),
    @('simplytooltips/config.toml','','enableTooltipRendering','true'),
    @('simplytooltips/config.toml','general','applyTooltipsToVanillaItems','true'),
    @('simplytooltips/config.toml','general','applyTooltipsToModItems','true'),
    @('simplytooltips/config.toml','general','scrollableTooltip','true'),
    @('simplytooltips/config.toml','general','tooltipTabs','false'),
    @('simplytooltips/config.toml','layout','maxTextWidth','160'),
    @('simplytooltips/config.toml','layout','maxBodyHeight','160')
)
function Set-TomlValue([string]$Text,[string]$Section,[string]$Key,[string]$Value) {
    $pattern = '(?m)^\s*' + [regex]::Escape($Key) + '\s*=[^\r\n]*'
    $replacement = "$Key = $Value"
    if (-not $Section) {
        if (-not [regex]::IsMatch($Text,$pattern)) { throw "Missing setting $Key" }
        return [regex]::Replace($Text,$pattern,$replacement)
    }
    $sectionPattern = '(?ms)^\s*\[' + [regex]::Escape($Section) + '\][^\r\n]*\r?\n.*?(?=^\s*\[|\z)'
    $match = [regex]::Match($Text,$sectionPattern)
    if (-not $match.Success -or -not [regex]::IsMatch($match.Value,$pattern)) { throw "Missing setting $Section.$Key" }
    return $Text.Substring(0,$match.Index) + [regex]::Replace($match.Value,$pattern,$replacement) + $Text.Substring($match.Index+$match.Length)
}
$planned = @{}
foreach ($change in $changes) {
    $name = $change[0]
    $path = Join-Path $target ('config/' + $name)
    if (-not $planned.ContainsKey($name)) {
        $planned[$name] = if (Test-Path -LiteralPath $path) { [IO.File]::ReadAllText($path) } else { [IO.File]::ReadAllText((Join-Path $PSScriptRoot ('config/' + $name))) }
    }
    $planned[$name] = Set-TomlValue $planned[$name] $change[1] $change[2] $change[3]
}
$name = 'wover/client.json'
$path = Join-Path $target ('config/' + $name)
$json = if (Test-Path -LiteralPath $path) { Get-Content -LiteralPath $path -Raw | ConvertFrom-Json } else { Get-Content -LiteralPath (Join-Path $PSScriptRoot ('config/' + $name)) -Raw | ConvertFrom-Json }
$json.internal.did_present_welcome_screen = $true
$json.general.check_for_new_versions = $false
$planned[$name] = ($json | ConvertTo-Json -Depth 20) + "`n"
# Prepare all changes before writing. Back up existing files and roll back on failure.
$backup = Join-Path $target ('AO-update-backups/tooltip-startup-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
$existed = @{}
foreach ($name in $planned.Keys) {
    $path = Join-Path $target ('config/' + $name)
    $existed[$name] = Test-Path -LiteralPath $path
    $directory = Split-Path $path
    foreach ($ancestor in @($target,(Join-Path $target 'config'),$directory)) {
        if ((Test-Path -LiteralPath $ancestor) -and ((Get-Item -LiteralPath $ancestor).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Linked config/profile folders are not supported.' }
    }
    if ((Test-Path -LiteralPath $path) -and ((Get-Item -LiteralPath $path).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Linked config files are not supported.' }
    if ($existed[$name]) {
        $copy = Join-Path $backup $name
        New-Item -ItemType Directory -Path (Split-Path $copy) -Force | Out-Null
        Copy-Item -LiteralPath $path -Destination $copy
    }
}
try {
    foreach ($name in $planned.Keys) {
        $path = Join-Path $target ('config/' + $name)
        New-Item -ItemType Directory -Path (Split-Path $path) -Force | Out-Null
        [IO.File]::WriteAllText($path,$planned[$name],[Text.UTF8Encoding]::new($false))
    }
} catch {
    foreach ($name in $planned.Keys) {
        $path = Join-Path $target ('config/' + $name)
        if ($existed[$name]) { Copy-Item -LiteralPath (Join-Path $backup $name) -Destination $path -Force }
        elseif (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path }
    }
    throw
}
Write-Host 'Tooltip and startup settings updated. Start the profile normally.' -ForegroundColor Green
Write-Host "Backup: $backup"
