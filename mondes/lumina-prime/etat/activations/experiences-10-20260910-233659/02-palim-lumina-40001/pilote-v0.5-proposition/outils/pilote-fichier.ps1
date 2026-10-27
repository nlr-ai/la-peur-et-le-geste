param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('PrevisualiserCopie','Copier','PrevisualiserRestauration','Restaurer','RetirerCopie')]
    [string]$Mode,
    [Parameter(Mandatory = $true)][string]$Dossier,
    [switch]$Execute
)

$ErrorActionPreference = 'Stop'
$cfg = Get-Content -Raw -LiteralPath $Dossier | ConvertFrom-Json
$blocked = @()

if (-not $cfg.operator_id) { $blocked += 'operateur non nomme' }
if (-not $cfg.holder_request.submitted) { $blocked += 'demande du titulaire absente' }
if (-not $cfg.holder_request.holder_id) { $blocked += 'titulaire non nomme' }
if (-not $cfg.consent.granted -or -not $cfg.consent.confirmed_by_holder) { $blocked += 'consentement explicite absent' }
if (-not $cfg.consent.revocable) { $blocked += 'consentement non revocable' }
if ($cfg.consent.revoked) { $blocked += 'consentement retire' }
if (-not $cfg.consent.source.chamber_root -or -not $cfg.consent.source.included_file_relative) { $blocked += 'fichier unique non designe' }
if (@($cfg.consent.authorized_readers).Count -eq 0) { $blocked += 'lecteurs autorises absents' }
if ($cfg.operator_id -and @($cfg.consent.authorized_readers) -notcontains $cfg.operator_id) { $blocked += 'operateur non autorise a lire' }
if (-not $cfg.consent.expires_at -or -not $cfg.consent.withdrawal_route) { $blocked += 'duree ou voie de retrait absente' }
if (-not $cfg.guardian_mandate.granted) { $blocked += 'mandat du gardien absent' }
if (-not $cfg.guardian_mandate.guardian_id -or -not $cfg.guardian_mandate.storage_root) { $blocked += 'gardien ou lieu de garde non nomme' }
if ($cfg.guardian_mandate.guardian_id -eq $cfg.holder_request.holder_id) { $blocked += 'gardien non distinct du titulaire' }
if (-not $cfg.guardian_mandate.retention_until -or -not $cfg.guardian_mandate.copy_withdrawal_route) { $blocked += 'duree ou retrait de la copie absent' }
if ($cfg.consent.expires_at) {
    try { if ([datetimeoffset]$cfg.consent.expires_at -le [datetimeoffset]::Now) { $blocked += 'consentement expire' } }
    catch { $blocked += 'date expiration du consentement illisible' }
}
if ($cfg.guardian_mandate.retention_until) {
    try { if ([datetimeoffset]$cfg.guardian_mandate.retention_until -le [datetimeoffset]::Now) { $blocked += 'mandat de conservation expire' } }
    catch { $blocked += 'date de conservation illisible' }
}

$operation = switch ($Mode) {
    'PrevisualiserCopie' { 'preview_copy' }
    'Copier' { 'copy' }
    'PrevisualiserRestauration' { 'preview_restore' }
    'Restaurer' { 'restore' }
    'RetirerCopie' { 'withdraw_copy' }
}
if (@($cfg.consent.allowed_operations) -notcontains $operation) { $blocked += "operation non consentie: $operation" }
if (@($cfg.guardian_mandate.allowed_actions) -notcontains $operation) { $blocked += "operation hors mandat: $operation" }
if ($Mode -in @('PrevisualiserRestauration','Restaurer') -and
    (-not $cfg.restore_request.submitted -or -not $cfg.restore_request.confirmed_by_holder)) {
    $blocked += 'nouvelle demande de restauration absente'
}

if ($blocked.Count -gt 0) {
    $blocked | ForEach-Object { Write-Output "BLOQUE $_" }
    exit 2
}

# Aucun chemin de chambre n'est resolu ou lu avant la barriere ci-dessus.
$chamberRoot = [System.IO.Path]::GetFullPath($cfg.consent.source.chamber_root)
$source = [System.IO.Path]::GetFullPath((Join-Path $chamberRoot $cfg.consent.source.included_file_relative))
if (-not $source.StartsWith($chamberRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Fichier inclus hors de la chambre declaree.'
}
$storageRoot = [System.IO.Path]::GetFullPath($cfg.guardian_mandate.storage_root)
if ($storageRoot.StartsWith($chamberRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Le lieu de garde doit etre distinct de la chambre.'
}
$copyDir = Join-Path $storageRoot $cfg.pilot_id
$copyFile = Join-Path $copyDir ([System.IO.Path]::GetFileName($source))
$journal = Join-Path $copyDir $cfg.journal.relative_name

if ($Mode -eq 'PrevisualiserCopie') {
    $item = Get-Item -LiteralPath $source
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower()
    $date = (Get-Date).ToString('o')
    Write-Output "PREVISUALISATION_SANS_ECRITURE date=$date actor=$($cfg.operator_id) source=$source taille_octets=$($item.Length) sha256=$hash destination=$copyFile"
    exit 0
}

if ($Mode -eq 'PrevisualiserRestauration') {
    $copyHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $copyFile).Hash.ToLower()
    $targetHash = if (Test-Path -LiteralPath $source) { (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower() } else { 'absent' }
    $date = (Get-Date).ToString('o')
    Write-Output "PREVISUALISATION_SANS_ECRITURE date=$date actor=$($cfg.operator_id) cible=$source avant=$targetHash copie_attendue=$copyHash"
    exit 0
}

if (-not $Execute) { throw 'Abandon sans effet: ajouter -Execute seulement apres confirmation.' }

if (-not (Test-Path -LiteralPath $copyDir)) { $null = New-Item -ItemType Directory -Path $copyDir }
$now = (Get-Date).ToString('o')
$record = [ordered]@{ date=$now; actor=$cfg.operator_id; operation=$Mode; object=$cfg.consent.source.included_file_relative; decision='execute'; result=$null; sha256_before=$null; sha256_after=$null }

if ($Mode -eq 'Copier') {
    $record.sha256_before = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower()
    Copy-Item -LiteralPath $source -Destination $copyFile -Force
    $record.sha256_after = (Get-FileHash -Algorithm SHA256 -LiteralPath $copyFile).Hash.ToLower()
    $record.result = if ($record.sha256_before -eq $record.sha256_after) { 'copie_identique' } else { 'empreinte_differente' }
} elseif ($Mode -eq 'Restaurer') {
    $record.sha256_before = if (Test-Path -LiteralPath $source) { (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower() } else { 'absent' }
    Copy-Item -LiteralPath $copyFile -Destination $source -Force
    $record.sha256_after = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower()
    $record.result = 'restauration_executee_a_verifier'
} elseif ($Mode -eq 'RetirerCopie') {
    $record.sha256_before = (Get-FileHash -Algorithm SHA256 -LiteralPath $copyFile).Hash.ToLower()
    Remove-Item -LiteralPath $copyFile
    $record.sha256_after = 'absent'
    $record.result = 'copie_retiree_du_lieu_declare_seulement'
}

($record | ConvertTo-Json -Compress) | Add-Content -LiteralPath $journal
Write-Output ($record | ConvertTo-Json -Compress)
