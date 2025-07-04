import requests

from getSaWeb.大模型视频.可灵AI视频 import handle_file

# cookies = {
#     '_tea_web_id': '7521783899552319022',
#     's_v_web_id': 'verify_mcjbvjmw_lMpJglhj_R2Ns_4AJS_Blod_UGNicqceltZw',
#     'fpk1': 'a33261eb03dff59b5503f63c8ce0ee46d8f0257bf105c1999a107e31cbc0cfcd147bc38b705524947ae88dface9915e2',
#     'uifid_temp': '45e0a7d58a97f5a646db36cbd19f7960938e279de34ff540536965a38b384d8c53d7cf6777c74e207f12dafdd4b80d93d4401db98b95b524855b383cbf2ef1318138313adb18d8ecab81e92c1a996092',
#     'uifid': '45e0a7d58a97f5a646db36cbd19f7960938e279de34ff540536965a38b384d8cb46e79b7ab4d4c33b37c168e092ac481a38fb5361717b562c02f707c9ba312eba20947cf855894071c169b36513379732637487bf335e496c387acf98c2c5f1bb3c26b8b93d665a65f7685dec43dc85d9ffdd0c17f1611d887b9bcf1ef3d23b150b660d86a4f530af2d85d8bd5aaa3e7b9843244980a93f509746a25e36353984b87b8a96a9b88ba3e8dc225e10be1da',
#     'passport_csrf_token': 'da5caee9f78a7d4dad536d0d3759cc51',
#     'passport_csrf_token_default': 'da5caee9f78a7d4dad536d0d3759cc51',
#     'ttwid': '1|ET3vx-jRJ8w0T-pE-8DfNwl1XmSd7VvCuz5qvLMxllY|1751384168|1baafac94e5e5b2a4005f998628dde6d7f06466bffa5dd89d42664ec69619fe8',
#     '_uetsid': '557210e055d111f09df8575e9f448dc6',
#     '_uetvid': '5571f50055d111f087c171302456d38a',
# }

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'app-sdk-version': '48.0.0',
    'appid': '513695',
    'appvr': '5.8.0',
    'content-type': 'application/json',
    'lan': 'zh-Hans',
    'loc': 'cn',
    'origin': 'https://jimeng.jianying.com',
    'pf': '7',
    'priority': 'u=1, i',
    'referer': 'https://jimeng.jianying.com/ai-tool/home?activeTab=short_video',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sign': '99b440cb5518c338b6a8ece4555d0846',
    'sign-ver': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    # 'cookie': '_tea_web_id=7522289114404111891; x-web-secsdk-uid=43c46a2b-5de0-4427-a227-34bd45239438; s_v_web_id=verify_mcl9ws6v_zTeDdPcC_GXiW_4dcn_9PFu_jjNvnE0RBhrW; fpk1=57f278a1c932bcc16be776d0dce45997d49f97597cc7796590bbd311232486dce16845aca76a9c72f6a38a1aaa0e719a; uifid_temp=45e0a7d58a97f5a646db36cbd19f7960938e279de34ff540536965a38b384d8c862eed91123ec7b5e52ed68352505d0601d8890e9ed09f367fb713765854ce7aaf955566a5f1d4fe77a7f6a1bac5c9d5; uifid=45e0a7d58a97f5a646db36cbd19f7960938e279de34ff540536965a38b384d8cb895c779314ead13ebc00d82572a0c326cbbe505b57f6f4c4a347529abff45a03776c39966f0d3f6e8875962149b5beff725ac76e5749891557342b1e9bb8f429b0a2c15f024488ceb14b3d41f8371cd20af532981c461836ef3ebb78734308ba53d108602d91994ec2300748f32122f31bc46b6345f3107eff8428dc8d644517938497179d7f16ef78d601ef7e5a625; ttwid=1|1U_KmZVktdXRfk7TY-wB-HfjoGan9CK92nX20JJCjmE|1751419445|439a27718363a27cee38bbe426e4b92dfb00a2ee83ea36869c3793472085492c',
}

