import os
import sys
import fitz  # PyMuPDF

KEYWORDS = ["六本木", "渋谷", "新宿"]
SEARCH_DIR = r"C:\Work-Excel"

print("正在读取 PDF 文本层搜索关键字:", KEYWORDS)

found = 0

for root, dirs, files in os.walk(SEARCH_DIR):
    for file in files:
        if file.lower().endswith(".pdf"):
            path = os.path.join(root, file)
            print(f"\n[处理中] {file}")

            try:
                doc = fitz.open(path)

                for idx, page in enumerate(doc):
                    text = page.get_text()

                    for kw in KEYWORDS:
                        if kw in text:
                            print(f"  ✅ 找到关键字 '{kw}' → 文件: {file} 页码: {idx+1}")
                            found += 1

                doc.close()

            except Exception as e:
                print("  [错误] 无法处理:", e)

print("\n搜索完成，共找到:", found)
input("按 Enter 退出")
