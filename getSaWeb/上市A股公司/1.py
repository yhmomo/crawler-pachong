import pandas as pd

# 读取数据
data1 = pd.read_csv(r"C:\Users\JBWang\Desktop\供应商\供应商1.csv")
data2 = pd.read_csv(r"C:\Users\JBWang\Desktop\供应商\供应商2.csv")
data3 = pd.read_csv('天眼查数据/A股公司.csv')

# 去重
df_unique_name1 = data1.drop_duplicates(subset=['企业名称'])
df_unique_name2 = data2.drop_duplicates(subset=['企业名称'])
df_unique_name3 = data3.drop_duplicates(subset=['股票公司'])

# 使用集合操作优化查找逻辑
unique_names1 = set(df_unique_name1['企业名称'])
unique_names2 = set(df_unique_name2['企业名称'])
unique_names3 = set(df_unique_name3['股票公司'])

# 找出不在供应商1中的股票公司
lou = unique_names3 - unique_names1
print(lou)

# 找出不在供应商2中的股票公司
lou2 = lou - unique_names2
dat = {
    "公司名称": list(lou2)
}
print(len(lou2))
df = pd.DataFrame(dat)
df.to_csv('需要补充A股公司.csv', index=False)

not_in_stock_companies = unique_names1.union(unique_names2) - unique_names3
print("\n企业名称不在股票公司里的内容：")
print(not_in_stock_companies)
print(len(not_in_stock_companies))
