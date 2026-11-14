# Lesson 11｜圖片與檔案下載

## 學習成果

- 能說明圖片與檔案是二進位資料：用 `response.content`（bytes）取得，用 `write_bytes` 或 `open(path, "wb")` 存檔。
- 能從 `<img>` 找出圖片網址：用 `urljoin` 處理相對路徑，認得「懶載入」（真正的網址在 `data-src`），用 `urlparse` 取出不含參數的檔名。
- 能寫出安全的下載函式：檢查狀態碼與 `Content-Type`（避開 404 與「回 200 的假圖」），檔案已存在就略過，每張之間 `sleep`，最後印統計。
- 會用 `requests.head` 先問大小再決定要不要下載，會用 `stream=True` 與 `iter_content` 下載大檔案，也會下載 CSV 並用 pandas 讀。
- 能用 Pillow 開啟圖片、讀取尺寸／格式／模式，分辨 `thumbnail`、`resize`、`ImageOps.fit` 的差別並做出縮圖。
- 能處理 RGBA 轉 JPEG（貼到白底），調整 JPEG 品質與檔案大小的取捨。
- 能依條件整理資料夾（依評分、安全的檔名），並用 `paste` 做出縮圖牆。

## 課前準備

- 學員已完成 Lesson 10，且 `requirements.txt` 的套件已安裝（本堂新增 `pillow`）：`python -m pip install -r requirements.txt`。
- 本堂使用 VS Code Notebook 逐格執行。
- 全部示範、練習與作業只用本機練習站（`tools/practice_site.py`）與 `fixtures/gallery/`，**不需要外部網路**，也不需要 Chrome：
  - `/gallery`：圖庫頁，17 個 `<img>`：12 張書的封面、3 張其他圖片，加上 2 張有問題的（`missing.jpg` 回 404；`fake.jpg` 回 200 但內容是網頁）。其中 `cover_02.jpg` 的網址帶 `?v=3`，`cover_12.jpg` 是懶載入（`src` 是佔位圖 `loading.gif`，真正的網址在 `data-src`）。
  - `/images/<檔名>`：圖片本身。
  - `/files/price_list.csv`（帶 `Content-Disposition`）、`/files/big.bin`（2 MiB，用來示範串流）。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 10 --run`（約 10 秒）。
- `fixtures/gallery/` 裡的 12 張封面是從 books.toscrape.com（練習用網站）各書詳細頁抓下來的圖，另外 3 張（`banner.png`、`landscape.jpg`、`icon.png`）是程式產生的，刻意做成有透明（RGBA）、很大、很小。重建：`python tools/build_fixtures.py images`（約 50 秒，需要網路與 Pillow）。重建後請核對各檔寫死的數字（見下方「標準答案」）。
- 實測環境：Pillow 12.3、macOS。練習用到的都是 Pillow 10 以後穩定的 API。

## 標準答案（寫死在練習與作業裡的數字）

- 圖庫頁 `<img>` 共 17 個；真的能下載成圖片的 15 個；下載統計：第一次 `{"ok": 15, "skipped": 0, "failed": 2}`，第二次 `{"ok": 0, "skipped": 15, "failed": 2}`。
- 封面評分：`One` 4 本（02、03、06、10）、`Two` 1 本（11）、`Three` 2 本（01、08）、`Four` 4 本（04、07、09、12）、`Five` 1 本（05）。
- 尺寸：`cover_01.jpg` 318×395（31,047 bytes）、`banner.png` 1200×400（RGBA）、`landscape.jpg` 1600×900、`icon.png` 64×64（RGBA）。
- 作業：先問大小再下載，小於 40,000 bytes 的共 11 張（排除封面 06、07、09、11）；縮到最大寬度 600 後 `landscape.jpg` 為 600×338、`banner.jpg` 為 600×200；最大的檔案是 `cover_11.jpg`（62.5 KB）；12 張封面平均寬度 260.5。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 10；成果預覽：一張封面變縮圖 | learning 01 |
| 15–40 | 圖片是 bytes；HEAD 只問標頭；找圖片網址（相對路徑、懶載入）；取出檔名 | learning 02–04 |
| 40–65 | 單張下載（404 與「回 200 的假圖」）；批次下載與略過已存在的檔案 | learning 05–06 |
| 65–75 | 串流下載大檔案；下載 CSV | learning 07–08 |
| 75–85 | 休息與環境排錯（確認 Pillow 已安裝） | |
| 85–110 | ⭐ Core、⭐⭐ Practice 前半：bytes、存檔、找網址、檔名、單張與批次下載 | exercises 1–6 |
| 110–135 | Pillow：看資訊、`thumbnail`／`resize`／`fit`、JPEG 品質、透明與 RGBA | learning 09–11 |
| 135–160 | ⭐⭐ Practice 後半：資訊與縮圖；老師示範整理資料夾與縮圖牆 | exercises 7–8、learning 12–13 |
| 160–170 | ⭐⭐⭐ Challenge（進度快的學員）：整理資料夾、縮圖牆 | exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson11_learning.ipynb`：14 個教學單元，分 A（下載圖片）、B（大檔案與其他檔案）、C（用 Pillow 處理圖片）三段。
- `lesson11_exercises.ipynb`：10 題分級練習，每題最後的 `assert` 自我檢查。
- `lesson11_solutions.ipynb`：教師解答（不進 git）。
- `lesson11_homework.ipynb`：3 題課後作業；解答 `lesson11_homework_solutions.ipynb` 不進 git。
- `fixtures/gallery/`：15 張圖片與 `manifest.csv`（檔名、書名、評分、類別）。

