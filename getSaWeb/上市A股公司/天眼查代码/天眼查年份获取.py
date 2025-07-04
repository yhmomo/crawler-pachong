import random
import re
import time

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type


# 自定义异常类
class RetryError(Exception):
    pass


# 请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}


# 重试装饰器
@retry(
    stop=stop_after_attempt(5),  # 最多重试5次
    wait=wait_random_exponential(multiplier=600, max=650),  # 指数退避策略
    retry=retry_if_exception_type(requests.exceptions.RequestException)  # 只对requests异常进行重试
)
def get_save_data(idpar, name, daima, year):
    try:
        response = requests.get('https://capi.tianyancha.com/cloud-business-state/supply/summaryList',
                                params=idpar,
                                headers=headers)
        response.raise_for_status()
        time.sleep(random.randint(8, 10))
        data = response.json()
        print(data)
        if data.get('state') == 'error' and '登录' in str(data):
            print("登录失效")
            raise RetryError("登录失效，需要重新登录")
        pageBean = data['data']['pageBean']
        result = pageBean['result']
        if not result:
            print("没有数据")
            return
        for item in result:
            supplier_name = item['supplier_name']  # 供应商名称
            ratio = item.get('ratio', '无')  # 采购占比
            amt = item['amt']  # 采购金额
            announcement_date = item['announcement_date']  # 公告时间戳
            time_standard = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(announcement_date) / 1000))  # 公告时间
            dataSource = item['dataSource']  # 数据来源
            summary = item['summary']

            # 创建或读取CSV文件
            filename = "A股公司供应商用年份.csv"
            # 检查文件是否存在，如果不存在则创建并写入表头
            file_exists = pd.io.common.file_exists(filename)
            df = pd.DataFrame({
                '股票名称': [name],
                '股票代码': [daima],
                '供应商名称': [supplier_name],
                '采购占比': [ratio],
                '采购金额': [amt],
                '公告时间': [time_standard],
                '数据来源': [dataSource],
                '供应商重复次数': [summary]
            })
            # 将数据追加到CSV文件
            df.to_csv(filename, mode='a', header=not file_exists, index=False, encoding='utf-8')


    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息: {e}")
        raise


def get_idparams(id, name, daima):
    df1 = pd.read_csv("A股公司_供应商数量为空.csv", encoding='utf-8')["股票名称"]
    df2 = pd.read_csv("A股公司供应商用年份.csv", encoding='utf-8')["股票名称"]
    if name in df1.values or name in df2.values:
        print(f"已处理过 {name}")
        return
    idparams = {
        'gid': id,
        'pageSize': '100',
        'pageNum': '1',
        'year': '-100',
    }
    response = requests.get('https://capi.tianyancha.com/cloud-business-state/supply/summaryList',
                            params=idparams,
                            headers=headers)
    data = response.json()['data']
    pageBean = data['pageBean']
    pageSize = int(pageBean['pageSize'])
    total = int(pageBean['total'])
    if pageSize == 0 or total == 0:
        print(f"没有数据" + name + id)
        # 创建或读取CSV文件
        filenamepageSize = "A股公司_供应商数量为空.csv"
        # 检查文件是否存在，如果不存在则创建并写入表头
        file_exists = pd.io.common.file_exists(filenamepageSize)
        dfpageSize = pd.DataFrame({
            'id': [id],
            '股票名称': [name],
            '股票代码': [daima],
        })
        # 将数据追加到CSV文件
        dfpageSize.to_csv(filenamepageSize, mode='a', header=not file_exists, index=False, encoding='utf-8')
        return
    suppliesYear = data['suppliesYear']
    for yearStr in suppliesYear:
        title = yearStr['title']
        if yearStr['title'] == "全部年份" or yearStr['value'] == 0:
            continue
        num = int(title[title.find("（") + 1:title.find(")"):])
        year = yearStr['value']
        if num <= 100:
            pass
        else:
            # 创建或读取CSV文件
            filenamenum = "A股公司_供应商数量单年份超过100.csv"
            # 检查文件是否存在，如果不存在则创建并写入表头
            file_exists = pd.io.common.file_exists(filenamenum)
            dfnum = pd.DataFrame({
                'id': [id],
                '股票名称': [name],
                '股票代码': [daima],
                '年份': [year],
                '数量': [num],
            })
            # 将数据追加到CSV文件
            dfnum.to_csv(filenamenum, mode='a', header=not file_exists, index=False, encoding='utf-8')
        params = {
            'gid': id,
            'pageSize': '100',
            'pageNum': '1',
            'year': str(year),
        }
        print(f"正在处理 {year} 年的数据")
        get_save_data(params, name, daima, str(year))


def main():
    df = pd.read_csv("A股公司_更新.csv", encoding='utf-8')
    for index, row in df.iterrows():
        name = row['股票名称']
        daima = row['股票代码']
        baseurllist = row['天眼查链接']
        if pd.isna(baseurllist):
            continue
        baseurllist = baseurllist.split(';')  # 假设链接以分号分隔
        for url in baseurllist:
            match = re.search(r'/(\d+)(?:-|&|$)', url.strip())
            id = match.group(1) if match else ""
            if id:
                print(f"处理 {url}，ID: {id}")
                get_idparams(id, name, daima)


if __name__ == '__main__':
    main()
    # 示例调用
