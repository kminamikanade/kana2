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


stamp_file = r""


sheet_settings = {
    "": {"cell": "I9", "right": 100, "down": -5, "size": 55},     
    "": {"cell": "I9", "right": 100, "down": -25, "size": 55},   
    "": {"cell": "I9", "right": 100, "down": -25, "size": 55}  
}

# 默认设置（如果某个 sheet 没在上面设置，就用这个）
default_setting = {"cell": "I9", "right": 100, "down": -5, "size": 55}


# =========================
# 主程序
# =========================

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

        # 遍历工作簿里的所有 sheet
        for ws in wb.worksheets:
            sheet_name = ws.title
            
            # 获取这个 sheet 的设置
            if sheet_name in sheet_settings:
                setting = sheet_settings[sheet_name]
            else:
                setting = default_setting
            
            print(f"  → {sheet_name}: 位置={setting['cell']}, 上移={setting['down']}")
            
            img = Image(stamp_file)
            img.width = setting["size"]
            img.height = setting["size"]
            
            row, col = coordinate_to_tuple(setting["cell"])
            
            marker = AnchorMarker(
                col=col - 1,
                row=row - 1,
                colOff=setting["right"] * 9525,
                rowOff=setting["down"] * 9525  # 负数就是往上移
            )
            
            size = XDRPositiveSize2D(
                cx=setting["size"] * 9525,
                cy=setting["size"] * 9525
            )
            
            anchor = OneCellAnchor(_from=marker, ext=size)
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