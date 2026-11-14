# Lesson 01｜Python 語法暖身與爬蟲先備

這堂是第一堂的暖身練習，幫大家喚回寫爬蟲會用到的 Python 基礎。先自己完成 Learning Exercise，再用 Solutions 對答案。建議先完成 Core；有餘裕再做 Practice 與 Challenge。


## 本章學習地圖

**複習基礎** → **練習爬蟲常用寫法** → **完成練習**

| 階段 | 會用到的語法或工具 | 完成後能做什麼 |
|---|---|---|
| ⭐ Core 1–5 | 變數、`float()`、字串方法、`if / else`、list 索引與切片、dict `.get()` | 轉換價格、清理文字、判斷狀態碼與取出資料 |
| ⭐⭐ Practice 6–10 | `for`、條件篩選、`def / return`、字串搜尋、`try / except` | 逐筆整理資料、撰寫函式並處理資料缺漏 |
| ⭐⭐⭐ Challenge 11–15 | 網址拆解、字串計數、`requests`、`timeout` 與狀態碼 | 認識爬蟲資料流程；第 13 題連網請求為選做 |

**課堂產出：**先完成 Core，再依時間挑戰 Practice 與 Challenge；執行每題並觀察提示。這一堂以 Colab 語法暖身為主。

## 學習目標

- 喚回變數、型別、字串、條件、list、dict、迴圈與函式。
- 練習錯誤處理、網址拆解、HTML 字串搜尋、requests 回應與儲存檔案。
- 知道 `timeout`、狀態碼與請求間隔在爬蟲中的用途。

## 練習方式

1. 開啟 `lesson01_learning.ipynb`，依序完成 Learning Exercise 區塊。
2. 每題先預測結果，再執行並依提示修正。
3. 全部完成後再看 `lesson01_solutions.ipynb`。

本堂練習使用內建資料與練習網站快照，不需大量連網；第 13 題為選擇性單次請求。不要對網站連續或大量請求。

## 第一堂 6 小時建議流程

| 時間 | 活動 | 目標 |
|---|---|---|
| 00:00–00:15 | 開場、快速診斷熟悉度 | 了解大家忘記哪些語法，不逐項重講。 |
| 00:15–01:00 | Lesson 01：完成 15 題 Learning Exercise | 學員先獨立嘗試；講師記下共通卡點，視情況挑題討論。 |
| 01:00–01:10 | 休息 |  |
| 01:10–04:10 | Lesson 02：網路原理、爬蟲倫理與環境 | 依 Lesson 02 README 的 180 分鐘教學腳本完整進行。 |
| 04:10–04:20 | 休息 |  |
| 04:20–05:50 | Lesson 03 試教：HTML 結構與 requests | 示範 HTML 標籤／屬性、一次 GET、timeout、狀態碼與回應；做到可理解的核心即可。 |
| 05:50–06:00 | Exit ticket 與作業說明 | 確認學員能說出下一步要怎麼從回應中找到資料。 |

若暖身發現多數人連 Core 題也不熟，先一起講解幾題並縮短 Lesson 03 試教；Lesson 02 的實作與練習優先保留。Lesson 03 後續再完整教，不必第一天趕完。

## 檔案

- `lesson01_learning.ipynb`：15 題學員練習，依 Core、Practice、Challenge 分級。
- `lesson01_solutions.ipynb`：完整參考解答。

