import pandas as pd

# 定义文件路径
file_path2 = r"供应商.csv"
file_path3 = '需要补充A股公司.csv'

# 读取数据
data2 = pd.read_csv(file_path2)
data3 = pd.read_csv(file_path3)

# 去重并获取唯一名称集合
unique_names2 = set(data2['企业名称'].drop_duplicates())
unique_names3 = set(data3['公司名称'].drop_duplicates())

# 计算差集并打印结果
lou = unique_names3 - unique_names2
print(lou)
print(len(lou))
