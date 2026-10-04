# %% [markdown]
# # Lesson 04 練習｜翻頁、相對網址、logging 與 CSV
#
# 把每一格的 `None` 或 `# TODO` 補完，再按 Run Cell。
# 每題最後的 `assert` 是自我檢查：沒有出現錯誤、而且印出「完成」，就代表答對了。
# 第 1–8、10 題只用本機 HTML；第 9 題會連到練習站抓 2 頁。
#
# - ⭐ Core：第 1–4 題
# - ⭐⭐ Practice：第 5–8 題
# - ⭐⭐⭐ Challenge：第 9–10 題
#
# 第 5 題起會一路用到前面寫好的函式，請依序完成。

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


def fetch(url, params=None, timeout=10):
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"抓取失敗：{url} → {type(error).__name__}")
        return None
    return response


# %% [markdown]
# ## ⭐ 第 1 題｜價格轉數字
#
# `price_text` 是字串。去掉 `£` 後轉成 `float`，存成 `price`。

# %%
price_text = "£51.77"

# TODO: 請在這裡寫程式
price = None

assert price == 51.77
assert price + 10 == 61.77
print("第 1 題完成：", price)

# %% [markdown]
# ## ⭐ 第 2 題｜用 re 取頁碼
#
# 從 `page_text` 取出「目前第幾頁」與「共幾頁」，各轉成 `int`，存成 `current` 與 `total`。
# 提示：`re.search(r"Page (\d+) of (\d+)", ...)` 然後 `group(1)`、`group(2)`。

# %%
page_text = "Page 3 of 50"

# TODO: 請在這裡寫程式
current = None
total = None

assert (current, total) == (3, 50)
print("第 2 題完成：第", current, "頁，共", total, "頁")

# %% [markdown]
# ## ⭐ 第 3 題｜評分轉數字
#
# `rating_classes` 是 `<p class="star-rating Four">` 取到的 class list。用 `RATING_WORDS` 轉成數字，存成 `rating`。

# %%
rating_classes = ["star-rating", "Four"]

# TODO: 請在這裡寫程式
rating = None

assert rating == 4
print("第 3 題完成：", rating)

# %% [markdown]
# ## ⭐ 第 4 題｜組完整網址
#
# 用 `urljoin` 組出兩個完整網址：
# - `url_a`：首頁 `https://books.toscrape.com/` 上的連結 `catalogue/page-2.html`
# - `url_b`：第 2 頁 `https://books.toscrape.com/catalogue/page-2.html` 上的連結 `page-3.html`

# %%
# TODO: 請在這裡寫程式
url_a = None
url_b = None

assert url_a == "https://books.toscrape.com/catalogue/page-2.html"
assert url_b == "https://books.toscrape.com/catalogue/page-3.html"
print("第 4 題完成：")
print(url_a)
print(url_b)

# %% [markdown]
# ## ⭐⭐ 第 5 題｜parse_books(html, page_url)
#
# 寫函式 `parse_books(html, page_url)`，回傳 list of dict。每本書有五個欄位：
# - `title`：完整書名（`h3 a` 的 `title` 屬性）
# - `price`：價格（float）
# - `rating`：評分（int）
# - `in_stock`：有庫存嗎（`"In stock"` 出現在 `p.availability` 的文字裡，回傳 True 或 False）
# - `url`：書本頁面的完整網址（用 `urljoin(page_url, href)`）

# %%
# TODO: 請在這裡寫程式
def parse_books(html, page_url):
    pass


index_html = Path("fixtures/books_index.html").read_text(encoding="utf-8")
page2_html = Path("fixtures/books_page2.html").read_text(encoding="utf-8")
page50_html = Path("fixtures/books_page50.html").read_text(encoding="utf-8")

HOME = "https://books.toscrape.com/"
PAGE2 = "https://books.toscrape.com/catalogue/page-2.html"
PAGE50 = "https://books.toscrape.com/catalogue/page-50.html"

books1 = parse_books(index_html, HOME)
books2 = parse_books(page2_html, PAGE2)
assert len(books1) == 20 and len(books2) == 20
assert books1[0] == {
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "in_stock": True,
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
}
assert books2[0]["title"] == "In Her Wake"
assert books2[0]["url"] == "https://books.toscrape.com/catalogue/in-her-wake_980/index.html"
print("第 5 題完成：", len(books1), "+", len(books2), "本")

# %% [markdown]
# ## ⭐⭐ 第 6 題｜find_next_url(html, page_url)
#
# 寫函式 `find_next_url(html, page_url)`：找到 `li.next a`，回傳下一頁的完整網址；沒有下一頁就回傳 `None`。

