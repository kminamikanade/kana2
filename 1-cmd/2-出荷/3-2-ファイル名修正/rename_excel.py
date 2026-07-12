from pathlib import Path
import openpyxl


# =========================
# PDF文件夹
# =========================

pdf_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\out"
)


# =========================
# Excel文件
# =========================

excel_file = Path(
    r"C:\c_wk\10_会社\PDF-相关\rename_list.xlsx"
)


# =========================
# 读取Excel
# =========================

wb = openpyxl.load_workbook(excel_file)

ws = wb.active


rename_dict = {}


for row in ws.iter_rows(min_row=2, values_only=True):

    # 跳过空行
    if row[0] is None or row[1] is None:
        continue

    old_name = str(row[0]).strip()

    new_name = str(row[1]).strip()


    # 去掉可能存在的.pdf
    old_name = old_name.replace(".pdf", "")
    new_name = new_name.replace(".pdf", "")


    rename_dict[old_name] = new_name



# =========================
# 批量修改文件名
# =========================

success = 0
skip = 0


for pdf_file in pdf_folder.glob("*.pdf"):


    old_pdf_name = pdf_file.stem


    if old_pdf_name in rename_dict:


        new_file = pdf_folder / (
            rename_dict[old_pdf_name]
            + ".pdf"
        )


        # 防止同名覆盖
        if new_file.exists():

            print(
                "跳过(文件已存在):",
                new_file.name
            )

            skip += 1
            continue


        pdf_file.rename(new_file)


        print(
            "完成:",
            new_file.name
        )


        success += 1


    else:

        skip += 1



# =========================
# 结果
# =========================

print()
print("======================")
print("修改完成:", success)
print("未匹配:", skip)
print("======================")

input("按 Enter 结束...")