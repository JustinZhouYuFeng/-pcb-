# 中文注释：下载 VisA 数据集中 PCB 子集的辅助脚本。
# 主要流程：创建数据目录、配置下载地址、保存并解压原始数据。
# 注意事项：脚本只负责数据准备，不参与后续贝叶斯建模计算。

# 行注释：这里声明脚本可接收的命令行参数。
param(
    # 行注释：这里执行当前 PowerShell 命令。
    [string]$ArchivePath = "",
    # 行注释：这里执行当前 PowerShell 命令。
    [switch]$DeleteArchiveAfterExtract
# 行注释：这里结束当前参数、数组或代码块。
)

# 行注释：这里设置 ErrorActionPreference，后续下载或解压会用到。
$ErrorActionPreference = "Stop"

# 模块说明：先确定项目根目录和原始数据保存位置。
# 行注释：这里设置 ProjectRoot，后续下载或解压会用到。
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
# 行注释：这里设置 RawRoot，后续下载或解压会用到。
$RawRoot = Join-Path $ProjectRoot "data\raw\visa"
# 行注释：这里设置 Url，后续下载或解压会用到。
$Url = "https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar"
# 行注释：这里设置 ExpectedBytes，后续下载或解压会用到。
$ExpectedBytes = 1929840640

# 行注释：这里判断当前环境或文件状态是否满足条件。
if (-not (Test-Path $RawRoot)) {
    # 行注释：这里创建需要的目录。
    New-Item -ItemType Directory -Force -Path $RawRoot | Out-Null
# 行注释：这里结束当前参数、数组或代码块。
}

# 行注释：这里判断当前环境或文件状态是否满足条件。
if ([string]::IsNullOrWhiteSpace($ArchivePath)) {
    # 行注释：这里判断当前环境或文件状态是否满足条件。
    if (Test-Path "D:\") {
        # 行注释：这里设置 ArchivePath，后续下载或解压会用到。
        $ArchivePath = "D:\VisA_20220922.tar"
    # 行注释：这里结束当前参数、数组或代码块。
    } else {
        # 行注释：这里设置 ArchivePath，后续下载或解压会用到。
        $ArchivePath = Join-Path $RawRoot "VisA_20220922.tar"
    # 行注释：这里结束当前参数、数组或代码块。
    }
# 行注释：这里结束当前参数、数组或代码块。
}

# 行注释：这里在终端输出提示信息。
Write-Host "Project root: $ProjectRoot"
# 行注释：这里在终端输出提示信息。
Write-Host "Raw data root: $RawRoot"
# 行注释：这里在终端输出提示信息。
Write-Host "Archive path: $ArchivePath"

# 模块说明：如果本地还没有完整压缩包，就从官方地址下载。
# 行注释：这里判断当前环境或文件状态是否满足条件。
if (-not (Test-Path $ArchivePath)) {
    # 行注释：这里在终端输出提示信息。
    Write-Host "Downloading VisA archive from AWS Open Data..."
    # 行注释：这里在终端输出提示信息。
    Write-Host "This file is about 1.93 GB."
    # 行注释：这里调用 curl 下载或续传数据压缩包。
    curl.exe -L --fail --continue-at - --output $ArchivePath $Url
# 行注释：这里结束当前参数、数组或代码块。
} else {
    # 行注释：这里设置 currentBytes，后续下载或解压会用到。
    $currentBytes = (Get-Item $ArchivePath).Length
    # 行注释：这里判断当前环境或文件状态是否满足条件。
    if ($currentBytes -eq $ExpectedBytes) {
        # 行注释：这里在终端输出提示信息。
        Write-Host "Archive already exists and appears complete. Reusing it."
    # 行注释：这里结束当前参数、数组或代码块。
    } elseif ($currentBytes -lt $ExpectedBytes) {
        # 行注释：这里在终端输出提示信息。
        Write-Host "Archive is incomplete: $currentBytes / $ExpectedBytes bytes."
        # 行注释：这里在终端输出提示信息。
        Write-Host "Resuming download..."
        # 行注释：这里调用 curl 下载或续传数据压缩包。
        curl.exe -L --fail --continue-at - --output $ArchivePath $Url
    # 行注释：这里结束当前参数、数组或代码块。
    } else {
        # 行注释：这里在终端输出提示信息。
        Write-Host "Archive is larger than expected: $currentBytes / $ExpectedBytes bytes."
        # 行注释：这里在终端输出提示信息。
        Write-Host "Redownloading from scratch to avoid using a corrupted tar file."
        # 行注释：这里删除不完整或临时的文件。
        Remove-Item -LiteralPath $ArchivePath -Force
        # 行注释：这里调用 curl 下载或续传数据压缩包。
        curl.exe -L --fail --output $ArchivePath $Url
    # 行注释：这里结束当前参数、数组或代码块。
    }
# 行注释：这里结束当前参数、数组或代码块。
}

