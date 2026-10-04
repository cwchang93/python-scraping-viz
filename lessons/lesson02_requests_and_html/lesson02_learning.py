# %% [markdown]
# # Lesson 02｜requests 與 HTML 結構
#
# 上一堂我們用三行程式抓回一頁。今天要把它變成可靠的工具：
# 看懂 HTML 的結構、控制請求、處理失敗，最後包成 `fetch(url)`。
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
# 先看結果：同一個函式，成功時拿到網頁，失敗時印出原因而不是讓程式當掉。

# %%
import requests


def preview_fetch(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print("抓取失敗：", type(error).__name__)
        return None
    return response


good = preview_fetch("https://quotes.toscrape.com/")
bad = preview_fetch("https://quotes.toscrape.com/no-such-page")
print("成功的那個：", good)
print("失敗的那個：", bad)

# %% [markdown]
# ## 02｜HTML 長什麼樣子
#
# HTML 由「標籤 tag」組成，標籤可以有「屬性」，標籤裡面可以再放標籤，形成一棵樹。
#
# ```
# <div class="quote">                      ← 標籤 div，屬性 class="quote"
#     <span class="text">名言內容</span>    ← 巢狀在 div 裡面
#     <a href="/author/Albert-Einstein">   ← 標籤 a，屬性 href 是連結位置
# </div>
# ```

# %%
snippet = """
<div class="quote">
  <span class="text">The world as we have created it is a process of our thinking.</span>
  <span>by <small class="author">Albert Einstein</small></span>
  <a href="/author/Albert-Einstein">(about)</a>
</div>
"""
print(snippet)

# %% [markdown]
# ## 03｜在真正的網頁裡找一則名言
#
# `fixtures/` 裡有存好的網頁，先用它看結構，不需要網路。

# %%
from pathlib import Path

html = Path("fixtures/quotes_tag_love.html").read_text(encoding="utf-8")
start = html.find('<div class="quote"')
end = html.find("</div>", html.find('class="tags"', start))
print(html[start : end + 6])

# %% [markdown]
# ## 04｜GET 參數：網址問號後面的東西
#
# 網址裡 `?` 後面的 `key=value` 是參數。用 `params=` 讓 requests 幫你組網址，不用自己拼字串。
# `Request(...).prepare()` 只組網址、不送出，可以安心檢查。

# %%
search = requests.Request(
    "GET",
    "https://example.com/search",
    params={"q": "python 爬蟲", "page": 2},
).prepare()
print("組出來的網址：", search.url)

# %%
response = requests.get("https://quotes.toscrape.com/", params={"page": 1}, timeout=10)
print("實際送出的網址：", response.url)
print("狀態碼：", response.status_code)

# %% [markdown]
# ## 05｜headers：請求附帶的說明
#
# headers 告訴網站「我是誰、想要什麼語言與格式」。上一堂用過 User-Agent。

# %%
USER_AGENT = "python-scraping-viz-class/0.1 (student project)"
headers = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}
response = requests.get("https://quotes.toscrape.com/", headers=headers, timeout=10)
print("送出的 User-Agent：", response.request.headers["User-Agent"])
print("送出的 Accept-Language：", response.request.headers["Accept-Language"])

# %% [markdown]
# ## 06｜狀態碼與重新導向
#
# 狀態碼分五類：2xx 成功、3xx 轉址、4xx 你的請求有問題、5xx 網站出問題。
# requests 預設會自動跟著轉址走，走過的路在 `response.history`。

# %%
redirected = requests.get("https://quotes.toscrape.com/tag/love", timeout=10)
print("最後的狀態碼：", redirected.status_code)
print("經過幾次轉址：", len(redirected.history))
for step in redirected.history:
    print("  轉址前：", step.status_code, step.url)
print("最後的網址：", redirected.url)

# %% [markdown]
# ## 07｜編碼：中文變亂碼的原因
#
# 網頁傳回來的是 bytes，必須用「正確的編碼」才能還原成文字。
# 台灣的老網站有些用 big5，用 utf-8 去讀就會亂碼。這裡用自己做的 bytes 示範。

# %%
data = "爬蟲很有趣".encode("big5")
print("原始 bytes：", data)
print("用 utf-8 讀（錯）：", data.decode("utf-8", errors="replace"))
print("用 big5 讀（對）：", data.decode("big5"))

