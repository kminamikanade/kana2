from pathlib import Path
import openpyxl
import win32com.client as win32

from openpyxl.drawing.image import Image
from openpyxl.drawing.spreadsheet_drawing import (
    AnchorMarker,
    OneCellAnchor
)
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.utils.cell import coordinate_to_tuple


# =========================
# 设置
# =========================

excel_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test"
)

stamp_file = (
    r"C:\c_wk\10_会社\PDF-相关\Test\電子印.png"
)

pdf_folder = excel_folder / "PDF"
pdf_folder.mkdir(exist_ok=True)


# =========================
# 盖章设置
# =========================

sheet_settings = {

    "11": {
        "cell": "I9",
        "right": 100,
        "down": -5,
        "size": 55
    },

    "22": {
        "cell": "I9",
        "right": 100,
        "down": -25,
        "size": 55
    },

    "35": {
        "cell": "I9",
        "right": 100,
        "down": -25,
        "size": 55
    }

}


print("开始处理...")
print("处理中，请稍候...")


# ==================================
# 第一阶段
# 修改行高 + 盖章
# ==================================

success = 0

for excel_file in excel_folder.glob("*.xlsx"):

    if excel_file.name.startswith("~$"):
        continue

    if excel_file.name == "rename_list.xlsx":
        continue

    try:

        wb = openpyxl.load_workbook(excel_file)

        # ------------------
        # 11 Sheet
        # ------------------

        if "11" in wb.sheetnames:

            ws = wb["11"]

            # 第1行高度加大
            ws.row_dimensions[1].height = 50

            # 第1行文字靠下
            for cell in ws[1]:
                cell.alignment = openpyxl.styles.Alignment(
                    horizontal="center",
                    vertical="bottom"
                )


            # 第11、12、13行高度12
            for row in [11, 12, 13]:
                ws.row_dimensions[row].height = 12


            # 第15、16、17行高度12
            for row in [15, 16, 17]:
                ws.row_dimensions[row].height = 12

        # ------------------
        # 22、33行高
        # ------------------

        for sheet_name in ["22", "33"]:

            if sheet_name not in wb.sheetnames:
                continue

            ws = wb[sheet_name]

            for row in [40, 41, 42, 43]:

                ws.row_dimensions[row].height = 18


        # ------------------
        # 盖章
        # ------------------

        for sheet_name, setting in sheet_settings.items():

            if sheet_name not in wb.sheetnames:
                continue

            ws = wb[sheet_name]

            img = Image(stamp_file)

            img.width = setting["size"]
            img.height = setting["size"]

            row, col = coordinate_to_tuple(
                setting["cell"]
            )

            marker = AnchorMarker(

                col=col - 1,
                row=row - 1,

                colOff=setting["right"] * 9525,
                rowOff=setting["down"] * 9525

            )

            size = XDRPositiveSize2D(

                cx=setting["size"] * 9525,
                cy=setting["size"] * 9525

            )

            anchor = OneCellAnchor(
                _from=marker,
                ext=size
            )

            img.anchor = anchor

            ws.add_image(img)

        wb.save(excel_file)
        wb.close()
        success += 1

    except Exception as e:

        print("错误:", excel_file.name, e)


# ==================================
# 第二阶段
# PDF导出 + 打印
# ==================================
# ==================================
# 第二阶段
# PDF导出
# ==================================

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


        sheets = [
            ws.Name for ws in wb.Worksheets
        ]


        # 导出22为PDF

# ------------------
# 导出22为PDF
# ------------------

        if "22" in [ws.Name for ws in wb.Worksheets]:

            ws_pdf = wb.Worksheets("22")

            pdf_file = pdf_folder / (
                excel_file.stem + ".pdf"
            )

            ws_pdf.ExportAsFixedFormat(
                0,
                str(pdf_file)
            )


        wb.Close(False)


    except Exception as e:

        print("错误:", excel_file.name, e)


excel.Quit()
print()
print("================")
print("完成文件:", success)
print("================")
print()

input("处理完成，按 Enter 结束...")