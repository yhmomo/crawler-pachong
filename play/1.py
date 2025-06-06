import requests

# cookies = {
#     'PHPSESSID': '9aruv50ojpjb2f82emlgo0kat1',
#     'libvio_714891571-1': '4874.976592',
#     'libvio_714892339-1': '2.630008',
#     'recente': '%5B%7B%22vod_name%22%3A%22%E4%B8%8D%E6%AD%BB%E8%80%85%E4%B9%8B%E7%8E%8B%20%E5%89%A7%E5%9C%BA%E7%89%88%20%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714892391-1-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%2C%7B%22vod_name%22%3A%22%E7%BE%8E%E5%9B%BD%E9%98%9F%E9%95%BF4%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714892339-1-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%2C%7B%22vod_name%22%3A%22%E6%B5%B7%E6%B4%8B%E5%A5%87%E7%BC%982%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714892246-1-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%2C%7B%22vod_name%22%3A%22%E5%93%A5%E6%96%AF%E6%8B%89%E5%A4%A7%E6%88%98%E9%87%91%E5%88%9A2%EF%BC%9A%E5%B8%9D%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714891571-3-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%5D',
#     'libvio_714892391-1': '1.708143',
# }

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    # 'cookie': 'PHPSESSID=9aruv50ojpjb2f82emlgo0kat1; libvio_714891571-1=4874.976592; libvio_714892339-1=2.630008; recente=%5B%7B%22vod_name%22%3A%22%E4%B8%8D%E6%AD%BB%E8%80%85%E4%B9%8B%E7%8E%8B%20%E5%89%A7%E5%9C%BA%E7%89%88%20%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714892391-1-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%2C%7B%22vod_name%22%3A%22%E7%BE%8E%E5%9B%BD%E9%98%9F%E9%95%BF4%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714892339-1-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%2C%7B%22vod_name%22%3A%22%E6%B5%B7%E6%B4%8B%E5%A5%87%E7%BC%982%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714892246-1-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%2C%7B%22vod_name%22%3A%22%E5%93%A5%E6%96%AF%E6%8B%89%E5%A4%A7%E6%88%98%E9%87%91%E5%88%9A2%EF%BC%9A%E5%B8%9D%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.cc%2Fplay%2F714891571-3-1.html%22%2C%22vod_part%22%3A%221080P%22%7D%5D; libvio_714892391-1=1.708143',
}

response = requests.get('https://www.libvio.cc/type/1.html', headers=headers)
print(response.text)