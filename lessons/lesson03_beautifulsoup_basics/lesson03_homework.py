# %% [markdown]
# # Lesson 03 作業｜解析標籤頁、處理缺值、找下一頁
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
from bs4 import BeautifulSoup


def text_or_none(parent, selector):
    tag = parent.select_one(selector)
    if tag is None:
        return None
    return tag.get_text(strip=True)


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


# %% [markdown]
# ## H1｜解析 love 標籤頁
#
# 讀取 `fixtures/quotes_tag_love.html`，用上面的 `parse_quotes` 解析：
# - 名言數量存成 `love_count`
# - 所有作者存成 `love_authors`（list）

# %%
love_html = Path("fixtures/quotes_tag_love.html").read_text(encoding="utf-8")

# TODO: 請在這裡寫程式
love_count = None
love_authors = None

assert love_count == 10
assert love_authors[0] == "André Gide"
print("H1 完成：", love_count, love_authors[:3])

# %% [markdown]
# ## H2｜缺值保護
#
# 下面這則名言沒有作者。用 `text_or_none` 取作者與名言文字，
# 分別存成 `broken_author`、`broken_text`，程式不可以出錯。

# %%
broken = BeautifulSoup(
    '<div class="quote"><span class="text">只有名言</span></div>', "html.parser"
).select_one("div.quote")

# TODO: 請在這裡寫程式
broken_author = "還沒填"
broken_text = None

assert broken_author is None
assert broken_text == "只有名言"
print("H2 完成")

# %% [markdown]
# ## H3｜找下一頁
#
# 在 love 標籤頁裡，找出「下一頁」連結的 `href`，存成 `love_next_href`。
# 提示：F12 看一下按鈕的結構，再寫選擇器。

# %%
# TODO: 請在這裡寫程式
love_next_href = None

assert love_next_href == "/tag/love/page/2/"
print("H3 完成：", love_next_href)
