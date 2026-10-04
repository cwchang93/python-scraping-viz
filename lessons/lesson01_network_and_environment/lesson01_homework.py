# %% [markdown]
# # Lesson 01 作業｜抓一頁、看一頁、寫下規則
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

# %% [markdown]
# ## H1｜抓名言網站的第 2 頁
#
# 網址：`https://quotes.toscrape.com/page/2/`
#
# 1. 用自訂的 User-Agent 抓回網頁。
# 2. 存成 `output/quotes_page2.html`。
# 3. 數出這一頁有幾則名言，存成 `page2_quote_count`。

# %%
from pathlib import Path

import requests

my_headers = {"User-Agent": "my-class-bot/0.1 (student project)"}
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# TODO: 請在這裡寫程式
page2_quote_count = None

assert Path("output/quotes_page2.html").exists(), "要先存成 output/quotes_page2.html"
assert page2_quote_count == 10
print("H1 完成：第 2 頁有", page2_quote_count, "則名言")

# %% [markdown]
# ## H2｜用 F12 觀察書店首頁
#
# 1. 用 Chrome 打開 `https://books.toscrape.com/`，按 F12，切到 Network，重新整理。
# 2. 點第一筆 request，把你看到的值填進 `observation`。

# %%
# TODO: 把 None 換成你在 Network 看到的值
observation = {
    "request_url": None,
    "method": None,
    "status_code": None,
    "content_type": None,
}

assert all(value is not None for value in observation.values()), "四個欄位都要填"
assert observation["method"] == "GET"
assert observation["status_code"] == 200
print("H2 完成：", observation)

# %% [markdown]
# ## H3｜寫下你的爬取守則
#
# 用自己的話寫出三條你會遵守的規則，再寫一件你絕對不會爬的資料。

# %%
# TODO: 請在這裡填寫
my_rules = []
never_scrape = ""

assert len(my_rules) == 3, "要寫三條規則"
assert never_scrape.strip() != "", "要寫一件不會爬的資料"
print("H3 完成")
for number, rule in enumerate(my_rules, start=1):
    print(number, rule)
print("我不會爬：", never_scrape)
