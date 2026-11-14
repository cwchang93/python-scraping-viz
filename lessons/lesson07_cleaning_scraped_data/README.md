# Lesson 07｜網頁資料清理

## 學習成果

- 能用 `isna`、`duplicated` 找出缺值與重複，並說明為什麼要「先統一格式、再找重複」。
- 能用 `strip`、`title`、`str.replace` 清理文字，用 `to_numeric`、`to_datetime` 轉型，並用 `errors="coerce"` 讓轉換失敗的資料變成看得見的缺值。
- 能把逗號串成的標籤切成 list，再用 `explode` 展開成一列一個標籤。
- 能從一句描述（出生地）裡切出需要的欄位（國家）。
- 能用 `merge` 合併兩張表，並用 `validate`、`isna` 檢查合併結果。
- 能把「應該成立的事」寫成 `assert`，並留下清理決策紀錄。

## 課前準備

- 學員已完成 Lesson 06（pandas 轉型、篩選、排序、groupby）。
- 本堂只用 `fixtures/`，不需要網路。
- 資料集用 `python tools/build_fixtures.py quotes` 從名言網站抓下來（10 頁名言、50 位作者的個人頁面，約 3 分鐘）；網站改版時用這支腳本重建，並更新練習的標準答案。
- 資料裡的真實問題（不是人為製造的）：3 則名言沒有標籤（缺值）、名言文字帶彎引號、標籤是逗號字串、日期是英文句子、出生地混著城市與國家、作者簡介前後有空白與換行。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 06；清理是一連串決策 | learning 01 |
| 15–45 | 小資料練手：缺值、重複、空白、`to_numeric` | learning 02 |
| 45–75 | 載入真實資料、列問題清單、文字與標籤清理 | learning 03–05 |
| 75–85 | 休息與環境排錯 | |
| 85–120 | ⭐ Core：統一格式、轉數字、找重複、載入資料 | exercises 1–4 |
| 120–150 | 日期、出生地、缺值與重複檢查；⭐⭐ Practice | learning 06–09、exercises 5–8 |
| 150–170 | 合併、驗證、存檔、清理紀錄；⭐⭐⭐ Challenge | learning 10–14、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson07_learning.ipynb`：14 個教學單元。
- `lesson07_exercises.ipynb`：10 題分級練習，只用本機資料。
- `lesson07_solutions.ipynb`：教師解答，含作業參考解答（不進 git）。
- `lesson07_homework.ipynb`：3 題課後作業。
- `fixtures/quotes_raw.csv`：100 則名言的原始爬取結果。
- `fixtures/authors_raw.csv`：50 位作者的個人頁面資料。

## 常見卡點與講法

- **清理順序**：先統一格式（`strip`、`title`），再找重複；順序反了會漏掉。
- **缺值不等於 0**：沒有標籤的名言，`tag_count` 記 0 是「沒有標籤」的意思；分數缺值則不能補 0，會拉低平均。每一個欄位都要問「缺值代表什麼」。
- **`fillna("")` 再 `split` 會得到 `[""]`**：長度變成 1。保持缺值（NaN）更安全，用 `str.len().fillna(0)` 處理。
- **`errors="coerce"`**：轉不了的變成 NaN 或 NaT，是「讓問題看得見」；`raise` 則是直接出錯。本資料的日期都能解析，要示範 NaT 請用小資料。
- **NaN 與空字串不同**：`isna()` 抓不到空字串，要另外用 `str.len() == 0` 檢查。
- **`explode` 之後筆數變多**：一則名言有幾個標籤就變成幾列，統計「名言數」與「標籤數」要分開算。
- **`merge` 後筆數變了**：用 `validate="many_to_one"` 確認對應關係，並檢查沒對應到的筆數。
- **`str.replace` 的 `regex`**：pandas 2.0 起預設不把字串當正規表達式，要用規則（例如 `^in\s+`）時要明確寫 `regex=True`；單純取代文字時寫 `regex=False`。

## 時間調整

- 時間不足：只做 Core 與第 5、6、10 題；日期與出生地改為老師示範。
- 時間充足：加做 Challenge，並讓學員自己找出資料裡還沒處理的問題（例如作者簡介裡的網址）。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
