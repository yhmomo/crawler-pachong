import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://movie.douban.com/subject/1292052/comments?start=40&limit=20&status=P&sort=new_score',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    # 'cookie': 'bid=iWSYmI_mgfQ; ll="118371"; ap_v=0,6.0',
}

params = {
    'percent_type': '',
    'start': str(20 * 1),
    'limit': '20',
    'status': 'P',
    'sort': 'new_score',
    'comments_only': '1',
}

response = requests.get('https://movie.douban.com/subject/1292052/comments', params=params, headers=headers)
print(response.text)