# 行注释：这里设置 finalBytes，后续下载或解压会用到。
$finalBytes = (Get-Item $ArchivePath).Length
# 行注释：这里判断当前环境或文件状态是否满足条件。
if ($finalBytes -ne $ExpectedBytes) {
    # 行注释：这里主动报错，提醒数据准备没有成功。
    throw "Downloaded archive size is $finalBytes bytes, expected $ExpectedBytes bytes."
# 行注释：这里结束当前参数、数组或代码块。
}

# 行注释：这里在终端输出提示信息。
Write-Host "Inspecting archive structure..."
# 模块说明：检查压缩包内部目录结构，判断解压时应该去掉几层路径前缀。
# 行注释：这里设置 members，后续下载或解压会用到。
$members = & tar -tf $ArchivePath

# 行注释：这里判断当前环境或文件状态是否满足条件。
if ($members -match "^VisA/pcb1/") {
    # 行注释：这里设置 Prefix，后续下载或解压会用到。
    $Prefix = "VisA/"
# 行注释：这里结束当前参数、数组或代码块。
} elseif ($members -match "^\./VisA/pcb1/") {
    # 行注释：这里设置 Prefix，后续下载或解压会用到。
    $Prefix = "./VisA/"
# 行注释：这里结束当前参数、数组或代码块。
} elseif ($members -match "^pcb1/") {
    # 行注释：这里设置 Prefix，后续下载或解压会用到。
    $Prefix = ""
# 行注释：这里结束当前参数、数组或代码块。
} else {
    # 行注释：这里在终端输出提示信息。
    Write-Host $members
    # 行注释：这里主动报错，提醒数据准备没有成功。
    throw "Could not find pcb1 in archive. Please inspect the tar file."
# 行注释：这里结束当前参数、数组或代码块。
}

# 行注释：这里在终端输出提示信息。
Write-Host "Extracting PCB subsets only: pcb1, pcb2, pcb3, pcb4"
# 模块说明：只抽取 PCB1 到 PCB4 的正常图、缺陷图和掩膜，避免解压无关类别。
# 行注释：这里设置 paths，后续下载或解压会用到。
$paths = @(
    # 行注释：这里执行当前 PowerShell 命令。
    "${Prefix}pcb1",
    # 行注释：这里执行当前 PowerShell 命令。
    "${Prefix}pcb2",
    # 行注释：这里执行当前 PowerShell 命令。
    "${Prefix}pcb3",
    # 行注释：这里执行当前 PowerShell 命令。
    "${Prefix}pcb4"
# 行注释：这里结束当前参数、数组或代码块。
)

# 行注释：这里执行当前 PowerShell 命令。
& tar -xf $ArchivePath -C $RawRoot @paths

# 行注释：这里判断当前环境或文件状态是否满足条件。
if ($DeleteArchiveAfterExtract) {
    # 行注释：这里删除不完整或临时的文件。
    Remove-Item -LiteralPath $ArchivePath -Force
    # 行注释：这里在终端输出提示信息。
    Write-Host "Deleted archive after extraction."
# 行注释：这里结束当前参数、数组或代码块。
} else {
    # 行注释：这里在终端输出提示信息。
    Write-Host "Keeping archive because it may be useful for re-extraction."
    # 行注释：这里在终端输出提示信息。
    Write-Host "To delete it manually later: $ArchivePath"
# 行注释：这里结束当前参数、数组或代码块。
}

# 模块说明：最后统计解压出的图像数量，快速确认数据是否准备成功。
# 行注释：这里设置 imageCount，后续下载或解压会用到。
$imageCount = (Get-ChildItem -Path $RawRoot -Recurse -File |
    Where-Object { $_.Extension -match "^\.(jpg|jpeg|png|bmp)$" }).Count

# 行注释：这里在终端输出提示信息。
Write-Host "Done."
# 行注释：这里在终端输出提示信息。
Write-Host "Extracted image count under raw/visa: $imageCount"
# 行注释：这里在终端输出提示信息。
Write-Host "Next step in MATLAB:"
# 行注释：这里在终端输出提示信息。
Write-Host "  run code/run_visa_pcb_bayes_project.m"
