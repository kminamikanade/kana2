@echo off
chcp 65001 >nul

echo ========================================
echo 文件名深度搜索工具
echo ========================================
echo.

set /p "keyword=请输入搜索关键词："

if "%keyword%"=="" (
    echo 未输入关键词！
    pause
    exit /b
)

echo.
echo 搜索关键词：%keyword%
echo 正在搜索，请稍候...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$keyword='%keyword%';" ^
"$searchDir='C:\c_wk\10_会社\PDF-相关';" ^
"$results=Get-ChildItem -Path $searchDir -Recurse -File | Where-Object { $_.Name -like ('*'+$keyword+'*') -and $_.Extension -in '.xls','.xlsx' };" ^
"if($results.Count -eq 0){Write-Host '没有找到文件。' -ForegroundColor Yellow}else{" ^
"Write-Host ('找到 '+$results.Count+' 个文件：') -ForegroundColor Green;" ^
"foreach($f in $results){Write-Host '';Write-Host ('文件名：'+$f.Name) -ForegroundColor Cyan;Write-Host ('完整路径：'+$f.FullName);Write-Host '----------------------------------------'}}"

echo.
pause