import requests

from getSaWeb.text.可灵AI视频 import handle_file

# 定义全局变量 token
token = ''
urllist = []

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://tongyi.aliyun.com',
    'priority': 'u=1, i',
    'referer': 'https://tongyi.aliyun.com/wanxiang/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}


def get_html(pageSize):
    global token  # 声明 token 为全局变量
    json_data = {
        'source': 'task_image',
        'pageSize': pageSize,
        'token': token,
        'taskTypes': [
            'image_to_video',
            'text_to_video',
            'image_to_video_effect',
        ],
    }

    response = requests.post('https://wanx.biz.aliyun.com/wanx/api/square/recommend', headers=headers, json=json_data)
    json = response.json()
    data = json['data']
    if 'token' not in data:
        token = ''
    else:
        token = data['token']
    works = data['works']
    for work in works:
        datawork = work['data']
        image = datawork['image']
        downloadUrl = image['downloadUrl']
        if downloadUrl in urllist:
            continue
        urllist.append(downloadUrl)


if __name__ == '__main__':
    for i in range(1, 50):
        get_html(20)
    son_path = r'D:\txet\通义万相'
    print(len(urllist))
    for downloadUrl in urllist:
        namepoth = downloadUrl[downloadUrl.rfind('/') + 1:]
        handle_file(downloadUrl, son_path, namepoth)
