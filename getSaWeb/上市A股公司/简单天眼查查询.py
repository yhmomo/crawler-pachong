import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Origin': 'https://www.tianyancha.com',
    'Referer': 'https://www.tianyancha.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'X-AUTH-TOKEN': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxOTA2NDA0MTAxMiIsImlhdCI6MTc1MTI4NDAxOCwiZXhwIjoxNzUzODc2MDE4fQ.f8aa2OmjyyQM2mctFdHJJwbkdqvBNfBs7bFC06tq-JMTAUCtrv7CUGFHlfwSto0UaYPnnLC-yAMkuus-xcUMHg',
    'X-TYCID': '8a4ecdb0059d11f09bd375dfd420a35f',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    '_': '1751284040111',
    'gid': '23402373',
    'pageSize': '10',
    'pageNum': '1',
    'year': '-100',
}

response = requests.get('https://capi.tianyancha.com/cloud-business-state/supply/summaryList', params=params,
                        headers=headers)
response.encoding = 'utf-8'
print(response.json())

# cookies = {
#     'CUID': 'f324650e3b182d5884129ecab779d257',
#     'TYCID': '8a4ecdb0059d11f09bd375dfd420a35f',
#     'HWWAFSESID': '4a2ac9786cd9d2861c',
#     'HWWAFSESTIME': '1751283982123',
#     'csrfToken': 'HEX9VK4RgiboxjTC9ATj4KdL',
#     'jsid': 'SEO-BAIDU-ALL-SY-000001',
#     'bdHomeCount': '0',
#     'bannerFlag': 'true',
#     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22339908444%22%2C%22first_id%22%3A%22195b41ba3bc8ed-0f2886492ed875-4c657b58-2073600-195b41ba3bd1967%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk1YjQxYmEzYmM4ZWQtMGYyODg2NDkyZWQ4NzUtNGM2NTdiNTgtMjA3MzYwMC0xOTViNDFiYTNiZDE5NjciLCIkaWRlbnRpdHlfbG9naW5faWQiOiIzMzk5MDg0NDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22339908444%22%7D%2C%22%24device_id%22%3A%22195b41ba3bc8ed-0f2886492ed875-4c657b58-2073600-195b41ba3bd1967%22%7D',
#     'tyc-user-info': '%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2219064041012%22%2C%22userId%22%3A%22339908444%22%7D',
#     'tyc-user-info-save-time': '1751284018205',
#     'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxOTA2NDA0MTAxMiIsImlhdCI6MTc1MTI4NDAxOCwiZXhwIjoxNzUzODc2MDE4fQ.f8aa2OmjyyQM2mctFdHJJwbkdqvBNfBs7bFC06tq-JMTAUCtrv7CUGFHlfwSto0UaYPnnLC-yAMkuus-xcUMHg',
#     'searchSessionId': '1751284018.26625672',
# }

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.tianyancha.com/nsearch?key=%E5%B0%8F%E7%B1%B3',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': 'CUID=f324650e3b182d5884129ecab779d257; TYCID=8a4ecdb0059d11f09bd375dfd420a35f; HWWAFSESID=4a2ac9786cd9d2861c; HWWAFSESTIME=1751283982123; csrfToken=HEX9VK4RgiboxjTC9ATj4KdL; jsid=SEO-BAIDU-ALL-SY-000001; bdHomeCount=0; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22339908444%22%2C%22first_id%22%3A%22195b41ba3bc8ed-0f2886492ed875-4c657b58-2073600-195b41ba3bd1967%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk1YjQxYmEzYmM4ZWQtMGYyODg2NDkyZWQ4NzUtNGM2NTdiNTgtMjA3MzYwMC0xOTViNDFiYTNiZDE5NjciLCIkaWRlbnRpdHlfbG9naW5faWQiOiIzMzk5MDg0NDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22339908444%22%7D%2C%22%24device_id%22%3A%22195b41ba3bc8ed-0f2886492ed875-4c657b58-2073600-195b41ba3bd1967%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2219064041012%22%2C%22userId%22%3A%22339908444%22%7D; tyc-user-info-save-time=1751284018205; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxOTA2NDA0MTAxMiIsImlhdCI6MTc1MTI4NDAxOCwiZXhwIjoxNzUzODc2MDE4fQ.f8aa2OmjyyQM2mctFdHJJwbkdqvBNfBs7bFC06tq-JMTAUCtrv7CUGFHlfwSto0UaYPnnLC-yAMkuus-xcUMHg; searchSessionId=1751284018.26625672',
}

params = {
    'key': '小米',
}

response = requests.get('https://www.tianyancha.com/nsearch', params=params, headers=headers)
response.encoding = 'utf-8'
print(response.text)
