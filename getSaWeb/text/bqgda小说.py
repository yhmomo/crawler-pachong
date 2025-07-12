import requests
from tqdm import tqdm

from getSaWeb.text.text import get_molui, get_text

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-platform': '"Windows"',
}
base_url = "https://www.d21d965.top"
response = requests.get(base_url + '/index/139518/', headers=headers)
response.encoding = response.encoding
mllist = get_molui(response.text)
contenttext = ""
for i in tqdm(mllist):
    title = i[0]
    herf = base_url + i[1]
    contentText = requests.get(herf, headers=headers)
    contenttext += get_text(contentText.text)

with open('择日飞升.txt', 'w+', encoding='utf-8') as f:
    f.write(contenttext)
    print("成功导出")
f.close()
