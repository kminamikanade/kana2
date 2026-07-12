import os
import re
import fitz
from collections import defaultdict
from PyPDF2 import PdfMerger
from rapidocr_onnxruntime import RapidOCR

# =====================================================
# 设置
# =====================================================

# 开启调试模式（会在屏幕上打印提取出的文字，方便排查）
# =====================================================
# 设置（请修改为您真实的绝对路径）
# =====================================================

# 开启调试模式（会在屏幕上打印提取出的文字，方便排查）
DEBUG = True 

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
        print("读取失败:", pdf_path)
        print(e)
    return text

# =====================================================
# 提取 15A 编号（放宽规则，兼容横杠和空格）
# =====================================================

def find_keyword(text):
    # 修改：允许 15A 后面跟着横杠、空格或字母数字
    matches = re.findall(
        r"15A[\s\-]*[A-Z0-9]{3,40}", 
        text,
        re.IGNORECASE
    )
    if not matches:
        return None
    
    # 清理提取出的编号（去掉横杠和多余空格，统一大写）
    best_match = max(matches, key=len).upper()
    clean_code = re.sub(r'[\s\-]', '', best_match)
    return clean_code

# =====================================================
# 提取日期
# =====================================================

def find_date(text):
    patterns = [
        r"\d{4}/\d{1,2}/\d{1,2}",
        r"\d{4}-\d{1,2}-\d{1,2}",
        r"\d{4}年\d{1,2}月\d{1,2}日"
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            d = m.group(0)
            d = d.replace("年", "-").replace("月", "-").replace("日", "").replace("/", "-")
            parts = d.split("-")
            if len(parts) == 3:
                return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
    return ""

# =====================================================
# 扫描
# =====================================================

groups = defaultdict(lambda: defaultdict(list))

print("=" * 80)
print("开始扫描")
print("=" * 80)

for rule in FOLDER_RULES:
    folder = rule["path"]
    must_have = rule["must_have"]
    regex_pattern = r"\s*".join(must_have)

    print(f"\n[目录] {folder} | [寻找关键词] {must_have}")

    if not os.path.exists(folder):
        print("目录不存在!")
        continue

    for file in os.listdir(folder):
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder, file)
        print(f"\n  -> 检查文件: {file}")

        text = extract_text(pdf_path)

        # 调试：打印提取出的前 300 个字符
        if DEBUG:
            print("     [提取文本预览]:", repr(text[:300])) 

        if not re.search(regex_pattern, text):
            print("     [失败] 找不到关键词")
            continue

        keyword = find_keyword(text)
        if not keyword:
            print("     [失败] 找不到 15A 编号")
            continue

        print(f"     [成功] 编号: {keyword}")
        groups[keyword][must_have].append({"pdf": pdf_path, "text": text})

# =====================================================
# 分组与合并
# =====================================================

print("\n" + "=" * 80)
print("分组结果")
print("=" * 80)

if not groups:
    print("没有任何文件匹配成功！请查看上面的 [失败] 原因。")
else:
    for keyword, items in groups.items():
        print(f"编号: {keyword} -> 包含条件: {list(items.keys())}")

print("\n" + "=" * 80)
print("开始合并")
print("=" * 80)

required_types = [x["must_have"] for x in FOLDER_RULES]
merged_count = 0

for keyword, items in groups.items():
    if not all(t in items for t in required_types):
        print(f"跳过: {keyword} (缺少 {set(required_types) - set(items.keys())})")
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
    print(f"完成: {out_name}")

print(f"\n共生成: {merged_count} 个文件")
input("按回车退出...")