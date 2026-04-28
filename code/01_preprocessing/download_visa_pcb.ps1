# 中文注释：下载 VisA 数据集中 PCB 子集的辅助脚本。
# 主要流程：创建数据目录、配置下载地址、保存并解压原始数据。
# 注意事项：脚本只负责数据准备，不参与后续贝叶斯建模计算。

param(
    [string]$ArchivePath = "",
    [switch]$DeleteArchiveAfterExtract
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$RawRoot = Join-Path $ProjectRoot "data\raw\visa"
$Url = "https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar"
$ExpectedBytes = 1929840640

if (-not (Test-Path $RawRoot)) {
    New-Item -ItemType Directory -Force -Path $RawRoot | Out-Null
}

if ([string]::IsNullOrWhiteSpace($ArchivePath)) {
    if (Test-Path "D:\") {
        $ArchivePath = "D:\VisA_20220922.tar"
    } else {
        $ArchivePath = Join-Path $RawRoot "VisA_20220922.tar"
    }
}

Write-Host "Project root: $ProjectRoot"
Write-Host "Raw data root: $RawRoot"
Write-Host "Archive path: $ArchivePath"

if (-not (Test-Path $ArchivePath)) {
    Write-Host "Downloading VisA archive from AWS Open Data..."
    Write-Host "This file is about 1.93 GB."
    curl.exe -L --fail --continue-at - --output $ArchivePath $Url
} else {
    $currentBytes = (Get-Item $ArchivePath).Length
    if ($currentBytes -eq $ExpectedBytes) {
        Write-Host "Archive already exists and appears complete. Reusing it."
    } elseif ($currentBytes -lt $ExpectedBytes) {
        Write-Host "Archive is incomplete: $currentBytes / $ExpectedBytes bytes."
        Write-Host "Resuming download..."
        curl.exe -L --fail --continue-at - --output $ArchivePath $Url
    } else {
        Write-Host "Archive is larger than expected: $currentBytes / $ExpectedBytes bytes."
        Write-Host "Redownloading from scratch to avoid using a corrupted tar file."
        Remove-Item -LiteralPath $ArchivePath -Force
        curl.exe -L --fail --output $ArchivePath $Url
    }
}

$finalBytes = (Get-Item $ArchivePath).Length
if ($finalBytes -ne $ExpectedBytes) {
    throw "Downloaded archive size is $finalBytes bytes, expected $ExpectedBytes bytes."
}

Write-Host "Inspecting archive structure..."
$members = & tar -tf $ArchivePath

if ($members -match "^VisA/pcb1/") {
    $Prefix = "VisA/"
} elseif ($members -match "^\./VisA/pcb1/") {
    $Prefix = "./VisA/"
} elseif ($members -match "^pcb1/") {
    $Prefix = ""
} else {
    Write-Host $members
    throw "Could not find pcb1 in archive. Please inspect the tar file."
}

Write-Host "Extracting PCB subsets only: pcb1, pcb2, pcb3, pcb4"
$paths = @(
    "${Prefix}pcb1",
    "${Prefix}pcb2",
    "${Prefix}pcb3",
    "${Prefix}pcb4"
)

& tar -xf $ArchivePath -C $RawRoot @paths

if ($DeleteArchiveAfterExtract) {
    Remove-Item -LiteralPath $ArchivePath -Force
    Write-Host "Deleted archive after extraction."
} else {
    Write-Host "Keeping archive because it may be useful for re-extraction."
    Write-Host "To delete it manually later: $ArchivePath"
}

$imageCount = (Get-ChildItem -Path $RawRoot -Recurse -File |
    Where-Object { $_.Extension -match "^\.(jpg|jpeg|png|bmp)$" }).Count

Write-Host "Done."
Write-Host "Extracted image count under raw/visa: $imageCount"
Write-Host "Next step in MATLAB:"
Write-Host "  run code/run_visa_pcb_bayes_project.m"
