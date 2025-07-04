import logging
import random
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_search_results(search_query):
    """
    获取搜索结果中的天眼查链接

    Args:
        search_query (str): 搜索栏输入的搜索关键词

    Returns:
        str or None: 搜索天气查链接，如果没有找到则返回 None
    """
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 访问百度，并进行搜索
            page.goto("https://www.baidu.com/s?wd=" + search_query)
            # page.click()

            # 等待页面加载完成
            page.wait_for_load_state("networkidle")
            time.sleep(random.randint(15, 25))

            # 解析页面，获取天眼查链接
            html_content = page.inner_html("body")
            soup = BeautifulSoup(html_content, "lxml")
            search_results = soup.find_all("div", class_="result c-container xpath-log new-pmd")
            for result in search_results:
                if "mu" in result.attrs:
                    if "tianyancha" not in result.attrs["mu"]:
                        pattern = 'https://www.tianyancha.com/\w+[^"\s]*'
                        matches = re.search(pattern, html_content)
                        if matches:
                            url = matches.group()
                            return url
                        else:
                            return result.attrs["mu"]
                    else:
                        return result.attrs["mu"]
            return None

        except Exception as e:
            logging.error(f"搜索 {search_query} 时出错: {e}")
            return None

        finally:
            browser.close()


def update_csv(data4, output_file):
    """
    更新 CSV 文件

    Args:
        data4 (DataFrame): 更新后的数据
        output_file (str): 输出的 CSV 文件路径
    """
    data4.to_csv(output_file, index=False)


# 使用示例
if __name__ == "__main__":
    # 读取原始 CSV 文件
    data4 = pd.read_csv('../天眼查代码/A股公司_更新.csv')

    # 遍历每一行数据，更新天眼查链接
    for index, row in data4.iterrows():
        link = row["天眼查链接"]  # 获取当前行的天眼查链接
        if pd.isna(link) or link == "" or "tian" not in link:  # 如果链接为空或不包含 "tianyancha"，则重新搜索
            company = row["股票公司"]
            if pd.isna(company):  # 检查公司名称是否为空
                logging.warning(f"第 {index} 行的公司名称为空，无法进行搜索。")
                continue

            search_query = f"{company} 天眼查"  # 构造搜索关键词
            try:
                results = get_search_results(search_query)
                data4.loc[index, "天眼查链接"] = results
                logging.info(f"已更新 {company} 的天眼查链接: {results}")
                update_csv(data4, '../天眼查代码/A股公司_更新.csv')
            except Exception as e:
                logging.error(f"更新 {company} 天眼查链接时出错: {e}")
                update_csv(data4, '../天眼查代码/A股公司_更新.csv')
        else:
            logging.info(f"{link} 链接正常。")

    logging.info("所有数据已处理完成。")
