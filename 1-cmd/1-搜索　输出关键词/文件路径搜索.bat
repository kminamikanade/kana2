@echo off
chcp 65001 >nul

echo ========================================
echo 文件名深度搜索工具
echo ========================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0文件搜索.ps1"

echo.
pause