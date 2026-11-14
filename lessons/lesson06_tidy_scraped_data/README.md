# Lesson 06｜爬回來的資料整理：pandas

## 學習成果

- 能用 `read_csv` 讀入爬回來的資料，並用 `shape`、`head`、`info` 檢查。
- 能把 list of dict 轉成 DataFrame，也能用 `pd.read_html` 直接讀網頁裡的表格。
- 能用 `str.replace`、`astype`、`map` 把字串欄位轉成數字。
- 能用條件篩選（`&`、`|`）、`sort_values`、`nlargest`、`groupby` 做出排行榜。
- 知道「書名重複」不等於「資料重複」，要用有唯一性的欄位判斷。
- 能把整理後的結果存成乾淨的 CSV，再讀回來驗證。

## 課前準備

- 學員已完成 Lesson 05，並學過 course_v2 的 pandas（DataFrame、篩選、排序、groupby）。
- 執行 `python -m pip install -r requirements.txt`，確認 `pandas` 與 `lxml` 已安裝（`read_html` 需要 lxml）。
- 本堂只用 `fixtures/`，不需要網路。
- 資料集 `books_raw.csv` 是用 `python tools/build_fixtures.py books` 從練習站抓下來的；網站改版時用這支腳本重建，並更新練習的標準答案。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 05；成果預覽：最貴的五本書 | learning 01 |
| 15–45 | 讀入與檢查、三種資料進 pandas 的路、`read_html` | learning 02–04 |
| 45–75 | 價格、評分、庫存轉型；重複檢查 | learning 05–08 |
| 75–85 | 休息與環境排錯 | |
| 85–120 | ⭐ Core：讀入、轉型 | exercises 1–4 |
| 120–150 | 基本統計、價格區間、篩選、排序；⭐⭐ Practice | learning 09–12、exercises 5–8 |
| 150–170 | 分組、排行榜、存檔驗證；⭐⭐⭐ Challenge | learning 13–16、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson06_learning.ipynb`：16 個教學單元。
- `lesson06_exercises.ipynb`：10 題分級練習，只用本機資料。
- `lesson06_solutions.ipynb`：教師解答，含作業參考解答（不進 git）。
- `lesson06_homework.ipynb`：3 題課後作業。
- `fixtures/books_raw.csv`：書店 1000 本書的原始爬取結果（價格、評分都還是字串）。
- `fixtures/book_detail.html`：一本書的詳細頁面，含 Product Information 表格。

## 常見卡點與講法

- **`read_html` 要傳 `StringIO`**：直接傳字串會被警告或出錯。檔案路徑或網址則可以直接傳。
- **`read_html` 找不到表格**：頁面沒有 `<table>`，或是 JavaScript 載入的（第 8、9 堂處理）。
- **條件忘記加括號**：`df[df["a"] > 1 & df["b"] < 2]` 會出錯，每個條件都要括號。
- **`and`、`or` 與 `&`、`|`**：整欄比較要用 `&`、`|`。
- **`map` 對照失敗會變 NaN**：轉完要檢查 `isna().sum()`。
- **CSV 不記得型態**：存檔再讀回來，數字欄位會被自動猜成數字，但日期、布林要自己處理（第 7 堂）。
- **pandas 版本不同**：pandas 3 的字串欄位型態顯示為 `str`，pandas 2 是 `object`，兩者行為相同，教材程式都能執行。

## 時間調整

- 時間不足：只做 Core 與第 5、6 題；`read_html` 與分組改為老師示範。
- 時間充足：加做 Challenge，並讓學員自己提一個問題（例如「哪個價格區間 5 星最多」）再用程式回答。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
