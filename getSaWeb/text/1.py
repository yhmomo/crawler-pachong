import requests

# cookies = {
#     'WMF-Last-Access-Global': '06-Jul-2025',
#     'GeoIP': 'US:CA:Los_Angeles:34.05:-118.24:v4',
#     'WMF-Uniq': '15pmQsjCEDtfN0HEo33nGQIoAAEBAFvdM_2kcYyLByv563-91RNaPa-Yt9wl7W2P',
#     'WMF-Last-Access': '06-Jul-2025',
#     'NetworkProbeLimit': '0.001',
#     'zhwikimwuser-sessionId': '908f7b4ff84d5c73379a',
#     'zhwikiBlockID': '614983%21718c327a9fe3c02c88cffcdfd993fa1df28b9e2d8c5d253c18eb8b52d8c83aa50436dfa40368c083325f20fbce3ac5ae0b3def504fc642f7610d7964b1dbf693',
#     'VEE': 'visualeditor',
#     'WMF-DP': '211,c3a',
# }

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=0, i',
    'referer': 'https://zh.wikipedia.org/wiki/2024%E5%B9%B4%E9%80%9D%E4%B8%96%E4%BA%BA%E7%89%A9%E5%88%97%E8%A1%A8',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'WMF-Last-Access-Global=06-Jul-2025; GeoIP=US:CA:Los_Angeles:34.05:-118.24:v4; WMF-Uniq=15pmQsjCEDtfN0HEo33nGQIoAAEBAFvdM_2kcYyLByv563-91RNaPa-Yt9wl7W2P; WMF-Last-Access=06-Jul-2025; NetworkProbeLimit=0.001; zhwikimwuser-sessionId=908f7b4ff84d5c73379a; zhwikiBlockID=614983%21718c327a9fe3c02c88cffcdfd993fa1df28b9e2d8c5d253c18eb8b52d8c83aa50436dfa40368c083325f20fbce3ac5ae0b3def504fc642f7610d7964b1dbf693; VEE=visualeditor; WMF-DP=211,c3a',
}

response = requests.get(
    'https://zh.wikipedia.org/wiki/2024%E5%B9%B41%E6%9C%88%E9%80%9D%E4%B8%96%E4%BA%BA%E7%89%A9%E5%88%97%E8%A1%A8',
    headers=headers,
)
print(response.text)
