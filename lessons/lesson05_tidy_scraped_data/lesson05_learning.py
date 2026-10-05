# %% [markdown]
# # Lesson 05｜爬回來的資料整理：pandas
#
# 上一堂我們把整個書店抓成 CSV。但爬回來的資料幾乎都是「字串」：價格是 `"£51.77"`、評分是 `"Three"`。
# 今天用 pandas 把它整理成能計算、能篩選、能排名的表格。
# 在 VS Code 按每格上方的 Run Cell 逐格執行。
#
# 本堂使用 `fixtures/books_raw.csv`：1000 本書的原始爬取結果，不需要網路。

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
# 先看結果：原始資料經過幾步整理，就能問「最貴的五本書是哪些」。

# %%
import pandas as pd

preview = pd.read_csv("fixtures/books_raw.csv", encoding="utf-8-sig")
preview["price"] = preview["price_text"].str.replace("£", "", regex=False).astype(float)
print(preview.nlargest(5, "price")[["title", "price"]].to_string(index=False))

# %% [markdown]
# ## 02｜讀進來，先看一眼
#
# 拿到爬回來的資料，第一件事永遠是：幾筆、哪些欄位、什麼型態、長什麼樣。

# %%
df = pd.read_csv("fixtures/books_raw.csv", encoding="utf-8-sig")

print("形狀（列, 欄）：", df.shape)
print("欄位：", df.columns.tolist())
print(df.head(3).to_string())

# %%
df.info()

# %% [markdown]
# 全部都是文字（`object` 或 `str`）。`"£51.77"` 還不能加總、不能比大小，所以要轉型。

# %% [markdown]
# ## 03｜list of dict → DataFrame
#
# 上一堂 `parse_books` 的輸出是 list of dict，可以直接變成 DataFrame，再用 `to_csv` 存檔。

# %%
rows = [
    {"title": "A Light in the Attic", "price": 51.77, "rating": 3},
    {"title": "Tipping the Velvet", "price": 53.74, "rating": 1},
    {"title": "Soumission", "price": 50.10, "rating": 1},
]
small = pd.DataFrame(rows)
print(small)
print(small.dtypes)

Path("output").mkdir(exist_ok=True)
small.to_csv("output/small_books.csv", index=False, encoding="utf-8-sig")
print("已存檔：output/small_books.csv")

# %% [markdown]
# ## 04｜網頁的 table：read_html 一行搞定
#
# 如果網頁本身就是 `<table>`，不用 BeautifulSoup，`pd.read_html` 直接把它變成 DataFrame。
# 書本頁面下方的「Product Information」就是一張表。

# %%
from io import StringIO

detail_html = Path("fixtures/book_detail.html").read_text(encoding="utf-8")
tables = pd.read_html(StringIO(detail_html))
print("頁面上找到的表格數量：", len(tables))

info = tables[0]
info.columns = ["item", "value"]
print(info.to_string(index=False))

# %%
# 想用項目名稱查數值，可以把 item 當成索引
info_by_item = info.set_index("item")["value"]
print("UPC：", info_by_item["UPC"])
print("庫存說明：", info_by_item["Availability"])

# %% [markdown]
# ## 05｜型態轉換：價格字串 → 數字
#
# 步驟：去掉貨幣符號，再 `astype(float)`。用 `.str` 讓整欄一次處理。

# %%
df["price"] = df["price_text"].str.replace("£", "", regex=False).astype(float)

print(df[["price_text", "price"]].head(3))
print("price 的型態：", df["price"].dtype)
print("總價：", round(df["price"].sum(), 2))

# %% [markdown]
# ## 06｜評分：英文字 → 數字
#
# 用字典對照，再 `map`。

# %%
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

df["rating"] = df["rating_word"].map(RATING_WORDS)
print(df[["rating_word", "rating"]].head(3))
print("對照失敗（NaN）的筆數：", df["rating"].isna().sum())

# %% [markdown]
# ## 07｜庫存：文字 → True / False

# %%
print(df["availability"].value_counts())

