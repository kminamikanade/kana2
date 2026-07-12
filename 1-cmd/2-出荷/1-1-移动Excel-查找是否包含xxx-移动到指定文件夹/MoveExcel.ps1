$SourcePaths = @(
    'C:\c_wk\10_会社\PDF-相关\Test',
    'C:\c_wk\10_会社\PDF-相关\Test2'
)

$TargetPath = 'C:\c_wk\10_会社\PDF-相关\完成'

$TargetNumbers = @(
    '1231T222',
    '1231T4422'
)

if (!(Test-Path $TargetPath)) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

$count = 0

foreach ($path in $SourcePaths) {

    Get-ChildItem $path -File |
    Where-Object { $_.Extension -in ".xls", ".xlsx" } |
    ForEach-Object {

        foreach ($num in $TargetNumbers) {

            if ($_.Name -like "*$num*") {

                Write-Host "COPY => $($_.Name)"

                Copy-Item $_.FullName $TargetPath -Force

                $count++

                break
            }
        }
    }
}

Write-Host ""
Write-Host "TOTAL : $count"

Read-Host "Press Enter"