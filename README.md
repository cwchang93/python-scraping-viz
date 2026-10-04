# Python 爬蟲程式與資料視覺化開發

這是 [Python 資料分析實戰（course_v2）](../Python-Tutorial/course_v2/README.md) 的續集：把資料從網路上取回來，整理成表格，再畫成圖並發布。

## 快速入口

- 完整課綱：[COURSE_SYLLABUS.md](COURSE_SYLLABUS.md)
- 通用教學規則：[TEACHER_GUIDE.md](TEACHER_GUIDE.md)
- 第一堂：[網路原理、爬蟲倫理與環境](lessons/lesson01_network_and_environment/README.md)
- 第二堂：[requests 與 HTML 結構](lessons/lesson02_requests_and_html/README.md)
- 簡報流程與連結：[slides/README.md](slides/README.md)

目前進度：Lesson 01、02 的教材與簡報完成，其餘 18 堂依課綱逐堂製作。

## 課程定位

- 對象：已完成 course_v2（Python 基礎、pandas、Matplotlib）的學員
- 節數：20 堂，每堂 3 小時
- 難度：以實作經驗為主，每堂只引入一到兩個新工具
- 產出：一份能重複執行的爬蟲程式，加上一個可公開展示的視覺化網頁
- 核心流程：看懂網頁 → 取回資料 → 解析 → 清理 → 視覺化 → 發布

## 教材約定

每堂課固定提供：

1. `README.md`：講師備課入口與 180 分鐘腳本
2. `lessonNN_learning.py`：教師示範與課堂講解
3. `lessonNN_exercises.py`：學生練習，不含答案，內建 `assert` 自我檢查
4. `lessonNN_solutions.py`：教師解答（不進 git）
5. `lessonNN_homework.py`：課後作業
6. `fixtures/`：存好的網頁快照，沒網路或網站改版時課堂照常進行

`.py` 檔使用 `# %%` 分格格式。在 VS Code 安裝 Python 與 Jupyter 擴充後，每格上方會出現 Run Cell，用法和 notebook 相同，但檔案是純文字，方便版本控制。

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
