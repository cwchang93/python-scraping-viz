"""Lesson 04 slide content. Build with: python tools/slides_kit.py slides/lesson04.py --out-dir <dir>"""

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

LESSON = "04"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "BeautifulSoup（二）：翻頁與整站",
        "從一頁到整站：1000 本書存成 CSV",
        "50\n頁",
        "整站\n爬取",
        "解析 → 下一頁 → 休息 → 記錄 → 存檔",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("解析一本書", "書名、價格、評分、庫存、連結。"),
            ("自動翻頁", "找下一頁，抓到最後一頁停下。"),
            ("有禮貌地抓", "sleep 與 logging，留下紀錄。"),
            ("存成 CSV", "list of dict 寫檔，再讀回驗證。"),
        ],
    ),
    statement(
        "會抓一頁，不等於會抓整站",
        "翻頁、相對網址與紀錄，\n決定爬蟲能不能穩定跑完。",
        "50 頁、1000 本書，程式要自己走完全程。",
    ),
    flow5(
        "整站爬取",
        "一頁一頁走，直到沒有下一頁",
        [
            ("抓一頁", "fetch\n加 sleep"),
            ("解析書本", "parse_\nbooks"),
            ("找下一頁", "li.next a\nurljoin"),
            ("記錄進度", "logging\n第 N 頁"),
            ("存成 CSV", "Dict\nWriter"),
        ],
    ),
    section(
        "A",
        "解析一本書",
        "標題、價格、評分、庫存，每個欄位都要整理過。",
        "字串先變成數字，才能比大小。",
    ),
    code(
        "一本書的資料在哪裡？",
        "PYTHON",
        'pod = soup.select_one("article.product_pod")\nlink = pod.select_one("h3 a")\n\nprint(link["title"])\nprint(pod.select_one("p.price_color").get_text())\nprint(pod.select_one("p.star-rating")["class"])',
        "三個陷阱",
        "書名要取 title 屬性\n\n價格是 £ 開頭的字串\n\n評分在 class 的第二個字",
        note="h3 a 的文字會被截短。",
        src="p15",
    ),
    cards3_labeled(
        "三種欄位，三種整理",
        [
            ("價格", "字串轉數字", "\"£51.77\" 去掉 £，轉成 51.77。"),
            ("評分", "英文字轉數字", "class 的 Three 對照成 3。"),
            ("連結", "相對轉完整", "用 urljoin 組出完整網址。"),
        ],
        kicker="欄位整理",
    ),
    compare2(
        "£ 變成 Â£，是編碼的問題",
        ("response.text", "用 ISO-8859-1 解碼", "網站沒宣告編碼，requests 預設用 ISO-8859-1，£ 會變成 Â£。", "Â£12.84"),
        ("response.content", "交給 BeautifulSoup", "它會讀網頁裡的 meta charset，自己判斷成 utf-8。", "£12.84"),
        src="p12",
    ),
    section(
        "B",
        "翻頁與相對網址",
        "找到下一頁，組成完整網址，最後一頁就停。",
        "測試時，永遠先設 max_pages。",
        src="p11",
    ),
    code(
        "urljoin：組出完整網址",
        "PYTHON",
        'from urllib.parse import urljoin\n\nhome = "https://books.toscrape.com/"\nprint(urljoin(home, "catalogue/page-2.html"))\n\npage2 = home + "catalogue/page-2.html"\nprint(urljoin(page2, "page-3.html"))',
        "為什麼不自己拼",
        "首頁的連結從 catalogue 開始\n\n第 2 頁的連結只有檔名\n\nurljoin 依目前頁面判斷",
        note="一律 urljoin(目前網址, href)。",
        src="p19",
    ),
    cards3_numbered(
        "翻頁",
        "翻頁迴圈的三個判斷",
        [
            ("找下一頁", "select_one(\"li.next a\") 取 href。"),
            ("組完整網址", "urljoin(目前網址, href)。"),
            ("找不到就停", "最後一頁沒有按鈕，回傳 None。"),
        ],
    ),
    code(
        "crawl_books：整站爬取迴圈",
        "PYTHON",
        'def crawl_books(start_url, max_pages=3, delay=1.0):\n    all_books, url, n = [], start_url, 0\n    while url and (max_pages is None or n < max_pages):\n        response = fetch(url)\n        if response is None:\n            break\n        n += 1\n        all_books += parse_books(response.content, url)\n        url = find_next_url(response.content, url)\n        if url:\n            time.sleep(delay)\n    return all_books',
        "三個設計",
        "條件看下一頁與頁數上限\n\n失敗就停止，不硬撐\n\n每頁之間 sleep",
        note="全站約 3 分鐘，先用 3 頁。",
        src="p21",
    ),
    section(
        "C",
        "紀錄與存檔",
        "跑很久的爬蟲，要留下紀錄，也要把結果存起來。",
        "紀錄檔是事後唯一的線索。",
    ),
    compare2(
        "print 與 logging",
        ("print", "只在畫面上看", "沒有時間、沒有等級，關掉視窗就消失了。", "適合隨手檢查"),
        ("logging", "有等級、有時間、能存檔", "INFO、WARNING 分開記，還能同時寫進檔案。", "適合爬蟲"),
        src="p10",
    ),
    code(
        "logging 與 CSV 的基本寫法",
        "PYTHON",
        'logging.basicConfig(\n    level=logging.INFO,\n    format="%(asctime)s %(levelname)s %(message)s",\n)\nlogger = logging.getLogger("books")\nlogger.info("第 %d 頁：%d 本", 1, 20)\n\nwith open(path, "w", newline="", encoding="utf-8-sig") as f:\n    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)\n    writer.writeheader()\n    writer.writerows(rows)',
        "存 CSV 的細節",
        "newline 設空字串\n\nutf-8-sig 讓 Excel 不亂碼\n\n讀回來都是字串",
        note="讀回也要用 utf-8-sig。",
        src="p21",
    ),
    cards3_numbered(
        "驗證",
        "存完之後，一定要讀回來看",
        [
            ("數筆數", "讀回的筆數要等於抓到的筆數。"),
            ("看欄位", "標頭與欄位順序是否正確。"),
            ("抽查幾筆", "價格、書名、網址有沒有亂碼。"),
        ],
        src="p6",
    ),
    checks5(
        "整站爬蟲的檢查清單",
        [
            ("設上限", "測試永遠先設 max_pages。"),
            ("有禮貌", "timeout、sleep、自訂 User-Agent。"),
            ("會停下", "找不到下一頁，或抓取失敗就停。"),
            ("有紀錄", "每頁記一行，失敗記 WARNING。"),
            ("存完驗證", "筆數與欄位要對得上。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能讓程式自己翻頁，\n把整個書店存成一份 CSV。",
        "完成：解析＋urljoin＋翻頁迴圈＋logging＋CSV",
    ),
]
