# Lesson 03–04 課前複習

建議作答時間：10–15 分鐘。請用自己的話回答；不確定的題目先寫下你記得的部分。

## Lesson 03｜requests 與 HTML

1. **HTML 結構**：觀察 `<a href="/author/Ada">Ada</a>`：標籤名稱、屬性名稱、屬性值與文字各是什麼？

2. **請求參數**：搜尋網址需要 `q=python` 和 `page=2`。請建立 `params` 字典；使用 `requests.get(url, params=params, timeout=10)` 時，這些參數會放在哪裡？本題不連網。

3. **狀態碼與例外**：請說明 `raise_for_status()` 的用途，以及發生 timeout 或收到 403 時，程式應該如何處理。

4. **回傳值與失敗處理**：假設 `fetch(url)` 失敗時回傳 `None`，為什麼呼叫端要先檢查結果，再使用 `response.text`？

## Lesson 04｜BeautifulSoup

5. **建立 BeautifulSoup**：用 `BeautifulSoup` 和 `html.parser` 解析下方 HTML，再找出第一個 `h1` 的文字。

6. **單一與多個元素**：`find` / `select_one` 和 `find_all` / `select` 的回傳結果有什麼不同？找不到元素時，各會得到什麼？

7. **CSS 選擇器**：請選出所有 `div.quote` 裡的 `span.text`，再將去除前後空白的文字存成 list。

8. **取屬性與缺值**：取得連結的 `href`。如果屬性不存在，`tag["href"]` 和 `tag.get("href")` 有什麼差別？如果找不到 `a` 元素，又要先檢查什麼？

9. **整理成資料**：把下方每一則名言整理成含 `text`、`author` 的字典，放進 list。
