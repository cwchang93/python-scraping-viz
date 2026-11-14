# Python 爬蟲程式與資料視覺化開發

這是 [Python 資料分析實戰（course_v2）](../Python-Tutorial/course_v2/README.md) 的續集：把資料從網路上取回來，整理成表格，再畫成圖並發布。

## 快速入口

- 第一堂｜Python 語法暖身與爬蟲先備：[Lesson 01](lessons/lesson01_python_warmup/README.md)
- 課程自學入口與環境準備：[開始自學](lessons/lesson00_getting_started/README.md)
- 學習路徑：[LEARNING_PATH.md](LEARNING_PATH.md)
- 專案大綱：[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- 完整課綱：[COURSE_SYLLABUS.md](COURSE_SYLLABUS.md)
- 通用教學規則：[TEACHER_GUIDE.md](TEACHER_GUIDE.md)
- 第二堂：[網路原理、爬蟲倫理與環境](lessons/lesson02_network_and_environment/README.md)
- 第三堂：[requests 與 HTML 結構](lessons/lesson03_requests_and_html/README.md)
- 第四堂：[BeautifulSoup（一）：解析 HTML](lessons/lesson04_beautifulsoup_basics/README.md)
- 第五堂：[BeautifulSoup（二）：翻頁與整站](lessons/lesson05_pagination_and_csv/README.md)
- 第六堂：[爬回來的資料整理：pandas](lessons/lesson06_tidy_scraped_data/README.md)
- 第七堂：[網頁資料清理](lessons/lesson07_cleaning_scraped_data/README.md)
- 第八堂：[JSON API、開放資料與登入](lessons/lesson08_json_api_and_sessions/README.md)
- 第九堂：[動態網頁（一）：Selenium 基礎](lessons/lesson09_selenium_basics/README.md)
- 第十堂：[動態網頁（二）：捲動載入與「載入更多」](lessons/lesson10_scroll_and_load_more/README.md)
- 第十一堂：[圖片與檔案下載](lessons/lesson11_images_and_files/README.md)
- 第一堂 6 小時流程：Lesson 01 暖身、Lesson 02 完整教學、Lesson 03 核心試教；詳見 [Lesson 01](lessons/lesson01_python_warmup/README.md#第一堂-6-小時建議流程)
- 簡報流程與連結：[slides/README.md](slides/README.md)

目前進度：Lesson 01–11 的教材與簡報原始碼完成，其餘 10 堂依課綱逐堂製作。

## 課程定位

- 對象：具備 Python 基礎、想用爬蟲取得並分析網頁資料的學員；不必先完整修完 course_v2，但需依語法暖身與課程入口檢查並在需要時回補基礎
- pandas、Matplotlib 等資料分析先備能力會在後續章節用到；可依課程入口的章節對照表補課
- 節數：21 堂，每堂 3 小時
- 難度：以實作經驗為主，每堂只引入一到兩個新工具
- 產出：一份能重複執行的爬蟲程式，加上一個可公開展示的視覺化網頁
- 核心流程：看懂網頁 → 取回資料 → 解析 → 清理 → 視覺化 → 發布

## 教材約定

每堂課固定提供：

1. `README.md`：講師備課入口與 180 分鐘腳本
2. `lessonNN_learning.ipynb`：教師示範與課堂講解
3. `lessonNN_exercises.ipynb`：學生練習，不含答案，內建檢查
4. `lessonNN_solutions.ipynb`：教師解答（不進 git）
5. `lessonNN_homework.ipynb`：課後作業
6. `fixtures/`：存好的網頁快照，沒網路或網站改版時課堂照常進行

Lesson 01–11 提供 Notebook 教材，適合在 VS Code 逐格學習：

1. 用 VS Code 開啟完整教材資料夾，安裝 Python 和 Jupyter 擴充，開啟對應的 `.ipynb`。
2. 在右上角選擇課程 Python 核心；由上到下執行，先執行「設定工作資料夾」那一格。
3. 練習與作業先完成 TODO 再執行。若出現 `NameError`，確認前面建立變數的格子已執行；必要時重啟核心後依序執行。
4. Lesson 08、11 會啟動本機練習站，完成後執行最後的關閉練習站格子。

Lesson 09–10 的 Selenium Notebook 請先依序執行設定和函式定義格，再執行各示範格；每次示範會啟動並關閉瀏覽器和練習站。練習完成後執行最後的檢查格。

## 爬取範圍

課堂只爬三類來源：

1. 專為練習設計的網站（quotes.toscrape.com、books.toscrape.com）
2. 政府與機構的開放資料
3. 公開頁面，且限速、小量、只保留分析需要的欄位

每堂都會提醒：沒有網站的明確許可就不要大量抓取，也不要嘗試繞過網站的防護機制。

## 建議環境

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Python 3.10 以上即可。
