param(
    [Parameter(Mandatory = $true)][string]$Archive,
    [Parameter(Mandatory = $true)][string]$Root,
    [Parameter(Mandatory = $true)][string]$RelativePath
)

$ErrorActionPreference = 'Stop'
$rootFull = [System.IO.Path]::GetFullPath($Root)
$target = [System.IO.Path]::GetFullPath((Join-Path $rootFull $RelativePath))
if (-not $target.StartsWith($rootFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Chemin demande hors du perimetre declare.'
}

$manifest = Get-Content -Raw -LiteralPath (Join-Path $rootFull 'manifest.json') | ConvertFrom-Json
$expected = $manifest.files | Where-Object { $_.path -eq $RelativePath }
if ($null -eq $expected) { throw 'Chemin absent du manifeste.' }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead([System.IO.Path]::GetFullPath($Archive))
try {
    $entry = $zip.Entries | Where-Object { $_.FullName -eq $RelativePath }
    if ($null -eq $entry) { throw 'Fichier absent de archive.' }
    $parent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $parent)) { $null = New-Item -ItemType Directory -Path $parent }
    [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $target, $true)
} finally {
    $zip.Dispose()
}

$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash.ToLower()
if ($actual -ne $expected.sha256) { throw 'Empreinte restauree differente de empreinte attendue.' }
Write-Output "RESTAURE $RelativePath sha256=$actual"
