import json
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

import requests

# -------------------- 配置区域 --------------------
START_PAGE = 1  # 起始页
END_PAGE = 20  # 结束页（含）
MAX_WORKERS = 100  # 最大并发线程数
TIMEOUT = 3  # 代理测试超时
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36"
}
TEST_URL = "http://httpbin.org/ip"
BASE_URL = "https://www.kuaidaili.com/free/inha/{page}/"
# -------------------------------------------------

proxy_pool: List[str] = []  # 最终可用代理池


# ---------- 抓取单页 ----------
def fetch_page(page: int) -> List[Tuple[str, int]]:
    url = BASE_URL.format(page=page)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[WARN] 第 {page} 页抓取失败：{e}")
        return []

    m = re.search(r"const fpsList = (.*?);", resp.text)
    if not m:
        print(f"[WARN] 第 {page} 页未匹配到 fpsList")
        return []

    try:
        fps_list = json.loads(m.group(1))
    except json.JSONDecodeError:
        print(f"[WARN] 第 {page} 页 JSON 解析失败")
        return []

    return [(d["ip"], int(d["port"])) for d in fps_list]


# ---------- 单代理验证 ----------
def check_proxy(ip: str, port: int) -> Tuple[str, int, bool]:
    proxy = f"http://{ip}:{port}"
    try:
        r = requests.get(
            TEST_URL,
            proxies={"http": proxy, "https": proxy},
            headers=HEADERS,
            timeout=TIMEOUT
        )
        if r.status_code == 200 and "origin" in r.json():
            return ip, port, True
    except Exception:
        pass
    return ip, port, False


# ---------- 主流程 ----------
if __name__ == "__main__":
    all_proxies: List[Tuple[str, int]] = []
    # 1. 抓取所有目标页
    for p in range(START_PAGE, END_PAGE + 1):
        print(f"[INFO] 正在抓取第 {p} 页 …")
        all_proxies.extend(fetch_page(p))
        # 简单反爬：随机 sleep
        time.sleep(random.uniform(0.5, 1.5))
    print(f"[INFO] 共抓取到 {len(all_proxies)} 条代理")

    # 2. 多线程验证
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        future_map = {pool.submit(check_proxy, ip, port): (ip, port)
                      for ip, port in all_proxies}
        for fut in as_completed(future_map):
            ip, port, ok = fut.result()
            if ok:
                proxy_pool.append(f"http://{ip}:{port}")
                print(f"[√] {ip}:{port}")
            else:
                print(f"[×] {ip}:{port}")

    # 3. 结果输出
    print("\n================== 代理池 ==================")
    for p in proxy_pool:
        print(p)
    print(f"\n可用代理总数：{len(proxy_pool)}")
    with open("valid_proxies.txt", "w", encoding="utf-8") as fp:
        fp.write("\n".join(proxy_pool))
    print(f"已写入 {len(proxy_pool)} 个代理到 valid_proxies.txt")
