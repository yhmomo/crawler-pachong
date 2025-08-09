import random
import time

import pandas as pd
import requests

# 读取数据

data1 = pd.read_csv('A股公司供应商用年份.csv', encoding='utf-8')
data2 = pd.read_csv("A股公司_更新1.csv", dtype={'天眼查ID': str}, encoding='utf-8')

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.tianyancha.com',
    'Referer': 'https://www.tianyancha.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}
MAX_RETRY = 5  # 最多重试 5 次
BASE_URL = "https://capi.tianyancha.com/cloud-business-state/supply/summaryList/detailList"
filename = "A股公司供应商用年份1.csv"
file_exists = pd.io.common.file_exists(filename)


def get_save_data(idpar: dict, name: str, daima: str, cfnum: int):
    """
    带重试机制的拉取并保存供应商数据
    """
    for attempt in range(1, MAX_RETRY + 1):
        try:
            resp = requests.get(BASE_URL, params=idpar, headers=headers, timeout=15)
            resp.raise_for_status()
            js = resp.json()
            data = js.get('data')
            if not data or not data.get('result'):
                print(f"[{attempt}/{MAX_RETRY}] 返回 data 为空，2 秒后重试...")
                time.sleep(7 + random.uniform(0, 1))  # 退避 + 随机抖动
                continue
            time.sleep(7 + random.uniform(0, 1))  # 退避 + 随机抖动
            # 正常解析并落盘
            for item in data['result'][1:]:
                supplier_name = item['supplier_name']
                ratio = item.get('ratio', '无')
                amt = item['amt']
                announcement_date = item['announcement_date']
                try:
                    time_standard = time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.localtime(int(announcement_date) / 1000)
                    )
                    dataSource = item['dataSource']
                except Exception:
                    time_standard = '无'
                    dataSource = '无'
                # 检查是否已经存在相同的记录
                # 如果不存在相同的记录，追加数据
                new_row = {
                    '股票名称': name,
                    '股票代码': daima,
                    '供应商名称': supplier_name,
                    '采购占比': ratio,
                    '采购金额': amt,
                    '公告时间': time_standard,
                    '数据来源': dataSource,
                    '供应商重复次数': cfnum
                }

                # 判断是否存在完全相同的记录
                mask = (
                        (existing_df['股票名称'] == name) &
                        (existing_df['供应商名称'] == supplier_name) &
                        (existing_df['公告时间'] == time_standard) &
                        (existing_df['采购金额'] == amt)
                )

                pd.DataFrame([new_row]).to_csv(filename, mode='a', header=not file_exists, index=False,
                                               encoding='utf-8')
            return  # 成功解析后直接结束
        except requests.exceptions.RequestException as e:
            print(f"[{attempt}/{MAX_RETRY}] 网络异常：{e}，5 秒后重试...")
            time.sleep(5)
    print("已达最大重试次数，放弃本次抓取。")


# 过滤出供应商重复次数 >= 2 的记录
filtered = data1[data1['供应商重复次数'] == 2]
# 使用 merge 替代双重循环
merged = filtered.merge(data2[['股票名称', '天眼查ID']], on='股票名称', how='left')
filtered1 = data1[data1['供应商重复次数'] > 101]
merged1 = filtered1.merge(data2[['股票名称', '天眼查ID']], on='股票名称', how='left')
print('总记录数:', len(merged1))
for _, row in merged1.iterrows():
    print(row['供应商名称'], row['供应商重复次数'], row['天眼查ID'])

# 输出结果
for _, row in merged.iterrows():
    existing_df = pd.read_csv(filename)
    gpnema = row['股票名称']
    gyname = row['供应商名称']
    gynum = row['供应商重复次数']
    print(row['股票名称'], row['股票代码'], row['供应商名称'], row['供应商重复次数'], row['天眼查ID'])
    params = {
        'gid': str(row['天眼查ID']),
        'pageNum': '1',
        'pageSize': '100',
        'supplierName': row['供应商名称'],
    }
    get_save_data(params, row['股票名称'], row['股票代码'], row['供应商重复次数'])
# print('总记录数:', len(merged))
