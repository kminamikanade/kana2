from pathlib import Path
import re


# =========================
# PDF文件夹
# =========================

folder = Path(
    r"C:\c_wk\10_会社\PDF-相关\Test\PDF"
)



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

    # 太短的编号过滤掉
    result = []

    for code in codes:

        if len(code) >= 8:
            result.append(code)

    return result



# =========================
# 输入新名字
# =========================

print("======================")
print("请输入新的文件名")
print("======================")
print()


new_names = []


while True:

    name = input("> ").strip()


    if name == "":
        break


    if not name.lower().endswith(".pdf"):

        name += ".pdf"


    new_names.append(name)



print()
print("输入数量:", len(new_names))
print()



# =========================
# 建立新名字编号表
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
# 开始匹配旧文件
# =========================

success = 0


for old_file in folder.glob("*.pdf"):


    old_codes = get_codes(
        old_file.name
    )


    if not old_codes:

        print(
            "跳过(没有编号):",
            old_file.name
        )

        continue



    new_name = None



    # 查找共同编号

    for codes, name in new_code_list:


        if set(old_codes) & set(codes):

            new_name = name
            break



    if not new_name:

        print(
            "没有匹配:",
            old_file.name
        )

        continue



    new_file = folder / new_name



    # 防止自己改自己

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
            new_name
        )


        success += 1



    except Exception as e:

        print(
            "错误:",
            old_file.name,
            e
        )



print()
print("======================")
print("完成数量:", success)
print("======================")

input("按 Enter 结束...")