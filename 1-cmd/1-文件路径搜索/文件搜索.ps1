$keyword = Read-Host "请输入搜索关键词"

if ([string]::IsNullOrWhiteSpace($keyword)) {
    Write-Host "未输入关键词！" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "搜索关键词：$keyword"
Write-Host "正在搜索，请稍候..."
Write-Host ""

$searchDir = "C:\c_wk\10_会社\PDF-相关"

$results = Get-ChildItem `
    -Path $searchDir `
    -Recurse `
    -File `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -like "*$keyword*"
    }


if ($null -eq $results -or $results.Count -eq 0) {

    Write-Host "没有找到文件。" -ForegroundColor Yellow

}
else {

    Write-Host "找到 $($results.Count) 个文件：" -ForegroundColor Green
    Write-Host "========================================"

    foreach ($f in $results) {

        Write-Host $f.FullName
    }
}