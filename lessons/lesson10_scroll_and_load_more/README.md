# Lesson 10｜動態網頁（二）：捲動載入與「載入更多」

## 學習成果

- 能說明無限捲動與「載入更多」按鈕的原理：資料是 JavaScript 在捲動或點擊時才向網站要來的，所以 requests 只看得到第一批（甚至什麼都看不到）。
- 能用 `driver.execute_script` 捲動頁面，並用 `WebDriverWait` 搭配 `lambda` 等到「新資料出現」。
- 能寫出有「停止條件」與「次數上限」的捲動迴圈：看到結尾提示就停、等不到新資料就停、找到目標就停。
- 能用迴圈按「載入更多」，直到按鈕消失。
- 能寫出基本的 XPath（屬性、文字、父層），知道什麼時候該用 XPath、什麼時候用 CSS 就夠。
- 能把捲完的 `page_source` 交給 BeautifulSoup 與 pandas，整理並存成 CSV。
- 能用 `performance.getEntriesByType('resource')` 找出網頁背後的 API，並說明為什麼「能找到 API 就不要開瀏覽器」。

## 課前準備

- 學員已完成 Lesson 09（Selenium、明確等待）。學員電腦已有 Google Chrome，且 chromedriver 第一次下載已經完成。
- 本堂使用 Notebook：先執行設定及函式定義格，再執行各示範格；各次示範結束會關閉瀏覽器與練習站。
- 所有頁面都在本機練習站（`tools/practice_site.py`），不需要外部網路：
  - `/feed`：無限捲動，一次 10 篇，共 60 篇。每次捲到底，網站要 0.3 秒才回應。
  - `/load-more`：網頁一開始就有 10 篇，按「載入更多」再取 10 篇，共 25 篇。
  - `/api/feed`：兩個頁面背後的 JSON，參數 `offset`、`limit`、`max`。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 09 --run`（無頭模式，約 40 秒）。
- 瀏覽器視窗大小固定 1280×900。無限捲動是否觸發和視窗高度有關，所以 `new_driver()` 一律指定視窗大小，請不要拿掉。
- 實測環境：Selenium 4.50、Chrome 154、macOS。Windows 與 Linux 請在開課前實際執行一次。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 09；成果預覽：瀏覽器自己捲到底，文章一批一批長出來 | learning 01 |
| 15–45 | requests 只看到空殼；`execute_script` 捲動；等「新資料」出現；捲到全部載入（兩種停止方法） | learning 02–05 |
| 45–75 | 找到目標就停；「載入更多」按鈕；XPath 入門 | learning 06–08 |
| 75–85 | 休息與環境排錯 | |
| 85–115 | ⭐ Core：第一批、捲一次、捲到底、最後一篇 | exercises 1–4 |
| 115–145 | ⭐⭐ Practice：按鈕、XPath、提早停止 | exercises 5–8 |
| 145–170 | 交給 BeautifulSoup 與 pandas；找 API 並比較速度；⭐⭐⭐ Challenge；常見問題 | learning 09–11、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson10_learning.ipynb`：先執行設定與函式定義，再執行各示範格。
- `lesson10_exercises.ipynb`：10 題，每題一個函式；完成各題後執行最後的檢查格，顯示 PASS 或 FAIL。
- `lesson10_solutions.ipynb`：教師解答（不進 git）。
- `lesson10_homework.ipynb`：3 題課後作業，同樣自動評分。解答 `lesson10_homework_solutions.ipynb` 不進 git。
- `fixtures/feed_rendered.html`：`/feed` 捲完之後的 HTML 快照（60 篇）。Chrome 出狀況時，學員仍可做第 09 單元的 BeautifulSoup 與 pandas 部分。

## 常見卡點與講法

- **捲了，但沒有新資料**：先確認視窗大小、有沒有真的捲到底、新資料要不要等待。網站載入需要時間，所以一定要「捲、等、再捲」，不能連續捲兩次就以為載完。
- **`execute_script` 沒有回傳值**：要把結果帶回 Python，JavaScript 裡要有 `return`（`"return document.body.scrollHeight"`）；只下動作（`window.scrollTo(...)`）不用 return。
- **迴圈停不下來**：一定要同時有「停止條件」（看到結尾提示、按鈕消失、數量不再增加）與「次數上限」（`range(30)`）。課堂上可以故意把停止條件拿掉，讓學員看看會發生什麼，再用上限救回來。
- **`TimeoutException` 該不該當作錯誤**：在「等不到新資料就當作到底」的做法裡，逾時是**預期中的結束訊號**，要用 `try / except` 接住。其他地方的逾時才是真的出問題。
- **兩種停止方法的取捨**：「等不到新資料就停」到哪個網站都能用，但最後要多等一個逾時時間；「看到結尾提示就停」最快，但要網頁真的有提示。
- **按鈕找得到卻點不到**：`ElementClickInterceptedException` 通常是被別的東西蓋住，或按鈕還在載入中（`disabled`）。先等按鈕可點擊（`EC.element_to_be_clickable`），或先 `scrollIntoView`。
- **XPath 的文字比對很嚴格**：`text()='進階'` 要完全相同，含空白也不行；寬鬆一點用 `contains(., '進階')`。`//` 開頭表示從整份文件找，`/..` 是往上一層。
- **CSS 還是 XPath**：能用 CSS 就用 CSS。XPath 留給「依文字找」和「由子元素找父層」。
- **找到 API 就不要用 Selenium**：同樣 60 篇，Selenium 要 3 秒左右，API 不到 0.5 秒，而且不會因為視窗大小或渲染時機出錯。這是本堂最重要的觀念，也呼應 Lesson 10。
- **真實網站的無限捲動**：可能真的捲不完（社群動態）。先決定要幾筆，達到就停；並且控制頻率，不要一口氣捲幾千筆。
- **瀏覽器視窗沒關**：同 Lesson 10，用 `with` 或 `try / finally` 保證關閉。

## 時間調整

- 時間不足：只做 Core 與第 5、8 題；XPath（單元 08）與 API（單元 10）改為老師示範，第 9、10 題留給作業。
- 時間充足：加做 Challenge；讓學員用 `https://quotes.toscrape.com/scroll`（公開的練習網站，無限捲動）重做第 3 題，再用 F12 找出它的 API，用 requests 抓完全部名言。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
