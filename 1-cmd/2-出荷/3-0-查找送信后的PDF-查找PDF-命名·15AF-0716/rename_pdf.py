from pathlib import Path
import fitz
from rapidocr_onnxruntime import RapidOCR
import re
import shutil
import numpy as np


# =========================
# 设置
# =========================

input_folder = Path(r"C:\c_wk\10_会社\PDF-相关\Test")

output_folder = input_folder / "out"
output_folder.mkdir(exist_ok=True)


ocr = RapidOCR()


success = 0
skip = 0


# =========================
# 扫描PDF
# =========================

for pdf_file in input_folder.glob("*.pdf"):

    try:

        doc = fitz.open(pdf_file)

        text = ""


        # 只读取第一页（编号一般在第一页）
        page = doc[0]


        # 2倍清晰度，提高速度
        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
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


        if result:

            for line in result:
                text += line[1]


        doc.close()


        # 去空格
        text = re.sub(r"\s+", "", text)


        # 找15A编号
        match = re.search(
            r"15A[A-Z]{2,3}\d+",
            text,
            re.IGNORECASE
        )


        if match:

            number = match.group(0).upper()


            new_file = output_folder / (number + ".pdf")


            shutil.copy2(
                pdf_file,
                new_file
            )


            success += 1

            print("完成:", number)


        else:

            skip += 1



    except Exception as e:

        skip += 1



print()
print("===================")
print("完成数量:", success)
print("未识别:", skip)
print("===================")

input("按 Enter 结束...")