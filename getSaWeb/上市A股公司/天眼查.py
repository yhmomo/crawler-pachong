import os
import random
import re
import time

import pandas as pd
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
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

datadict = {
    '股票代码': [],
    '股票名称': [],
    '供应商名称': [],
    '采购占比': [],
    '采购金额': [],
    '公告时间': [],
    '数据来源': [],
}
passlist = {
    '股票名称': [],
    '供应商名称数量': [],
}


def get_id(key, daima):
    params = {
        'ie': 'UTF-8',
        'wd': key + '集团公司天眼查',
    }
    response = requests.get('https://www.baidu.com/s', params=params, headers=headers)
    time.sleep(random.randint(5, 15))
    text = response.text
    pattern = r'https://www.tianyancha.com/company[^"]+'
    matches = re.search(pattern, text)
    url = ""
    if matches:
        url = matches.group()
        if url:
            id = url.split('/')[-1]
            print("id是：", id, type(id))
            get_summaryList(id, key, daima)
    else:
        print("没有找到匹配的href值")


def get_summaryList(id, name, daima):
    idparams = {
        'gid': id,
        'pageSize': '99',
        'pageNum': '1',
        'year': '-100',
    }
    response = requests.get('https://capi.tianyancha.com/cloud-business-state/supply/summaryList', params=idparams)
    json = response.json()
    print(json)
    data = json['data']
    pageBean = data['pageBean']
    total = pageBean['total']
    print(total, type(total))
    if total > 100:
        passlist['股票名称'].append(name)
        passlist['供应商名称数量'].append(total)
    result = pageBean['result']
    for item in result:
        supplier_name = item['supplier_name']  # 供应商名称
        ratio = '无'  # 采购占比
        if ratio in item.keys():
            ratio = item['ratio']
        amt = item['amt']  # 采购金额
        announcement_date = item['announcement_date']  # 公告时间戳
        time_struct = time.localtime(int(announcement_date) / 1000)
        time_standard = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)  # 公告时间
        dataSource = item['dataSource']  # 数据来源
        datadict['股票名称'].append(name)
        datadict['股票代码'].append(daima)
        datadict['供应商名称'].append(supplier_name)
        datadict['采购占比'].append(ratio)
        datadict['采购金额'].append(amt)
        datadict['公告时间'].append(time_standard)
        datadict['数据来源'].append(dataSource)


if __name__ == '__main__':
    df = pd.read_csv("A股公司.csv")
    df_names = df['股票名称']
    df_num = df['股票代码']

    # 确保表格文件夹存在
    if not os.path.exists('表格'):
        os.makedirs('表格')

    son_path = "表格"  # 假设表格文件夹路径为 "表格"

    for i in range(len(df_names)):
        filename = df_num[i]
        filepath = os.path.join(son_path, f"{filename}.csv")  # 构造文件路径
        file_names = os.listdir(son_path)  # 获取文件夹中的所有文件名
        if f"{filename}.csv" in file_names:
            datadict = {
                '股票名称': [],
                '股票代码': [],
                '供应商名称': [],
                '采购占比': [],
                '采购金额': [],
                '公告时间': [],
                '数据来源': []
            }
            # 判断文件是否在文件夹中
            print(f"文件 {filepath} 已存在，跳过")
            continue
        # 每次获取完一个股票代码的数据后，保存到一个单独的 CSV 文件中
        get_id(df_names[i], df_num[i])
        data_df = pd.DataFrame(datadict)
        # 使用股票名称作为文件名，并确保文件名合法
        data_df.to_csv(f'表格/{filename}.csv', index=False, encoding='utf-8')
        print(f"保存文件 {filename}.csv 成功")
        time.sleep(random.randint(8, 15))
        # 清空 datadict 以便存储下一个股票代码的数据
        datadict = {
            '股票名称': [],
            '股票代码': [],
            '供应商名称': [],
            '采购占比': [],
            '采购金额': [],
            '公告时间': [],
            '数据来源': []
        }
        # 保存超过 100 的数据到一个单独的 CSV 文件中
        passdf = pd.DataFrame(passlist)
        passdf.to_csv(f'超过100的股票/{filename}.csv', index=False, encoding='utf-8')
