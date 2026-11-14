"""Lesson 03 slide content. Build with: python tools/slides_kit.py slides/lesson03.py --out-dir <dir>"""

from slides_kit import (
    cards3_labeled,
    cards3_numbered,
    cards4,
    checkpoint,
    checks5,
    code,
    compare2,
    flow5,
    section,
    statement,
    title_slide,
)

LESSON = "03"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "requests 與 HTML 結構",
        "看懂網頁的結構，做出不會當掉的 fetch(url)",
        "fetch\n(url)",
        "可靠的\n抓取工具",
        "結構 → 請求 → 例外 → 函式",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("讀懂 HTML", "能說出標籤、屬性與巢狀結構。"),
            ("控制請求", "會用 params、headers 與 timeout。"),
            ("處理失敗", "轉址、編碼與例外不再讓程式當掉。"),
            ("fetch(url)", "把抓取流程包成可重複使用的函式。"),
        ],
    ),
    statement(
        "抓取程式最常見的問題是什麼？",
        "網路本來就會出狀況，\n好的爬蟲要能好好地失敗。",
        "逾時、404、亂碼、被拒絕，都是正常情況。",
    ),
    flow5(
        "請求的路徑",
        "一個請求從出發到交出結果",
        [
            ("設定請求", "params\nheaders"),
            ("送出", "get\ntimeout"),
            ("檢查", "狀態碼\n轉址"),
            ("解碼", "encoding\ntext"),
            ("交出結果", "Response\n或 None"),
        ],
    ),
    section(
        "A",
        "看懂 HTML",
        "網頁是一棵樹：標籤、屬性、巢狀。",
        "先會讀，下一堂才會取。",
    ),
    cards3_labeled(
        "HTML 的三個基本零件",
        [
            ("標籤", "決定內容的種類", "例：div、span、a。"),
            ("屬性", "附加的資訊", '例：class="quote"、href="/about"。'),
            ("巢狀", "標籤裡再放標籤", "div 裡有 span 與 a，形成一棵樹。"),
        ],
        kicker="HTML",
    ),
    code(
        "讀一則名言的 HTML",
        "HTML",
        '<div class="quote">\n  <span class="text">名言內容</span>\n  <small class="author">作者</small>\n  <a href="/author/Albert-Einstein">\n    (about)\n  </a>\n</div>',
        "找出三個資訊",
        "1. 外層 class 是 quote\n\n2. 作者在 small.author\n\n3. 連結在 a 的 href",
        note="下一堂用 BeautifulSoup 取出它們。",
        src="p15",
    ),
    section(
        "B",
        "控制請求",
        "params、headers、timeout，決定請求長什麼樣。",
        "請求由你設計，不是碰運氣。",
        src="p11",
    ),
    code(
        "params：讓 requests 組網址",
        "PYTHON",
        'import requests\n\nsearch = requests.Request(\n    "GET",\n    "https://example.com/search",\n    params={"q": "python", "page": 2},\n).prepare()\n\nprint(search.url)',
        "組出來的網址",
        "? 後面是參數\n\n& 分隔多個參數\n\n中文會自動編碼",
        note="prepare 只組網址，不送出。",
        src="p19",
    ),
    compare2(
        "headers 與 timeout",
        ("headers", "說明自己是誰", "User-Agent 與 Accept-Language 告訴網站請求來自哪裡、想要什麼語言。", "用 headers= 傳入。"),
        ("timeout", "最多等多久", "沒有 timeout，請求可能永遠卡住。每個請求都要設定。", "例：timeout=10"),
        src="p20",
    ),
    cards3_numbered(
        "狀態碼與轉址",
        "讀懂回應，決定下一步",
        [
            ("2xx 成功", "可以繼續解析網頁。"),
            ("3xx 轉址", "requests 會自動跟隨，history 記錄過程。"),
            ("4xx、5xx", "raise_for_status 會把它變成例外。"),
        ],
    ),
    compare2(
        "中文變亂碼，是編碼用錯了",
        ("亂碼", "用錯編碼讀 bytes", "big5 的網頁用 utf-8 讀，中文就變成問號。", "不是網站壞掉"),
        ("還原", "指定正確的編碼", "設定 response.encoding 為 big5，再讀 response.text。", "bytes → 文字"),
        src="p12",
    ),
    section(
        "C",
        "包成函式",
        "把重複的步驟打包，失敗時也不會讓程式當掉。",
        "失敗是正常情況，要有處理辦法。",
    ),
    code(
        "fetch(url)：可重複使用的抓取函式",
        "PYTHON",
        'def fetch(url, params=None, timeout=10):\n    headers = {"User-Agent": USER_AGENT}\n    try:\n        response = requests.get(\n            url, params=params,\n            headers=headers, timeout=timeout)\n        response.raise_for_status()\n    except requests.RequestException as error:\n        print("抓取失敗：", type(error).__name__)\n        return None\n    return response',
        "三個設計",
        "成功回傳 Response\n\n失敗印出原因、回傳 None\n\n呼叫端要檢查 None",
        note="失敗是正常情況。",
        src="p21",
    ),
    cards3_numbered(
        "禮貌",
        "連續抓取要有禮貌",
        [
            ("sleep", "每次請求之間停一下。"),
            ("存檔", "抓完存起來，解析時不用再連網。"),
            ("小量", "先抓少數頁面確認，再擴大。"),
        ],
        src="p6",
    ),
    compare2(
        "不是每個網站都讓你抓",
        ("遇到 403", "停下來判斷", "找官方 API、開放資料或授權方式；看服務條款，沒有許可就換資料來源。", "不要重試轟炸。"),
        ("不要做", "偽裝去繞過防護", "偽裝成瀏覽器突破防護，可能違反服務條款，也不是這門課教的事。", "換資料來源。"),
        src="p9",
    ),
    checks5(
        "好用的 fetch 要有五件事",
        [
            ("帶 User-Agent", "說明自己的身分。"),
            ("設 timeout", "避免永遠卡住。"),
            ("檢查狀態碼", "raise_for_status。"),
            ("接住例外", "RequestException。"),
            ("失敗回 None", "呼叫端判斷。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我有一個不會當掉的 fetch(url)，\n失敗時也知道該怎麼辦。",
        "完成：HTML 結構＋請求控制＋編碼＋fetch(url)＋403 判斷",
    ),
]
