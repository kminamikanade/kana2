
@echo off
chcp 65001 >nul

rem ====== 在这里修改您的 PDF 文件夹绝对路径 ======
set "targetFolder=C:\Users\qinza\Downloads"
rem ================================================

echo 正在解除文件夹的锁定：%targetFolder%
echo.

powershell -NoLogo -NoProfile -Command "Get-ChildItem '%targetFolder%' -Recurse -Filter *.pdf | Unblock-File"

echo.
echo 完成！所有 PDF 已解除锁定。
pause