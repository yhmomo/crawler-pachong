import csv
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.szpsq.gov.cn/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_data(param, csv_writer):
    params = {
        'callback': 'jQuery09288836383027246_1750766718663',
        'page': param,
        'pagesize': '20',
        'isgkml': '1',
        'text': '培训',
        'order': '0',
        'including_url_doc': '1',
        'including_attach_doc': '1',
        'classify_main_name': '',
        'classify_mains': '',
        'classify_mains_excluded': '',
        'position': 'title',
        '_': '1750766718664',
    }

    response = requests.get('https://search.gd.gov.cn/jsonp/site/755468', params=params, headers=headers)
    response.encoding = 'utf-8'
    data = response.text[len('jQuery09288836383027246_1750766718663'):].strip('()')
    Json_data = json.loads(data)
    results = Json_data['results']
    for result in results:
        title = BeautifulSoup(result['title'], "lxml").text
        if "采购" not in title:
            continue
        url = result['url']
        timestamp = result['display_publish_time']
        time = datetime.fromtimestamp(timestamp)
        csv_writer.writerow([url, title, str(time)])


if __name__ == '__main__':
    with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
        # 创建 CSV 写入器
        csv_writer = csv.writer(csvfile)
        for i in range(1, 3):
            get_data(i, csv_writer)