params = {
    'aid': '513695',
    'da_version': '3.2.5',
    'aigc_features': 'app_lip_sync',
    # 'msToken': 'bJta5RYZzwq5Dcq832Isb_HHJF7yBhpEqCAdzCNip1FSoZhIQNtojnVp1SxeSOtqAXDzQVH_pqiKdilk_RsEzv_7HD84MkOmllw4NPsvC3Syc41_MRRcE0EgTNLKL9g=',
    # 'a_bogus': 'YfMEDOhAMsm16/m2jwkz9bmFARy0YW-FgZENpMKRqUoF',
}
video_urllist = []
video_idlist = []
datadict = {}


def get_html(page):
    para = str(20 + (page - 1) * 40)
    datatext = '{"count":40,"filter":{"work_type_list":["short_video"]},"offset":' + para + ',"image_info":{"width":2048,"height":2048,"format":"webp","image_scene_list":[{"scene":"smart_crop","width":240,"height":240,"format":"webp","uniq_key":"smart_crop-w:240-h:240"},{"scene":"smart_crop","width":320,"height":320,"format":"webp","uniq_key":"smart_crop-w:320-h:320"},{"scene":"smart_crop","width":480,"height":480,"format":"webp","uniq_key":"smart_crop-w:480-h:480"},{"scene":"smart_crop","width":480,"height":320,"format":"webp","uniq_key":"smart_crop-w:480-h:320"},{"scene":"smart_crop","width":240,"height":160,"format":"webp","uniq_key":"smart_crop-w:240-h:160"},{"scene":"smart_crop","width":160,"height":213,"format":"webp","uniq_key":"smart_crop-w:160-h:213"},{"scene":"smart_crop","width":320,"height":427,"format":"webp","uniq_key":"smart_crop-w:320-h:427"},{"scene":"loss","width":1080,"height":1080,"format":"webp","uniq_key":"1080"},{"scene":"loss","width":900,"height":900,"format":"webp","uniq_key":"900"},{"scene":"loss","width":720,"height":720,"format":"webp","uniq_key":"720"},{"scene":"loss","width":480,"height":480,"format":"webp","uniq_key":"480"},{"scene":"loss","width":360,"height":360,"format":"webp","uniq_key":"360"},{"scene":"normal","width":2048,"height":2048,"format":"webp","uniq_key":"2048"}]},"category_id":11780,"feed_refer":"feed_loadmore"}'
    response = requests.post(
        'https://jimeng.jianying.com/mweb/v1/get_explore',
        params=params,
        # cookies=cookies,
        headers=headers,
        data=datatext,
    )
    json = response.json()
    data = json['data']
    item_list = data['item_list']
    for item in item_list:
        video = item['video']
        transcoded_video = video['transcoded_video']
        if "1080p" in transcoded_video.keys():
            transcodedvideo = transcoded_video["1080p"]
        else:
            transcodedvideo = transcoded_video["360p"]
        video_url = transcodedvideo["video_url"]
        video_id = video['video_id']
        if video_url not in video_urllist:
            id = video_id
            if id not in video_idlist:
                if id not in datadict.keys():
                    video_idlist.append(id)
                    video_urllist.append(video_url)
                    datadict[id] = video_url
            else:
                print("视频 ID 已存在")
                continue
        else:
            print("视频 URL 已存在")
            continue


if __name__ == '__main__':
    for i in range(1, 120):
        get_html(i)
        if len(video_urllist) >= 360:
            with open('即梦video_url.txt', 'w', encoding='utf-8') as f:
                for video_url in video_urllist:
                    f.write(video_url + ',')
            f.close()
            break
        else:
            print(len(video_urllist))
            # time.sleep(5)
    son_path = r'D:\txet\即梦'
    for id, video_url in datadict.items():
        namepoth = id + '.mp4'
        print(namepoth)
        handle_file(video_url, son_path, namepoth)
