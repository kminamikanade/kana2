@echo off
chcp 65001 >nul
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0search.ps1"
echo.
echo 処理が完了しました。Enterキーを押して終了します。
pause >nul