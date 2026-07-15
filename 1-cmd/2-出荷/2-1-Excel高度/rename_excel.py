from pathlib import Path
import openpyxl


# =========================
# Excel文件所在文件夹
# =========================

input_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test"
)


# =========================
# 处理所有Excel
# =========================

success = 0


for excel_file in input_folder.glob("*.xlsx"):

    print("处理:", excel_file.name)

    try:

        wb = openpyxl.load_workbook(excel_file)


        # 两个Sheet
        for sheet_name in ["22", "33"]:


            if sheet_name in wb.sheetnames:

                ws = wb[sheet_name]


                # 设置50、51行高度
                ws.row_dimensions[40 41].height = 18
                ws.row_dimensions[42 43].height = 18



        # 保存
        wb.save(excel_file)


        success += 1


    except Exception as e:

        print("错误:", excel_file.name, e)



print()
print("================")
print("完成文件数:", success)
print("================")

input("按 Enter 结束...")