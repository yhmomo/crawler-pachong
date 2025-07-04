import time

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
    'X-AUTH-TOKEN': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxOTA2NDA0MTAxMiIsImlhdCI6MTc1MTI4NzQ4OCwiZXhwIjoxNzUzODc5NDg4fQ.tWbzui1PUsCZ6lKz3Rms7bKANWWX-wonAfUwx26RgUKv2dtAcVxxhsEgucM2lkqxQN6Wk8VVeP0znvCPXwgZ0w',
    'X-TYCID': '8ac8d26055af11f0a77fb3297a8a9a57',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
cookies = {
    'CUID': '3b79a298ca80245ff8e6f1d9196f0353',
    'TYCID': '8ac8d26055af11f0a77fb3297a8a9a57',
    'ssuid': '7684853980',
    'tyc-user-info': '{%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2219064041012%22%2C%22userId%22:%22339908444%22}',
    'tyc-user-info-save-time': '1751287489519',
    'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxOTA2NDA0MTAxMiIsImlhdCI6MTc1MTI4NzQ4OCwiZXhwIjoxNzUzODc5NDg4fQ.tWbzui1PUsCZ6lKz3Rms7bKANWWX-wonAfUwx26RgUKv2dtAcVxxhsEgucM2lkqxQN6Wk8VVeP0znvCPXwgZ0w',
    'tyc-user-phone': '%255B%252219064041012%2522%255D',
    'HWWAFSESID': '27bce856694c3e363a',
    'HWWAFSESTIME': '1751473523698',
    'csrfToken': 'HydZ5zEZwumVtlQQEo6Z3w4n',
    'jsid': 'SEO-BAIDU-ALL-SY-000001',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22339908444%22%2C%22first_id%22%3A%22197c0dbef651de-0605b05b05b05b-4c657b58-2073600-197c0dbef661567%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3YzBkYmVmNjUxZGUtMDYwNWIwNWIwNWIwNWItNGM2NTdiNTgtMjA3MzYwMC0xOTdjMGRiZWY2NjE1NjciLCIkaWRlbnRpdHlfbG9naW5faWQiOiIzMzk5MDg0NDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22339908444%22%7D%2C%22%24device_id%22%3A%22197c0dbef651de-0605b05b05b05b-4c657b58-2073600-197c0dbef661567%22%7D',
}
for i in range(1, 10):
    timestamp_13_1 = int(time.time() * 1000)
    params = {
        # '_': str(timestamp_13_1),
        'gid': '13637692',
        'pageSize': '100',
        'pageNum': str(i),
        # 'year': '-100',
    }

    response = requests.get('https://capi.tianyancha.com/cloud-business-state/supply/summaryList', params=params,
                            headers=headers, cookies=cookies)
    print(response.json())
