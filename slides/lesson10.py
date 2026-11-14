"""Lesson 10 slide content. Build with: python tools/slides_kit.py slides/lesson10.py --out-dir <dir>"""

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

LESSON = "10"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "動態網頁（二）：捲動與按鈕",
        "讓程式自己捲、自己按，直到資料全部出現",
        "捲動\n載入",
        "按鈕 XPath\nAPI 資料",
        "捲動 → 等待 → 重複 → 解析 → 存檔",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("自動捲動", "用 JavaScript 捲到底，載入更多。"),
            ("等待與停止", "等新資料出現，再決定要不要繼續。"),
            ("按鈕與 XPath", "按「載入更多」，用 XPath 找元素。"),
            ("整理與找 API", "存成 CSV，並找出背後的 API。"),
        ],
    ),
    statement(
        "第一批之後的資料，要靠動作觸發",
        "捲到底、按下按鈕，\n網頁才會去要下一批。",
        "程式要替人做這些動作，直到沒有新資料為止。",
    ),
    flow5(
        "捲動載入的流程",
        "捲、等、檢查，重複到結束",
        [
            ("打開網頁", "get\n(url)"),
            ("捲到底", "scroll\nTo"),
            ("等新資料", "Wait\nlambda"),
            ("檢查結束", "end\nmarker"),
            ("取資料", "page_\nsource"),
        ],
    ),
    section(
        "A",
        "捲動載入",
        "用 execute_script 捲到底，等新資料出現。",
        "迴圈一定要有停止條件與次數上限。",
    ),
    code(
        "捲到底，並等新文章出現",
        "PYTHON",
        'before = post_count(driver)\n\ndriver.execute_script(\n    "window.scrollTo(0, document.body.scrollHeight)"\n)\nWebDriverWait(driver, 5).until(\n    lambda d: post_count(d) > before\n)',
        "三個重點",
        "execute_script 下 JavaScript\n\n捲完要等新資料\n\n用 lambda 寫等待條件",
        note="先數、再捲、再等。",
        src="p15",
    ),
    compare2(
        "兩種停止的方法",
        ("看結尾提示", "出現「已載入全部」就停", "最快，但網頁要真的有提示。", "較快"),
        ("等不到新資料", "等 3 秒沒有新文章就停", "到哪個網站都能用，但最後要多等一次。", "通用"),
        src="p12",
    ),
    cards3_labeled(
        "捲動與按鈕的三種動作",
        [
            ("捲底", "scrollTo", "捲到頁面最底，觸發載入。"),
            ("對準", "scrollIntoView", "把某個元素捲進畫面。"),
            ("按鈕", "click", "按「載入更多」取得下一批。"),
        ],
        kicker="動作",
    ),
    section(
        "B",
        "停止、按鈕與 XPath",
        "看到結尾、找到目標、按鈕消失，都是停止條件。",
        "找到目標就停，少載入就少請求。",
        src="p11",
    ),
    code(
        "按「載入更多」，直到按鈕消失",
        "PYTHON",
        'while driver.find_elements(By.ID, "load-more"):\n    before = post_count(driver)\n    driver.find_element(\n        By.ID, "load-more"\n    ).click()\n    WebDriverWait(driver, 5).until(\n        lambda d: post_count(d) > before\n    )',
        "三個設計",
        "按鈕還在，就代表還有資料\n\n按完要等數量增加\n\n按鈕消失，迴圈結束",
        note="用 find_elements 檢查，不會出錯。",
        src="p19",
    ),
    cards3_numbered(
        "停止",
        "三種停止的條件",
        [
            ("看結尾提示", "出現「已載入全部」就停，最快。"),
            ("等不到新資料", "等幾秒都沒有新的，就當作到底。"),
            ("找到目標", "需要的資料出現了，就提早停止。"),
        ],
    ),
    compare2(
        "CSS 與 XPath",
        ("CSS", "短，你已經會", "依 class、id、標籤找，大多數情況夠用。", "優先使用"),
        ("XPath", "依文字、找父層", "例如 //button[text()='載入更多']。", "需要時再用"),
        src="p20",
    ),
    code(
        "渲染完成後，整理成表格並存檔",
        "PYTHON",
        'soup = BeautifulSoup(driver.page_source, "html.parser")\nrows = [\n    {"id": int(a["data-id"]),\n     "title": a.select_one("h3").get_text(strip=True)}\n    for a in soup.select("article.post")\n]\ndf = pd.DataFrame(rows)\ndf.to_csv("output/feed.csv", index=False)',
        "三個設計",
        "捲完才解析一次\n\npage_source 交給 bs4\n\n再轉成 DataFrame",
        note="前面學的整理都能接上。",
        src="p21",
    ),
    section(
        "C",
        "找 API 與守則",
        "網頁其實是向 API 要資料，找到它就不用開瀏覽器。",
        "同樣 60 篇，API 比 Selenium 快得多。",
        src="p5",
    ),
    cards3_numbered(
        "找 API",
        "找出網頁背後的 API",
        [
            ("看請求", "F12 的 Network，只看 Fetch/XHR。"),
            ("找規律", "offset、limit 是翻頁的參數。"),
            ("改用 requests", "一頁一頁呼叫，直到沒有下一頁。"),
        ],
        src="p6",
    ),
    compare2(
        "Selenium 捲動與呼叫 API",
        ("Selenium 捲動", "要開瀏覽器", "受視窗大小與渲染時機影響，比較慢。", "最後的選擇"),
        ("呼叫 API", "直接要資料", "不用瀏覽器，又快又穩。", "優先選擇"),
        src="p9",
    ),
    checks5(
        "捲動與載入的檢查清單",
        [
            ("有停止條件", "看結尾、按鈕消失，或找到目標。"),
            ("有次數上限", "迴圈最多跑 N 次，避免停不下來。"),
            ("捲完要等", "用 lambda 等新資料，不用 sleep。"),
            ("先找 API", "找得到，就用 requests。"),
            ("控制數量", "先決定要幾筆，達到就停。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能讓程式自己捲動、按按鈕，\n直到資料全部載入。",
        "完成：捲動＋等待＋停止條件＋XPath＋API",
    ),
]
