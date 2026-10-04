# Lesson 01｜網路原理、爬蟲倫理與環境

## 學習成果

- 能說明瀏覽器打開網頁時，URL、請求、回應與 HTML 之間的關係。
- 能用 F12 的 Network 與 Elements 觀察一個網頁。
- 能說明 robots.txt 與基本爬取守則。
- 能建立虛擬環境並安裝 requests。
- 能用 `requests.get` 抓回一頁，檢查狀態碼，並存成 HTML 檔。

## 課前準備

- 學員已安裝 Python 3.10 以上與 VS Code（含 Python、Jupyter 擴充）。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 01 --run`，確認練習站可連線。
- 確認 `fixtures/` 內有 `quotes_page1.html` 與 `books_index.html`。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 今日成果預覽：用 Python 抓回一個網頁 | learning 01 |
| 15–45 | 瀏覽器開網頁的五步驟、URL、狀態碼；F12 觀察 | learning 02–05 |
| 45–75 | 建 venv、安裝 requests、第一支 `requests.get` | learning 06–08 |
| 75–85 | 休息與環境排錯 | |
| 85–120 | ⭐ Core：抓一頁、看狀態碼與 headers、看 HTML | exercises 1–5 |
| 120–150 | ⭐⭐ Practice：字串計數、存檔、404、robots.txt、User-Agent | exercises 6–10 |
| 150–170 | 解答、常見錯誤；爬取守則；⭐⭐⭐ Challenge | learning 12–17、exercises 11–12 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson01_learning.py`：17 個教學單元，`# %%` 分格。
- `lesson01_exercises.py`：學員練習。
- `lesson01_solutions.py`：教師解答（不進 git）。
- `lesson01_homework.py`：課後作業。
- `fixtures/quotes_page1.html`、`fixtures/books_index.html`：練習站快照。

## 常見卡點與講法

- **相對路徑找不到檔案**：每個檔案開頭有「設定工作資料夾」那一格，會把工作目錄切到檔案所在資料夾，所以從終端機或 VS Code 執行都能找到 `fixtures/`。要先執行過那一格，才用得到 Run Cell 的逐格執行。
- **macOS 出現 SSL 憑證錯誤**：python.org 安裝的 Python 需執行 Applications 裡的 `Install Certificates.command`。
- **PowerShell 無法啟動 venv**：執行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`。
- **`pip` 與 Python 不是同一套**：一律用 `python -m pip install`。
- **`.text` 與 `.content` 的差別**：`.text` 是解碼後的字串，`.content` 是原始 bytes；存檔用 `.content`。
- **公司或學校網路擋外部網站**：改用 `fixtures/`，不要在課堂上排查網路。

## 時間調整

- 時間不足：只做 Core 與 Practice 的 6、7；robots.txt 與 User-Agent 留給作業。
- 時間充足：加做 Challenge，並讓學員用 F12 觀察 books.toscrape.com 的 Network。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
