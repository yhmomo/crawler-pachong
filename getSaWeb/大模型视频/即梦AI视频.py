import requests

# 定义全局变量 token
token = ''
urllist = []

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'app-sdk-version': '48.0.0',
    'appid': '513695',
    'appvr': '5.8.0',
    'content-type': 'application/json',
    'device-time': '1751301888',
    'dnt': '1',
    'lan': 'zh-Hans',
    'loc': 'cn',
    'origin': 'https://jimeng.jianying.com',
    'pf': '7',
    'priority': 'u=1, i',
    'referer': 'https://jimeng.jianying.com/ai-tool/home?type=video&activeTab=short_video',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sign': 'ceced57a30678bbebe3ac2f6c53532bc',
    'sign-ver': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}

# params = {
#     'aid': '513695',
#     'da_version': '3.2.5',
#     'aigc_features': 'app_lip_sync',
#     'msToken': 'FKXINsFWZ5eI7opUnNhqkhN7Nv00PUO4dVf3ukQbIh1yr7JG4ZfV9ax5vepXhE7lY4uIA2v3pkvGeG4iQHAHROShlnth0pA8AlTvuXtmVbo4arilZ7KeVA==',
#     # 'a_bogus': 'Yv4mgch4Msm1VHR29Xkz9SJ4A3f0YW-DgZENdCDizULl',
# }

data = '{"count":40,"filter":{"work_type_list":["video","image","canvas"]},"offset":60,"image_info":{"width":2048,"height":2048,"format":"webp","image_scene_list":[{"scene":"smart_crop","width":240,"height":240,"format":"webp","uniq_key":"smart_crop-w:240-h:240"},{"scene":"smart_crop","width":320,"height":320,"format":"webp","uniq_key":"smart_crop-w:320-h:320"},{"scene":"smart_crop","width":480,"height":480,"format":"webp","uniq_key":"smart_crop-w:480-h:480"},{"scene":"smart_crop","width":480,"height":320,"format":"webp","uniq_key":"smart_crop-w:480-h:320"},{"scene":"smart_crop","width":240,"height":160,"format":"webp","uniq_key":"smart_crop-w:240-h:160"},{"scene":"smart_crop","width":160,"height":213,"format":"webp","uniq_key":"smart_crop-w:160-h:213"},{"scene":"smart_crop","width":320,"height":427,"format":"webp","uniq_key":"smart_crop-w:320-h:427"},{"scene":"loss","width":1080,"height":1080,"format":"webp","uniq_key":"1080"},{"scene":"loss","width":900,"height":900,"format":"webp","uniq_key":"900"},{"scene":"loss","width":720,"height":720,"format":"webp","uniq_key":"720"},{"scene":"loss","width":480,"height":480,"format":"webp","uniq_key":"480"},{"scene":"loss","width":360,"height":360,"format":"webp","uniq_key":"360"},{"scene":"normal","width":2048,"height":2048,"format":"webp","uniq_key":"2048"}]},"category_id":11222,"feed_refer":"feed_loadmore"}'
response = requests.post(
    'https://jimeng.jianying.com/mweb/v1/get_explore',
    # params=params,
    # cookies=cookies,
    headers=headers,
    data=data,
)
print(response.json())
