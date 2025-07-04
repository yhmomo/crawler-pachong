import time

import pandas as pd
import requests

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'dnt': '1',
    'origin': 'https://www.autohome.com.cn',
    'priority': 'u=1, i',
    'referer': 'https://www.autohome.com.cn/',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
}
seriesnamelist = []
seriesminpricelist = []
seriesmaxpricelist = []
averagelist = []
specnumlist = []


def get_series_info(param):
    params = {
        'searchtype': '6',
        'pageindex': str(param),
        'pagesize': '20',
        'orderid': '0',
        'state': '2',
    }

    response = requests.get('https://car-web-api.autohome.com.cn/car/search/searchcar', params=params, headers=headers)
    json_response = response.json()
    result = json_response['result']
    seriesgrouplist = result['seriesgrouplist']
    for seriesgroup in seriesgrouplist:
        seriesname = seriesgroup['seriesname']
        seriesminprice = seriesgroup['seriesminprice']
        seriesmaxprice = seriesgroup['seriesmaxprice']
        average = seriesgroup['average']
        specnum = seriesgroup['specnum']
        seriesnamelist.append(seriesname)
        seriesminpricelist.append(seriesminprice)
        seriesmaxpricelist.append(seriesmaxprice)
        averagelist.append(average)
        specnumlist.append(specnum)


def series_group_to_dict():
    for i in range(1, 100):
        get_series_info(i)
        time.sleep(5)
    data = {
        "车辆型号": seriesnamelist,
        "最低价": seriesminpricelist,
        "最高价": seriesmaxpricelist,
        "评分": averagelist,
        "款型": specnumlist
    }
    df = pd.DataFrame(data)
    print(df)
    df.to_csv('output.csv', index=False)


if __name__ == '__main__':
    series_group_to_dict()
