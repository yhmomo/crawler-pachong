#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tianyancha_thread.py
多线程 + 代理池并发抓取天眼查供应商信息
一条代理独占一个线程，代理不共用
"""

import csv
import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

# -------------------------- 全局配置 ---------------------------------
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'Connection': 'keep-alive'
}
API_URL = 'https://capi.tianyancha.com/cloud-business-state/supply/summaryList'

# 读取代理池
PROXY_FILE = 'valid_proxies.txt'
if not os.path.exists(PROXY_FILE):
    raise FileNotFoundError(f'请把代理列表放在 {PROXY_FILE}，每行一条 http://ip:port')
with open(PROXY_FILE, 'r', encoding='utf-8') as f:
    PROXIES = [line.strip() for line in f if line.strip()]
if not PROXIES:
    raise ValueError('代理池为空')


# -------------------------- 工具函数 ---------------------------------
class RetryError(Exception):
    """登录失效时手动抛出"""
    pass


@retry(
    stop=stop_after_attempt(5),
    wait=wait_random_exponential(multiplier=600, max=650),
    retry=retry_if_exception_type(requests.exceptions.RequestException)
)
def safe_get(url, params, proxy):
    """带重试、超时、代理的请求"""
    proxies = {'http': proxy, 'https': proxy}
    resp = requests.get(url, params=params, headers=HEADERS,
                        proxies=proxies, timeout=15)
    resp.raise_for_status()
    sleep_time = random.randint(8, 10)
    time.sleep(sleep_time)
    return resp


def save_csv(filename, row_dict, first_headers=None):
    """追加写 CSV，自动写表头"""
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=first_headers or row_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)


# -------------------------- 业务函数 ---------------------------------
def handle_year(gid, name, code, year, proxy):
    """下载并保存某一年数据"""
    params = {'gid': gid, 'pageSize': 100, 'pageNum': 1, 'year': year}
    resp = safe_get(API_URL, params, proxy)
    js = resp.json()
    if js.get('state') == 'error' and '登录' in str(js):
        raise RetryError('登录失效')

    result = js['data']['pageBean']['result']
    if not result:
        return
    # 👇 新增提示：哪一年、哪家公司、多少条
    print(f"✔ 保存 {name}({code}) {year} 年数据，共 {len(result)} 条")
    for item in js['data']['pageBean']['result']:
        row = {
            '股票名称': name,
            '股票代码': code,
            '供应商名称': item['supplier_name'],
            '采购占比': item.get('ratio', '无'),
            '采购金额': item['amt'],
            '公告时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['announcement_date'] / 1000)),
            '数据来源': item['dataSource'],
            '供应商重复次数': item['summary']
        }
        save_csv('A股公司供应商用年份.csv', row)


def handle_company(gid, name, code, proxy):
    """处理一家公司所有年份（含跳过已处理）"""
    try:
        df1 = pd.read_csv("A股公司_供应商数量为空.csv", encoding='utf-8')["股票名称"]
    except FileNotFoundError:
        df1 = pd.Series(dtype='object')
    try:
        df2 = pd.read_csv("A股公司供应商用年份.csv", encoding='utf-8')["股票名称"]
    except FileNotFoundError:
        df2 = pd.Series(dtype='object')

    if name in df1.values or name in df2.values:
        print(f"已处理过 {name}")
        return

    # ---------- 以下为原逻辑 ----------
    params = {'gid': gid, 'pageSize': 100, 'pageNum': 1, 'year': -100}
    resp = safe_get(API_URL, params, proxy)
    data = resp.json()['data']
    pb = data['pageBean']
    if pb['total'] == 0 or pb['pageSize'] == 0:
        save_csv('A股公司_供应商数量为空.csv',
                 {'id': gid, '股票名称': name, '股票代码': code})
        return

    for yd in data['suppliesYear']:
        if yd['title'] == '全部年份' or yd['value'] == 0:
            continue
        year = yd['value']
        num = int(re.search(r'（(\d+)）', yd['title']).group(1))
        if num > 100:
            save_csv('A股公司_供应商数量单年份超过100.csv',
                     {'id': gid, '股票名称': name, '股票代码': code, '年份': year, '数量': num})
        handle_year(gid, name, code, year, proxy)


# -------------------------- 任务构造 ---------------------------------
def build_tasks():
    """生成任务列表 [(gid, name, code, proxy), ...]"""
    src = pd.read_csv('A股公司_更新.csv', encoding='utf-8')
    tasks = []
    idx = 0
    for _, row in src.iterrows():
        name, code, link = row['股票名称'], row['股票代码'], row['天眼查链接']
        if pd.isna(link):
            continue
        for url in str(link).split(';'):
            m = re.search(r'/(\d+)(?:-|&|$)', url.strip())
            if m:
                gid = m.group(1)
                proxy = PROXIES[idx % len(PROXIES)]
                tasks.append((gid, name, code, proxy))
                idx += 1
    return tasks


# -------------------------- 主入口 ---------------------------------
def main():
    tasks = build_tasks()
    print(f'共 {len(tasks)} 任务，代理 {len(PROXIES)} 条')
    with ThreadPoolExecutor(max_workers=len(PROXIES)) as pool:
        futures = {pool.submit(handle_company, *t): t for t in tasks}
        for f in as_completed(futures):
            gid, name, code, proxy = futures[f]
            try:
                f.result()
                print(f'√ {name}({code}) 代理 {proxy}')
            except Exception as e:
                print(f'× {name}({code}) 代理 {proxy} 失败: {e}')


if __name__ == '__main__':
    main()
