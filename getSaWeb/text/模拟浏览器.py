import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_search_results(base_url):
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(base_url)

            # 等待页面加载完成
            # page.wait_for_load_state("networkidle")
            time.sleep(5)
            # 解析页面，获取天眼查链接
            html_content = page.inner_html("body")

            return html_content
        except Exception as e:
            print(f"请求{base_url}时出错:", e)
            return None
        finally:
            browser.close()


if __name__ == "__main__":
    base_url = "https://cgxt.xju.edu.cn/provider/#/publish/20MAUZ6WNRGXN9VV"
    html_content = get_search_results(base_url)
    soup = BeautifulSoup(html_content, "lxml")
    html = soup.find('div', class_='bg-white padding20 mb20 ng-scope')
    print(html)
