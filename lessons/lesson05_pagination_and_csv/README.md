# Lesson 05｜BeautifulSoup（二）：翻頁與整站爬取

## 學習成果

- 能解析一本書的標題、價格、評分、庫存與連結，並把價格、評分轉成數字。
- 能用 `re.search`、`re.sub` 從文字裡取出數字與頁碼。
- 能用 `urljoin` 把相對網址組成完整網址，說明為什麼不能自己拼字串。
- 能找到「下一頁」連結，寫出翻頁迴圈，並在最後一頁停下。
- 連續請求時加上 `time.sleep`，並用 `logging` 記錄進度與失敗。
- 能把 list of dict 存成 CSV，再讀回來驗證。

## 課前準備

- 學員已完成 Lesson 04（`find`、`select`、`parse_quotes`）。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 04 --run`，確認練習站可連線。
- 確認 `fixtures/` 內有 `books_index.html`、`books_page2.html`、`books_page50.html`。
- 教學示範的第 11 格會連到練習站抓 3 頁（約 8 秒）；整站 50 頁實測約 2.6 分鐘（1000 本），建議老師課前跑好，課堂只示範 3 頁。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 04；成果預覽：一頁書本資料 | learning 01 |
| 15–45 | 解析一本書、價格轉數字、£ 亂碼、re 小工具、評分 | learning 02–06 |
| 45–75 | 相對網址 `urljoin`、`parse_books`、找下一頁 | learning 07–09 |
| 75–85 | 休息與環境排錯 | |
| 85–120 | ⭐ Core：價格、頁碼、評分、`urljoin` | exercises 1–4 |
| 120–150 | `logging`、翻頁迴圈、⭐⭐ Practice | learning 10–11、exercises 5–8 |
| 150–170 | 存 CSV、讀回驗證；⭐⭐⭐ Challenge | learning 12–15、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson05_learning.ipynb`：15 個教學單元。
- `lesson05_exercises.ipynb`：10 題分級練習；第 9 題連網，其餘用本機快照。
- `lesson05_solutions.ipynb`：教師解答，含作業參考解答（不進 git）。
- `lesson05_homework.ipynb`：3 題課後作業。
- `fixtures/books_index.html`、`books_page2.html`、`books_page50.html`：書店首頁、第 2 頁與最後一頁。

## 常見卡點與講法

- **£ 變成 Â£**：這個站沒宣告編碼，`requests` 預設 ISO-8859-1。教學第 04 格先用自製 bytes 說明，再用實際請求對照。解法是把 `response.content` 交給 BeautifulSoup。這是 Lesson 05 編碼單元的實例。
- **書名被截短**：`h3 a` 的文字是 `A Light in the ...`，完整書名在 `title` 屬性。
- **`class` 取到的是 list**：`pod.select_one("p.star-rating")["class"]` 是 `["star-rating", "Three"]`，要取 `[1]`。
- **相對網址的基準不同**：首頁的下一頁是 `catalogue/page-2.html`，第 2 頁的下一頁卻是 `page-3.html`。一律 `urljoin(目前頁面網址, href)`。
- **翻頁迴圈停不下來**：條件要同時看「有沒有下一頁」與「有沒有超過 `max_pages`」；測試時永遠先設 `max_pages`。
- **`logging` 沒有輸出**：Jupyter 或互動視窗可能已有設定，`basicConfig` 加 `force=True`；等級低於設定值（如 DEBUG）的訊息不會顯示。
- **CSV 在 Excel 變亂碼**：用 `encoding="utf-8-sig"`；讀回時也要用同樣的編碼，否則第一個欄位名稱前會多一個看不見的字元。
- **CSV 讀回來都是字串**：價格、評分要用數字時再轉換，第 6 堂會用 pandas 處理。

## 時間調整

- 時間不足：只做 Core 與第 5、6、8 題；`logging` 與第 9 題改為老師示範。
- 時間充足：加做 Challenge，讓學員把 `max_pages` 改成 `None` 抓整站，觀察紀錄與耗時。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