# %%
response = requests.get("https://quotes.toscrape.com/", timeout=10)
print("伺服器宣告的 encoding：", response.encoding)
print("requests 猜測的 encoding：", response.apparent_encoding)
# 遇到亂碼時：response.encoding = "big5" 或 response.apparent_encoding，再讀 response.text

# %% [markdown]
# ## 08｜timeout 與例外：網路本來就會出狀況
#
# 沒有設定 timeout，請求可能永遠卡住。requests 的錯誤都繼承自 `requests.RequestException`，
# 用它一次接住所有狀況。

# %%
try:
    requests.get("https://quotes.toscrape.com/", timeout=0.001)
except requests.RequestException as error:
    print("錯誤種類：", type(error).__name__)
    print("說明：", error)

# %%
for url in [
    "https://quotes.toscrape.com/no-such-page",
    "https://this-domain-does-not-exist-abc123.example/",
]:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.HTTPError:
        print("HTTPError（網站回了錯誤狀態碼）：", url)
    except requests.ConnectionError:
        print("ConnectionError（連不上）：", url)

# %% [markdown]
# ## 09｜把它包成 fetch(url)
#
# 把「帶 User-Agent、設 timeout、檢查狀態碼、接住例外」打包成一個函式。
# 成功回傳 Response，失敗印出原因並回傳 `None`。

# %%
def fetch(url, params=None, timeout=10):
    """抓回網頁。成功回傳 Response，失敗印出原因並回傳 None。"""
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"抓取失敗：{url} → {type(error).__name__}")
        return None
    return response


ok_response = fetch("https://quotes.toscrape.com/")
missing_response = fetch("https://quotes.toscrape.com/no-such-page")
print("成功：", ok_response)
print("失敗：", missing_response)

# %% [markdown]
# ## 10｜呼叫端要記得檢查 None

# %%
page = fetch("https://quotes.toscrape.com/", params={"page": 1})
if page is None:
    print("沒抓到，這一頁先跳過")
else:
    print("抓到了，網頁長度：", len(page.text), "個字元")

# %% [markdown]
# ## 11｜連續抓多頁：要有禮貌
#
# 連續請求之間 `time.sleep`，網站才不會覺得你在攻擊它。

# %%
import time

urls = [
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/tag/love/",
    "https://quotes.toscrape.com/page/2/",
]
started = time.time()
for url in urls:
    result = fetch(url)
    if result is not None:
        print(result.status_code, url)
    time.sleep(1)
print(f"共花了 {time.time() - started:.1f} 秒")

# %% [markdown]
# ## 12｜存檔：抓完就存，之後解析不用再連網
#
# 這是爬蟲常用的習慣：把原始網頁存起來，解析的時候讀檔，改程式不用一直打擾網站。

# %%
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

page = fetch("https://quotes.toscrape.com/tag/love/")
if page is not None:
    saved = output_dir / "quotes_tag_love.html"
    saved.write_bytes(page.content)
    print("已存檔：", saved, "，", saved.stat().st_size, "bytes")

# %% [markdown]
# ## 13｜不是每個網站都讓你抓：403 案例
#
# 下面這一格會請求 Dcard 看板頁。**結果以當天為準**：我們檢查時它回 403，
# 代表網站明確拒絕這種請求。
#
# 遇到 403 該怎麼做？
# 1. 停下來，不要重試轟炸。
# 2. 看網站有沒有官方 API、開放資料或授權方式。
# 3. 看服務條款。沒有許可就換資料來源。
# 4. **不要**想辦法偽裝成瀏覽器去繞過防護。

# %%
dcard_response = fetch("https://www.dcard.tw/f")
if dcard_response is None:
    print("這個網站拒絕了我們的請求，換資料來源。")
else:
    print("這次抓到了，狀態碼：", dcard_response.status_code)

# %% [markdown]
# ## 14｜沒網路也能上課

# %%
fixture = Path("fixtures/books_page2.html").read_text(encoding="utf-8")
print("本機快照裡的書本數量：", fixture.count('<article class="product_pod">'))
print("有沒有下一頁連結：", 'class="next"' in fixture)