df["in_stock"] = df["availability"].eq("In stock")
print("有庫存的書：", df["in_stock"].sum(), "本")

# %% [markdown]
# ## 08｜重複檢查：書名重複，不等於資料重複
#
# 爬蟲常見的問題是重複抓到同一筆。但「同名」不代表「同一筆」，要用有唯一性的欄位判斷。

# %%
print("書名重複的列：", df["title"].duplicated().sum())
print(df[df["title"].duplicated(keep=False)][["title", "price_text", "url"]].to_string(index=False))

# %%
print("網址重複的列：", df["url"].duplicated().sum())
# 兩本《The Star-Touched Queen》價格與網址都不同，是兩本不同的書，所以不刪除。

# %% [markdown]
# ## 09｜基本統計

# %%
print(df["price"].describe().round(2))
print("中位數：", df["price"].median())
print("最便宜：", df["price"].min(), "，最貴：", df["price"].max())

# %% [markdown]
# ## 10｜新增欄位：價格區間
#
# `pd.cut` 把連續數字切成區間，常用來做分組統計。

# %%
df["price_band"] = pd.cut(
    df["price"],
    bins=[0, 20, 40, 60],
    labels=["20 以下", "20–40", "40 以上"],
)
print(df["price_band"].value_counts(sort=False))

# %% [markdown]
# ## 11｜篩選：用條件選出資料
#
# 條件放在 `df[...]` 裡面。多個條件用 `&`（而且）、`|`（或），**每個條件都要加括號**。

# %%
expensive = df[df["price"] > 55]
print("價格超過 55 的書：", len(expensive), "本")

five_star_cheap = df[(df["rating"] == 5) & (df["price"] < 15)]
print("5 星而且低於 15 元：", len(five_star_cheap), "本")

# %%
print("書名含 Love：", df["title"].str.contains("Love", case=False).sum(), "本")
print(df[df["rating"].isin([4, 5]) & (df["price"] < 12)][["title", "price", "rating"]].to_string(index=False))

# %% [markdown]
# ## 12｜排序：sort_values 與 nlargest

# %%
cheapest = df.sort_values("price").head(3)[["title", "price"]]
print(cheapest.to_string(index=False))

# %%
# 兩個排序條件：評分由高到低，同分時價格由低到高
ranked = df.sort_values(["rating", "price"], ascending=[False, True])
print(ranked[["title", "rating", "price"]].head(5).to_string(index=False))

# %%
print(df.nlargest(3, "price")[["title", "price"]].to_string(index=False))

# %% [markdown]
# ## 13｜分組統計：groupby

# %%
by_rating = df.groupby("rating")["price"].agg(["count", "mean"]).round(2)
print(by_rating)

# %% [markdown]
# ## 14｜排行榜：每個評分最便宜的一本
#
# 先排序，再每組取第一筆。

# %%
best_deals = (
    df.sort_values(["rating", "price"], ascending=[False, True])
    .groupby("rating")
    .head(1)
    .sort_values("rating", ascending=False)
)
print(best_deals[["rating", "title", "price"]].to_string(index=False))

# %% [markdown]
# ## 15｜整理欄位、存成乾淨的 CSV
#
# 只留下需要的欄位、改成好讀的順序，再存檔。`index=False` 避免多出一欄編號。

# %%
clean = df[["title", "price", "rating", "in_stock", "url"]].copy()
Path("output").mkdir(exist_ok=True)
clean.to_csv("output/books_clean.csv", index=False, encoding="utf-8-sig")
print("已存檔：output/books_clean.csv，", len(clean), "筆")

# %% [markdown]
# ## 16｜讀回來驗證
#
# CSV 不記得型態，但 `read_csv` 會自動猜：`price` 看起來是數字就讀成 float。

# %%
check = pd.read_csv("output/books_clean.csv", encoding="utf-8-sig")
print(check.dtypes)
print("筆數相同：", len(check) == len(clean))
print("總價相同：", round(check["price"].sum(), 2) == round(clean["price"].sum(), 2))
