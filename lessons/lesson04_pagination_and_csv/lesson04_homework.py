# %% [markdown]
# # Lesson 04 作業｜整站爬取、挑書、寫紀錄檔
#
# 完成三題，並確認每題最後的 `assert` 沒有出現錯誤。

# %% [markdown]
# ## 設定工作資料夾
#
# 不論從哪個資料夾執行這個檔案，下面用到的 `fixtures/`、`output/` 都以這個檔案所在的資料夾為基準。

# %%
import os
from pathlib import Path

_this_file = globals().get("__vsc_ipynb_file__") or globals().get("__file__")
if _this_file:
    os.chdir(Path(_this_file).resolve().parent)

# %%
import csv
import logging
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

USER_AGENT = "my-class-bot/0.1 (student project)"
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
FIELDNAMES = ["title", "price", "rating", "in_stock", "url"]
HOME = "https://books.toscrape.com/"
PAGE2 = "https://books.toscrape.com/catalogue/page-2.html"
PAGE50 = "https://books.toscrape.com/catalogue/page-50.html"


def fetch(url, params=None, timeout=10):
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"抓取失敗：{url} → {type(error).__name__}")
        return None
    return response


def parse_books(html, page_url):
    page = BeautifulSoup(html, "html.parser")
    books = []
    for pod in page.select("article.product_pod"):
        link = pod.select_one("h3 a")
        price_text = pod.select_one("p.price_color").get_text()
        rating_word = pod.select_one("p.star-rating")["class"][1]
        books.append(
            {
                "title": link["title"],
                "price": float(re.search(r"\d+(?:\.\d+)?", price_text).group()),
                "rating": RATING_WORDS[rating_word],
                "in_stock": "In stock" in pod.select_one("p.availability").get_text(),
                "url": urljoin(page_url, link["href"]),
            }
        )
    return books


def find_next_url(html, page_url):
    link = BeautifulSoup(html, "html.parser").select_one("li.next a")
    if link is None:
        return None
    return urljoin(page_url, link["href"])


def save_csv(rows, path):
    Path(path).parent.mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def crawl_books(start_url=HOME, max_pages=3, delay=1.0):
    all_books = []
    url = start_url
    page_number = 0
    while url is not None and (max_pages is None or page_number < max_pages):
        response = fetch(url)
        if response is None:
            break
        page_number += 1
        all_books.extend(parse_books(response.content, url))
        url = find_next_url(response.content, url)
        if url is not None:
            time.sleep(delay)
    return all_books


index_html = Path("fixtures/books_index.html").read_text(encoding="utf-8")
page2_html = Path("fixtures/books_page2.html").read_text(encoding="utf-8")
page50_html = Path("fixtures/books_page50.html").read_text(encoding="utf-8")

# %% [markdown]
# ## H1｜爬 3 頁並存成 CSV
#
# 用上面的 `crawl_books` 抓 3 頁（`max_pages=3`），用 `save_csv` 存成 `output/books_3pages.csv`，
# 再讀回來，把讀回的資料列存成 `rows_3pages`（list of dict）。
#
# 想挑戰的話，把 `max_pages` 改成 `None` 抓整個書店（約 3 分鐘，1000 本），但交作業用 3 頁就好。

# %%
# TODO: 請在這裡寫程式
rows_3pages = []

assert len(rows_3pages) == 60
assert list(rows_3pages[0]) == FIELDNAMES
print("H1 完成：", len(rows_3pages), "筆")

# %% [markdown]
# ## H2｜挑出最便宜的三本書
#
# 用本機的 40 本書（`parse_books` 解析首頁與第 2 頁快照）找出價格最低的三本，
# 把書名依價格由低到高存成 list `cheapest_three`。

# %%
rows40 = parse_books(index_html, HOME) + parse_books(page2_html, PAGE2)

# TODO: 請在這裡寫程式
cheapest_three = []

assert cheapest_three == [
    "In Her Wake",
    "Starving Hearts (Triangular Trade Trilogy, #1)",
    "Sophie's World",
]
print("H2 完成：", cheapest_three)

# %% [markdown]
# ## H3｜寫一份紀錄檔
#
# 建立一個 logger（名稱 `homework`），讓它把 INFO 等級的紀錄寫進 `output/homework.log`（`FileHandler`）。
# 紀錄的格式要包含等級，例如 `%(asctime)s %(levelname)s %(message)s`（用 `logging.Formatter` 設定）。
# 然後對三份快照（`books_index`、`books_page2`、`books_page50`）各記一行：
# `解析 books_index：20 本`（用 `%s`、`%d` 帶入名稱與數量）。
# 記完之後，記得 `close()` 你的 FileHandler，內容才會確實寫進檔案。

# %%
log_path = Path("output/homework.log")
Path("output").mkdir(exist_ok=True)
log_path.unlink(missing_ok=True)

pages = [
    ("books_index", index_html, HOME),
    ("books_page2", page2_html, PAGE2),
    ("books_page50", page50_html, PAGE50),
]

# TODO: 請在這裡寫程式（建立 logger 與 FileHandler，再逐頁記錄）

log_lines = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
assert len(log_lines) == 3, "紀錄檔應該有 3 行"
assert all("INFO" in line for line in log_lines)
assert "books_page50：20 本" in log_lines[2]
print("H3 完成：")
print("\n".join(log_lines))
