import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.tianyancha.com',
    'Referer': 'https://www.tianyancha.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'X-TYCID': '9e5e8fb060c011f091ddc34ee3ac3d6e',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    '_': '1752505571326',
    'gid': '594378026',
    'pageNum': '1',
    'pageSize': '100',
    'supplierName': '安徽云诺机电有限公司',
    # 'supplierGid': '3417917547',
    'year': '-100',
}

response = requests.get(
    'https://capi.tianyancha.com/cloud-business-state/supply/summaryList/detailList',
    params=params,
)
print(response.json())
