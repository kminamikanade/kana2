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
    r""
)

# 印章图片
stamp_file = r""

sheet_settings = {

    "": {
        "cell": "I9",
        "right": 100,
        "down": -5,
        "size": 55
    },

    "": {
        "cell": "I9",
        "right": 100,
        "down": -25,
        "size": 55
    },

    "": {
        "cell": "I9",
        "right": 100,
        "down": -25,
        "size": 55
    }

}


# =========================
# 开始
# =========================

print("开始处理...")
print("处理中，请稍候...")

success = 0


for excel_file in excel_folder.glob("*.xlsx"):

    if excel_file.name.startswith("~$"):
        continue

    if excel_file.name == "rename_list.xlsx":
        continue

    try:

        wb = openpyxl.load_workbook(excel_file)

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

        success += 1

    except:
        pass


print()
print("================")
print("完成文件:", success)
print("================")
print()

input("处理完成，按 Enter 结束...")