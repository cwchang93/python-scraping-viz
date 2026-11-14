# Lesson 04｜BeautifulSoup（一）：解析 HTML

## 學習成果

- 能用 `BeautifulSoup(html, "html.parser")` 建立 soup。
- 能用 `find`、`find_all`、`select`、`select_one` 找到元素，並說明它們的回傳型態。
- 能用 `get_text(strip=True)` 取文字，用 `tag["href"]`、`tag.get("href")` 取屬性。
- 能把一頁名言解析成 list of dict，並包成 `parse_quotes(html)`。
- 知道 `find` 找不到會回傳 `None`，並先檢查再取值。
- 能用 F12 的 Copy selector 找到選擇器，再簡化。

## 課前準備

- 學員已完成 Lesson 03（有 `fetch(url)`）。
- 開課前執行 `python -m pip install -r requirements.txt` 確認 `beautifulsoup4` 已安裝。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 03 --run`。
- 本堂的練習只用 `fixtures/`，不依賴網路；教學示範的第 14 格才連網。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 03；成果預覽：不到十行取出名言與作者 | learning 01–02 |
| 15–45 | 建立 soup、`find`、`find_all`、取屬性與文字 | learning 03–07 |
| 45–75 | CSS 選擇器、在真正的名言網頁找一則名言 | learning 08–09 |
| 75–85 | 休息與環境排錯 | |
| 85–120 | ⭐ Core：小型 HTML 的標題、find、屬性 | exercises 1–4 |
| 120–150 | 整頁解析、缺值保護、⭐⭐ Practice | learning 10–12、exercises 5–8 |
| 150–170 | 包成 `parse_quotes`、F12 找選擇器；⭐⭐⭐ Challenge | learning 13–16、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson04_learning.ipynb`：16 個教學單元。
- `lesson04_exercises.ipynb`：10 題分級練習，只用本機 HTML。
- `lesson04_solutions.ipynb`：教師解答，含作業參考解答（不進 git）。
- `lesson04_homework.ipynb`：3 題課後作業。
- `fixtures/quotes_page1.html`、`fixtures/quotes_tag_love.html`：練習站快照。

## 常見卡點與講法

- **`class` 要寫成 `class_`**：`class` 是 Python 保留字。用 `select("div.quote")` 就沒有這個問題，可以趁機推廣 CSS 選擇器。
- **`find` 與 `find_all` 的回傳不同**：一個是單一元素或 `None`，一個是類似 list 的結果。看到 `AttributeError: 'NoneType'` 就是 `find` 找不到。
- **`select("a")` 取到的不一定是你要的那個**：名言網頁的 `div.quote` 裡有多個 `a`，第一個是作者連結，標籤要用 `a.tag`。先看 F12 再選。
- **`tag["href"]` 與 `.get("href")`**：前者缺屬性會 `KeyError`，後者回傳 `None`。
- **空白與換行**：`get_text()` 常帶換行，整理資料時加 `strip=True`。
- **瀏覽器看到的和程式拿到的不同**：F12 的 Elements 是瀏覽器執行 JavaScript 之後的結果；如果程式找不到，先存下 HTML 看原始內容（第 8、9 堂處理動態網頁）。

## 時間調整

- 時間不足：只做 Core 與第 6、9 題；缺值保護留給作業。
- 時間充足：加做 Challenge，並讓學員用 F12 找出作者頁面（`/author/...`）的資料結構。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
