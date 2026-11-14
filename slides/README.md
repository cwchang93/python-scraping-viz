# 簡報流程

簡報放在 Google Drive 資料夾 [Python 爬蟲課](https://drive.google.com/drive/folders/16N3d2nqiHb6HCiasWV_wyOQ0wlmrLxHS)。
每堂的內容寫在 `slides/lessonNN.py`，版型沿用 course_v2 的 Lesson 19 簡報。

## 已完成

| 堂次 | 主題 | 內容檔 | Google Slides |
|---|---|---|---|
| Lesson 01 | Python 語法暖身與爬蟲先備 | `lesson01.py` | [開啟](https://docs.google.com/presentation/d/18xxYAqb-RhT7QqWui7VutjjZt9ywJ0_HMtSDek3v3eE/edit) |
| Lesson 02 | 網路原理、爬蟲倫理與環境 | `lesson02.py` | [開啟](https://docs.google.com/presentation/d/1IQxZkXgyuMFdmWZ1h8gwzsZ3opc0cUvwrdlUjTpw9uo/edit) |
| Lesson 03 | requests 與 HTML 結構 | `lesson03.py` | [開啟](https://docs.google.com/presentation/d/1lppaJ-OsQ4OykK-cDkFge71Iu2Z5bnT01WloRUmZcvI/edit) |
| Lesson 04 | BeautifulSoup（一）：解析 HTML | `lesson04.py` | [開啟](https://docs.google.com/presentation/d/1cAmVWhxAz7S9_96glAecv6mIPm0kO1DwipiuCmo5fzw/edit) |
| Lesson 05 | BeautifulSoup（二）：翻頁與整站 | `lesson05.py` | [開啟](https://docs.google.com/presentation/d/1C1X4rg24Ubtk0kyXld8-orMYqQ0kxllL5tvjudp4TME/edit) |
| Lesson 06 | 爬回來的資料整理：pandas | `lesson06.py` | [開啟](https://docs.google.com/presentation/d/1YC_Oew008X3BhFpjaA2tFtKEOYL-e_4xKXjcqC6JwJE/edit) |
| Lesson 07 | 網頁資料清理 | `lesson07.py` | [開啟](https://docs.google.com/presentation/d/1xnEyQaDVpnCA52RQaJgUazxYjjqtlTIpkBzY6KQ6Hw0/edit) |
| Lesson 08 | JSON API、開放資料與登入 | `lesson08.py` | [開啟](https://docs.google.com/presentation/d/1eY9Ue3DuO6pFb8XQZlwqXzz9lQYpnUAfCajrI90sMKE/edit) |
| Lesson 09 | 動態網頁（一）：Selenium 基礎 | `lesson09.py` | [開啟](https://docs.google.com/presentation/d/19kWeR-TfuA9j6IUZlJIfbonbMGsVTFm6j6lhEJvsjeg/edit) |
| Lesson 10 | 動態網頁（二）：捲動與載入 | `lesson10.py` | [開啟](https://docs.google.com/presentation/d/1dl5X0rRt7rLik_trq_8B7x6qgRWVJ_gmmzNnB0VwL58/edit) |
| Lesson 11 | 圖片與檔案下載 | `lesson11.py` | [開啟](https://docs.google.com/presentation/d/1OhsIS52DSYGXTa-QKlitHOQkUBp7xqO2tH9GMzhaquE/edit) |

版型來源：Lesson 19 簡報，ID `1xw_J_QN45gv4TR_QvVuJJxKO3ddS4LxKxWlb4x0Ae1c`。
`l19_template_catalog.json` 記錄了版型每一頁的元素 ID 與原文。

## 新增一堂簡報

1. 在 `slides/lessonNN.py` 用 `tools/slides_kit.py` 的版型函式寫出每一頁（參考 `lesson01.py`）。
2. 產生修改請求：`python tools/slides_kit.py slides/lessonNN.py --out-dir <資料夾>`，會得到 `req_00.json` 起的多個檔案。
3. 用 Drive 複製版型簡報到課程資料夾，標題命名為 `Lesson NN｜主題`。
4. 依序把每個 `req_*.json` 的內容送給 Google Slides connector 的 `update_presentation`。
5. 讀回文字校對，並渲染縮圖檢查有沒有溢出。

## 之後只改某一頁

只改 `lessonNN.py` 裡那一頁的文字，再用 Slides connector 對該頁的文字框原地修改（`replaceAllText` 並限定 `pageObjectIds`），不需要重做整份簡報。

## 注意事項

- **替換文字要保留格式**：先 `insertText` 插入新文字，再 `deleteText` 刪除後面的舊文字範圍。若先刪光再插入，新文字會變成預設的小字深色，失去版型的樣式。
- **刪除範圍要用目前的長度**：全域替換（系列名稱、課號）會讓某些框的文字變長，計算範圍要用替換後的長度。`slides_kit.py` 已處理。
- **同一個版型用多次會自動複製**：一堂簡報裡 p5（章節頁）、p6（三張編號卡）、p21（長程式碼頁）重複使用時，`slides_kit.py` 會先複製再改。
- **貼上請求時要逐字照抄**：請求內容由人（或 AI）貼進 Slides 工具時可能打錯字（例如把「靠」寫成「靜」），套用後一定要讀回文字校對，不要只看渲染結果。貼的時候直接用中文字元，不要手動轉成 `\uXXXX`。
- **標籤框很短**：`checks5` 的標籤、`cards3_labeled` 的標籤框只放得下 4–5 個字；`slides_kit.py` 會用 `WARN` 提示可能溢出，請縮短文字再產生。
- **文字長度**：Slides 不會自動縮字。`slides_kit.py` 在新文字比版型長太多時會警告，仍要看渲染結果。
- **Slides connector 的帳號**：必須和 Drive connector 是同一個 Google 帳號，否則讀不到私人簡報。
