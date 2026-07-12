import os
import shutil
import fitz  # PyMuPDF
from rapidocr_onnxruntime import RapidOCR

# ====== 用户配置 ======
SOURCE_DIR = r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\1"          # PDF来源目录
DEST_DIR = r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\output"        # 匹配后移动到这里
KEYWORDS = ["32850"]  # 模糊搜索关键词
# ======================

ocr = RapidOCR()

def extract_text(pdf_path):
    """优先读取文本层，若无文本则自动OCR"""
    doc = fitz.open(pdf_path)
    full_text = ""

    # ① 文本层读取
    for page in doc:
        text = page.get_text()
        if text:
            full_text += text

    # 若文本层为空 → 自动OCR
    if full_text.strip() == "":
        print(f"[OCR] {pdf_path}")
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            ocr_result, _ = ocr(img_bytes)
            if ocr_result:
                full_text += "\n".join([line[1] for line in ocr_result])

    return full_text


def contains_keywords(text, keywords):
    """模糊匹配关键词"""
    for kw in keywords:
        if kw in text:
            return True
    return False


def main():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                print(f"▶ 検索中: {pdf_path}")

                text = extract_text(pdf_path)

                if contains_keywords(text, KEYWORDS):
                    print(f"✔ マッチ: {file}")
                    shutil.move(pdf_path, os.path.join(DEST_DIR, file))
                else:
                    print(f"✘ 未命中: {file}")

    print("\n=== 完了しました ===")


if __name__ == "__main__":
    main()
