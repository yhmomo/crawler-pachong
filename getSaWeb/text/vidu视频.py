import requests

from getSaWeb.text.可灵AI视频 import handle_file

# 定义全局变量 token
next_page_token = ''
urllist = []
headers = {
    'accept': '*/*',
    'accept-language': 'zh',
    'dnt': '1',
    'origin': 'https://www.vidu.cn',
    'priority': 'u=1, i',
    'referer': 'https://www.vidu.cn/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}


def get_html():
    global next_page_token  # 声明 token 为全局变量
    params = {
        'pager.page_token': next_page_token,
        'pager.pagesz': '20',
        'channel_type': 'media_asset',
        'sort_type': 'recommended',
    }
    response = requests.get('https://service.vidu.cn/vidu/v1/feed', params=params, headers=headers)
    json = response.json()
    if 'next_page_token' in json:
        next_page_token = json['next_page_token']
    else:
        next_page_token = ''
    inspirations = json['inspirations']
    for inspiration in inspirations:
        media_asset = inspiration['media_asset']
        id = media_asset['id'] + ".mp4"
        creation = media_asset['creation']
        uri = creation['uri']
        if uri in urllist:
            continue
        else:
            urllist.append(uri)


if __name__ == '__main__':
    for i in range(1, 60):
        get_html()
    son_path = r'D:\txet\vidu'
    print(len(urllist))
    for downloadUrl in urllist:
        namepoth = (downloadUrl[downloadUrl.rfind("tasks") + 6:downloadUrl.rfind("?")]).replace('/', '')
        handle_file(downloadUrl, son_path, namepoth)