# %%
# TODO: 請在這裡寫程式
def find_next_url(html, page_url):
    pass


assert find_next_url(index_html, HOME) == "https://books.toscrape.com/catalogue/page-2.html"
assert find_next_url(page2_html, PAGE2) == "https://books.toscrape.com/catalogue/page-3.html"
assert find_next_url(page50_html, PAGE50) is None
print("第 6 題完成")

# %% [markdown]
# ## ⭐⭐ 第 7 題｜用 logging 記錄進度
#
# 寫函式 `log_page(logger, page_number, book_count)`，用 `logger.info` 記錄一行，格式是：
# `第 2 頁：20 本`（用 `%d` 帶入數字，不要自己組字串）。


# %%
class ListHandler(logging.Handler):
    """把收到的紀錄存進 list，方便檢查。"""

    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(record.getMessage())


# TODO: 請在這裡寫程式
def log_page(logger, page_number, book_count):
    pass


test_logger = logging.getLogger("exercise")
test_logger.setLevel(logging.INFO)
handler = ListHandler()
test_logger.addHandler(handler)

log_page(test_logger, 2, 20)
log_page(test_logger, 3, 20)
assert handler.messages == ["第 2 頁：20 本", "第 3 頁：20 本"]
print("第 7 題完成：", handler.messages)

# %% [markdown]
# ## ⭐⭐ 第 8 題｜存成 CSV 再讀回
#
# 寫函式 `save_csv(rows, path)`：用 `csv.DictWriter` 寫出標頭與所有資料列。
# 欄位順序是 `FIELDNAMES`；開檔要加 `newline=""` 與 `encoding="utf-8-sig"`。

# %%
FIELDNAMES = ["title", "price", "rating", "in_stock", "url"]
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)


# TODO: 請在這裡寫程式
def save_csv(rows, path):
    pass


csv_path = output_dir / "exercise_books.csv"
save_csv(books1 + books2, csv_path)

with open(csv_path, newline="", encoding="utf-8-sig") as file:
    saved = list(csv.DictReader(file))
assert len(saved) == 40
assert list(saved[0]) == FIELDNAMES
assert saved[0]["title"] == "A Light in the Attic"
assert float(saved[1]["price"]) == books1[1]["price"]
print("第 8 題完成：存了", len(saved), "筆")

# %% [markdown]
# ## ⭐⭐⭐ 第 9 題｜寫 crawl_books
#
# 寫函式 `crawl_books(start_url, max_pages, delay)`：
# - 從 `start_url` 開始，用 `fetch` 抓頁面，用 `parse_books` 解析（記得傳 `response.content`）
# - 用 `find_next_url` 找下一頁，抓到沒有下一頁，或已抓了 `max_pages` 頁就停
# - 每次抓完一頁後（如果還有下一頁）`time.sleep(delay)`
# - 抓取失敗（`fetch` 回傳 `None`）就停止
# - 回傳所有書的 list
#
# 這一題會連到練習站抓 2 頁。

# %%
# TODO: 請在這裡寫程式
def crawl_books(start_url, max_pages, delay):
    pass


started = time.time()
crawled = crawl_books(HOME, max_pages=2, delay=1.0)
elapsed = time.time() - started

assert len(crawled) == 40
assert crawled[0]["title"] == "A Light in the Attic"
assert crawled[20]["title"] == "In Her Wake"
assert all(book["url"].startswith("https://books.toscrape.com/catalogue/") for book in crawled)
assert elapsed >= 1.0, "兩頁之間要有 time.sleep(delay)"
print("第 9 題完成：", len(crawled), "本，花了", round(elapsed, 1), "秒")

# %% [markdown]
# ## ⭐⭐⭐ 第 10 題｜統計
#
# 用本機的 40 本書 `rows40 = books1 + books2`，算出：
# - `average_price`：平均價格（四捨五入到小數第 2 位）
# - `most_expensive_title`：最貴的書名
# - `rating_counts`：每個評分有幾本，格式 `{1: 9, 2: 6, ...}`

# %%
rows40 = books1 + books2

# TODO: 請在這裡寫程式
average_price = None
most_expensive_title = None
rating_counts = {}

assert average_price == 34.96
assert most_expensive_title.startswith("Our Band Could Be Your Life")
assert rating_counts == {1: 9, 2: 6, 3: 9, 4: 6, 5: 10}
print("第 10 題完成：平均", average_price, "，評分統計", rating_counts)
