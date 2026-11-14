# Lesson 03｜requests 與 HTML 結構

## 學習成果

- 能讀懂 HTML 的標籤、屬性與巢狀結構。
- 能用 `params`、`headers`、`timeout` 控制請求。
- 能說明狀態碼與重新導向，並用 `response.history` 檢查轉址。
- 能說明亂碼的成因，並設定正確的編碼。
- 能把抓取流程包成可重複使用的 `fetch(url)`，失敗時不讓程式當掉。
- 遇到 403 時知道該停下來，而不是想辦法繞過。

## 課前準備

- 學員已完成 Lesson 02 的環境（venv、requests）。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 02 --run`。
- 確認 `fixtures/` 內有 `quotes_tag_love.html` 與 `books_page2.html`。
- 第 13 格會請求 Dcard，結果以當天為準；若回 200，改口講「這次剛好沒擋，但不保證下次」。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 02；成果預覽：失敗時不會當掉的抓取函式 | learning 01 |
| 15–45 | HTML 的標籤、屬性、巢狀；在真網頁裡找一則名言 | learning 02–03 |
| 45–75 | params、headers、狀態碼與轉址、編碼 | learning 04–07 |
| 75–85 | 休息與環境排錯 | |
| 85–120 | ⭐ Core：讀 HTML、組網址、接住 timeout、解碼 | exercises 1–4 |
| 120–150 | timeout 與例外、包成 `fetch`、⭐⭐ Practice | learning 08–10、exercises 5–8 |
| 150–170 | 連續抓取要禮貌、存檔、403 案例；⭐⭐⭐ Challenge | learning 11–13、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson03_learning.ipynb`：14 個教學單元，可逐格執行。
- `lesson03_exercises.ipynb`：10 題分級練習，內建 `assert`。
- `lesson03_solutions.ipynb`：教師解答，含作業參考解答（不進 git）。
- `lesson03_homework.ipynb`：3 題課後作業。
- `fixtures/quotes_tag_love.html`、`fixtures/books_page2.html`：練習站快照。

## 常見卡點與講法

- **函式沒有 `return` 就是回傳 `None`**：第 6 題先看 `fetch` 失敗時回傳什麼，再要求學員在呼叫端檢查 `None`。
- **`raise_for_status()` 是在檢查，不是在抓**：沒有它，404 不會報錯，`response.ok` 只是 `False`。
- **timeout 沒設會卡住**：用第 3 題展示 `timeout=0.001` 立刻出錯。
- **亂碼不是網站壞掉**：是 bytes 用錯編碼。有些台灣的老網站用 big5，用 utf-8 讀就會亂碼。
- **轉址次數可能是 0 或 1**：網站改版後結果會變，第 5 題只檢查它是合理的數字。
- **403 案例不要變成破解教學**：只示範判斷與放棄，並帶出官方 API、開放資料。

## 時間調整

- 時間不足：只做 Core 與第 6、7 題；第 9、10 題留給作業討論。
- 時間充足：加做 Challenge，並讓學員自己找一個網站，用 `fetch` 測它的狀態碼。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
