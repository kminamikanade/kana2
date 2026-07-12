import os
import re
import time
import fitz
from collections import defaultdict
from PyPDF2 import PdfMerger
from rapidocr_onnxruntime import RapidOCR

# =====================================================
# 设置（请修改为您真实的绝对路径）
# =====================================================

base_path = r"C:\Users\qinza\OneDrive\Documents\kana2\1-cmd\1-結合" # 记得改 xxx

FOLDER_RULES = [
    {"path": os.path.join(base_path, "1"), "must_have": "出荷日"},
    {"path": os.path.join(base_path, "2"), "must_have": "当社PJNo"}
]

OUTPUT_DIR = os.path.join(base_path, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

ocr = RapidOCR()

# =====================================================
# 核心函数（已优化加速）
# =====================================================

def find_keyword(text):
    matches = re.findall(r"15A[\s\-]*[A-Z0-9]{3,40}", text, re.IGNORECASE)
    if not matches: return None
    return re.sub(r'[\s\-]', '', max(matches, key=len).upper())

def find_date(text):
    patterns = [r"\d{4}/\d{1,2}/\d{1,2}", r"\d{4}-\d{1,2}-\d{1,2}", r"\d{4}年\d{1,2}月\d{1,2}日"]
    all_dates = []
    for p in patterns:
        for m in re.finditer(p, text):
            d = m.group(0).replace("年", "-").replace("月", "-").replace("日", "").replace("/", "-")
            parts = d.split("-")
            if len(parts) == 3: all_dates.append(f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}")
    return max(all_dates) if all_dates else ""

# 【加速版】提取文本：找到关键词和编号后立刻停止
def extract_text_fast(pdf_path, must_have_pattern):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
            else:
                # 降低 DPI 到 150 以加快速度
                pix = page.get_pixmap(dpi=150)
                ocr_result, _ = ocr(pix.tobytes("png"))
                if ocr_result: text += "\n".join([line[1] for line in ocr_result])
            
            # 核心加速：如果关键词和编号都找到了，立刻跳出循环，不读后面的页了！
            if re.search(must_have_pattern, text) and find_keyword(text):
                break
        doc.close()
    except: pass
    return text

# 格式化时间显示
def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0: return f"{h}时 {m}分 {s}秒"
    if m > 0: return f"{m}分 {s}秒"
    return f"{s}秒"

# =====================================================
# 主程序
# =====================================================

# 1. 收集所有需要处理的文件
tasks = []
for rule in FOLDER_RULES:
    if os.path.exists(rule["path"]):
        for f in os.listdir(rule["path"]):
            if f.lower().endswith(".pdf"):
                tasks.append({"path": os.path.join(rule["path"], f), "must_have": rule["must_have"]})

total = len(tasks)
if total == 0:
    print("没有找到任何 PDF 文件！")
    input("按回车退出...")
    exit()

print(f"共找到 {total} 个文件，开始处理...\n")

groups = defaultdict(lambda: defaultdict(list))
start_time = time.time()

# 2. 带进度条的处理循环
for i, task in enumerate(tasks, 1):
    pdf_path = task["path"]
    must_have = task["must_have"]
    pattern = r"\s*".join(must_have) # 允许关键词中间有空格

    text = extract_text_fast(pdf_path, pattern)

    # 检查是否匹配
    if re.search(pattern, text):
        keyword = find_keyword(text)
        if keyword:
            groups[keyword][must_have].append({"pdf": pdf_path, "text": text})

    # 3. 计算并显示进度和剩余时间
    elapsed = time.time() - start_time
    if i < total:
        avg_time = elapsed / i
        remaining = avg_time * (total - i)
        # \r 让光标回到行首，实现覆盖打印效果
        print(f"\r处理中: [{i}/{total}] ({i/total*100:.1f}%) | 已用: {format_time(elapsed)} | 预计剩余: {format_time(remaining)}", end="", flush=True)
    else:
        print(f"\r处理中: [{i}/{total}] (100%) | 总耗时: {format_time(elapsed)}")

# =====================================================
# 合并与输出
# =====================================================

print("\n" + "=" * 50)
print("开始合并")
print("=" * 50)

required_types = [x["must_have"] for x in FOLDER_RULES]
merged_count = 0

for keyword, items in groups.items():
    if not all(t in items for t in required_types): continue

    merger = PdfMerger()
    date_str = ""
    for t in required_types:
        pdf_info = items[t][0]
        merger.append(pdf_info["pdf"])
        if not date_str: date_str = find_date(pdf_info["text"])

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