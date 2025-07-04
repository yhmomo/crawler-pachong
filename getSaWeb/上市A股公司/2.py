import pandas as pd

df = pd.read_csv('天眼查代码/A股公司_更新.csv')
for index, row in df.iterrows():
    link = row["天眼查链接"]
    if "tianyancha" not in link or "&" in link:
        company_name = row["股票公司"]
        print(company_name)
        print(link)
