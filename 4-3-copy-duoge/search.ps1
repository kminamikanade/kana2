[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$SearchPaths = @(
    "C:\c_wk",
    "C:\Work"
)

$CopyDest = "C:\Work\新しいフォルダー"

$TargetNumbers = @(
'3 (1)',
"1(1) - コピー",
"222",
"555",
"1111"



# '1 (2)'
)
$ExcludeKeywords = @('送')

Clear-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PDF 正確検索＆コピーツール（複数フォルダ対応）" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "対象番号: $($TargetNumbers -join ', ')" -ForegroundColor Yellow
Write-Host "除外キーワード: $($ExcludeKeywords -join ', ')" -ForegroundColor Magenta

if (-not (Test-Path $CopyDest)) {
    New-Item -ItemType Directory -Path $CopyDest | Out-Null
}

Write-Host "`n複数フォルダを検索しています。しばらくお待ちください..." -ForegroundColor Green

$allPdfs = foreach ($path in $SearchPaths) {
    if (Test-Path $path) {
        Get-ChildItem -Path $path -Filter "*" -Recurse -ErrorAction SilentlyContinue
    } else {
        Write-Host "[警告] フォルダが存在しません: $path" -ForegroundColor Red
    }
}

$matchedFiles = $allPdfs | Where-Object {
    $name = $_.Name
    
    $isTarget = $TargetNumbers | ForEach-Object { $name -like "*$_*" } | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count
    $isTarget = ($isTarget -gt 0)

    $isExclude = $ExcludeKeywords | ForEach-Object { $name -like "*$_*" } | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count
    $isExclude = ($isExclude -gt 0)

    $isTarget -and -not $isExclude
}

$uniqueFiles = $matchedFiles | Sort-Object FullName -Unique

if ($uniqueFiles.Count -eq 0) {
    Write-Host "`n条件に一致するPDFファイルは見つかりませんでした。" -ForegroundColor Red
} else {
    Write-Host "`n$($uniqueFiles.Count) 個のPDFファイルが見つかりました：" -ForegroundColor Green
    $i = 1
    foreach ($file in $uniqueFiles) {
        Write-Host "[$i] $($file.FullName)" -ForegroundColor White
        $i++
    }

    Write-Host "`nコピー中: $CopyDest" -ForegroundColor Yellow
    $copiedCount = 0
    foreach ($file in $uniqueFiles) {
        try {
            Copy-Item -Path $file.FullName -Destination $CopyDest -Force
            $copiedCount++
        } catch {
            Write-Host "コピーできません: $($file.Name)" -ForegroundColor Red
        }
    }
    Write-Host "`n$copiedCount 個のファイルのコピーに成功しました！" -ForegroundColor Green
}


Write-Host "処理完了" -ForegroundColor Green
