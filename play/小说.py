import requests
from lxml import etree
from tqdm import tqdm
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Cookie': 'Hm_lvt_50197259502a3d0c1205c442586116e2=1698478735; Hm_lpvt_50197259502a3d0c1205c442586116e2=1698478744; Hm_lvt_8d2482c3fea84719a275266911661516=1698478735; Hm_lpvt_8d2482c3fea84719a275266911661516=1698478744',
    'Host': 'www.xbiquyue.net',
    'Connection': 'keep-alive'
}
o_url = "https://www.beqege.cc"
url = "https://www.beqege.cc/8/"
resp = requests.get(url, headers=headers)
text = resp.content.decode('utf-8')
html = resp.text
ele = etree.HTML(html)
bookname = ele.xpath("/html/body/div[1]/div[5]/div[1]/div[2]/div[1]/h1")
book_chapters = ele.xpath("//div[@class='box_con']/div[@id='list']/dl/dd/a/text()")
book_c_urls = ele.xpath("//div[@class='box_con']/div[@id='list']/dl/dd/a/@href")
s = ""
for book_chapter in range(len(book_chapters)):
     s += book_chapters[book_chapter] + "\n" + book_c_urls[book_chapter] + "\n"
with open(bookname+"目录.txt","w") as f:
     f.write(s)
print("输入完成！")

with open(bookname+"目录.txt", 'r') as file:
    s = file.read()
s = s.split("\n")

chapter_titles = s[::2]
chapter_urls = s[1::2]


def remove_upprintable_chars(s):
    """移除所有不可见字符"""
    return ''.join(x for x in s if x.isprintable())



pbar = tqdm(range(len(chapter_urls)))
for i in pbar:
    new_url = o_url +  chapter_urls[i]

    response = requests.get(new_url)
    response.encoding = "utf-8"
    html = response.text
    ele = etree.HTML(html)
    book_bodys = ele.xpath("//div[@id='content']/text()")
    s = "\n" + chapter_titles[i] + "\n"
    with open(bookname+".txt", "a",encoding='utf-8') as f:
        f.write(s)
        for book_body in book_bodys:
            f.write(book_body)
            f.write('\n\n')

print("文章 下载完毕！")
