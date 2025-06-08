import os
import time
from pathlib import Path
import socket
import requests
from PIL import Image
from bs4 import BeautifulSoup

from Tool.Strclean import clean_string as cstr

path = "D:/txet/cangcuc"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://cangcuc.com/',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    # 'cookie': 'PHPSESSID=b1a6774034d326847af83fd355391d9d; script_shown_this_session=true',
}


def imgStr_get(url):  # 请求图片详情页
    responsedoc = requests.get(url, headers=headers)
    responsedoc.encoding = 'utf-8'
    soup = BeautifulSoup(responsedoc.text, 'lxml')
    time.sleep(5)
    return soup


def doc_get(param):  # 请求主页
    params = {
        'page': str(param),
    }
    responsedoc = requests.get('https://cangcuc.com/', params=params, headers=headers)
    responsedoc.encoding = 'utf-8'
    soup = BeautifulSoup(responsedoc.text, 'lxml')
    time.sleep(5)
    return soup


def getos(param):
    # 主页
    docsoup = doc_get(param)
    # 创建文件夹
    folder_path = Path(path + '/' + f'第{param}页内容')
    folder_path.mkdir(parents=True, exist_ok=True)  # parents=True表示如果父目录不存在也一并创建，exist_ok=True表示如果目录已存在则不抛出异常
    # 获取图片列表、链接、名称，遍历图片列表
    divlist = docsoup.select("div.col-xl-4.col-lg-6.col-md-6.masonry-item")
    for div in divlist:
        xq_href = div.select("a")[0].get("href")
        xq_name = cstr(div.select("h5")[0].get_text())
        # 创建子文件夹
        son_path = Path(folder_path, xq_name)
        son_path.mkdir(parents=True, exist_ok=True)
        # 请求图片页面
        imgsoup = imgStr_get(xq_href)
        img_class = "col-xl-4 col-lg-6 col-md-6 grid-item p-1"
        video_class = "col-12 grid-item p-1"
        if img_class in imgsoup.prettify():
            img_save(imgsoup, son_path, xq_name)
        # if video_class in imgsoup.prettify():
        #     video_save(imgsoup, son_path, xq_name)
    print(f"第{param}页下载完成")


def img_save(imgsoup, son_path, xq_name):
    img_divlist = imgsoup.select("div.col-xl-4.col-lg-6.col-md-6.grid-item.p-1")
    for f in img_divlist:
        # 图片链接
        img_src_url = f.select("img")[0].get("src")
        #  图片名称
        img_src_name = cstr(f.select("img")[0].get("alt")) + ".jpg"
        # 判断文件是否存在
        file_names = os.listdir(son_path)
        filepath = os.path.join(son_path, img_src_name)
        if img_src_name in file_names:
            print(f"{img_src_name}已存在")
            continue
        #  请求图片
        try:
            img_src_url = cstr(img_src_url)
            response = requests.get(img_src_url)  # 请求图片
            #  判断请求成功 写入文件
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                # 使用Pillow库打开并保存图像文件
                image = Image.open(filepath)
                image.save(filepath)
                print(f"图片下载完成: {img_src_name}")
        except  Exception:
            print(f"{img_src_name}图片链接错误")
    print("------------------图片下载完成--------------------------")
    print(f"图片下载完成: {xq_name}")


def video_save(imgsoup, son_path, xq_name):
    video_divlist = imgsoup.select("div.col-12.grid-item.p-1")
    for f in video_divlist:
        #  视频链接
        video_src_url = f.select("source")[0].get("src")
        #  视频名称
        video_src_name = cstr(video_src_url[video_src_url.rindex("/") + 1:])
        # 判断文件是否存在
        file_names = os.listdir(son_path)
        filepath = os.path.join(son_path, video_src_name)
        if video_src_name in file_names:
            print(f"{video_src_name}已存在")
            continue
        #  请求
        video_src_url = cstr(video_src_url)
        video_response = requests.get(video_src_url)
        video_response.raise_for_status()  # 检查下载是否成功
        #  判断请求成功 写入文件
        with open(filepath, 'wb') as f:
            f.write(video_response.content)
        print(f"视频下载完成{xq_name + video_src_name}")
    print("-------------视频下载完成-------------------------------")
    print(f"视频下载完成: {xq_name}")


def rs(i):
    retry_limit = 3
    retry_count = 0
    should_retry = True
    print(f"正在请求第 {i} 页...")

    while should_retry and retry_count < retry_limit:
        try:
            socket.setdefaulttimeout(20)
            getos(i)
            should_retry = False  # 请求成功，停止重试
            print(f"第 {i} 页下载完成")
        except requests.exceptions.RequestException as e:
            retry_count += 1
            print(f"第 {i} 页请求失败，正在进行第 {retry_count} 次重试...")
            time.sleep(10)  # 等待10秒再重试
    if retry_count >= retry_limit:
        print(f"第 {i} 页请求失败，已达最大重试次数，跳过此页")


if __name__ == '__main__':
    for i in range(1, 21):  # 获取到20页
        # for j in range(1, 4):  # 防止下载不全部。
        rs(i)
