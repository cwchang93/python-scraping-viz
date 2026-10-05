# %% [markdown]
# # Lesson 06 練習｜網頁資料清理
#
# 把每一格的 `None` 或 `# TODO` 補完，再按 Run Cell。
# 每題最後的 `assert` 是自我檢查：沒有出現錯誤、而且印出「完成」，就代表答對了。
# 這份練習只用本機的 `fixtures/`，不需要網路。
#
# - ⭐ Core：第 1–4 題
# - ⭐⭐ Practice：第 5–8 題
# - ⭐⭐⭐ Challenge：第 9–10 題
#
# 第 5 題起會用到前面題目建立的 `quotes`、`authors`，請依序完成。

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

# %% [markdown]
# ## ⭐ 第 1 題｜統一格式
#
# 下面的 `people` 名字有多餘空白、大小寫不一致。
# 把 `name` 整理成「去掉前後空白、每個字首字母大寫」，存成 `names_clean`（Series）。

# %%
people = pd.DataFrame(
    {
        "name": [" Amy ", "BEN", "ben", None],
        "age": ["30", "x", "25", None],
    }
)

# TODO: 請在這裡寫程式
names_clean = None

assert names_clean.dropna().tolist() == ["Amy", "Ben", "Ben"]
print("第 1 題完成：", names_clean.dropna().tolist())

# %% [markdown]
# ## ⭐ 第 2 題｜轉成數字，讓問題看得見
#
# 把 `age` 轉成數字（轉不了的變成缺值），存成 `age_num`，
# 再算出缺值有幾個，存成 `age_missing`。

# %%
# TODO: 請在這裡寫程式
age_num = None
age_missing = None

assert age_missing == 2
assert age_num.dropna().tolist() == [30.0, 25.0]
print("第 2 題完成：缺值", age_missing, "個")

# %% [markdown]
# ## ⭐ 第 3 題｜先統一，再找重複
#
# 用第 1 題的 `names_clean`（先去掉缺值），算出有幾個名字是重複的（第二次以後出現的），存成 `dup_count`。

# %%
# TODO: 請在這裡寫程式
dup_count = None

assert dup_count == 1
print("第 3 題完成：重複", dup_count, "個")

# %% [markdown]
# ## ⭐ 第 4 題｜載入真實資料
#
# 讀取 `fixtures/quotes_raw.csv` 存成 `quotes`、`fixtures/authors_raw.csv` 存成 `authors`（編碼 `utf-8-sig`）。
# 再算出名言表的 `tags_text` 有幾個缺值，存成 `missing_tags`。

# %%
# TODO: 請在這裡寫程式
quotes = None
authors = None
missing_tags = None

assert quotes.shape == (100, 5)
assert authors.shape == (50, 5)
assert missing_tags == 3
print("第 4 題完成：", quotes.shape, authors.shape, "，沒有標籤", missing_tags, "則")

# %% [markdown]
# ## ⭐⭐ 第 5 題｜去掉引號
#
# 清理 `quotes["text"]`：去掉前後空白與彎引號 `“ ”`（直接改寫 `text` 欄）。

# %%
# TODO: 請在這裡寫程式

assert quotes["text"].str.contains("[“”]").sum() == 0
assert quotes["text"].iloc[0].startswith("The world as we have created it")
print("第 5 題完成：", quotes["text"].iloc[0][:40], "...")

# %% [markdown]
# ## ⭐⭐ 第 6 題｜標籤數量
#
# 1. 新增 `tags` 欄：把 `tags_text` 用逗號切成 list（缺值維持缺值）。
# 2. 新增 `tag_count` 欄：每則名言的標籤數量（整數）；**沒有標籤的算 0**。

# %%
# TODO: 請在這裡寫程式

assert quotes["tag_count"].dtype.kind == "i", "tag_count 要是整數"
assert (quotes["tag_count"] == 0).sum() == 3
assert quotes["tag_count"].max() == 8
print("第 6 題完成：最多", quotes["tag_count"].max(), "個標籤")

# %% [markdown]
# ## ⭐⭐ 第 7 題｜展開標籤，找出最熱門
#
# 把 `tags` 展開成「一個標籤一列」的表 `tags_long`（欄位 `text`、`tag`，沒有標籤的名言不要產生列），
# 再找出出現最多次的標籤，存成 `top_tag`。

# %%
# TODO: 請在這裡寫程式
tags_long = None
top_tag = None

assert len(tags_long) == 232
assert top_tag == "love"
print("第 7 題完成：", len(tags_long), "列，最熱門的標籤", top_tag)

# %% [markdown]
# ## ⭐⭐ 第 8 題｜日期
#
# 把 `authors["born_date_text"]`（例如 `March 14, 1879`）轉成日期，存成新欄 `born_date`；
# 再新增 `born_year`（年份）。解析失敗要變成缺值，不要讓程式出錯。
# 算出解析失敗的筆數存成 `bad_dates`，最早出生的作者名字存成 `oldest_name`。

# %%
# TODO: 請在這裡寫程式
bad_dates = None
oldest_name = None

assert bad_dates == 0
assert authors["born_year"].min() == 1775
assert oldest_name == "Jane Austen"
print("第 8 題完成：", oldest_name, authors["born_year"].min())

# %% [markdown]
# ## ⭐⭐⭐ 第 9 題｜從出生地切出國家
#
# `born_location_text` 長得像 `in Yate, South Gloucestershire, England, The United Kingdom`。
# 新增 `country` 欄：去掉開頭的 `in `，取最後一段逗號後的文字，並去掉開頭的 `The `
# （`The United Kingdom` → `United Kingdom`）。
# 算出不重複的國家有幾個，存成 `country_count`；作者最多的國家存成 `top_country`。

# %%
# TODO: 請在這裡寫程式
country_count = None
top_country = None

assert country_count == 14
assert top_country == "United States"
print("第 9 題完成：", country_count, "個國家，最多的是", top_country)

# %% [markdown]
# ## ⭐⭐⭐ 第 10 題｜合併兩張表並驗證
#
# 用 `author_url` 把 `quotes` 與 `authors[["author_url", "born_year", "country"]]` 合併成 `merged`
# （保留所有名言，並用 `validate="many_to_one"` 確認對應關係）。
# 然後算出：
# - `unmatched`：沒對應到作者的名言數量
# - `uk_quotes`：作者來自 United Kingdom 的名言數量

# %%
# TODO: 請在這裡寫程式
merged = None
unmatched = None
uk_quotes = None

assert merged.shape == (100, 9)
assert unmatched == 0
assert uk_quotes == 21
print("第 10 題完成：", merged.shape, "，英國作者的名言", uk_quotes, "則")
