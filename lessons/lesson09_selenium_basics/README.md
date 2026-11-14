# Lesson 09｜動態網頁（一）：Selenium 基礎

## 學習成果

- 能說明 requests 為什麼看不到 JavaScript 產生的內容，以及 Selenium 如何解決。
- 能啟動與關閉 Chrome（有視窗與無頭模式），並用 `with` 確保瀏覽器一定關閉。
- 能用 `find_element`、`find_elements` 配合 CSS 選擇器找元素，取文字與屬性。
- 能點擊、輸入文字、登入、截圖，並讀取登入後的資料。
- 能用 `WebDriverWait` 搭配 `expected_conditions` 做明確等待，說明為什麼不該用固定的 `time.sleep`。
- 能把 `driver.page_source` 交給 BeautifulSoup，接上前面學的解析與整理。

## 課前準備

- 學員電腦已安裝 **Google Chrome**（最新版）。第一次執行時，Selenium 會自動下載對應版本的 chromedriver，**需要網路**；公司或學校網路若擋下載，請老師事先在教室準備好。
- 執行 `python -m pip install -r requirements.txt` 確認 `selenium` 已安裝。
- 本堂使用 Notebook：先執行設定及函式定義格，再執行各示範格；各次示範結束會關閉瀏覽器與練習站。
- 所有頁面都在本機練習站（`tools/practice_site.py`），程式自動啟動，不需要外部網路。測試帳號密碼定義在該檔案，只對本機練習站有效。
- 開課前跑一次 `python tools/validate_lessons.py --lesson 08 --run`（無頭模式，約 10 秒）。
- 實測環境：Selenium 4.50、Chrome 154、macOS。Windows 與 Linux 請在開課前實際執行一次。

## 180 分鐘腳本

| 時間 | 教學活動 | 教材 |
|---|---|---|
| 0–15 | 回顧 Lesson 08；成果預覽：瀏覽器看到 6 個項目 | learning 01 |
| 15–45 | requests 看不到、Selenium 看得到；啟動與關閉；找元素 | learning 02–05 |
| 45–75 | 點擊、輸入、登入；**等待**（本堂重點） | learning 06–09 |
| 75–85 | 休息與環境排錯（Chrome、chromedriver 常卡在這裡） | |
| 85–120 | ⭐ Core：標題、JavaScript 清單、導覽列、搜尋 | exercises 1–4 |
| 120–150 | ⭐⭐ Practice：登入、錯誤訊息、讀訂單、明確等待 | exercises 5–8 |
| 150–170 | 截圖、錯誤處理；⭐⭐⭐ Challenge：渲染後交給 BeautifulSoup、搜尋並截圖 | learning 10–11、exercises 9–10 |
| 170–180 | Exit Ticket、作業說明、下堂預告 | homework |

## 教材檔案

- `lesson09_learning.ipynb`：先執行設定與函式定義，再執行各示範格。
- `lesson09_exercises.ipynb`：10 題，每題一個函式；完成各題後執行最後的檢查格，顯示 PASS 或 FAIL。
- `lesson09_solutions.ipynb`：教師解答（不進 git）。
- `lesson09_homework.ipynb`：3 題課後作業，同樣自動評分。
- `fixtures/delayed_rendered.html`：瀏覽器渲染完成後的 HTML 快照，用來說明 `page_source`。

## 常見卡點與講法

- **讀到舊頁面（最常見）**：點擊或送出表單後，新頁面可能還沒載入完，程式就往下執行，讀到的是舊頁面的內容，而且**時好時壞**。解法是明確等待：等網址變了（`EC.url_contains`）或新元素出現（`EC.presence_of_element_located`），再讀資料。本堂的練習設計成不等待就會偶爾失敗，請當成教學機會。
- **`send_keys(Keys.ENTER)` 與 `click()`**：兩者都不保證等到新頁面載入，都要搭配明確等待。
- **`time.sleep` 為什麼不好**：等太短會失敗，等太長浪費時間；明確等待條件一成立就繼續。
- **`find_element` 與 `find_elements`**：前者找不到會丟 `NoSuchElementException`，後者回傳空 list。
- **`NoSuchElementException`**：先確認選擇器（F12），再確認元素是不是還沒出現（要不要等待）。
- **`StaleElementReferenceException`**：換頁後，先前找到的元素已失效，要重新找。
- **瀏覽器視窗沒關**：程式出錯中斷時，用 `with` 或 `try / finally` 才能保證關閉；已殘留的可以在工作管理員（Windows）或活動監視器（macOS）結束 Chrome 與 chromedriver。
- **chromedriver 下載失敗**：確認網路；公司網路可能擋 `googlechromelabs.github.io` 與 `storage.googleapis.com`。
- **要看到瀏覽器動作**：不要設定 `HEADLESS=1`；上課時建議一律有視窗，學員才看得到程式在做什麼。
- **爬取守則仍然適用**：Selenium 比 requests 更像真人，更要遵守網站規則與頻率限制，不示範繞過防護。

## 時間調整

- 時間不足：只做 Core 與第 5、8 題；截圖與錯誤處理改為老師示範。
- 時間充足：加做 Challenge；讓學員用公開的練習網頁 `https://quotes.toscrape.com/js/` 重做第 2 題，確認 requests 找不到、Selenium 找得到。

## 課後紀錄

- 實際進度：
- 常見問題：
- 下次調整：
