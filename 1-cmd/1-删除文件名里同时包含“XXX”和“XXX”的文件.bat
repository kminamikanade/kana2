@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "target=C:\c_wk\10_会社\PDF-相关\Test"

rem ====== 主关键字（必须包含） ======
set "main=12321"

rem ====== 附加关键字（包含任意一个即可删除） ======
set "extra1=購買"
set "extra2=送付"

rem ====== 测试模式开关 ======
set "DRY_RUN=false"

echo 正在处理文件夹：%target%
echo 主关键字：%main%
echo 附加关键字：%extra1%, %extra2%
echo ----------------------------------------

for %%f in ("%target%\*.*") do (
    set "name=%%~nxf"
    set "hasMain=0"
    set "hasExtra=0"

    rem 检查主关键字
    set "test=!name:%main%=!"
    if "!test!" neq "!name!" set "hasMain=1"

    if !hasMain! equ 1 (
        rem 检查附加关键字1
        set "test=!name:%extra1%=!"
        if "!test!" neq "!name!" set "hasExtra=1"

        rem 检查附加关键字2
        set "test=!name:%extra2%=!"
        if "!test!" neq "!name!" set "hasExtra=1"

        if !hasExtra! equ 1 (
            if "%DRY_RUN%"=="true" (
                echo [测试] 准备删除：%%~nxf
            ) else (
                echo [删除] %%~nxf
                del /f "%%f"
            )
        )
    )
)

echo ----------------------------------------
echo 完成！
pause