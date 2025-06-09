import os
import gevent
from gevent import monkey

monkey.patch_all()

import requests
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from Tool.Strclean import clean_string as cstr

# 配置全局路径和请求头
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
}


# 重试装饰器
def retry(retry_limit=3, timeout=600):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < retry_limit:
                try:
                    with gevent.Timeout(timeout, False):
                        return func(*args, **kwargs)
                except gevent.Timeout:
                    print(f"请求超时，正在进行第 {retry_count + 1} 次重试...")
                except Exception as e:
                    print(f"请求出错：{str(e)}，正在进行第 {retry_count + 1} 次重试...")
                retry_count += 1
                gevent.sleep(10)
            print(f"请求失败，已达最大重试次数")

        return wrapper

    return decorator


# 获取页面内容
@retry()
def imgStr_get(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


@retry()
def doc_get(param):
    params = {'page': str(param)}
    response = requests.get('https://cangcuc.com/', params=params, headers=headers)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


# 处理单页内容
def getos(param):
    docsoup = doc_get(param)
    if docsoup is None:
        print(f"无法获取第 {param} 页内容，跳过此页")
        return
    folder_path = Path(path + '/')
    folder_path.mkdir(parents=True, exist_ok=True)

    divlist = docsoup.select("div.col-xl-4.col-lg-6.col-md-6.masonry-item")
    for div in divlist:
        xq_href = div.select("a")[0].get("href")
        xq_name = cstr(div.select("h5")[0].get_text())
        son_path = Path(folder_path, xq_name)
        son_path.mkdir(parents=True, exist_ok=True)

        imgsoup = imgStr_get(xq_href)
        if imgsoup is None:
            print(f"无法获取 {xq_name} 的详情页，跳过此项目")
            continue
        img_class = "col-xl-4 col-lg-6 col-md-6 grid-item p-1"
        video_class = "col-12 grid-item p-1"

        if img_class in imgsoup.prettify():
            img_save(imgsoup, son_path, xq_name)
        if video_class in imgsoup.prettify():
            video_save(imgsoup, son_path, xq_name)
    print(f"第{param}页下载完成")


# 保存图片
def img_save(imgsoup, son_path, xq_name):
    img_divlist = imgsoup.select("div.col-xl-4.col-lg-6.col-md-6.grid-item.p-1")
    for f in img_divlist:
        img_src_url = f.select("img")[0].get("src")
        img_src_name = cstr(f.select("img")[0].get("alt")) + ".jpg"
        file_names = os.listdir(son_path)
        filepath = os.path.join(son_path, img_src_name)
        if img_src_name in file_names:
            # print(f"{img_src_name}已存在")
            continue
        try:
            response = requests.get(img_src_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                image = Image.open(filepath)
                image.save(filepath)
                # print(f"图片下载完成: {img_src_name}")
        except Exception as e:
            print(f"下载 {img_src_name} 出错：{str(e)}")
    # print(f"图片下载完成: {xq_name}")


# 保存视频
def video_save(imgsoup, son_path, xq_name):
    video_divlist = imgsoup.select("div.col-12.grid-item.p-1")
    for f in video_divlist:
        video_src_url = cstr(f.select("source")[0].get("src"))
        video_src_name = cstr(video_src_url[video_src_url.rindex("/") + 1:])
        file_names = os.listdir(son_path)
        filepath = os.path.join(son_path, video_src_name)
        if video_src_name in file_names:
            print(f"{video_src_name}已存在")
            continue
        try:
            video_response = requests.get(video_src_url)
            video_response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(video_response.content)
            print(f"视频下载完成{xq_name + video_src_name}")
        except Exception as e:
            print(f"下载 {video_src_name} 出错：{str(e)}")
    print(f"视频下载完成: {xq_name}")


# 请求单页
def rs(i):
    print(f"正在请求第 {i} 页...")
    getos(i)


# 主函数
def main(param):
    jobs = []
    for i in range(1, param + 1):
        jobs.append(gevent.spawn(rs, i))
    gevent.joinall(jobs)

    # 检查每个协程的状态
    for job in jobs:
        if not job.ready():
            print(f"协程 {job} 未完成")
        else:
            print(f"协程 {job} 已完成")


if __name__ == '__main__':
    main(20)
    print("程序结束")