## 常見卡點與講法

- **圖片存成壞檔**：用了 `response.text` 或用文字模式（`"w"`）寫檔。圖片要用 `response.content` 搭配 `write_bytes`／`"wb"`。
- **狀態碼 200 卻不是圖片**：很多網站圖片被移除後仍回 200 加一個網頁。所以要檢查 `Content-Type` 是否以 `image/` 開頭；事後症狀是 Pillow 丟 `UnidentifiedImageError`。
- **相對路徑**：`src="images/a.jpg"` 要用 `urljoin(頁面網址, src)`；開頭有 `/` 代表從網站根目錄算起。
- **懶載入**：`src` 是佔位圖、真正的網址在 `data-src`（也可能是 `data-original`、`data-lazy-src`）。學員會抓到 `loading.gif`，用 F12 看 `<img>` 的屬性就能發現。
- **檔名帶參數**：`url.split("/")[-1]` 會得到 `cover_02.jpg?v=3`；改用 `Path(urlparse(url).path).name`。
- **`thumbnail` 會就地修改圖片**：而且不放大、可能比框小；要保留原圖就先 `copy()`。`resize` 會變形；要剛好的尺寸又不變形用 `ImageOps.fit`（會裁掉邊緣）。
- **RGBA 存 JPEG 出錯**（`OSError: cannot write mode RGBA as JPEG`）：先貼到白底變 RGB。直接 `convert("RGB")` 能存，但透明的地方會變黑色。
- **`Image.open` 之後檔案沒關**：用 `with Image.open(...) as picture:`。Windows 上沒關檔會導致之後刪不掉、改不了。
- **有些網站不支援 HEAD**（回 405）：改用 `requests.get(url, stream=True)` 只讀標頭，不要讀內容，再關閉連線。
- **串流下載要關連線**：用 `with requests.get(..., stream=True) as response:`。
- **Windows 檔名不能有 `\ / : * ? " < > |`**：書名或標題當檔名前先 `slugify`。檔名太長也會出問題（Windows 路徑上限 260 字元）。
- **版權與流量**：圖片檔大，先看大小、設上限、控制頻率；自己分析、學習可以，重新發布別人的圖片通常不行。課堂的圖來自練習網站。

## 時間調整

- 時間不足：只做 Core 與第 5、7 題；單元 07–08（串流與 CSV）、12–13（整理資料夾與縮圖牆）改為老師示範；第 9、10 題留給作業。
- 時間充足：加做 Challenge；讓學員到 `https://books.toscrape.com/` 第一頁，找出 20 張封面縮圖的網址（`src` 是 `media/cache/...` 的相對路徑，要 `urljoin`），重做第 6 題，每張間隔 1 秒，再用第 10 題的函式做成縮圖牆。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
