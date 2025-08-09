import json
import re

import requests

cookies = {
    'channelid': '0',
    'ref': 'ldwkjqipvz6c',
    'sid': '1751659497455164',
    '_ss_s_uid': 'e82c3bf105caa667c5d562c71013eac2',
    'sessionid': 'c82d8075598f3e84ae952556a5fda806',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=0, i',
    'referer': 'https://www.kuaidaili.com/free/dps/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

response = requests.get('https://www.kuaidaili.com/free/inha/2/', headers=headers)
response.encoding = 'utf-8'
pattern = r'const fpsList =(.*)?;'
match = re.search(pattern, response.text)
fps_lists = json.loads(match.group(1))
for fps in fps_lists:
    ip = fps['ip']
    port = fps['port']
    proxy = f'{ip}:{port}'
    print(proxy)
    params = {
        'gid': '23718623',
        'pageSize': '10',
        'pageNum': '1',
        'year': '-100',
    }
    for i in range(1, 25):
        response1 = requests.get('https://capi.tianyancha.com/cloud-business-state/client/summaryList', params=params,
                                 proxies={"http": proxy})
        print(response1.text)
