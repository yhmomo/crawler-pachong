import re

import pandas as pd

# 1. 读取数据
df = pd.read_csv("A股公司_更新.csv", encoding='utf-8')


# 2. 定义提取 id 的函数
def extract_id(link_string: str) -> str:
    """
    从一串天眼查链接中提取第一个有效的 id。
    如果提取不到，返回空字符串。
    """
    if pd.isna(link_string):
        return ""
    for url in str(link_string).split(';'):
        match = re.search(r'/(\d+)(?:-|&|$)', url.strip())
        if match:
            return match.group(1)
    return ""


# 3-A. 新增一列（推荐，保留原链接）
df['天眼查ID'] = df['天眼查链接'].apply(extract_id)
df.to_csv("A股公司_更新1.csv", index=False, encoding='utf-8-sig')  # utf-8-sig 防止 Excel 乱码
print("已新增列“天眼查ID”，并保存回文件。")

# 3-B. 如果想直接替换掉原来的“天眼查链接”列，用下面两行代替 3-A
# df['天眼查链接'] = df['天眼查链接'].apply(extract_id)
# df.rename(columns={'天眼查链接': '天眼查ID'}, inplace=True)
# df.to_csv("A股公司_更新.csv", index=False, encoding='utf-8-sig')
