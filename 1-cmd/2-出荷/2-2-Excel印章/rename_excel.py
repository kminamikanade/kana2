from pathlib import Path
import openpyxl

from openpyxl.drawing.image import Image
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, OneCellAnchor
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.utils.cell import coordinate_to_tuple


# =========================
# Excel文件夹
# =========================

excel_folder = Path(
    r"c:\c_wk\10_会社\PDF-相关\Test"
)


# =========================
# 印章图片
# =========================

stamp_file = r"c:\c_wk\10_会社\PDF-相关\Test\電子印.png"


# =========================
# Sheet
# =========================

sheet_list = [
    "発送案内 (シFサ)"

]


# =========================
# 位置
# =========================

cell_position = "I9"


# 图片大小
stamp_width = 40
stamp_height = 40


# 右移动像素
right_pixel = 100

# 下移动像素
down_pixel = 0



success = 0



for excel_file in excel_folder.glob("*.xlsx"):


    # 跳过临时文件
    if excel_file.name.startswith("~$"):
        continue


    # 跳过设置Excel
    if excel_file.name == "rename_list.xlsx":
        continue


    print("处理:", excel_file.name)


    try:

        wb = openpyxl.load_workbook(excel_file)


        for sheet_name in sheet_list:


            if sheet_name in wb.sheetnames:


                ws = wb[sheet_name]


                img = Image(stamp_file)


                img.width = stamp_width
                img.height = stamp_height


                row, col = coordinate_to_tuple(
                    cell_position
                )


                marker = AnchorMarker(

                    col=col - 1,

                    row=row - 1,

                    colOff=right_pixel * 9525,

                    rowOff=down_pixel * 9525

                )


                size = XDRPositiveSize2D(

                    cx=stamp_width * 9525,

                    cy=stamp_height * 9525

                )


                anchor = OneCellAnchor(

                    _from=marker,

                    ext=size

                )


                img.anchor = anchor


                ws.add_image(img)



        wb.save(excel_file)


        success += 1


    except Exception as e:

        print(
            "错误:",
            excel_file.name,
            e
        )



print()
print("================")
print("完成文件:", success)
print("================")

input("按 Enter 结束...")