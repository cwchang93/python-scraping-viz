# %% [markdown]
# # Lesson 04｜BeautifulSoup（二）：翻頁與整站爬取
#
# 上一堂我們能解析一頁。今天要讓程式自己翻頁，把整個書店的書抓下來存成 CSV：
# 處理相對網址、禮貌地連續請求、用 logging 留下紀錄。
# 在 VS Code 按每格上方的 Run Cell 逐格執行。

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

# %% [markdown]
# ## 01｜今天的成果預覽
#
# 練習站 books.toscrape.com 共有 50 頁、1000 本書。先用存好的第一頁看看我們要的資料長什麼樣子。

# %%
from bs4 import BeautifulSoup

html = Path("fixtures/books_index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
print("這一頁的書本數量：", len(soup.select("article.product_pod")))
print(soup.select_one("li.current").get_text(strip=True))

# %% [markdown]
# ## 02｜解析一本書
#
# 每本書是 `article.product_pod`。注意書名：`h3 a` 的文字會被截短（`A Light in the ...`），
# 完整書名在 `title` 屬性裡。

# %%
pod = soup.select_one("article.product_pod")
link = pod.select_one("h3 a")
print("截短的文字：", link.get_text())
print("完整書名：", link["title"])
print("價格文字：", pod.select_one("p.price_color").get_text())
print("相對連結：", link["href"])
print("庫存：", pod.select_one("p.availability").get_text(strip=True))
print("評分的 class：", pod.select_one("p.star-rating")["class"])

# %% [markdown]
# ## 03｜價格：字串要變成數字
#
# `"£51.77"` 是字串，不能比大小或加總。最簡單的做法是去掉貨幣符號再轉 `float`。

# %%
price_text = pod.select_one("p.price_color").get_text()
price = float(price_text.replace("£", ""))
print(price, type(price).__name__)
print("加 10 元：", price + 10)

# %% [markdown]
# ## 04｜小心：£ 變成 Â£ 的亂碼
#
# 這個網站沒有宣告編碼，`requests` 會預設用 ISO-8859-1 解碼。
# 先用自己做的 bytes 看看發生什麼事。

# %%
data = "£12.84".encode("utf-8")
print("正確解碼：", data.decode("utf-8"))
print("用 ISO-8859-1 解碼：", data.decode("latin-1"))

# %% [markdown]
# 實際抓網頁看看。解法：把 `response.content`（原始 bytes）交給 BeautifulSoup，
# 它會自己讀網頁裡的 `<meta charset>` 判斷編碼。

# %%
import requests

USER_AGENT = "python-scraping-viz-class/0.1 (student project)"


def fetch(url, params=None, timeout=10):
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"抓取失敗：{url} → {type(error).__name__}")
        return None
    return response


response = fetch("https://books.toscrape.com/catalogue/page-2.html")
if response is not None:
    print("requests 判斷的 encoding：", response.encoding)
    for label, source in [("response.text", response.text), ("response.content", response.content)]:
        price_tag = BeautifulSoup(source, "html.parser").select_one("p.price_color")
        print(f"{label:17}→", price_tag.get_text())

# %% [markdown]
# ## 05｜re 小工具：從文字裡挖出數字
#
# 用 `re`（正規表達式）處理「規則固定但不好切」的文字。今天只用三個：
# - `re.search(規則, 文字)`：找第一個符合的，回傳 match 物件（找不到是 `None`）
# - `match.group()`：取出符合的文字
# - `re.sub(規則, 取代文字, 文字)`：取代

# %%
import re

print(re.search(r"\d+\.\d+", "£51.77").group())
print(re.sub(r"[^\d.]", "", "£51.77"))

page_text = soup.select_one("li.current").get_text(strip=True)
print("原文：", page_text)

match = re.search(r"Page (\d+) of (\d+)", page_text)
current_page, total_pages = int(match.group(1)), int(match.group(2))
print("第", current_page, "頁，共", total_pages, "頁")

# %% [markdown]
# ## 06｜評分：class 裡的英文字轉數字
#
# `p.star-rating` 的 class 是 `["star-rating", "Three"]`，第二個字就是評分。

# %%
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

rating_word = pod.select_one("p.star-rating")["class"][1]
print(rating_word, "→", RATING_WORDS.get(rating_word))

# %% [markdown]
# ## 07｜相對網址：urljoin
#
# 網頁裡的連結常常只寫一半（相對網址）。`urljoin(目前頁面的網址, 連結)` 幫你組成完整網址。
# 同一個網站，不同頁面的「相對基準」不一樣，所以一定要用 `urljoin`，不要自己拼字串。

# %%
from urllib.parse import urljoin

home = "https://books.toscrape.com/"
print(urljoin(home, "catalogue/page-2.html"))

page2 = "https://books.toscrape.com/catalogue/page-2.html"
print(urljoin(page2, "page-3.html"))
print(urljoin(page2, "in-her-wake_980/index.html"))
print(urljoin(page2, "/about"))

# %% [markdown]
# ## 08｜整頁解析：parse_books
#
# 把前面的步驟包成函式。輸入 HTML 和「這一頁的網址」，回傳 list of dict。

