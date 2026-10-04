# %% [markdown]
# # Lesson 03 練習｜BeautifulSoup（一）
#
# 把每一格的 `None` 或 `# TODO` 補完，再按 Run Cell。
# 每題最後的 `assert` 是自我檢查：沒有出現錯誤、而且印出「完成」，就代表答對了。
# 這份練習全部使用本機的 HTML，不需要網路。
#
# - ⭐ Core：第 1–4 題
# - ⭐⭐ Practice：第 5–8 題
# - ⭐⭐⭐ Challenge：第 9–10 題

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
from bs4 import BeautifulSoup

menu_html = """
<html>
  <head><title>咖啡店菜單</title></head>
  <body>
    <h1>今日飲品</h1>
    <ul id="menu">
      <li class="drink"><span class="name">拿鐵</span><span class="price">120</span></li>
      <li class="drink"><span class="name">美式</span><span class="price">80</span></li>
      <li class="drink hot"><span class="name">熱可可</span><span class="price">100</span></li>
    </ul>
    <a href="/order" class="btn">立即訂購</a>
  </body>
</html>
"""
menu = BeautifulSoup(menu_html, "html.parser")

# %% [markdown]
# ## ⭐ 第 1 題｜標題與 h1
#
# 從 `menu` 取出網頁標題（`<title>`）與第一個 `<h1>` 的文字。

# %%
# TODO: 請在這裡寫程式
title_text = None
h1_text = None

assert title_text == "咖啡店菜單"
assert h1_text == "今日飲品"
print("第 1 題完成：", title_text, "/", h1_text)

# %% [markdown]
# ## ⭐ 第 2 題｜find 與 find_all
#
# 1. 用 `find` 找第一個 `class="price"` 的 `span`，文字存成 `first_price`。
# 2. 用 `find_all` 找所有 `class="drink"` 的 `li`，數量存成 `drink_count`。

# %%
# TODO: 請在這裡寫程式
first_price = None
drink_count = None

assert first_price == "120"
assert drink_count == 3
print("第 2 題完成：", first_price, drink_count)

# %% [markdown]
# ## ⭐ 第 3 題｜所有飲品名稱
#
# 把所有 `span.name` 的文字收集成 list，存成 `names`。

# %%
# TODO: 請在這裡寫程式
names = None

assert names == ["拿鐵", "美式", "熱可可"]
print("第 3 題完成：", names)

# %% [markdown]
# ## ⭐ 第 4 題｜取屬性
#
# 1. 取出 `<a>` 的 `href`，存成 `order_href`。
# 2. 用 `.get()` 取出 `<a>` 的 `title` 屬性（它沒有這個屬性），存成 `order_title`。

# %%
# TODO: 請在這裡寫程式
order_href = None
order_title = "還沒填"

assert order_href == "/order"
assert order_title is None
print("第 4 題完成：", order_href, order_title)

# %% [markdown]
# ## ⭐⭐ 第 5 題｜select 與價格加總
#
# 1. 用 `select("span.price")` 取出所有價格，轉成整數 list，存成 `prices`。
# 2. 用 `select("li.hot span.name")` 找出熱飲名稱，存成 `hot_names`。

# %%
# TODO: 請在這裡寫程式
prices = None
hot_names = None

assert prices == [120, 80, 100]
assert sum(prices) == 300
assert hot_names == ["熱可可"]
print("第 5 題完成：總價", sum(prices), "，熱飲", hot_names)

# %% [markdown]
# ## ⭐⭐ 第 6 題｜讀名言網頁
#
# 讀取 `fixtures/quotes_page1.html` 建立 `soup`，數出有幾則名言（`div.quote`），
# 並取出第一則的作者（`small.author`）。

# %%
html = Path("fixtures/quotes_page1.html").read_text(encoding="utf-8")

# TODO: 請在這裡寫程式
soup = None
quote_count = None
first_author = None

assert quote_count == 10
assert first_author == "Albert Einstein"
print("第 6 題完成：", quote_count, "則，第一則作者", first_author)

# %% [markdown]
# ## ⭐⭐ 第 7 題｜誰的名言最多
#
# 1. 把這一頁所有作者收集成 list `authors`（10 筆）。
# 2. 用 dict 統計每位作者出現幾次，存成 `author_counts`。

# %%
# TODO: 請在這裡寫程式
authors = None
author_counts = {}

assert len(authors) == 10
assert len(author_counts) == 8
assert author_counts["Albert Einstein"] == 3
print("第 7 題完成：", author_counts)

# %% [markdown]
# ## ⭐⭐ 第 8 題｜標籤與下一頁
#
# 1. 取出第一則名言的所有標籤文字，存成 `first_tags`。
# 2. 用 `select_one("li.next a")` 找到「下一頁」連結，取出它的 `href`，存成 `next_href`。

# %%
# TODO: 請在這裡寫程式
first_tags = None
next_href = None

assert first_tags == ["change", "deep-thoughts", "thinking", "world"]
assert next_href == "/page/2/"
print("第 8 題完成：", first_tags, next_href)

# %% [markdown]
# ## ⭐⭐⭐ 第 9 題｜寫 parse_quotes(html)
#
# 寫函式 `parse_quotes(html)`，回傳 list of dict。每個 dict 有三個欄位：
# - `text`：名言文字（用 `strip("“”")` 去掉彎引號）
# - `author`：作者
# - `tags`：標籤 list

# %%
# TODO: 請在這裡寫程式
def parse_quotes(html):
    pass


rows = parse_quotes(html)
assert len(rows) == 10
assert set(rows[0]) == {"text", "author", "tags"}
assert rows[0]["text"].startswith("The world as we have created it")
assert rows[1]["author"] == "J.K. Rowling"
print("第 9 題完成：", len(rows), "筆")

# %% [markdown]
# ## ⭐⭐⭐ 第 10 題｜標籤最多的名言
#
# 用 `rows`（第 9 題的結果）找出標籤最多的那一則，
# 把它的作者存成 `most_tags_author`、標籤數量存成 `most_tags_count`。

# %%
# TODO: 請在這裡寫程式
most_tags_author = None
most_tags_count = None

assert most_tags_author == "Albert Einstein"
assert most_tags_count == 5
print("第 10 題完成：", most_tags_author, most_tags_count)
