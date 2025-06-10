import os

import gevent
from gevent import monkey

monkey.patch_all()
from threading import Thread

import requests
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
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
}


def imgStr_get(url):
    try:
        with gevent.Timeout(120, False):
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            gevent.sleep(5)
            return soup
    except gevent.Timeout:
        print(f"请求 {url} 超时，跳过此链接")
        return None
    except Exception as e:
        print(f"请求 {url} 出错：{str(e)}")
        return None


def doc_get(param):
    params = {'page': str(param)}
    try:
        with gevent.Timeout(120, False):
            response = requests.get('https://cangcuc.com/', params=params, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            gevent.sleep(5)
            return soup
    except gevent.Timeout:
        print(f"请求第 {param} 页超时，跳过此页")
        return None
    except Exception as e:
        print(f"请求第 {param} 页出错：{str(e)}")
        return None


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
        if "AIGenerated" in xq_name:
            continue
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


def img_save(imgsoup, son_path, xq_name):
    img_divlist = imgsoup.select("div.col-xl-4.col-lg-6.col-md-6.grid-item.p-1")
    for f in img_divlist:
        img_src_url = f.select("img")[0].get("src")
        img_src_name = cstr(f.select("img")[0].get("alt")) + ".jpg"
        file_names = os.listdir(son_path)
        filepath = os.path.join(son_path, img_src_name)

        if img_src_name in file_names:
            # print(f"{img_src_name} 已存在")
            continue

        try:
            with gevent.Timeout(300, False):
                img_src_url = cstr(img_src_url)
                response = requests.get(img_src_url, headers=headers, stream=True, timeout=60)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    # 尝试打开图片并转换为 RGB 模式
                    try:
                        image = Image.open(filepath)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        image.save(filepath, 'JPEG')
                        print(f"图片下载完成：{img_src_name}")
                    except Exception as e:
                        print(f"转换图片格式时出错：{str(e)}")
        except gevent.Timeout:
            print(f"请求 {img_src_name} 超时，跳过此图片")
        except Exception as e:
            print(f"下载 {img_src_name} 出错：{str(e)}")
    print(f"图片下载完成：{xq_name}")


def video_save(imgsoup, son_path, xq_name):
    video_divlist = imgsoup.select("div.col-12.grid-item.p-1")
    for f in video_divlist:
        video_src_url = cstr(f.select("source")[0].get("src"))
        if "https" not in video_src_url:
            video_src_url = "https://cangcuc.com" + video_src_url
        video_src_name = video_src_url[video_src_url.rindex("/") + 1:]
        file_names = os.listdir(son_path)
        filepath = os.path.join(son_path, video_src_name)
        if video_src_name in file_names:
            # print(f"{video_src_name}已存在")
            continue
        try:
            # 设置合适的chunk_size，
            chunk_size = 1024 * 1024 * 10  # 1MB 每块
            with requests.get(video_src_url, headers=headers, stream=True, timeout=60) as video_response:
                video_response.raise_for_status()
                total_size = int(video_response.headers.get('content-length', 0))
                downloaded_size = 0
                with open(filepath, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            print(f"Downloaded {downloaded_size}/{total_size} bytes", end='\r')
                print(f"\n视频下载完成: {xq_name + video_src_name}")
        except Exception as e:
            print(f"下载 {video_src_name} 出错：{str(e)}")
        print(f"视频下载完成: {xq_name}")


def rs(i):
    retry_limit = 3
    retry_count = 0
    should_retry = True
    print(f"正在请求第 {i} 页...")

    while should_retry and retry_count < retry_limit:
        try:
            with gevent.Timeout(480, False):
                getos(i)
                should_retry = False
                print(f"第 {i} 页下载完成")
        except gevent.Timeout:
            retry_count += 1
            print(f"第 {i} 页处理超时，正在进行第 {retry_count} 次重试...")
            gevent.sleep(10)
        except Exception as e:
            retry_count += 1
            print(f"第 {i} 页处理出错：{str(e)}，正在进行第 {retry_count} 次重试...")
            gevent.sleep(10)

    if retry_count >= retry_limit:
        print(f"第 {i} 页请求失败，已达最大重试次数，跳过此页")


def thread_worker(start, end):
    jobs = []
    for i in range(start, end + 1):
        jobs.append(gevent.spawn(rs, i))
    gevent.joinall(jobs)


def main(param):
    threads = []
    num_threads = 100  # 设置线程数量为 50
    total_pages = param  # 总页数
    pages_per_thread = total_pages // num_threads  # 每个线程处理的页数
    remainder = total_pages % num_threads  # 余数，用于分配给前几个线程

    start = 1
    for i in range(num_threads):
        # 计算每个线程的起始和结束页码
        if i < remainder:
            end = start + pages_per_thread
        else:
            end = start + pages_per_thread - 1
        # 创建并启动线程
        thread = Thread(target=thread_worker, args=(start, end))
        threads.append(thread)
        thread.start()
        start = end + 1

    # 等待所有线程完成
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main(6)
