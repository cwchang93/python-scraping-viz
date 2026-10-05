# %% [markdown]
# # Lesson 06｜網頁資料清理
#
# 爬回來的資料很少乾淨：多餘的空白、包在文字裡的引號、「逗號串在一起」的標籤、寫成英文句子的日期。
# 今天學的是**清理的思路**：先找出問題，再逐項決定怎麼處理，最後驗證結果。
# 在 VS Code 按每格上方的 Run Cell 逐格執行。
#
# 本堂使用 `fixtures/` 裡的兩份真實爬取資料：
# - `quotes_raw.csv`：名言網站 10 頁，共 100 則名言
# - `authors_raw.csv`：每位作者的個人頁面資料（生日、出生地、簡介）

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
# ## 01｜清理是一連串決策
#
# 1. **找問題**：缺值、重複、空白、型態、格式不一致
# 2. **做決策**：補值？刪除？標記？每一個都要有理由
# 3. **驗證**：筆數、型態、範圍對不對
# 4. **留紀錄**：之後才知道資料動過什麼

# %% [markdown]
# ## 02｜先用小資料練手：缺值、重複、空白
#
# 下面是故意弄髒的小表，每一種問題都出現一次。

# %%
import pandas as pd

toy = pd.DataFrame(
    {
        "name": [" Alice ", "bob", "Bob", "Carol", None, "alice"],
        "score": ["90", "85", "85", "abc", "70", None],
        "city": ["Taipei", "taipei ", "Taipei", "Tainan", "Taichung", "Taipei"],
    }
)
print(toy)

# %%
print("每欄缺值數量：")
print(toy.isna().sum())

print("完全重複的列：", toy.duplicated().sum())

# %% [markdown]
# `" Alice "` 和 `"alice"`、`"bob"` 和 `"Bob"` 其實是同一個人，只是寫法不同，所以**要先統一格式，再找重複**。

# %%
cleaned = toy.copy()
cleaned["name"] = cleaned["name"].str.strip().str.title()
cleaned["city"] = cleaned["city"].str.strip().str.title()
print(cleaned)
print("統一格式後的重複列：", cleaned.duplicated().sum())

# %% [markdown]
# `score` 裡有 `"abc"`，無法轉成數字。`errors="coerce"` 會把它變成缺值（NaN），讓問題「看得見」，再決定怎麼處理。

# %%
cleaned["score"] = pd.to_numeric(cleaned["score"], errors="coerce")
print(cleaned["score"].tolist())
print("轉換失敗（變成缺值）的筆數：", cleaned["score"].isna().sum())

# %%
# 決策一：沒有名字的列無法使用 → 刪除
# 決策二：重複的列只留一筆
# 決策三：分數缺值先保留（不補成 0，避免拉低平均）
final = cleaned.dropna(subset=["name"]).drop_duplicates().reset_index(drop=True)
print(final)
print("平均分數（自動忽略缺值）：", final["score"].mean())

# %% [markdown]
# ## 03｜載入真實資料，先看一眼

# %%
quotes = pd.read_csv("fixtures/quotes_raw.csv", encoding="utf-8-sig")
authors = pd.read_csv("fixtures/authors_raw.csv", encoding="utf-8-sig")

print("名言：", quotes.shape, "｜作者：", authors.shape)
print(quotes.head(3).to_string())

# %%
print(authors.drop(columns="description").head(3).to_string())
print("description 的長度（字元）：", authors["description"].str.len().describe().round(0).to_dict())

# %% [markdown]
# 觀察到的問題（先列清單，再逐項處理）：
# - `text`：前後有彎引號 “ ”
# - `tags_text`：標籤用逗號串成一個字串
# - `born_date_text`：`"March 14, 1879"` 是文字，不是日期
# - `born_location_text`：開頭有 `"in "`，國家藏在最後一段
# - `description`：前後帶著空白與換行
# - `tags_text`：有幾則名言沒有標籤（缺值）
# - `author_url`：兩張表要靠它對應

# %% [markdown]
# ## 04｜文字清理：去引號與空白

# %%
quotes["text"] = quotes["text"].str.strip().str.strip("“”")
print(quotes["text"].head(2).tolist())

quotes["author"] = quotes["author"].str.strip()
print("名言字數（單字）：", quotes["text"].str.split().str.len().describe().round(1).to_dict())

# %% [markdown]
# ## 05｜標籤：一個字串 → 一個 list → 一筆一個標籤
#
# `str.split(",")` 把字串切成 list；`explode` 再把每個 list 展開成一列。

# %%
print("沒有標籤（缺值）的名言：", quotes["tags_text"].isna().sum(), "則")

quotes["tags"] = quotes["tags_text"].str.split(",")  # 缺值會維持缺值
quotes["tag_count"] = quotes["tags"].str.len().fillna(0).astype(int)  # 沒有標籤 → 0 個
print(quotes[["author", "tags", "tag_count"]].head(3).to_string())
print("tag_count 為 0 的名言：", (quotes["tag_count"] == 0).sum(), "則")

# %%
tags_long = quotes[["text", "tags"]].explode("tags").rename(columns={"tags": "tag"})
tags_long = tags_long.dropna(subset=["tag"])  # 沒有標籤的名言不產生標籤列
print("展開後的筆數：", len(tags_long))
print(tags_long["tag"].value_counts().head(5))

