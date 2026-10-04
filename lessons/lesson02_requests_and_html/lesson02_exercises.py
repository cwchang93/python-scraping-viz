# %% [markdown]
# # Lesson 02 練習｜requests 與 HTML 結構
#
# 把每一格的 `None` 或 `# TODO` 補完，再按 Run Cell。
# 每題最後的 `assert` 是自我檢查：沒有出現錯誤、而且印出「完成」，就代表答對了。
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
import time
from pathlib import Path

import requests

USER_AGENT = "my-class-bot/0.1 (student project)"

# %% [markdown]
# ## ⭐ 第 1 題｜讀 HTML
#
# 看下面這段 HTML，填入答案。

# %%
snippet = """
<article class="product_pod">
  <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in ...</a></h3>
  <p class="price_color">£51.77</p>
</article>
"""

# TODO: 請在這裡填入答案（用字串）
outer_class = None  # <article> 的 class 屬性值
link_href = None  # <a> 的 href 屬性值
price_text = None  # 價格文字（含貨幣符號）

assert outer_class == "product_pod"
assert link_href == "catalogue/a-light-in-the-attic_1000/index.html"
assert price_text == "£51.77"
print("第 1 題完成")

# %% [markdown]
# ## ⭐ 第 2 題｜用 params 組網址
#
# 用 `requests.Request("GET", base_url, params=...).prepare().url` 組出網址，存成 `built_url`。
# 參數是 `q=scraping` 與 `page=3`（照這個順序）。

# %%
base_url = "https://example.com/search"

# TODO: 請在這裡寫程式
built_url = None

assert built_url == "https://example.com/search?q=scraping&page=3"
print("第 2 題完成：", built_url)

# %% [markdown]
# ## ⭐ 第 3 題｜接住 timeout
#
# 對 `https://quotes.toscrape.com/` 送出 `timeout=0.001` 的請求，
# 用 `except requests.RequestException as error` 接住，把錯誤類別名稱存成 `error_name`。
# （提示：`type(error).__name__`）

# %%
error_name = None

# TODO: 請在這裡寫程式

assert error_name is not None and "Timeout" in error_name or error_name == "ConnectionError"
print("第 3 題完成：", error_name)

# %% [markdown]
# ## ⭐ 第 4 題｜解碼 big5
#
# `raw` 是用 big5 編碼的 bytes。還原成正確的文字，存成 `fixed_text`。

# %%
raw = "資料視覺化".encode("big5")

# TODO: 請在這裡寫程式
fixed_text = None

assert fixed_text == "資料視覺化"
print("第 4 題完成：", fixed_text)

# %% [markdown]
# ## ⭐⭐ 第 5 題｜看轉址
#
# 抓 `https://quotes.toscrape.com/tag/love`（結尾沒有斜線），
# 把經過的轉址次數存成 `redirect_count`。

# %%
# TODO: 請在這裡寫程式
redirect_count = None

assert redirect_count is not None and redirect_count >= 0
print("第 5 題完成：經過", redirect_count, "次轉址")

# %% [markdown]
# ## ⭐⭐ 第 6 題｜寫 fetch(url)
#
# 寫函式 `fetch(url)`：
# - 帶上 `USER_AGENT`，`timeout=10`
# - 用 `raise_for_status()` 檢查
# - 失敗時印出「抓取失敗」並回傳 `None`；成功回傳 Response

# %%
# TODO: 請在這裡寫程式
def fetch(url):
    pass


assert fetch("https://quotes.toscrape.com/") is not None
assert fetch("https://quotes.toscrape.com/no-such-page") is None
print("第 6 題完成")

# %% [markdown]
# ## ⭐⭐ 第 7 題｜讓 fetch 支援 params
#
# 改寫 `fetch`，多一個參數 `params=None`，並傳給 `requests.get`。

# %%
# TODO: 請在這裡改寫
def fetch(url, params=None):
    pass


page = fetch("https://quotes.toscrape.com/", params={"page": 1})
assert page is not None and page.url.endswith("?page=1")
print("第 7 題完成：", page.url)

# %% [markdown]
# ## ⭐⭐ 第 8 題｜只要文字
#
# 寫 `fetch_text(url)`：抓成功就回傳網頁文字（`.text`），失敗回傳空字串 `""`。
# 要用到上一題的 `fetch`。

# %%
# TODO: 請在這裡寫程式
def fetch_text(url):
    pass


assert "Quotes to Scrape" in fetch_text("https://quotes.toscrape.com/")
assert fetch_text("https://quotes.toscrape.com/no-such-page") == ""
print("第 8 題完成")

# %% [markdown]
# ## ⭐⭐⭐ 第 9 題｜一次抓多頁
#
# 寫 `fetch_many(urls, delay=1)`：依序抓每個網址，回傳字典 `{網址: 狀態碼 或 None}`。
# - 抓成功的狀態碼用 `response.status_code`，失敗存 `None`
# - 每次請求之後 `time.sleep(delay)`

# %%
# TODO: 請在這裡寫程式
def fetch_many(urls, delay=1):
    pass


test_urls = [
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/no-such-page",
    "https://quotes.toscrape.com/page/2/",
]
started = time.time()
statuses = fetch_many(test_urls, delay=1)
elapsed = time.time() - started

assert statuses[test_urls[0]] == 200
assert statuses[test_urls[1]] is None
assert statuses[test_urls[2]] == 200
assert elapsed >= 2.5, "每次請求之間要有 time.sleep(delay)"
print("第 9 題完成：", statuses)

# %% [markdown]
# ## ⭐⭐⭐ 第 10 題｜抓了就存
#
# 寫 `save_page(url, path)`：用 `fetch` 抓網頁，成功就把 `response.content` 存到 `path` 並回傳 `True`，失敗回傳 `False`。

# %%
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)


# TODO: 請在這裡寫程式
def save_page(url, path):
    pass


target = output_dir / "exercise_page2.html"
assert save_page("https://quotes.toscrape.com/page/2/", target) is True
assert target.exists() and target.stat().st_size > 1000
assert save_page("https://quotes.toscrape.com/no-such-page", output_dir / "nope.html") is False
assert not (output_dir / "nope.html").exists()
print("第 10 題完成")
