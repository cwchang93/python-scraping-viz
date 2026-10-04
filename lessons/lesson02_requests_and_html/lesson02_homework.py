# %% [markdown]
# # Lesson 02 作業｜讓 fetch 更可靠
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
import time

import requests

USER_AGENT = "my-class-bot/0.1 (student project)"


def fetch(url, params=None):
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"抓取失敗：{url} → {type(error).__name__}")
        return None
    return response


# %% [markdown]
# ## H1｜失敗時重試
#
# 寫 `fetch_with_retry(url, retries=2, delay=0.5)`：
# - 用上面的 `fetch` 抓，成功就立刻回傳
# - 失敗就印出「第 N 次失敗」，還有機會就 `time.sleep(delay)` 再試
# - 全部失敗回傳 `None`

# %%
# TODO: 請在這裡寫程式
def fetch_with_retry(url, retries=2, delay=0.5):
    pass


started = time.time()
assert fetch_with_retry("https://quotes.toscrape.com/no-such-page", retries=2, delay=0.5) is None
assert time.time() - started >= 0.5, "失敗之後要先 sleep 再重試"
assert fetch_with_retry("https://quotes.toscrape.com/") is not None
print("H1 完成")

# %% [markdown]
# ## H2｜有沒有下一頁
#
# 抓 `https://books.toscrape.com/catalogue/page-2.html`，
# 判斷網頁裡有沒有 `class="next"`（下一頁按鈕），把結果（True 或 False）存成 `has_next`。

# %%
# TODO: 請在這裡寫程式
has_next = None

assert has_next is True
print("H2 完成：有下一頁 =", has_next)

# %% [markdown]
# ## H3｜遇到 403 怎麼辦
#
# 用一兩句話寫下：如果你的爬蟲遇到 403，你會怎麼做？哪一件事你不會做？

# %%
# TODO: 請在這裡填寫
what_i_would_do = ""

assert len(what_i_would_do) >= 10, "至少寫 10 個字"
print("H3 完成")
print(what_i_would_do)
