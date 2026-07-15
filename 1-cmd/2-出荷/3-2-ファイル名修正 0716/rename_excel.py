from pathlib import Path
import re


# =========================
# PDF文件夹
# =========================

folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\PDF"
)



# =========================
# 新文件名
# 直接粘贴
# 一行一个
# 不需要引号、逗号、.pdf
# =========================

new_names_text = """
16GG033246 14AWE1240144-125478 公司
26T12345 14AWE1240145-125478 東京株式会社
"""

# =========================
# 自动整理新名字
# =========================

new_names = []


for line in new_names_text.splitlines():

    line = line.strip()


    if line:

        if not line.lower().endswith(".pdf"):

            line += ".pdf"


        new_names.append(line)



# =========================
# 提取编号
# =========================

def get_codes(text):

    # 支持：
    # 15AADF123456740
    # 16GG033246
    # 24DD12324
    # 26T123456789

    codes = re.findall(
        r"\d+[A-Z]{1,5}\d+",
        text.upper()
    )


    result = []


    for code in codes:

        # 太短的不参与匹配
        if len(code) >= 8:

            result.append(code)


    return result



# =========================
# 建立新文件编号
# =========================

new_code_list = []


for name in new_names:

    codes = get_codes(name)


    if codes:

        new_code_list.append(
            (
                codes,
                name
            )
        )



# =========================
# 开始匹配改名
# =========================

success = 0


for old_file in folder.glob("*.pdf"):


    old_codes = get_codes(
        old_file.name
    )


    if not old_codes:

        print(
            "跳过(无编号):",
            old_file.name
        )

        continue



    match_name = None



    for codes, new_name in new_code_list:


        # 只要有一个编号相同

        if set(old_codes) & set(codes):

            match_name = new_name

            break



    if not match_name:

        print(
            "未找到对应:",
            old_file.name
        )

        continue



    new_file = folder / match_name



    if old_file == new_file:

        continue



    try:

        old_file.rename(
            new_file
        )


        print(
            "完成:",
            old_file.name,
            "→",
            match_name
        )


        success += 1



    except Exception as e:

        print(
            "错误:",
            old_file.name,
            e
        )



print()
print("================")
print("完成数量:", success)
print("================")

input(
    "处理完成，按 Enter 结束..."
)