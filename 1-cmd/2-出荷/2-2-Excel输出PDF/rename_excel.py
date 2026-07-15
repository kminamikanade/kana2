from pathlib import Path
import win32com.client as win32


# Excel文件夹
excel_folder = Path(
    r"c:\c_wk\10_会社\PDF-相关\Test"
)

# PDF输出文件夹
pdf_folder = excel_folder / "PDF"

pdf_folder.mkdir(exist_ok=True)

print("开始导出PDF...")
print("处理中，请稍候...")

success = 0

excel = win32.Dispatch("Excel.Application")

excel.Visible = False
excel.DisplayAlerts = False


for excel_file in excel_folder.glob("*.xlsx"):

    if excel_file.name.startswith("~$"):
        continue

    if excel_file.name == "rename_list.xlsx":
        continue

    try:

        wb = excel.Workbooks.Open(
            str(excel_file.resolve())
        )

        if "22" in [ws.Name for ws in wb.Worksheets]:

            ws = wb.Worksheets("11")

            pdf_file = pdf_folder / (
                excel_file.stem + ".pdf"
            )

            ws.ExportAsFixedFormat(
                0,
                str(pdf_file)
            )

            success += 1

        wb.Close(False)

    except Exception as e:

        print("错误:", excel_file.name)

print()
print("================")
print("完成文件:", success)
print("================")

excel.Quit()

input("处理完成，按 Enter 结束...")