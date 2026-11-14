"""Lesson 02 slide content. Build with: python tools/slides_kit.py slides/lesson02.py --out-dir <dir>"""

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

LESSON = "02"
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
        "先把爬蟲想成一位訪客",
        "Python 程式像一位\n受邀來訪的客人。",
        "程式依地址敲門，請求公開資料。屋主回覆後，程式讀取允許的內容，不闖入屋裡。",
    ),
    flow5(
        "網頁怎麼來",
        "訪客從找到地址到收到資料，會經過五步",
        [
            ("找到門牌", "URL｜要去哪戶人家"),
            ("找到門牌位置", "DNS｜查到伺服器位置"),
            ("到門口敲門", "Request｜提出資料請求"),
            ("屋主回覆", "Response｜同意、轉址或拒絕"),
            ("收到資料", "HTML｜程式讀取的網頁內容"),
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
        "HTTP 回覆",
        "狀態碼像屋主對訪客的答覆",
        [
            ("200｜同意回覆", "屋主交付你詢問的資料，可以閱讀。"),
            ("301／302｜搬家", "屋主留下新地址或暫時轉址；跟著正式指示前往。"),
            ("拒絕、找不到或暫停", "403 拒絕；404 不存在；429 太頻繁先停；500 服務故障稍後再試。"),
        ],
    ),
    checks5(
        "F12 Network：看請求和屋主回覆",
        [
            ("Request URL", "這次敲的是哪一戶、哪個房間"),
            ("Method", "GET 是詢問；POST 是送資料"),
            ("Status Code", "屋主答覆：200、403、404……"),
            ("Content-Type", "資料格式：HTML 網頁或 JSON 欄位"),
            ("Response", "屋主實際交回來的內容"),
        ],
    ),
    cards4(
        "資料入口",
        "有 API，為什麼不必解析 HTML？",
        [
            ("HTML 網頁", "像屋主給訪客看的型錄；資料混在版面裡，要自己找。"),
            ("API 授權窗口", "像屋主開好的取件窗口；欄位清楚，直接取指定資料。"),
            ("少走繞路", "不用開瀏覽器找按鈕、翻頁，再從網頁裡找欄位。"),
            ("權限有範圍", "API 仍是程式請求；只取授權資料，照規則控制頻率。"),
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
        "屋主的回覆",
        "程式收到回覆後，先看這三樣",
        [
            ("status_code", "屋主答覆的代碼：成功、拒絕或找不到。"),
            ("headers", "回覆標籤：告訴你內容格式、編碼。"),
            ("text", "讀得到的頁面文字，像屋主交來的資料單。"),
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
        "門口告示與訪客名牌",
        ("到訪前", "讀門口告示", "robots.txt 像區域提醒，不等於授權；仍要遵守服務條款。", "不確定，就先不要進。"),
        ("敲門時", "說明程式來意", "User-Agent 標明程式，像訪客名牌；timeout、sleep 控制頻率。", "別偽裝成別人。"),
        src="p9",
    ),
    checks5(
        "我的爬取守則：五件事",
        [
            ("先找資料窗口", "有 API 或開放資料，先走授權入口。"),
            ("遵守門口規則", "看 robots.txt、服務條款和明確授權。"),
            ("少敲幾次門", "設定 timeout，請求之間加 time.sleep。"),
            ("只拿允許的資料", "只取分析需要、而且有權使用的欄位。"),
            ("屋主拒絕就停", "403／429 被拒或過快就停；404 核對地址。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能用 Python 抓回一頁、存成檔案，\n也知道哪些事不能做。",
        "完成：看懂請求流程＋requests.get＋存檔＋爬取守則",
    ),
]
