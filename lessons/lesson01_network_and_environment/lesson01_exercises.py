# %% [markdown]
# # Lesson 01 練習｜網路原理、爬蟲倫理與環境
#
# 把每一格的 `None` 或 `# TODO` 補完，再按 Run Cell。
# 每題最後的 `assert` 是自我檢查：沒有出現錯誤、而且印出「完成」，就代表答對了。
#
# - ⭐ Core：第 1–5 題
# - ⭐⭐ Practice：第 6–10 題
# - ⭐⭐⭐ Challenge：第 11–12 題

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
# ## ⭐ 第 1 題｜拆開網址
#
# 用 `urlparse` 取出 `book_url` 的主機（host）與路徑（path）。

# %%
from urllib.parse import urlparse

book_url = "https://books.toscrape.com/catalogue/page-2.html"

# TODO: 請在這裡寫程式
host = None
path = None

assert host == "books.toscrape.com", "host 不對，提示：urlparse(...).netloc"
assert path == "/catalogue/page-2.html", "path 不對，提示：urlparse(...).path"
print("第 1 題完成：host =", host, "，path =", path)

# %% [markdown]
# ## ⭐ 第 2 題｜狀態碼說明
#
# 用 `.get()` 查詢字典。404 要得到「找不到頁面」；字典裡沒有的 418，要得到「不認識的狀態碼」。

# %%
status_meaning = {200: "成功", 403: "被拒絕", 404: "找不到頁面", 500: "伺服器出錯"}

# TODO: 請在這裡寫程式
meaning_404 = None
meaning_418 = None

assert meaning_404 == "找不到頁面"
assert meaning_418 == "不認識的狀態碼", "提示：.get(418, 預設文字)"
print("第 2 題完成")

# %% [markdown]
# ## ⭐ 第 3 題｜抓回第一個網頁
#
# 用 `requests.get` 抓 `https://quotes.toscrape.com/`，記得加 `timeout=10`。

# %%
import requests

quotes_url = "https://quotes.toscrape.com/"

# TODO: 請在這裡寫程式
response = None

assert response is not None and response.status_code == 200, "狀態碼要是 200"
print("第 3 題完成：狀態碼 =", response.status_code)

# %% [markdown]
# ## ⭐ 第 4 題｜看 headers
#
# 取出回應的 `Content-Type`，存成 `content_type`。

# %%
# TODO: 請在這裡寫程式
content_type = None

assert content_type is not None and "text/html" in content_type
print("第 4 題完成：Content-Type =", content_type)

# %% [markdown]
# ## ⭐ 第 5 題｜取得 HTML 文字
#
# 把網頁文字存成 `html`，並印出前 100 個字元。

# %%
# TODO: 請在這裡寫程式
html = None

assert isinstance(html, str) and html.lstrip().startswith("<!DOCTYPE html>")
print("第 5 題完成，前 100 字：")
print(html[:100])

# %% [markdown]
# ## ⭐⭐ 第 6 題｜數名言
#
# 網頁上每則名言都有 `class="quote"`。算出 `html` 裡出現幾次，存成 `quote_count`。

# %%
# TODO: 請在這裡寫程式
quote_count = None

assert quote_count == 10
print("第 6 題完成：這一頁有", quote_count, "則名言")

# %% [markdown]
# ## ⭐⭐ 第 7 題｜存檔再讀回
#
# 把 `response.content` 存成 `output/exercise_quotes.html`，再用 `read_bytes()` 讀回來確認內容相同。

# %%
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
saved_path = output_dir / "exercise_quotes.html"

# TODO: 請在這裡寫程式（先 write_bytes，再 read_bytes）
saved_bytes = None

assert saved_bytes == response.content, "讀回的內容要和 response.content 相同"
print("第 7 題完成：已存檔", saved_path)

# %% [markdown]
# ## ⭐⭐ 第 8 題｜處理 404
#
# 抓 `https://quotes.toscrape.com/no-such-page`，用 `try / except requests.HTTPError` 捕捉 `raise_for_status()` 的錯誤。
# 在 `except` 裡把 `caught` 改成 `True`。

# %%
missing_url = "https://quotes.toscrape.com/no-such-page"
caught = False

# TODO: 請在這裡寫程式

assert caught is True, "要在 except 區塊裡把 caught 設成 True"
print("第 8 題完成：成功捕捉到 HTTPError")

# %% [markdown]
# ## ⭐⭐ 第 9 題｜robots.txt
#
# 用 `RobotFileParser` 解析下面這段 robots 規則，判斷三個路徑能不能抓，結果存進字典 `allowed`。

# %%
from urllib.robotparser import RobotFileParser

robots_text = """User-agent: *
Disallow: /private/
Disallow: /tmp
Allow: /
"""
paths = ["/", "/private/data", "/blog/"]

# TODO: 請在這裡寫程式，allowed 的格式：{"/": True, ...}
allowed = {}

assert allowed == {"/": True, "/private/data": False, "/blog/": True}
print("第 9 題完成：", allowed)

# %% [markdown]
# ## ⭐⭐ 第 10 題｜自訂 User-Agent
#
# 用 `headers` 帶上 `my_headers` 再抓一次首頁，並把實際送出的 User-Agent 存成 `sent_user_agent`。

# %%
my_headers = {"User-Agent": "my-class-bot/0.1 (student project)"}

# TODO: 請在這裡寫程式
sent_user_agent = None

assert sent_user_agent == "my-class-bot/0.1 (student project)"
print("第 10 題完成：", sent_user_agent)

# %% [markdown]
# ## ⭐⭐⭐ 第 11 題｜書店首頁有幾本書
#
# 抓 `https://books.toscrape.com/`，數出 `<article class="product_pod">` 出現幾次，存成 `book_count`。
# 比較名言頁（10 則）與書店頁的數量。

# %%
import time

time.sleep(1)  # 連續請求之間先停一下

# TODO: 請在這裡寫程式
book_count = None

assert book_count == 20
print("第 11 題完成：名言頁", quote_count, "則，書店頁", book_count, "本")

# %% [markdown]
# ## ⭐⭐⭐ 第 12 題｜一次抓兩頁並存檔
#
# 用 `for` 迴圈走訪 `targets`：每一頁都要
# 1. 用 `my_headers` 抓回網頁
# 2. 狀態碼是 200 才存成 `output/<名字>.html`
# 3. 把檔案大小（bytes）記在字典 `sizes`
# 4. 每次請求之間 `time.sleep(1)`

# %%
targets = {
    "quotes": "https://quotes.toscrape.com/",
    "books": "https://books.toscrape.com/",
}
sizes = {}

# TODO: 請在這裡寫程式

assert set(sizes) == {"quotes", "books"}
assert all(size > 1000 for size in sizes.values())
print("第 12 題完成：", sizes)
