# Lesson 08｜JSON API、開放資料與登入

## 學習成果

- 能說明 JSON 與 Python 的 dict、list 如何對應，會用 `json.loads`、`json.dumps`、`response.json()`。
- 能用 F12 的 Network（Fetch/XHR）找到網頁背後的資料來源（API），並直接用 `requests` 取用。
- 能一層一層取出巢狀的 JSON，並用 `.get()` 安全取值；能用 `pd.json_normalize` 轉成 DataFrame。
- 能說明開放資料的授權、格式、更新頻率，並完成一次真實的開放資料分析。
- 能說明登入與 Cookie 的原理，用 `requests.Session` 登入、帶著 Cookie 抓會員頁。
- 知道隱藏欄位（CSRF token）要一起送出，也知道登入只用在自己有帳號、且條款允許的網站。

## 課前準備

- 學員已完成 Lesson 07（pandas 清理、`read_html`）。
- 本堂練習、解答與作業只用 `fixtures/` 與本機練習站，不需要外部網路；教學示範的第 04、07、11、14 格會連到外部（名言網站 API、台北市 YouBike），沒有網路時會自動改用快照。
- 本機練習站是 `tools/practice_site.py`，只監聽 127.0.0.1、只用 Python 標準函式庫。課堂程式會用 `start_server()` 自動啟動；也可以直接 `python tools/practice_site.py`，用瀏覽器開 `http://127.0.0.1:8000` 先看看。
- 練習站的測試帳號密碼定義在 `tools/practice_site.py`，只對本機練習站有效。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 07 --run`。
- `fixtures/youbike_sample.json` 是每 6 站取 1 站的快照（302 站）。即時資料每分鐘變動，所以課堂分析一律用快照；要更新快照用 `python tools/build_fixtures.py api`，並同步更新練習裡寫死的數字。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 07；成果預覽：JSON 直接變表格 | learning 01 |
| 15–45 | JSON 是什麼；F12 找 API；呼叫 API、看結構、取巢狀值 | learning 02–06 |
| 45–75 | API 翻頁、`json_normalize`；API 與 HTML 爬蟲比較 | learning 07–09 |
| 75–85 | 休息與環境排錯 | |
| 85–115 | ⭐ Core、⭐⭐ Practice 前半：JSON 基礎與 `json_normalize` | exercises 1–6 |
| 115–145 | 開放資料：YouBike 載入、整理、分析、錯誤處理、存檔 | learning 10–15、exercises 7–8 |
| 145–170 | 登入與 Cookies：Session、隱藏欄位、會員頁；⭐⭐⭐ Challenge | learning 16–21、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson08_learning.ipynb`：21 個教學單元，分 A（JSON 與 API）、B（開放資料）、C（登入與 Cookies）三段。
- `lesson08_exercises.ipynb`：10 題分級練習。
- `lesson08_solutions.ipynb`：教師解答，含作業參考解答（不進 git）。
- `lesson08_homework.ipynb`：3 題課後作業。
- `fixtures/quotes_api_page1.json`、`quotes_api_page2.json`：名言 API 第 1、2 頁的回應。
- `fixtures/youbike_sample.json`：YouBike 即時資料快照（302 站）。

## 常見卡點與講法

- **`json.loads` 與 `response.json()`**：前者吃文字，後者吃 HTTP 回應；`json.load`（沒有 s）吃檔案。三個名稱很像，容易混淆。
- **F12 看不到請求**：先開 Network 再重新整理或捲動頁面；要點 Fetch/XHR 篩選；請求出現後才能點開看 Response。
- **`KeyError`**：先印出 `data.keys()` 確認層級；不確定有沒有這個欄位用 `.get()`。
- **欄位名稱看不懂**：開放資料的欄位要查資料說明（`Quantity` 是總車位，不是 `total`），不要用猜的。
- **`act` 是字串**：`"1"` 不等於 `1`；比較前先確認型態。
- **登入後還是被導回登入頁**：沒有用同一個 `session` 發請求，Cookie 沒帶上；或沒有送 `csrf_token`。
- **`csrf_token` 每次都不同**：每次載入登入頁都會換新的，所以要「先 GET 取得、再 POST 送出」，而且 GET 與 POST 要用同一個 `session`。
- **真實帳號不要寫進程式碼**：課堂用練習站的測試帳號，真實網站請由學員自己輸入，不要放進 repo。
- **Port 被占用**：`start_server()` 預設用空閒的 port，不會衝突；手動啟動 `python tools/practice_site.py` 才固定 8000。

## 時間調整

- 時間不足：只做 Core 與第 5、8 題；登入與 Cookies（C 段）改為老師示範，第 9、10 題留給作業。
- 時間充足：加做 Challenge，並讓學員用 F12 找出 `https://quotes.toscrape.com/scroll` 的 API，自己寫出抓 5 頁的迴圈。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
