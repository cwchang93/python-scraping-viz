# Lesson 02｜網路原理、爬蟲倫理與環境

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

- `lesson02_learning.ipynb`：17 個教學單元，可逐格執行。
- `lesson02_exercises.ipynb`：學員練習。
- `lesson02_solutions.ipynb`：教師解答（不進 git）。
- `lesson02_homework.ipynb`：課後作業。
- `fixtures/quotes_page1.html`、`fixtures/books_index.html`：練習站快照。

## 可選練習網站

以下網站可用來多練習發送 GET 請求、檢查狀態碼與觀察 HTML。先用瀏覽器和 F12 看頁面，再用 `requests.get(url, timeout=10)` 取回 HTML；這一堂先練「取得網頁」，下一堂再練解析欄位。

| 網站 | 可以觀察／練習 | 難度 |
|---|---|---|
| [Quotes to Scrape](https://quotes.toscrape.com/) | 名言頁與分頁；課堂主要範例 | 入門 |
| [Books to Scrape](https://books.toscrape.com/) | 書籍目錄；觀察商品頁與分頁 | 入門 |
| [Books to Scrape 商品頁](https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html) | 從目錄點進單筆資料，觀察網址路徑如何改變 | 入門 |
| [HTTPBin HTML](https://httpbin.org/html) | 簡單 HTML 回應，適合練狀態碼、`Content-Type` 與存檔 | 入門 |
| [JSONPlaceholder Posts](https://jsonplaceholder.typicode.com/posts) | JSON API 回應；比較 `response.text` 與 `response.json()` | 入門＋ |

建議每次只請求一頁、設定 timeout，並留意網站條款與 `robots.txt`。若遇到 403、429 或其他拒絕回應，停止請求並改用課程的 `fixtures/` 練習；不要嘗試繞過限制。外部服務可能調整內容或暫時無法連線。

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
