# UTF-8エンコーディングを設定し、文字化けを防止します
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ================= 設定エリア =================
$SearchPath = "C:\c_wk"                     # 検索ルートディレクトリ
$SearchPath = "C:\Work"                     # 検索ルートディレクトリ

$CopyDest = "C:\Work\新しいフォルダー"      # 見つかったファイルはここにコピーされます

# 検索対象とする5つの正確な番号
$TargetNumbers = @('3 (1)', '1 (2)') 

# 除外キーワード（ファイル名にこれらの文字が含まれている場合はスキップします）
$ExcludeKeywords = @('送') 
# ============================================

Clear-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   15Aシリーズ PDF 正確検索＆コピーツール  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "対象番号: $($TargetNumbers -join ', ')" -ForegroundColor Yellow
Write-Host "除外キーワード: $($ExcludeKeywords -join ', ')" -ForegroundColor Magenta

# ディレクトリの存在確認
if (-not (Test-Path $SearchPath)) {
    Write-Host "`n[エラー] ディレクトリが見つかりません: $SearchPath" -ForegroundColor Red
    Read-Host "`nEnterキーを押して終了します"
    exit
}

# コピー先フォルダの作成
if (-not (Test-Path $CopyDest)) {
    New-Item -ItemType Directory -Path $CopyDest | Out-Null
}

Write-Host "`n指定された番号を正確に検索しています。しばらくお待ちください..." -ForegroundColor Green

# 全PDFファイルを取得
$allPdfs = Get-ChildItem -Path $SearchPath -Filter "*" -Recurse -ErrorAction SilentlyContinue

# 条件に一致するファイルをフィルタリング
$matchedFiles = $allPdfs | Where-Object {
    $name = $_.Name
    
    # 1. 対象番号が含まれているかチェック
    $isTarget = $false
    foreach ($num in $TargetNumbers) {
        if ($name -like "*$num*") { 
            $isTarget = $true
            break 
        }
    }
    
    # 2. 除外キーワードが含まれているかチェック
    $isExclude = $false
    foreach ($ex in $ExcludeKeywords) {
        if ($name -like "*$ex*") { 
            $isExclude = $true
            break 
        }
    }
    
    # 対象番号を含み、かつ除外キーワードを含まない場合のみTrue
    $isTarget -and -not $isExclude
}

# 重複を削除（念のため）
$uniqueFiles = $matchedFiles | Sort-Object FullName -Unique

if ($uniqueFiles.Count -eq 0) {
    Write-Host "`n[案内] 条件に一致するPDFファイルは見つかりませんでした。" -ForegroundColor Red
} else {
    Write-Host "`n[成功] 正確に $($uniqueFiles.Count) 個のPDFファイルが見つかりました：" -ForegroundColor Green
    $i = 1
    foreach ($file in $uniqueFiles) {
        Write-Host "[$i] $($file.Name)" -ForegroundColor White
        $i++
    }

    # 自動コピー
    Write-Host "`n自動的にコピー中: $CopyDest" -ForegroundColor Yellow
    $copiedCount = 0
    foreach ($file in $uniqueFiles) {
        try {
            Copy-Item -Path $file.FullName -Destination $CopyDest -Force
            $copiedCount++
        } catch {
            Write-Host "[失敗] コピーできません: $($file.Name)" -ForegroundColor Red
        }
    }
    Write-Host "`n[完了] $copiedCount 個のファイルのコピーに成功しました！" -ForegroundColor Green
    Write-Host "フォルダを開いて確認してください: $CopyDest" -ForegroundColor Cyan
}

# ================= 終了待機 =================
Read-Host "`n処理が完了しました。Enterキーを押して終了します"