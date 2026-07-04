@echo off
chcp 65001 >nul
echo ========================================
echo   PDF 自動結合ツール (フォルダ1 + フォルダ2)
echo ========================================
echo.

REM Pythonスクリプトを実行
python "%~dp0merge.py"

echo.
echo 処理が完了しました。Enterキーを押して終了します。
pause >nul