# Lesson 01–02 課前複習

建議作答時間：5–8 分鐘。請用自己的話回答；不確定的題目先寫下你記得的部分。

## Lesson 01｜Python 基礎

1. `price_text = "120"` 是文字。要計算含稅價格，為什麼要先把它轉成數字？可以用哪個函式？

2. `title = "  Python   爬蟲  "`。要去掉前後空白，並把中間連續空白整理成一格，你會用什麼方法？

3. 程式檢查 `status_code`：200 代表成功、404 代表找不到。為什麼這裡適合用 `if / else`？

4. `author = book.get("author", "未知作者")` 做了什麼？如果直接用 `book["author"]`，欄位不存在時可能發生什麼事？

5. 函式中的 `return result` 和 `print(result)` 有什麼不同？

## Lesson 02｜網路與請求

6. 看網址 `https://example.com/search?q=python&page=2`：主機、路徑和查詢參數各是哪一段？

7. 用 `requests.get(url)` 抓網頁時，程式送出什麼、又收到什麼？`requests` 會替我們打開瀏覽器畫面嗎？

8. HTTP 狀態碼 200、404 和 429 各代表什麼？遇到 429 時應該怎麼做？

9. `response.text` 和 `response.content` 有什麼差別？要原樣把網頁存成檔案時，通常用哪一個？

