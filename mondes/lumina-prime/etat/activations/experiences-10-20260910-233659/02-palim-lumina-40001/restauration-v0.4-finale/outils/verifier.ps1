param(
    [string]$Root = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$rootFull = [System.IO.Path]::GetFullPath($Root)
$manifestPath = Join-Path $rootFull 'manifest.json'
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$errors = @()

foreach ($item in $manifest.files) {
    $path = [System.IO.Path]::GetFullPath((Join-Path $rootFull $item.path))
    if (-not $path.StartsWith($rootFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        $errors += "Hors racine: $($item.path)"
        continue
    }
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $errors += "Fichier absent: $($item.path)"
        continue
    }
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower()
    if ($actual -ne $item.sha256) {
        $errors += "Empreinte différente: $($item.path)"
    }
}

$jsonFiles = Get-ChildItem -Recurse -File -LiteralPath $rootFull -Filter '*.json'
foreach ($file in $jsonFiles) {
    try { $null = Get-Content -Raw -LiteralPath $file.FullName | ConvertFrom-Json }
    catch { $errors += "JSON illisible: $($file.FullName.Substring($rootFull.Length + 1))" }
}

foreach ($reference in $manifest.references) {
    $path = [System.IO.Path]::GetFullPath((Join-Path $rootFull $reference))
    if (-not $path.StartsWith($rootFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        $errors += "Référence hors racine: $reference"
    } elseif (-not (Test-Path -LiteralPath $path)) {
        $errors += "Référence manquante: $reference"
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Output "ERREUR $_" }
    exit 1
}

Write-Output "OK fichiers=$($manifest.files.Count) json=$($jsonFiles.Count) references=$($manifest.references.Count)"

