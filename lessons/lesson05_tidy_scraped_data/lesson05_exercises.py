# %% [markdown]
# # Lesson 05 練習｜爬回來的資料整理
#
# 把每一格的 `None` 或 `# TODO` 補完，再按 Run Cell。
# 每題最後的 `assert` 是自我檢查：沒有出現錯誤、而且印出「完成」，就代表答對了。
# 這份練習只用本機的 `fixtures/`，不需要網路。
#
# - ⭐ Core：第 1–4 題
# - ⭐⭐ Practice：第 5–8 題
# - ⭐⭐⭐ Challenge：第 9–10 題
#
# 後面的題目會用到前面題目建立的 `df`，請依序完成。

# %% [markdown]
# ## 設定工作資料夾
#
# 不論從哪個資料夾執行這個檔案，下面用到的 `fixtures/`、`output/` 都以這個檔案所在的資料夾為基準。

# %%
import os
import re
from io import StringIO
from pathlib import Path

import pandas as pd

_this_file = globals().get("__vsc_ipynb_file__") or globals().get("__file__")
if _this_file:
    os.chdir(Path(_this_file).resolve().parent)

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# %% [markdown]
# ## ⭐ 第 1 題｜讀入並檢查
#
# 讀取 `fixtures/books_raw.csv`（編碼 `utf-8-sig`），存成 `df`。

# %%
# TODO: 請在這裡寫程式
df = None

assert df.shape == (1000, 5)
assert df.columns.tolist() == ["title", "price_text", "rating_word", "availability", "url"]
print("第 1 題完成：", df.shape)

# %% [markdown]
# ## ⭐ 第 2 題｜價格轉成數字
#
# 新增 `price` 欄：把 `price_text`（例如 `"£51.77"`）去掉 `£`，轉成 `float`。

# %%
# TODO: 請在這裡寫程式

assert df["price"].dtype == "float64"
assert round(df["price"].sum(), 2) == 35070.35
print("第 2 題完成：總價", round(df["price"].sum(), 2))

# %% [markdown]
# ## ⭐ 第 3 題｜評分轉成數字
#
# 新增 `rating` 欄：用 `RATING_WORDS` 把 `rating_word` 對照成 1–5。
# 再算出 5 星的書有幾本，存成 `five_star_count`。

# %%
# TODO: 請在這裡寫程式
five_star_count = None

assert df["rating"].isna().sum() == 0, "有對照失敗的評分"
assert five_star_count == 196
print("第 3 題完成：5 星有", five_star_count, "本")

# %% [markdown]
# ## ⭐ 第 4 題｜庫存欄位
#
# 新增布林欄 `in_stock`：`availability` 等於 `"In stock"` 就是 True。
# 把有庫存的書本數存成 `in_stock_count`。

# %%
# TODO: 請在這裡寫程式
in_stock_count = None

assert in_stock_count == 1000
print("第 4 題完成：有庫存", in_stock_count, "本")

# %% [markdown]
# ## ⭐⭐ 第 5 題｜篩選
#
# 找出價格超過 55 的書，把筆數存成 `expensive_count`。

# %%
# TODO: 請在這裡寫程式
expensive_count = None

assert expensive_count == 98
print("第 5 題完成：", expensive_count, "本")

# %% [markdown]
# ## ⭐⭐ 第 6 題｜最貴的三本
#
# 找出價格最高的三本書，把書名依價格由高到低存成 list `top3_titles`。

# %%
# TODO: 請在這裡寫程式
top3_titles = None

assert top3_titles == [
    "The Perfect Play (Play by Play #1)",
    "Last One Home (New Beginnings #1)",
    "Civilization and Its Discontents",
]
print("第 6 題完成：", top3_titles)

# %% [markdown]
# ## ⭐⭐ 第 7 題｜兩個條件
#
# 找出「5 星而且價格低於 15」的書：
# - 筆數存成 `cheap_five_count`
# - 其中價格最低那一本的書名存成 `cheapest_five_title`

# %%
# TODO: 請在這裡寫程式
cheap_five_count = None
cheapest_five_title = None

assert cheap_five_count == 23
assert cheapest_five_title == "An Abundance of Katherines"
print("第 7 題完成：", cheap_five_count, "本，最便宜", cheapest_five_title)

# %% [markdown]
# ## ⭐⭐ 第 8 題｜分組統計
#
# 算出每個評分的平均價格（四捨五入到小數第 2 位），存成 dict `mean_by_rating`，
# 格式像 `{1: 34.56, 2: 34.81, ...}`。

# %%
# TODO: 請在這裡寫程式
mean_by_rating = None

assert mean_by_rating == {1: 34.56, 2: 34.81, 3: 34.69, 4: 36.09, 5: 35.37}
print("第 8 題完成：", mean_by_rating)

# %% [markdown]
# ## ⭐⭐⭐ 第 9 題｜用 read_html 讀網頁的表格
#
# 讀取 `fixtures/book_detail.html`，用 `pd.read_html` 取得 Product Information 表格。
# - 把 UPC 的值存成 `upc`
# - 從 Availability 的文字（例如 `In stock (22 available)`）取出數字，存成整數 `available`

# %%
detail_html = Path("fixtures/book_detail.html").read_text(encoding="utf-8")

# TODO: 請在這裡寫程式
upc = None
available = None

assert upc == "a897fe39b1053632"
assert available == 22
print("第 9 題完成：", upc, available)

# %% [markdown]
# ## ⭐⭐⭐ 第 10 題｜每個評分最便宜的一本
#
# 做出排行榜 `best_deals`：每個評分（1–5）各取價格最低的一本，
# 欄位依序是 `rating`、`title`、`price`，依評分由高到低排列，並存成 `output/best_deals.csv`。
# 價格相同時用書名排序。

# %%
Path("output").mkdir(exist_ok=True)

# TODO: 請在這裡寫程式
best_deals = None

saved = pd.read_csv("output/best_deals.csv", encoding="utf-8-sig")
assert saved.columns.tolist() == ["rating", "title", "price"]
assert saved["rating"].tolist() == [5, 4, 3, 2, 1]
assert saved.loc[0, "title"] == "An Abundance of Katherines"
assert saved.loc[0, "price"] == 10.0
print("第 10 題完成：")
print(saved.to_string(index=False))
