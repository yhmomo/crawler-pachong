import os
import time

import requests

# monkey.patch_all()

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}


def get_html(page_num):
    params = {
        'entrance': 'homepage',
        'isCommunity': 'true',
        'match': '',
        'pageNum': str(page_num),
        'pageSize': '20',
        'sortType': 'recommend',
    }

    response = requests.get('https://api-app-cn.klingai.com/api/works', params=params, headers=headers)

    time.sleep(5)
    json = response.json()
    data = json['data']
    for i in data:
        resource = i['resource']
        resourceUrl = resource['resource']
        if 'jpg' in resourceUrl or 'png' in resourceUrl:
            continue
        son_path = r'D:\txet\可灵'
        video_src_name = resourceUrl[resourceUrl.rfind('/') + 1:resourceUrl.find('?')]
        handle_file(resourceUrl, son_path, video_src_name)


def handle_file(resource_url, son_path, video_src_name):
    file_names = os.listdir(son_path)
    if len(file_names) >= 1000:
        print("文件数量大于等于1000")
        return
    print(f"当前文件夹内文件数量: {len(file_names)}")

    filepath = os.path.join(son_path, video_src_name)
    if video_src_name in file_names:
        print(f"{video_src_name} 已存在")
        return
    video_save(resource_url, filepath, video_src_name)


def video_save(resource_url, filepath, video_src_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        chunk_size = 512
        with requests.get(resource_url, headers=headers, stream=True, timeout=60) as video_response:
            video_response.raise_for_status()
            total_size = int(video_response.headers.get('content-length', 0))
            downloaded_size = 0
            with open(filepath, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        print(f"Downloaded {downloaded_size}/{total_size} bytes", end='\r')
            print(f"\n视频下载完成: {video_src_name}")
    except Exception as e:
        print(f"下载 {video_src_name} 出错：{str(e)}")


if __name__ == '__main__':
    for i in range(102, 150):
        get_html(i)

# def rs(i):
#     retry_limit = 3
#     retry_count = 0
#     should_retry = True
#     print(f"正在请求第 {i} 页...")
#
#     while should_retry and retry_count < retry_limit:
#         try:
#             with gevent.Timeout(480, False):
#                 get_html(i)
#                 should_retry = False
#                 print(f"第 {i} 页下载完成")
#         except gevent.Timeout:
#             retry_count += 1
#             print(f"第 {i} 页处理超时，正在进行第 {retry_count} 次重试...")
#             gevent.sleep(10)
#         except Exception as e:
#             retry_count += 1
#             print(f"第 {i} 页处理出错：{str(e)}，正在进行第 {retry_count} 次重试...")
#             gevent.sleep(10)
#
#     if retry_count >= retry_limit:
#         print(f"第 {i} 页请求失败，已达最大重试次数，跳过此页")
#
#
# def thread_worker(start, end):
#     jobs = []
#     for i in range(start, end + 1):
#         jobs.append(gevent.spawn(rs, i))
#     gevent.joinall(jobs)
#
#
# def main(param):
#     threads = []
#     num_threads = 100  # 设置线程数量为 50
#     total_pages = param  # 总页数
#     pages_per_thread = total_pages // num_threads  # 每个线程处理的页数
#     remainder = total_pages % num_threads  # 余数，用于分配给前几个线程
#
#     start = 1
#     for i in range(num_threads, num_threads + 50):
#         # 计算每个线程的起始和结束页码
#         if i < remainder:
#             end = start + pages_per_thread
#         else:
#             end = start + pages_per_thread - 1
#         # 创建并启动线程
#         thread = Thread(target=thread_worker, args=(start, end))
#         threads.append(thread)
#         thread.start()
#         start = end + 1
#
#     # 等待所有线程完成
#     for thread in threads:
#         thread.join()
#
#
# if __name__ == '__main__':
#     main(100)
