"""Lesson 01 slide content. Build with: python tools/slides_kit.py slides/lesson01.py --out-dir <dir>"""

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

LESSON = "01"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "網路原理、爬蟲倫理與環境",
        "看懂網頁怎麼來，再用 Python 抓回第一頁",
        "HTTP\nGET",
        "從瀏覽器\n走到程式",
        "網址 → 請求 → 回應 → HTML → 存檔",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("看懂請求", "能說出網址、請求、回應與 HTML 的關係。"),
            ("抓回一頁", "用 requests.get 取得網頁並檢查狀態碼。"),
            ("存成檔案", "把網頁原樣存成 HTML，再讀回來。"),
            ("守則一份", "寫下自己會遵守的爬取規則。"),
        ],
    ),
    statement(
        "爬蟲到底在做什麼？",
        "爬蟲就是用程式，\n代替瀏覽器去要網頁。",
        "瀏覽器會畫出畫面；程式只需要 HTML 裡的資料。",
    ),
    flow5(
        "網頁怎麼來",
        "打開一個網頁，背後走了五步",
        [
            ("輸入網址", "URL\n網址"),
            ("找伺服器", "DNS\n找位置"),
            ("送請求", "request\nGET"),
            ("收回應", "response\nHTML"),
            ("畫畫面", "爬蟲不需\n要這一步"),
        ],
    ),
    section(
        "A",
        "網路怎麼運作",
        "先看懂瀏覽器做了什麼，爬蟲才知道要模仿哪一步。",
        "把每一步看得見，才知道程式要做什麼。",
    ),
    cards3_labeled(
        "網址可以拆成三個部分",
        [
            ("主機", "找哪一台伺服器", "例：quotes.toscrape.com"),
            ("路徑", "找哪一頁", "例：/tag/love/page/2/"),
            ("查詢", "附帶的條件", "例：?sort=new。用 urlparse 可以拆開。"),
        ],
        kicker="URL",
    ),
    cards3_numbered(
        "狀態碼",
        "看到狀態碼，先判斷發生什麼事",
        [
            ("200 成功", "可以繼續解析網頁內容。"),
            ("403、404", "被拒絕，或是找不到頁面。"),
            ("429、500", "請求太頻繁，或網站出錯。"),
        ],
    ),
    checks5(
        "用 F12 的 Network，看五個欄位",
        [
            ("Request URL", "這次請求的完整網址"),
            ("Method", "GET 還是 POST"),
            ("Status Code", "200、404、403……"),
            ("Content-Type", "回來的是 HTML 還是 JSON"),
            ("Response", "實際收到的內容"),
        ],
    ),
    section(
        "B",
        "動手抓一頁",
        "先建好環境，再用幾行程式抓回第一個網頁。",
        "看到 200，才進下一步。",
        src="p11",
    ),
    code(
        "第一步：建立虛擬環境並安裝 requests",
        "TERMINAL",
        "python -m venv .venv\nsource .venv/bin/activate\npython -m pip install requests",
        "先確認三件事",
        "1. .venv 資料夾出現\n\n2. 終端機前面有 (.venv)\n\n3. 顯示 Successfully installed",
        note="Windows：.venv\\Scripts\\Activate.ps1",
        src="p16",
    ),
    code(
        "requests.get：抓回第一頁",
        "PYTHON",
        'import requests\n\nurl = "https://quotes.toscrape.com/"\nresponse = requests.get(url, timeout=10)\n\nprint(response.status_code)\nprint(len(response.text))',
        "三個重點",
        "get：送出請求\n\ntimeout：最多等 10 秒\n\nstatus_code：先看結果",
        note="先看狀態碼，再看內容。",
        src="p15",
    ),
    cards3_numbered(
        "Response",
        "Response 物件的三個重點欄位",
        [
            ("status_code", "200 代表成功。"),
            ("headers", "Content-Type 說明內容格式。"),
            ("text", "解碼後的網頁文字。"),
        ],
        src="p6",
    ),
    code(
        "把網頁原樣存成 HTML 檔",
        "PYTHON",
        'from pathlib import Path\n\noutput_dir = Path("output")\noutput_dir.mkdir(exist_ok=True)\n\npath = output_dir / "quotes_page1.html"\npath.write_bytes(response.content)',
        "存檔三步",
        "建立 output 資料夾\n\n組出檔案路徑\n\nwrite_bytes 原樣寫入",
        note="存檔用 content，不是 text。",
        src="p19",
    ),
    compare2(
        ".text 與 .content 有什麼不同？",
        (".TEXT", "已解碼的文字", "str，方便搜尋與解析。", "response.text"),
        (".CONTENT", "原始的 bytes", "存檔時用它，內容完全不變。", "response.content"),
        src="p10",
    ),
    section(
        "C",
        "爬取守則",
        "能抓不代表可以抓：先看規則，再動手。",
        "被擋就停下來，不要想辦法繞過。",
    ),
    compare2(
        "robots.txt 與 User-Agent",
        ("抓取前", "看網站的規則", "robots.txt 列出哪些路徑不歡迎爬蟲；服務條款有最後決定權。", "不確定，就不要抓。"),
        ("請求時", "表明自己的身分", "用自訂 User-Agent 說明這是課堂練習，並設定 timeout、加上 sleep。", "有禮貌，才抓得久。"),
        src="p9",
    ),
    checks5(
        "我的爬取守則：五件事",
        [
            ("先找 API", "有開放資料或 API，就不要爬網頁。"),
            ("看規則", "robots.txt 與服務條款。"),
            ("慢慢來", "設定 timeout，加 time.sleep。"),
            ("少拿一點", "只抓分析需要的欄位。"),
            ("被擋就停", "403、429 不要繞過。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能用 Python 抓回一頁、存成檔案，\n也知道哪些事不能做。",
        "完成：看懂請求流程＋requests.get＋存檔＋爬取守則",
    ),
]
