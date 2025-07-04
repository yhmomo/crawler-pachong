import random
import re
import time

import pandas as pd
import requests
from tqdm import tqdm

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
cookies = None

df = pd.read_csv("A股公司.csv")

df['天眼查链接'] = ''

stock_codes = df['股票公司'].tolist()

for i, code in tqdm(enumerate(stock_codes), total=len(stock_codes)):
    try:
        params = {
            'wd': stock_codes[i] + "天眼查",
        }
        response = requests.get('https://www.baidu.com/s', params=params, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        cookies = response.cookies

        text = response.text
        pattern = r'https://www.tianyancha.com/company[^"]+'
        matches = re.search(pattern, text)
        url = ""
        if matches:
            url = matches.group()
            df.at[i, '天眼查链接'] = url
        else:
            print("没有找到匹配的href值")
            df.at[i, '天眼查链接'] = '获取失败'  # 标记错误信息
        time.sleep(random.randint(5, 15))
    except Exception as e:
        print(f"天眼查链接 {code} 时出错: {str(e)}")
        df.at[i, '天眼查链接'] = '获取失败'  # 标记错误信息
# 保存结果到新文件
df.to_csv('A股公司天眼查链接.csv', index=False, encoding='utf-8')
print("数据处理完成，结果已保存！")
