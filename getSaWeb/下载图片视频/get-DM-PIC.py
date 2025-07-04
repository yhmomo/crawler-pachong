import os
import time

import requests
from PIL import Image
from bs4 import BeautifulSoup

from Tool.Strclean import clean_string as strclean


def imgPT(endpage):
    headers = {
        'DNT': '1',
        'Referer': 'https://pic.netbian.com/4kdongman/index.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    TP_PATH = "C:/Users/JBWang/Desktop/dong/"
    url_PATH = "https://pic.netbian.com"
    for i in range(1, endpage + 1):
        urlpme = "" if i == 1 else f"_{i}"
        url = f'https://pic.netbian.com/4kdongman/index{urlpme}.html'
        response = requests.get(url, headers=headers)
        time.sleep(5)
        if response.status_code == 200:
            response.encoding = "GBK"
            soup = BeautifulSoup(response.text, "lxml")
            list = soup.select("ul.clearfix")[0]
            li = list.select("li")
            for f in li:
                imgurl = url_PATH + f.select("a")[0].get("href")
                response = requests.get(imgurl, headers=headers)
                time.sleep(5)
                response.encoding = "GBK"
                imgsoup = BeautifulSoup(response.text, "lxml")
                imgdiv = imgsoup.select("div.photo-pic")[0]
                img = imgdiv.select("img")[0]
                src = url_PATH + img.get("src")
                name = strclean(img.get("title")) + ".jpg"
                file_names = os.listdir(TP_PATH)
                filepath = os.path.join(TP_PATH, name)
                if name in file_names:
                    print(f"{name}已存在")
                    continue
                response = requests.get(src)
                time.sleep(5)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    # 使用Pillow库打开并保存图像文件
                    image = Image.open(filepath)
                    image.save(filepath)
                    print(f"下载成功: {filepath}")
            print(f"下载完成: 第{i}页{url}")
        else:
            print(f"请求失败: {url}")
    print(f"已运行到第{endpage}页，运行结束，下载完成")


if __name__ == '__main__':
    imgPT(50)
