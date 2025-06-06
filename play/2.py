import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/10'
}
for start_num in range(0, 250, 25):

    response = requests.get(f"https://movie.douban.com/top250?start={start_num}", headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    # print(soup)
    all1 = soup.findAll("span", attrs={"class": "title"})
    for i in all1:
        i_string = i.string
        if "/" not in i_string:
            print(i_string)
