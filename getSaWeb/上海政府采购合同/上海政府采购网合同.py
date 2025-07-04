import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://www.zfcg.sh.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
}

datadict = {
    '项目': [],
    '发布时间': [],
    '供应商（乙方）': [],
    '法定代表人': [],
    '联系方式': [],
    '合同金额（元）': [],
}


def get_text(pageNo):
    json_data = {
        'pageNo': pageNo,
        'pageSize': 100,
        'categoryCode': 'ZcyAnnouncement5',
        'isProvince': True,
        'districtCode': [
            '319900',
        ],
    }

    response = requests.post('http://www.zfcg.sh.gov.cn/portal/category', headers=headers, json=json_data, verify=False)
    json_data = response.json()
    result = json_data['result']
    data1 = result['data']
    data2 = data1['data']
    if data2 == None:
        return
    for i in data2:
        title = i['title']
        datadict['项目'].append(title)
        articleId = i['articleId']
        titleparams = {
            'articleId': articleId,
            'parentId': '137027',
            'timestamp': '1751337684',
        }
        publishDate = i['publishDate']
        time_struct = time.localtime(int(publishDate) / 1000)
        time_standard = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        datadict['发布时间'].append(time_standard)

        textresponse = requests.get('http://www.zfcg.sh.gov.cn/portal/detail', params=titleparams, headers=headers,
                                    verify=False)
        json_text = textresponse.json()
        textresult = json_text['result']
        textdata = textresult['data']
        content = textdata['content']
        soup = BeautifulSoup(content, 'lxml')
        text = soup.text
        # 匹配联系方式
        pattern = r"联系方式：(\d{3}-\d{8}|\d{11})"
        matcher = re.search(pattern, text)
        if matcher:
            dianhua = matcher.group(1)
            datadict['联系方式'].append(dianhua)
        else:
            datadict['联系方式'].append("无")
        # 匹配供应商（乙方）
        pattern1 = r"供应商（乙方）：(\S+)"
        matcher1 = re.search(pattern1, text)
        if matcher1:
            datadict['供应商（乙方）'].append(matcher1.group(1))
        else:
            datadict['供应商（乙方）'].append("无")
        # 匹配法定代表人
        pattern2 = r"法定代表人：(\S+)"
        matcher2 = re.search(pattern2, text)
        if matcher2:
            datadict['法定代表人'].append(matcher2.group(1))
        else:
            datadict['法定代表人'].append("无")
        # 匹配合同金额（元）
        pattern3 = r"合同金额（元）：\s*(\d+\.\d{2})"
        matcher3 = re.search(pattern3, text)
        if matcher3:
            datadict['合同金额（元）'].append(matcher3.group(1))
        else:
            datadict['合同金额（元）'].append("无")
    print("第", pageNo, "页数据已获取")


if __name__ == '__main__':
    for i in range(1, 100):
        get_text(i)
    df = pd.DataFrame(datadict)
    df.to_csv("上海政府采购网合同.csv", index=False, encoding="UTF-8")
