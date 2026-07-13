from pathlib import Path
import win32com.client as win32


# Excel文件夹
excel_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test"
)


# 要打印的Sheet名称
print_sheets = [
    "工事１",
    "工事２"
]


excel = win32.Dispatch("Excel.Application")

excel.Visible = False
excel.DisplayAlerts = False

count = 0


for file in excel_folder.glob("*.xlsx"):

    # 跳过Excel临时文件
    if file.name.startswith("~$"):
        continue

    try:

        print("打印:", file.name)

        wb = excel.Workbooks.Open(
            str(file.resolve())
        )


        for sheet_name in print_sheets:

            try:

                ws = wb.Worksheets(sheet_name)

                ws.PrintOut()

            except:

                print(
                    f"  找不到Sheet: {sheet_name}"
                )


        wb.Close(False)

        count += 1


    except Exception as e:

        print(
            "错误:",
            file.name,
            e
        )


excel.Quit()


print()
print("===================")
print("打印完成:", count)
print("===================")

input("按 Enter 结束...")