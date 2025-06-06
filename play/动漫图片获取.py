import os

import requests
from bs4 import BeautifulSoup


def imgPT(endpame):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'http://www.netbian.com/dongman/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    }
    TP_PATH = "C:/Users/JBWang/Desktop/dong"
    pame = 1
    urlpme = ""
    for i in range(1, endpame + 1):
        if pame != 1:
            urlpme = "_" + str(pame)
        url = f'http://www.netbian.com/dongman/index{urlpme}.htm'
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            pame += 1
            soup = BeautifulSoup(response.content, 'lxml')
            list = soup.select("div.list")[0]
            li = list.select("li")
            for f in li:
                img = f.select("img")[0]
                src = img.get("src")
                name = src[src.rfind("/") + 1:]
                file_names = os.listdir(TP_PATH)
                filepath = os.path.join(TP_PATH + "/", name)
                if name in file_names:
                    print(f"{name}已存在")
                    continue
                response = requests.get(src)
                if response.status_code == 200:
                    with open(filepath, 'wb+') as f:
                        f.write(response.content)
                        f.close()
                        print(f"下载成功: {src}")

            print(f"下载成功: 第{i}页{url}")
        else:
            print("请求失败")
    print(f"已运行到第{endpame}页，运行结束，下载完成")


if __name__ == '__main__':
    imgPT(8)