# %%
def parse_price(text):
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def parse_books(html, page_url):
    page = BeautifulSoup(html, "html.parser")
    books = []
    for pod in page.select("article.product_pod"):
        link = pod.select_one("h3 a")
        rating_word = pod.select_one("p.star-rating")["class"][1]
        books.append(
            {
                "title": link["title"],
                "price": parse_price(pod.select_one("p.price_color").get_text()),
                "rating": RATING_WORDS.get(rating_word),
                "in_stock": "In stock" in pod.select_one("p.availability").get_text(),
                "url": urljoin(page_url, link["href"]),
            }
        )
    return books


books = parse_books(html, "https://books.toscrape.com/")
print("筆數：", len(books))
print(books[0])

# %% [markdown]
# ## 09｜找下一頁
#
# 「下一頁」按鈕是 `li.next a`。最後一頁沒有這個按鈕，`select_one` 會回傳 `None`，
# 這就是「該停了」的訊號。

# %%
def find_next_url(html, page_url):
    link = BeautifulSoup(html, "html.parser").select_one("li.next a")
    if link is None:
        return None
    return urljoin(page_url, link["href"])


fixtures = [
    ("fixtures/books_index.html", "https://books.toscrape.com/"),
    ("fixtures/books_page2.html", "https://books.toscrape.com/catalogue/page-2.html"),
    ("fixtures/books_page50.html", "https://books.toscrape.com/catalogue/page-50.html"),
]
for path, page_url in fixtures:
    page_html = Path(path).read_text(encoding="utf-8")
    print(Path(path).name, "→ 下一頁：", find_next_url(page_html, page_url))

# %% [markdown]
# ## 10｜logging：比 print 更適合爬蟲的紀錄方式
#
# `print` 只能在畫面上看。`logging` 有等級（INFO、WARNING、ERROR）、有時間，還能同時寫進檔案。
# 爬蟲跑很久時，紀錄檔是你事後唯一的線索。

# %%
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    force=True,
)
logger = logging.getLogger("books")

logger.info("開始爬取")
logger.warning("第 %d 頁抓取失敗：%s", 3, "timeout")
logger.debug("這行不會出現，因為等級是 INFO")

# %% [markdown]
# 同時寫進檔案：加一個 `FileHandler`。

# %%
Path("output").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("output/crawl.log", encoding="utf-8"),
    ],
    force=True,
)
logger.info("這行會同時出現在畫面和 output/crawl.log")

# %% [markdown]
# ## 11｜翻頁迴圈：crawl_books
#
# 迴圈的條件：還有下一頁、而且沒超過 `max_pages`。每抓完一頁就 `sleep` 一下，並記錄進度。
# `max_pages=None` 代表一直抓到最後一頁。

# %%
import time


def crawl_books(start_url="https://books.toscrape.com/", max_pages=3, delay=1.0):
    all_books = []
    url = start_url
    page_number = 0
    while url is not None and (max_pages is None or page_number < max_pages):
        response = fetch(url)
        if response is None:
            logger.warning("第 %d 頁抓取失敗，停止：%s", page_number + 1, url)
            break
        page_number += 1
        books = parse_books(response.content, url)
        all_books.extend(books)
        logger.info("第 %d 頁：%d 本（累計 %d 本）", page_number, len(books), len(all_books))
        url = find_next_url(response.content, url)
        if url is not None:
            time.sleep(delay)
    return all_books


books = crawl_books(max_pages=3, delay=1.0)
print("共", len(books), "本")

# %% [markdown]
# ## 12｜存成 CSV
#
# - `csv.DictWriter`：list of dict 直接寫成 CSV。
# - `newline=""`：避免 Windows 多出空白行。
# - `encoding="utf-8-sig"`：讓 Excel 打開中文不會亂碼。

# %%
import csv

FIELDNAMES = ["title", "price", "rating", "in_stock", "url"]


def save_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return path


csv_path = save_csv(books, "output/books.csv")
print("已存檔：", csv_path, "，大小：", csv_path.stat().st_size, "bytes")

# %% [markdown]
# ## 13｜讀回來驗證
#
# CSV 讀回來每個欄位都是字串，要用數字時再轉換。

# %%
with open(csv_path, newline="", encoding="utf-8-sig") as file:
    saved_rows = list(csv.DictReader(file))

print("讀回筆數：", len(saved_rows), "，原本筆數：", len(books))
print("第一筆：", saved_rows[0])
print("價格是字串：", repr(saved_rows[0]["price"]))

# %% [markdown]
# ## 14｜抓整個書店
#
# 全站 50 頁，每頁間隔 1 秒，加上每頁請求的時間，約需 3 分鐘。要抓全站，把 `max_pages` 改成 `None`：
#
# ```python
# books = crawl_books(max_pages=None, delay=1.0)   # 1000 本
# ```
#
# 課堂上先用 3 頁確認程式正確，作業再跑全站。跑之前先想：
# 這個站是專為練習爬蟲設計的，所以可以；換成別人的網站，就要回到上一堂的爬取守則。

# %% [markdown]
# ## 15｜沒網路也能上課
#
# `parse_books` 與 `find_next_url` 只吃 HTML，用 `fixtures/` 就能練習。

# %%
page2_html = Path("fixtures/books_page2.html").read_text(encoding="utf-8")
page2_books = parse_books(page2_html, "https://books.toscrape.com/catalogue/page-2.html")
cheapest = min(page2_books, key=lambda book: book["price"])
print("第 2 頁最便宜的書：", cheapest["title"], cheapest["price"])
