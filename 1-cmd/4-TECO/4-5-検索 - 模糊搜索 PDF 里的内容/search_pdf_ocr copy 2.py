import os
import re
import fitz
from rapidocr_onnxruntime import RapidOCR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FOLDER_RULES = [
    {
        "path": r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\1",
        "main_prefix": "15A",
        "unique_prefix": "お問い合"
    },
    {
        "path": r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\2",
        "main_prefix": "15A",
        "unique_prefix": "発送案内"
    }
]

ocr = RapidOCR()

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num, page in enumerate(doc, start=1):

        t = page.get_text()

        if not t.strip():

            print(f"    OCR页面 {page_num}")

            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")

            ocr_result, _ = ocr(img_bytes)

            if ocr_result:
                t = "\n".join([line[1] for line in ocr_result])

        text += t

    return text


def find_prefix_text(text, prefix):

    match = re.search(re.escape(prefix) + r"\S*", text)

    if match:
        return match.group(0)

    return None


print("=" * 80)
print("开始检查")
print("=" * 80)

for rule in FOLDER_RULES:

    folder = rule["path"]
    main_prefix = rule["main_prefix"]
    unique_prefix = rule["unique_prefix"]

    print("")
    print("=" * 80)
    print("文件夹:", folder)
    print("主关键词:", main_prefix)
    print("唯一关键词:", unique_prefix)
    print("=" * 80)

    if not os.path.exists(folder):
        print("目录不存在！")
        continue

    for file in os.listdir(folder):

        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder, file)

        print("")
        print("检查文件:", file)

        try:

            text = extract_text(pdf_path)

            print("")
            print("前500个字符:")
            print("-" * 50)
            print(text[:500])
            print("-" * 50)

            mk = find_prefix_text(text, main_prefix)
            uk = find_prefix_text(text, unique_prefix)

            print("主关键词结果:", mk)
            print("唯一关键词结果:", uk)

            if mk and uk:

                print("")
                print("★★★★★ 匹配成功 ★★★★★")
                print("文件:", file)

        except Exception as e:

            print("错误:", e)

print("")
print("=" * 80)
print("检查结束")
print("=" * 80)

input("按回车退出...")