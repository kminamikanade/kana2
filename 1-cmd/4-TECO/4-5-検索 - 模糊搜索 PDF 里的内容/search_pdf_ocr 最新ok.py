import os
import re
import fitz
from collections import defaultdict
from PyPDF2 import PdfMerger
from rapidocr_onnxruntime import RapidOCR

# =====================================================
# 设置（请修改为您真实的绝对路径）
# =====================================================

# 【修改这里】：把 xxx 改成您电脑真实的用户名
base_path = r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合"

FOLDER_RULES = [
    {
        "path": os.path.join(base_path, "1"),
        "must_have": "出荷日"
    },
    {
        "path": os.path.join(base_path, "2"),
        "must_have": "当社PJNo"
    }
]

OUTPUT_DIR = os.path.join(base_path, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

ocr = RapidOCR()

# =====================================================
# OCR 提取文本
# =====================================================

def extract_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
            else:
                pix = page.get_pixmap(dpi=200)
                img_bytes = pix.tobytes("png")
                ocr_result, _ = ocr(img_bytes)
                if ocr_result:
                    text += "\n".join([line[1] for line in ocr_result])
        doc.close()
    except Exception as e:
        pass
    return text

# =====================================================
# 提取 15A 编号
# =====================================================

def find_keyword(text):
    matches = re.findall(
        r"15A[\s\-]*[A-Z0-9]{3,40}", 
        text,
        re.IGNORECASE
    )
    if not matches:
        return None
    best_match = max(matches, key=len).upper()
    clean_code = re.sub(r'[\s\-]', '', best_match)
    return clean_code

# =====================================================
# 提取最大日期
# =====================================================

def find_date(text):
    patterns = [
        r"\d{4}/\d{1,2}/\d{1,2}",
        r"\d{4}-\d{1,2}-\d{1,2}",
        r"\d{4}年\d{1,2}月\d{1,2}日"
    ]
    all_dates = []
    for pattern in patterns:
        for m in re.finditer(pattern, text):
            d = m.group(0)
            d = d.replace("年", "-").replace("月", "-").replace("日", "").replace("/", "-")
            parts = d.split("-")
            if len(parts) == 3:
                all_dates.append(f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}")
    
    if not all_dates:
        return ""
    all_dates.sort()
    return all_dates[-1]

# =====================================================
# 扫描与合并
# =====================================================

groups = defaultdict(lambda: defaultdict(list))

for rule in FOLDER_RULES:
    folder = rule["path"]
    must_have = rule["must_have"]
    regex_pattern = r"\s*".join(must_have)

    if not os.path.exists(folder):
        continue

    for file in os.listdir(folder):
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder, file)
        text = extract_text(pdf_path)

        if not re.search(regex_pattern, text):
            continue

        keyword = find_keyword(text)
        if not keyword:
            continue

        groups[keyword][must_have].append({"pdf": pdf_path, "text": text})

# =====================================================
# 输出结果
# =====================================================

print("=" * 50)
print("开始合并")
print("=" * 50)

required_types = [x["must_have"] for x in FOLDER_RULES]
merged_count = 0

for keyword, items in groups.items():
    if not all(t in items for t in required_types):
        continue

    merger = PdfMerger()
    date_str = ""
    for t in required_types:
        pdf_info = items[t][0]
        merger.append(pdf_info["pdf"])
        if not date_str:
            date_str = find_date(pdf_info["text"])

    out_name = f"{keyword}({date_str}).pdf" if date_str else f"{keyword}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    
    merger.write(out_path)
    merger.close()
    merged_count += 1
    print(f"✔ {out_name}")

print("=" * 50)
print(f"合并完成！共生成 {merged_count} 个文件。")
print("=" * 50)

input("按回车退出...")