import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from Tool.Strclean import trim

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://movie.douban.com/top250',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}

movies_info = []


def get_html(page_num):
    start = (page_num - 1) * 25
    params = {
        'start': str(start),
        'filter': '',
    }
    response = requests.get('https://movie.douban.com/top250', params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    grid_view = soup.find("ol", class_="grid_view")
    lilist = grid_view.select("li")
    for movie in lilist:
        movie_data = {
            '中文名': '',
            '外文名': '',
            '上映年份': '',
            '豆瓣评分': '',
            '评分人数': '',
            '电影类型': '',
            '制片国家/地区': '',
            '制片人与主演': ''
        }

        # 提取电影名称
        title_tags = movie.find_all('span', class_='title')
        movie_data['中文名'] = trim(title_tags[0].get_text())
        if len(title_tags) > 1:
            movie_data['外文名'] = trim(title_tags[1].get_text().strip('/'))

        other_title = movie.find('span', class_='other')
        if other_title:
            other_titles = other_title.get_text().strip('/').split('/')
            movie_data['外文名'] = trim(
                other_titles[0].strip() if movie_data['外文名'] == '' else movie_data['外文名'])
            movie_data['其他名称'] = trim(str([title.strip() for title in other_titles[1:]]))
            if movie_data['外文名'] == '' or movie_data['外文名'] is None:
                if ([title.strip() for title in other_titles[1:]]).__len__() > 1:
                    movie_data['外文名'] = trim(str(([title.strip() for title in other_titles[1:]])[1]))
                else:
                    movie_data['外文名'] = trim(str(([title.strip() for title in other_titles[1:]])[0]))

        son = movie.find('p').get_text().split('\n')[1].strip()
        movie_data['制片人与主演'] = trim(son)

        rating_num = movie.find('span', class_='rating_num')
        movie_data['豆瓣评分'] = trim(rating_num.get_text() if rating_num else '')

        rating_people = movie.find('span', property="v:best")
        movie_data['评分人数'] = trim(rating_people.find_next_sibling('span').get_text().replace('人评价',
                                                                                                 '') if rating_people else '')

        genres = movie.find('p').get_text().split('\n')[2].strip().split('/')
        movie_data['电影类型'] = trim(genres[2])
        movie_data['制片国家/地区'] = trim(genres[1])
        movie_data['上映年份'] = trim(genres[0])
        if "(" in trim(genres[0]):
            year_pattern = r"\b\d{4}\b"
            year = re.search(year_pattern, trim(genres[0])).group()
            movie_data['上映年份'] = year
            movie_data['制片国家/地区'] = trim(genres[0][genres[0].find('(') + 1:genres[0].find(')')])
        movies_info.append(movie_data)


if __name__ == '__main__':
    for i in range(1, 11):
        get_html(i)
    df = pd.DataFrame(movies_info)
    df.to_csv('movies.csv', index=False, encoding='utf-8-sig')
    print(df.values)