# %% [markdown]
# ## 06｜日期：文字 → datetime
#
# `format="%B %d, %Y"` 對應 `March 14, 1879`（`%B` 月份英文全名、`%d` 日、`%Y` 四位數年）。
# `errors="coerce"` 讓無法解析的日期變成 `NaT`（日期版的缺值）。

# %%
authors["name"] = authors["name"].str.strip()
authors["description"] = authors["description"].str.strip()
authors["born_date"] = pd.to_datetime(authors["born_date_text"].str.strip(), format="%B %d, %Y", errors="coerce")

print(authors[["name", "born_date_text", "born_date"]].head(3).to_string())
print("日期解析失敗（NaT）的筆數：", authors["born_date"].isna().sum())

# %%
authors["born_year"] = authors["born_date"].dt.year
print("最早出生年：", authors["born_year"].min(), "｜最晚：", authors["born_year"].max())

# %% [markdown]
# ## 07｜出生地：切出國家
#
# `"in Ulm, Germany"` → 去掉開頭的 `in ` → 取最後一段逗號後面的文字。
# 有些國家名稱前面帶 `The `（The United States），一併去掉，讓同一個國家只有一種寫法。

# %%
location = authors["born_location_text"].str.strip().str.replace(r"^in\s+", "", regex=True)
authors["born_location"] = location

country = location.str.split(",").str[-1].str.strip()
authors["country"] = country.str.replace(r"^The\s+", "", regex=True)

print(authors[["name", "born_location", "country"]].head(5).to_string())

# %%
print(authors["country"].value_counts().head(6))

# %% [markdown]
# ## 08｜缺值檢查：NaN 和「空字串」是兩回事
#
# 網頁上沒有資料時，爬下來可能是空字串 `""`，不是 `NaN`，所以 `isna()` 抓不到。

# %%
print("作者表的 NaN 缺值：")
print(authors[["born_date", "born_location", "country"]].isna().sum())
print("名言表的 tags_text 缺值：", quotes["tags_text"].isna().sum())

print("空字串的筆數：", (authors["born_location"].str.len() == 0).sum())

# %% [markdown]
# ## 09｜名言有沒有重複？
#
# 爬蟲常常抓到重複的資料，合併前先確認。

# %%
print("名言文字重複：", quotes["text"].duplicated().sum(), "則")
print("作者網址重複（authors 表應該沒有）：", authors["author_url"].duplicated().sum(), "筆")

# %% [markdown]
# ## 10｜合併兩張表：merge
#
# 名言表和作者表用 `author_url` 對應。`how="left"` 保留所有名言；
# `validate="many_to_one"` 檢查「一個作者對應多則名言」這個假設真的成立。

# %%
merged = quotes.merge(
    authors[["author_url", "born_year", "country"]],
    on="author_url",
    how="left",
    validate="many_to_one",
)
print("合併後：", merged.shape)
print("沒對應到作者的名言：", merged["born_year"].isna().sum())

# %% [markdown]
# ## 11｜新增欄位，回答一個小問題
#
# 哪個國家的作者名言最多？

# %%
print(merged["country"].value_counts().head(5))

oldest = merged.loc[merged["born_year"].idxmin(), ["author", "born_year"]]
print("最早出生的作者：", oldest["author"], oldest["born_year"])

# %% [markdown]
# ## 12｜驗證清單
#
# 清理完成後，把「應該成立的事」寫成 `assert`，之後資料更新，一跑就知道有沒有壞。

# %%
assert len(merged) == 100, "名言應該有 100 則"
assert merged["text"].str.contains("[“”]").sum() == 0, "還有彎引號沒去掉"
assert merged["text"].duplicated().sum() == 0, "有重複的名言"
assert (merged["tag_count"] == 0).sum() == 3, "應該有 3 則名言沒有標籤"
assert merged["tag_count"].min() >= 0
assert merged["born_year"].notna().all(), "有作者沒有出生年"
assert merged["country"].notna().all(), "有作者沒有國家"
print("驗證通過")

# %% [markdown]
# ## 13｜存檔
#
# 存三份：合併後的名言、展開的標籤、清理後的作者。
# `tags` 是 list，存進 CSV 前先轉回逗號字串。

# %%
Path("output").mkdir(exist_ok=True)

out = merged.drop(columns=["tags_text"]).copy()
out["tags"] = out["tags"].str.join(",")
out.to_csv("output/quotes_clean.csv", index=False, encoding="utf-8-sig")
tags_long.to_csv("output/tags_long.csv", index=False, encoding="utf-8-sig")
authors.drop(columns=["born_date_text", "born_location_text"]).to_csv(
    "output/authors_clean.csv", index=False, encoding="utf-8-sig"
)
print("已存檔：output/quotes_clean.csv、tags_long.csv、authors_clean.csv")

# %% [markdown]
# ## 14｜寫下清理決策
#
# 好的清理會留下紀錄，資料交給別人（或三個月後的自己）時才看得懂。

# %%
cleaning_log = [
    "text：去掉前後空白與彎引號",
    "tags_text：用逗號切開，展開成 tags_long；3 則沒有標籤的名言保留，tag_count 記 0",
    "description：去掉前後空白與換行",
    "born_date_text：轉成 datetime；解析失敗會變 NaT，已確認沒有",
    "born_location_text：去掉開頭 in，取最後一段當國家，並去掉 The",
    "兩張表用 author_url 合併，確認每則名言都對應到作者",
]
for number, decision in enumerate(cleaning_log, start=1):
    print(number, decision)
