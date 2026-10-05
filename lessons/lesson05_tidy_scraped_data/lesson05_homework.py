# %% [markdown]
# # Lesson 05 作業｜分區間、找同名的書、做排行榜
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

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

df = pd.read_csv("fixtures/books_raw.csv", encoding="utf-8-sig")
df["price"] = df["price_text"].str.replace("£", "", regex=False).astype(float)
df["rating"] = df["rating_word"].map(RATING_WORDS)
Path("output").mkdir(exist_ok=True)

# %% [markdown]
# ## H1｜價格區間
#
# 用 `pd.cut` 把價格切成三個區間：`(0, 20]`、`(20, 40]`、`(40, 60]`，
# 標籤依序是 `"20 以下"`、`"20–40"`、`"40 以上"`。
# 算出每個區間有幾本書，存成 dict `band_counts`（key 是標籤文字、value 是整數）。

# %%
# TODO: 請在這裡寫程式
band_counts = {}

assert band_counts == {"20 以下": 196, "20–40": 401, "40 以上": 403}
print("H1 完成：", band_counts)

# %% [markdown]
# ## H2｜同名的書是同一本嗎？
#
# 資料裡有一個書名出現兩次。找出這兩列（用 `duplicated(keep=False)`），存成 `same_title`。
# 再用 `url` 判斷：它們是重複的資料，還是兩本不同的書？把你的判斷寫成字串，存成 `my_answer`
# （只能是 `"重複資料"` 或 `"不同的書"`）。

# %%
# TODO: 請在這裡寫程式
same_title = None
my_answer = ""

assert len(same_title) == 2
assert same_title["title"].nunique() == 1
assert my_answer == "不同的書"
print("H2 完成：", same_title["title"].iloc[0], same_title["price"].tolist())

# %% [markdown]
# ## H3｜最貴的 20 本
#
# 找出價格最高的 20 本，只留 `title`、`price`、`rating` 三欄（照這個順序），
# 存成 `output/top20_expensive.csv`（`index=False`、`encoding="utf-8-sig"`）。

# %%
# TODO: 請在這裡寫程式

check = pd.read_csv("output/top20_expensive.csv", encoding="utf-8-sig")
assert check.columns.tolist() == ["title", "price", "rating"]
assert len(check) == 20
assert check.loc[0, "title"] == "The Perfect Play (Play by Play #1)"
assert check.loc[19, "title"] == "Alight (The Generations Trilogy #2)"
print("H3 完成")
