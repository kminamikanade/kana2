from pathlib import Path
import fitz
from rapidocr_onnxruntime import RapidOCR
import re
import numpy as np


# =========================
# 设置
# =========================

input_folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test"
)


ocr = RapidOCR()


success = 0
skip = 0



# =========================
# 扫描PDF
# =========================

for pdf_file in input_folder.glob("*.pdf"):

    try:

        doc = fitz.open(pdf_file)

        page = doc[0]


        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3)
        )


        img = np.frombuffer(
            pix.samples,
            dtype=np.uint8
        )


        img = img.reshape(
            pix.height,
            pix.width,
            pix.n
        )


        result, _ = ocr(img)


        text = ""


        if result:

            for line in result:

                text += line[1]



        doc.close()



        # =========================
        # OCR整理
        # =========================

        text_clean = re.sub(
            r"\s+",
            "",
            text
        )



        print()
        print("====================")
        print("文件:", pdf_file.name)
        print(text_clean)
        print("====================")



        # =========================
        # 1. 找15A编号
        # =========================

        code_match = re.search(
            r"15A[A-Z0-9]+",
            text_clean,
            re.IGNORECASE
        )


        code = None


        if code_match:

            code = code_match.group(0).upper()



        print(
            "15A编号:",
            code if code else "没有"
        )



        # =========================
        # 2. 找合世送状No号码
        # 例:
        # 周合世送状No.：4540-8146-8122
        # =========================

        no_match = re.search(
            r"合世送状No[^0-9]{0,10}([0-9]{3,5}-[0-9]{3,5}-[0-9]{3,5})",
            text_clean,
            re.IGNORECASE
        )


        inquiry = None


        if no_match:

            inquiry = (
                no_match.group(1)
                .replace("-", "")
            )


        print(
            "合世送状No:",
            inquiry if inquiry else "没有"
        )



        # =========================
        # 3. 找出荷日
        # =========================

        date_match = re.search(
            r"出荷日[^0-9]*(\d{4}[年/.-]?\d{1,2}[月/.-]?\d{1,2}日?)",
            text_clean
        )


        date = None


        if date_match:

            date = re.sub(
                r"\D",
                "",
                date_match.group(1)
            )


        print(
            "出荷日:",
            date if date else "没有"
        )



        # =========================
        # 判断
        # =========================

        if not inquiry or not date:

            print(
                "信息不足，跳过:",
                pdf_file.name
            )

            skip += 1
            continue



        # =========================
        # 生成文件名
        # =========================

        if code:

            new_name = (
                code
                + "_"
                + inquiry
                + "_"
                + date
                + ".pdf"
            )

        else:

            new_name = (
                inquiry
                + "_"
                + date
                + ".pdf"
            )



        new_file = (
            input_folder
            /
            new_name
        )



        # 防止覆盖

        if new_file.exists():

            print(
                "已存在:",
                new_name
            )

            skip += 1
            continue



        # =========================
        # 改名
        # =========================

        pdf_file.rename(
            new_file
        )


        success += 1


        print(
            "完成改名:",
            new_name
        )



    except Exception as e:

        skip += 1

        print(
            "错误:",
            pdf_file.name,
            e
        )



print()
print("===================")
print("完成数量:", success)
print("未识别:", skip)
print("===================")


input("按 Enter 结束...")