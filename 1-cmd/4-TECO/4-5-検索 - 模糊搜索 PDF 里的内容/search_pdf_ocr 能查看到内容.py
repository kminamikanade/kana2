import os
import re
import fitz
import shutil
from PyPDF2 import PdfMerger
from rapidocr_onnxruntime import RapidOCR

SOURCE_DIRS = [
    r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\1",
    r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\2"
]
DEST_DIR = r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合\output"
KEYWORDS = ["15AFG32850"]

ocr = RapidOCR()

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        t = page.get_text()
        if not t.strip():
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            ocr_result, _ = ocr(img_bytes)
            if ocr_result:
                t += "\n".join([line[1] for line in ocr_result])
        text += t
    return text

def find_date(text):
    match = re.search(r"\d{4}/\d{2}/\d{2}", text)
    return match.group(0) if match else None

def main():
    matched_files = {}
    for folder in SOURCE_DIRS:
        for file in os.listdir(folder):
            if file.lower().endswith(".pdf"):
                path = os.path.join(folder, file)
                text = extract_text(path)
                for kw in KEYWORDS:
                    if kw in text:
                        date = find_date(text)
                        matched_files.setdefault(kw, []).append((path, date))

    for kw, files in matched_files.items():
        if len(files) > 1:
            merger = PdfMerger()
            date = files[0][1] or "no_date"
            for f, _ in files:
                merger.append(f)
            out_name = f"{kw}({date.replace('/', '-')}).pdf"
            out_path = os.path.join(DEST_DIR, out_name)
            merger.write(out_path)
            merger.close()
            print(f"✔ 結合完了: {out_name}")

if __name__ == "__main__":
    main()
