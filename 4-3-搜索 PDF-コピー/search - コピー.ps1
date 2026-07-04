# UTF-8エンコーディングを設定し、文字化けを防止します
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ================= 設定エリア =================

# 多个搜索目录
$SearchPaths = @(
    "C:\c_wk\10_会社\PDF-相关\pypdf\4-3-検索 - 模糊搜索 PDF 并复制到目标文件夹 - コピー"
    "C:\c_wk\10_会社\PDF-相关\pypdf\4-3-検索 - 模糊搜索 PDF 并复制到目标文件夹 - コピー\新しいフォルダー - コピー"
    # "E:\Backup\PDF"
)

# 复制目标文件夹
$CopyDest = "C:\c_wk\10_会社\PDF-相关\pypdf\新しいフォルダー"

# 搜索编号
$TargetNumbers = @('23','84','76','33','59')

# 复制时加上的日期
$AddDate = "202606"

# 排除关键字（可选）
$ExcludeKeywords = @()

Clear-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PDF 多目录搜索 + 自动改名 + 自动复制ツール" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 创建目标文件夹
if (-not (Test-Path $CopyDest)) {
    New-Item -ItemType Directory -Path $CopyDest | Out-Null
}

Write-Host "`nPDFを検索しています。しばらくお待ちください..." -ForegroundColor Green

# ================= 搜索所有目录 =================
$allPdfs = @()

foreach ($path in $SearchPaths) {
    if (Test-Path $path) {
        $pdfs = Get-ChildItem -Path $path -Filter "*.pdf" -Recurse -ErrorAction SilentlyContinue
        $allPdfs += $pdfs
    } else {
        Write-Host "[警告] ディレクトリが見つかりません: $path" -ForegroundColor Yellow
    }
}

# ================= 条件过滤 =================
$matchedFiles = $allPdfs | Where-Object {
    $name = $_.Name

    # 空格前截断
    $shortName = $name.Split(" ")[0]

    # 匹配编号
    $isTarget = $false
    foreach ($num in $TargetNumbers) {
        if ($shortName -like "*$num*") {
            $isTarget = $true
            break
        }
    }

    # 排除关键字
    $isExclude = $false
    foreach ($ex in $ExcludeKeywords) {
        if ($name -like "*$ex*") {
            $isExclude = $true
            break
        }
    }

    $isTarget -and -not $isExclude
}

# 去重
$uniqueFiles = $matchedFiles | Sort-Object FullName -Unique

# ================= 输出结果 =================
if ($uniqueFiles.Count -eq 0) {
    Write-Host "`n[案内] 条件に一致するPDFファイルは見つかりませんでした。" -ForegroundColor Red
} else {
    Write-Host "`n[成功] $($uniqueFiles.Count) 個のPDFファイルが見つかりました：" -ForegroundColor Green
    $i = 1
    foreach ($file in $uniqueFiles) {
        Write-Host "[$i] $($file.Name)" -ForegroundColor White
        $i++
    }

    # ================= 自动复制 + 自动改名 =================
    Write-Host "`nコピー中: $CopyDest" -ForegroundColor Yellow
    $copiedCount = 0

    foreach ($file in $uniqueFiles) {
        try {
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
            $shortName = $baseName.Split(" ")[0]
            $ext = $file.Extension

            # 新文件名：空格前 + (202606)
            $newName = "$shortName ($AddDate)$ext"
            $destPath = Join-Path $CopyDest $newName

            Copy-Item -Path $file.FullName -Destination $destPath -Force
            $copiedCount++
        } catch {
            Write-Host "[失敗] コピーできません: $($file.Name)" -ForegroundColor Red
        }
    }

    Write-Host "`n[完了] $copiedCount 個のファイルをコピーしました！" -ForegroundColor Green
}

Write-Host "`n[完了] $copiedCount 個のファイルをコピーしました！" -ForegroundColor Green
Write-Host "フォルダを開いて確認してください: $CopyDest" -ForegroundColor Cyan

# ================= 自動終了 =================
Start-Sleep -Seconds 1
exit

