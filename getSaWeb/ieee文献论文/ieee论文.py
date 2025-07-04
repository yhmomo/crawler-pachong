import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://ieeexplore.ieee.org',
    'priority': 'u=1, i',
    'referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&matchBoolean=true&queryText=(%22Document%20Title%22:UAV)%20AND%20(%22Full%20Text%20.AND.%20Metadata%22:battery)%20AND%20(%22Full%20Text%20.AND.%20Metadata%22:GPS)&highlight=true&returnType=SEARCH&matchPubs=true&refinements=ContentType:Conferences&ranges=1884_2025_Year&returnFacets=ALL&pageNumber=2',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'x-security-request': 'required',
}

data = []


def get_html(page_num):
    json_data = {
        'action': 'search',
        'matchBoolean': True,
        'queryText': '("Document Title":UAV) AND ("Full Text .AND. Metadata":battery) AND ("Full Text .AND. Metadata":GPS)',
        'highlight': True,
        'returnType': 'SEARCH',
        'matchPubs': True,
        'pageNumber': str(page_num),
        'refinements': [
            'ContentType:Conferences',
        ],
        'ranges': [
            '1884_2025_Year',
        ],
        'returnFacets': [
            'ALL',
        ],
    }

    response = requests.post('https://ieeexplore.ieee.org/rest/search', headers=headers, json=json_data)
    records = response.json()['records']
    for record in records:
        articleTitle = record['articleTitle']
        htmlLink = "https://ieeexplore.ieee.org" + record['htmlLink']
        htmlresponse = requests.get(htmlLink, headers=headers)
        soup = BeautifulSoup(htmlresponse.content, "lxml")
        Abstract = soup.select("meta[property='twitter:description']")[0].get("content")
        datalist = {
            '网站链接': htmlLink,
            '文章标题': articleTitle,
            '文章摘要': Abstract,
        }
        data.append(datalist)
        print(datalist)


if __name__ == '__main__':
    for i in range(1, 3):
        get_html(i)
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
