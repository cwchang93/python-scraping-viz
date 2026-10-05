# %% [markdown]
# # Lesson 06 作業｜作者簡介、20 世紀的作者、交出乾淨的檔案
#
# 完成三題，並確認每題最後的 `assert` 沒有出現錯誤。

# %% [markdown]
# ## 設定工作資料夾
#
# 不論從哪個資料夾執行這個檔案，下面用到的 `fixtures/`、`output/` 都以這個檔案所在的資料夾為基準。

# %%
import os
from pathlib import Path

import pandas as pd

_this_file = globals().get("__vsc_ipynb_file__") or globals().get("__file__")
if _this_file:
    os.chdir(Path(_this_file).resolve().parent)

# 下面這段是課堂上清理好的結果，直接使用
quotes = pd.read_csv("fixtures/quotes_raw.csv", encoding="utf-8-sig")
authors = pd.read_csv("fixtures/authors_raw.csv", encoding="utf-8-sig")

quotes["text"] = quotes["text"].str.strip().str.strip("“”")
quotes["tags"] = quotes["tags_text"].str.split(",")
quotes["tag_count"] = quotes["tags"].str.len().fillna(0).astype(int)

authors["born_date"] = pd.to_datetime(authors["born_date_text"].str.strip(), format="%B %d, %Y", errors="coerce")
authors["born_year"] = authors["born_date"].dt.year
location = authors["born_location_text"].str.strip().str.replace(r"^in\s+", "", regex=True)
authors["country"] = location.str.split(",").str[-1].str.strip().str.replace(r"^The\s+", "", regex=True)

merged = quotes.merge(
    authors[["author_url", "born_year", "country"]], on="author_url", how="left", validate="many_to_one"
)

# %% [markdown]
# ## H1｜作者簡介的長度
#
# `authors["description"]` 前後有空白與換行。
# 1. 去掉前後空白（直接改寫 `description` 欄）。
# 2. 新增 `description_len`：簡介的字元數。
# 3. 簡介最長的作者名字存成 `longest_author`；最短的簡介長度存成 `shortest_len`。

# %%
# TODO: 請在這裡寫程式
longest_author = None
shortest_len = None

assert longest_author == "Albert Einstein"
assert shortest_len == 762
print("H1 完成：", longest_author, shortest_len)

# %% [markdown]
# ## H2｜20 世紀出生的作者
#
# 找出 `born_year` 介於 1900（含）到 1999（含）的作者：
# - 人數存成 `twentieth_count`
# - 其中作者最多的國家存成 `twentieth_top_country`

# %%
# TODO: 請在這裡寫程式
twentieth_count = None
twentieth_top_country = None

assert twentieth_count == 29
assert twentieth_top_country == "United States"
print("H2 完成：", twentieth_count, twentieth_top_country)

# %% [markdown]
# ## H3｜交出乾淨的檔案，並寫下清理決策
#
# 1. 從 `merged` 取出這些欄位（照順序）：`page`、`text`、`author`、`tags`、`tag_count`、`born_year`、`country`。
# 2. `tags` 是 list，存檔前先用 `str.join(",")` 轉回逗號字串。
# 3. 存成 `output/quotes_clean.csv`（`index=False`、`encoding="utf-8-sig"`）。
# 4. 把你做過的清理決策寫成 list `cleaning_log`，至少 4 條，每條說明「處理了什麼、為什麼」。

# %%
Path("output").mkdir(exist_ok=True)

# TODO: 請在這裡寫程式
cleaning_log = []

saved = pd.read_csv("output/quotes_clean.csv", encoding="utf-8-sig")
assert saved.columns.tolist() == ["page", "text", "author", "tags", "tag_count", "born_year", "country"]
assert len(saved) == 100
assert len(cleaning_log) >= 4, "至少寫 4 條清理決策"
print("H3 完成")
for number, decision in enumerate(cleaning_log, start=1):
    print(number, decision)
