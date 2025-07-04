import pandas as pd

# 读取 Excel 文件中的所有 sheet，返回一个字典，键为 sheet 名，值为 DataFrame
file_path = 'output_1.xlsx'  # 替换为你的文件路径
dfs = pd.read_excel(file_path, sheet_name=None, header=None, skiprows=1)

# 将所有 sheet 的 DataFrame 合并为一个 DataFrame
merged_df = pd.concat(dfs.values(), ignore_index=True)

# 输出合并后的 DataFrame
print(merged_df)

# 保存合并后的数据到新的 Excel 文件
merged_df.to_excel('merged_1.xlsx', index=False)
