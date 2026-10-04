# %% [markdown]
# # Lesson 03｜BeautifulSoup（一）：解析 HTML
#
# 上一堂我們用字串搜尋網頁，能找，但很不方便。
# 今天改用 BeautifulSoup：把 HTML 變成一棵可以查詢的樹，用標籤與 class 直接取資料。
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
# 先看結果：不到十行，把名言網站第一頁變成「一則名言一筆資料」。
# 這裡讀 `fixtures/` 裡存好的網頁，沒有網路也能執行。

# %%
from bs4 import BeautifulSoup

html = Path("fixtures/quotes_page1.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

for quote in soup.select("div.quote")[:3]:
    print(quote.select_one("small.author").get_text(), "：", quote.select_one("span.text").get_text()[:30], "...")

# %% [markdown]
# ## 02｜解析流程
#
# 1. 取得 HTML（上一堂的 `fetch`，或讀本機檔案）
# 2. 建立 `soup`
# 3. 找元素：`find`、`find_all`、`select`
# 4. 取值：文字或屬性
# 5. 整理成 list of dict

# %% [markdown]
# ## 03｜建立 soup
#
# `BeautifulSoup(html, "html.parser")`：第二個參數指定用 Python 內建的解析器，不必另外安裝。

# %%
small_html = """
<html>
  <head><title>我的小書店</title></head>
  <body>
    <h1>本週推薦</h1>
    <ul id="books">
      <li class="book">Python 入門</li>
      <li class="book">爬蟲實戰</li>
      <li class="book sale">資料視覺化</li>
    </ul>
    <a href="/about" class="link">關於我們</a>
  </body>
</html>
"""
small_soup = BeautifulSoup(small_html, "html.parser")
print("網頁標題：", small_soup.title.get_text())
print("第一個 h1：", small_soup.h1.get_text())

# %% [markdown]
# ## 04｜find：找第一個符合的元素
#
# `find(標籤, class_=...)`。注意是 `class_`，因為 `class` 是 Python 的保留字。
# 找不到時回傳 `None`。

# %%
first_book = small_soup.find("li", class_="book")
print("型態：", type(first_book).__name__)
print("文字：", first_book.get_text())

missing = small_soup.find("li", class_="no-such-class")
print("找不到時：", missing)

# %% [markdown]
# ## 05｜find_all：找全部符合的元素
#
# 回傳像 list 的結果，可以 `for` 逐筆處理，也可以 `len()`。

# %%
books = small_soup.find_all("li", class_="book")
print("數量：", len(books))
for book in books:
    print("-", book.get_text())

# %% [markdown]
# ## 06｜取屬性：標籤上的 href、class、id
#
# - `tag["href"]`：沒有這個屬性會出錯
# - `tag.get("href")`：沒有這個屬性回傳 `None`

# %%
link = small_soup.find("a")
print("href：", link["href"])
print("用 get 取 href：", link.get("href"))
print("沒有 title 屬性：", link.get("title"))
print("所有屬性：", link.attrs)

# %% [markdown]
# ## 07｜get_text：取出文字
#
# `get_text(strip=True)` 會去掉前後的空白與換行，整理資料時幾乎都要加。

# %%
raw = small_soup.find("ul", id="books")
print(repr(raw.get_text()))
print(repr(raw.get_text(strip=True)))

# %% [markdown]
# ## 08｜CSS 選擇器：select 與 select_one
#
# 和 F12 裡看到的選擇器寫法一樣：
# - `li.book`：標籤加 class
# - `#books`：id
# - `ul#books li`：ul 裡面的所有 li（空格代表「裡面」）
#
# `select` 回傳全部，`select_one` 回傳第一個（找不到是 `None`）。

# %%
print("select 全部：", [li.get_text() for li in small_soup.select("ul#books li")])
print("select_one：", small_soup.select_one("li.sale").get_text())
print("同時有 book 與 sale：", small_soup.select("li.book.sale"))

# %% [markdown]
# ## 09｜回到真正的網頁：找一則名言
#
# 每則名言是 `div.quote`；裡面有 `span.text`（名言）、`small.author`（作者）、多個 `a.tag`（標籤）。

# %%
quotes = soup.select("div.quote")
print("這一頁的名言數量：", len(quotes))

first = quotes[0]
print("名言：", first.select_one("span.text").get_text())
print("作者：", first.select_one("small.author").get_text())
print("標籤：", [tag.get_text() for tag in first.select("a.tag")])

# %% [markdown]
# ## 10｜一則名言 → 一個 dict
#
# 名言文字前後有彎引號 “ ”，用 `strip("“”")` 去掉。
# 作者連結是相對網址，下一堂會學怎麼組成完整網址。

# %%
def quote_to_dict(quote):
    return {
        "text": quote.select_one("span.text").get_text(strip=True).strip("“”"),
        "author": quote.select_one("small.author").get_text(strip=True),
        "tags": [tag.get_text(strip=True) for tag in quote.select("a.tag")],
        "author_url": quote.select_one("a")["href"],
    }


one = quote_to_dict(first)
print(one["author"], one["tags"], one["author_url"])

# %% [markdown]
# ## 11｜整頁 → list of dict

# %%
rows = [quote_to_dict(quote) for quote in soup.select("div.quote")]
print("筆數：", len(rows))
for row in rows[:3]:
    print(row["author"], "|", row["text"][:25], "...")

# %% [markdown]
# ## 12｜找不到時怎麼辦：先檢查再取值
#
# 網頁上的資料常常缺一塊。`find` 找不到會回傳 `None`，再 `.get_text()` 就會 `AttributeError`。

# %%
broken_html = '<div class="quote"><span class="text">只有名言，沒有作者</span></div>'
broken = BeautifulSoup(broken_html, "html.parser").select_one("div.quote")

author_tag = broken.select_one("small.author")
print("找到的作者元素：", author_tag)

try:
    print(author_tag.get_text())
except AttributeError as error:
    print("直接取值會出錯：", error)

# %%
def text_or_none(parent, selector):
    """找到元素就回傳文字，找不到回傳 None。"""
    tag = parent.select_one(selector)
    if tag is None:
        return None
    return tag.get_text(strip=True)


print("安全版：", text_or_none(broken, "small.author"))
print("有的欄位：", text_or_none(broken, "span.text"))

# %% [markdown]
# ## 13｜包成函式：parse_quotes(html)
#
# 輸入 HTML 字串，回傳 list of dict。之後換成任何一頁都能用。

# %%
def parse_quotes(html):
    page = BeautifulSoup(html, "html.parser")
    rows = []
    for quote in page.select("div.quote"):
        text = text_or_none(quote, "span.text")
        if text is not None:
            text = text.strip("“”")
        rows.append(
            {
                "text": text,
                "author": text_or_none(quote, "small.author"),
                "tags": [tag.get_text(strip=True) for tag in quote.select("a.tag")],
            }
        )
    return rows


rows = parse_quotes(html)
print("第一頁：", len(rows), "則")

love_html = Path("fixtures/quotes_tag_love.html").read_text(encoding="utf-8")
love_rows = parse_quotes(love_html)
print("love 標籤頁：", len(love_rows), "則，第一則作者：", love_rows[0]["author"])

# %% [markdown]
# ## 14｜搭配上一堂的 fetch：從網路抓再解析

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


response = fetch("https://quotes.toscrape.com/")
if response is None:
    print("沒有網路，改用本機快照")
    live_rows = rows
else:
    live_rows = parse_quotes(response.text)
print("解析到", len(live_rows), "則名言")

# %% [markdown]
# ## 15｜用 F12 找選擇器
#
# 1. 在網頁上對要的資料按右鍵，選「檢查」。
# 2. 在 Elements 裡對該元素按右鍵 → Copy → Copy selector。
# 3. 貼進 `select_one()` 試試看。複製下來的選擇器常常太長，可以簡化成 `small.author` 這種短的。
#
# 習慣：**先只解析一筆，確認對了，再跑全部。**

# %% [markdown]
# ## 16｜小結：整理成表格前的最後檢查

# %%
authors = [row["author"] for row in rows]
print("作者清單：", authors)
print("不重複的作者：", len(set(authors)))
print("有缺作者的筆數：", sum(1 for author in authors if author is None))
