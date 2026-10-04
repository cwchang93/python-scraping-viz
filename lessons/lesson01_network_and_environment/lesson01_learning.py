# %% [markdown]
# # Lesson 01｜網路原理、爬蟲倫理與環境
#
# 今天先搞懂「瀏覽器怎麼拿到網頁」，再用 Python 做同樣的事。
# 在 VS Code 按每格上方的 Run Cell 逐格執行。沒有網路時，直接跳到最後一格。

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
# 先看結果，再拆解程式：用 Python 抓回一個網頁。

# %%
import requests

url = "https://quotes.toscrape.com/"
response = requests.get(url, timeout=10)
print("狀態碼：", response.status_code)
print("網頁長度：", len(response.text), "個字元")

# %% [markdown]
# ## 02｜瀏覽器打開網頁的五個步驟
#
# 爬蟲做的事，就是自己完成第 3、4 步，不需要第 5 步的畫面。

# %%
steps = [
    "輸入網址 URL",
    "用主機名稱找到伺服器的位置（DNS）",
    "送出 HTTP 請求 request",
    "收到 HTTP 回應 response（內容是 HTML）",
    "瀏覽器把 HTML 畫成畫面",
]
for number, step in enumerate(steps, start=1):
    print(number, step)

# %% [markdown]
# ## 03｜URL 的組成
#
# 同一個網站的不同頁面，差別通常就在 path 與 query。

# %%
from urllib.parse import parse_qs, urlparse

example_url = "https://quotes.toscrape.com/tag/love/page/2/?sort=new"
parts = urlparse(example_url)
print("通訊協定 scheme：", parts.scheme)
print("主機 host：", parts.netloc)
print("路徑 path：", parts.path)
print("查詢 query：", parts.query)
print("query 轉成字典：", parse_qs(parts.query))

# %% [markdown]
# ## 04｜常見的 HTTP 狀態碼
#
# 爬蟲每次請求後，第一件事就是看狀態碼。

# %%
status_meaning = {
    200: "成功",
    301: "網址搬家了（重新導向）",
    403: "被拒絕：沒有權限，或被網站擋下",
    404: "找不到頁面",
    429: "請求太頻繁",
    500: "網站伺服器出錯",
}
for code in [200, 404, 403]:
    print(code, status_meaning.get(code, "不認識的狀態碼"))

# %% [markdown]
# ## 05｜用 F12 看瀏覽器做了什麼（課堂操作，無程式）
#
# 1. 用 Chrome 打開 https://quotes.toscrape.com/ ，按 F12。
# 2. 切到 **Network**，按 Ctrl+R（Mac 是 Cmd+R）重新整理。
# 3. 點第一筆 request，看 Headers：Request URL、Request Method、Status Code。
# 4. 切到 **Elements**，把滑鼠移到網頁上的一則名言，看對應的 HTML。

# %% [markdown]
# ## 06｜環境檢查
#
# 建立虛擬環境並安裝套件（在終端機執行，不是在這一格）：
#
# ```bash
# python -m venv .venv
# source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
# python -m pip install -r requirements.txt
# ```

# %%
import sys

print("Python 版本：", sys.version.split()[0])
print("Python 位置：", sys.executable)
print("requests 版本：", requests.__version__)

# %% [markdown]
# ## 07｜Response 物件的重點欄位

# %%
print(response)
print("status_code：", response.status_code)
print("ok：", response.ok)
print("Content-Type：", response.headers["Content-Type"])
print("encoding：", response.encoding)
print("最終網址：", response.url)

# %% [markdown]
# ## 08｜看看 HTML 長什麼樣子

# %%
html = response.text
print(html[:300])

# %% [markdown]
# ## 09｜先用字串工具找內容
#
# 能找，但很不方便。這就是第 3 堂要學 BeautifulSoup 的原因。

# %%
print("有沒有 <title>：", "<title>" in html)
print("頁面上的名言數量：", html.count('class="quote"'))

start = html.find('<span class="text"')
print(html[start : start + 150])

# %% [markdown]
# ## 10｜把網頁存成檔案
#
# `response.text` 是已解碼的文字，`response.content` 是原始 bytes。
# 要原樣保存整個網頁，存 `content`。

# %%
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
save_path = output_dir / "quotes_page1.html"
save_path.write_bytes(response.content)
print("已存檔：", save_path, "，大小：", save_path.stat().st_size, "bytes")

# %% [markdown]
# ## 11｜讀回本機檔案

# %%
saved_html = save_path.read_text(encoding="utf-8")
print("讀回的名言數量：", saved_html.count('class="quote"'))

# %% [markdown]
# ## 12｜找不到頁面：404 與 raise_for_status

# %%
bad_response = requests.get("https://quotes.toscrape.com/no-such-page", timeout=10)
print("狀態碼：", bad_response.status_code, "，ok：", bad_response.ok)

try:
    bad_response.raise_for_status()
except requests.HTTPError as error:
    print("捕捉到 HTTPError：", error)

# %% [markdown]
# ## 13｜robots.txt：網站寫給爬蟲看的規則
#
# 這裡用一段自己寫的內容示範，結果每次都一樣。

# %%
from urllib.robotparser import RobotFileParser

robots_text = """User-agent: *
Disallow: /admin/
Disallow: /search
Allow: /
"""
parser = RobotFileParser()
parser.parse(robots_text.splitlines())

for path in ["/", "/admin/users", "/search?q=python"]:
    print(path, "可以抓嗎？", parser.can_fetch("*", path))

# %% [markdown]
# ## 14｜表明身分：User-Agent

# %%
print("預設送出的 User-Agent：", response.request.headers["User-Agent"])

my_headers = {"User-Agent": "python-scraping-viz-class/0.1 (student project)"}
polite_response = requests.get(url, headers=my_headers, timeout=10)
print("自訂後送出的 User-Agent：", polite_response.request.headers["User-Agent"])

# %% [markdown]
# ## 15｜爬取守則

# %%
rules = [
    "先看網站有沒有開放資料或 API，再考慮爬網頁",
    "看 robots.txt 與服務條款，不確定就不要抓",
    "設定 timeout，連續請求之間加 time.sleep",
    "只抓分析需要的欄位，不公開轉載別人的內文",
    "被擋（403、429）就停下來，不要想辦法繞過",
]
for number, rule in enumerate(rules, start=1):
    print(number, rule)

# %% [markdown]
# ## 16｜小結：抓取、檢查、存檔

# %%
import time

book_url = "https://books.toscrape.com/"
book_response = requests.get(book_url, headers=my_headers, timeout=10)

if book_response.ok:
    book_path = output_dir / "books_index.html"
    book_path.write_bytes(book_response.content)
    print("已存檔：", book_path, "，共", len(book_response.content), "bytes")
else:
    print("失敗，狀態碼：", book_response.status_code)

time.sleep(1)

# %% [markdown]
# ## 17｜沒網路也能上課
#
# `fixtures/` 裡有事先存好的網頁，讀它就能繼續練習。

# %%
fixture_html = Path("fixtures/quotes_page1.html").read_text(encoding="utf-8")
print("本機快照的名言數量：", fixture_html.count('class="quote"'))
