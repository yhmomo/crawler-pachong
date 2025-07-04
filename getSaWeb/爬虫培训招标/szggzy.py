import csv
import json
import re
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from Tool.Strclean import clean_string
from Tool.reStr import get_money

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.szggzy.com',
    'priority': 'u=1, i',
    'referer': 'https://www.szggzy.com/jygg/list.html',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
}


def get_data(page, writer):
    contact_name = "未识别"
    json_data = {
        'modelId': 1378,
        'channelId': 2850,
        'fields': [
            {
                'fieldName': 'jygg_gglxmc_rank1',
                'fieldValue': '采购公告',
            },
        ],
        'parentBusinessType': '政府采购框架采购',
        'title': '培训',
        'releaseTimeBegin': '',
        'releaseTimeEnd': '',
        'page': page,
        'size': 10,
        'siteId': 1,
    }
    data = json.dumps(json_data, ensure_ascii=False)
    response = requests.post('https://www.szggzy.com/cms/api/v1/trade/content/page', headers=headers, data=data)
    time.sleep(10)
    print("第" + str(page) + "页开始下载")
    Json_response = response.json()
    data = Json_response['data']
    content = data['content']
    for i in content:
        releaseTime = i['releaseTime']
        release_time = datetime.strptime(releaseTime, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        three_years_ago = current_time - timedelta(days=3 * 365)
        if release_time >= three_years_ago:
            pass
        else:
            break
        title = i['title']
        contentId = i['contentId']
        contentUrl = "https://www.szggzy.com/jygg/details.html?contentId=" + str(contentId)
        dataUrl = "https://www.szggzy.com/cms/api/v1/trade/content/detail?contentId=" + str(contentId)
        data = requests.get(dataUrl, headers=headers).json()["data"]
        time.sleep(10)
        print(title + "开始下载")

        text = clean_string(BeautifulSoup(data["txt"], "html.parser")).text
        pattern = r"采购人信息\s*([\s\S]*?)\d"
        match = re.search(pattern, text)
        if match:
            contact_name = clean_string(match.group(1).strip())
        extracted_data = get_money(text)
        # 写入数据
        writer.writerow([contentUrl, title, contact_name, extracted_data])


if __name__ == '__main__':
    csv_file = "procurement_info.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(["项目URL", "项目名称", "采购人信息", "项目金额"])
        for i in range(0, 101):
            get_data(i, writer)
