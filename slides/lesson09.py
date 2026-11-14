"""Lesson 09 slide content. Build with: python tools/slides_kit.py slides/lesson09.py --out-dir <dir>"""

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

LESSON = "09"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "動態網頁（一）：Selenium 基礎",
        "讓程式開啟瀏覽器，取得 JavaScript 產生的內容",
        "Chrome\n自動化",
        "點擊 輸入\n等待 截圖",
        "開啟 → 找元素 → 互動 → 等待 → 取資料",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("控制瀏覽器", "用程式開啟、關閉 Chrome。"),
            ("找到並操作", "找元素、輸入文字、點擊、登入。"),
            ("等待內容", "用明確等待取得動態內容。"),
            ("截圖與解析", "截圖，並把 HTML 交給 BeautifulSoup。"),
        ],
    ),
    statement(
        "requests 看到的，不一定是你看到的",
        "JavaScript 執行之後，\n內容才會長出來。",
        "需要瀏覽器把網頁跑完，程式才拿得到資料。",
    ),
    flow5(
        "Selenium 的流程",
        "像真人一樣操作瀏覽器",
        [
            ("啟動", "Chrome\nwith"),
            ("打開網頁", "get\n(url)"),
            ("找元素", "find_\nelement"),
            ("互動等待", "click\nWait"),
            ("取資料", "text\npage_source"),
        ],
    ),
    section(
        "A",
        "看見動態網頁",
        "同一個網址，requests 與瀏覽器看到的不一樣。",
        "先確認內容是不是 JavaScript 產生的。",
    ),
    compare2(
        "同一頁，兩種工具的結果",
        ("requests", "原始 HTML", "只拿到空的清單，找到 0 個項目。", "0 個"),
        ("Selenium", "瀏覽器執行後", "JavaScript 跑完，找到 6 個項目。", "6 個"),
        src="p12",
    ),
    code(
        "啟動與關閉瀏覽器",
        "PYTHON",
        'from selenium import webdriver\n\noptions = webdriver.ChromeOptions()\noptions.add_argument("--headless=new")\n\nwith webdriver.Chrome(options=options) as driver:\n    driver.get("http://127.0.0.1:8000/js-list")\n    print(driver.title)',
        "三個重點",
        "with 結束就會關閉瀏覽器\n\nheadless 不顯示視窗\n\n第一次需要網路",
        note="沒關閉會留下殘留程序。",
        src="p15",
    ),
    cards3_labeled(
        "找元素：三種常用的方法",
        [
            ("ID", "By.ID", "最準確，頁面上通常只有一個。"),
            ("CSS", "By.CSS_SELECTOR", "和 BeautifulSoup 的 select 完全相同。"),
            ("文字", "By.LINK_TEXT", "用連結上看到的文字。"),
        ],
        kicker="找元素",
    ),
    section(
        "B",
        "互動與等待",
        "輸入、點擊、登入，並等到內容真的出現。",
        "等待，是 Selenium 最重要的觀念。",
        src="p11",
    ),
    code(
        "輸入、點擊，並等待新頁面",
        "PYTHON",
        'box = driver.find_element(By.ID, "q")\nbox.send_keys("python")\ndriver.find_element(\n    By.ID, "search-button"\n).click()\n\nWebDriverWait(driver, 10).until(\n    EC.url_contains("q=")\n)',
        "三個動作",
        "send_keys 輸入文字\n\nclick 點擊按鈕\n\nWait 等新頁面出現",
        note="點擊之後，一定要等。",
        src="p19",
    ),
    cards3_numbered(
        "互動",
        "和頁面互動的三個動作",
        [
            ("send_keys", "在輸入框輸入文字。"),
            ("click", "點擊按鈕或連結。"),
            ("save_screenshot", "把畫面存成圖片。"),
        ],
    ),
    compare2(
        "等待的兩種做法",
        ("time.sleep", "固定等幾秒", "等太短會失敗，等太長浪費時間。", "不建議"),
        ("WebDriverWait", "等到條件成立", "元素出現或網址改變，就立刻往下走。", "建議"),
        src="p20",
    ),
    code(
        "明確等待，再交給 BeautifulSoup",
        "PYTHON",
        'driver.get(f"{base}/delayed")\n\nresult = WebDriverWait(driver, 10).until(\n    EC.presence_of_element_located(\n        (By.ID, "result")\n    )\n)\nprint(result.text)\n\nsoup = BeautifulSoup(driver.page_source, "html.parser")\nitems = [li.text for li in soup.select("ul#items li")]',
        "三個設計",
        "最多等 10 秒，成立就繼續\n\n渲染完成才讀資料\n\npage_source 交給 bs4",
        note="前面學的解析都能接上。",
        src="p21",
    ),
    section(
        "C",
        "常見錯誤與守則",
        "多數錯誤都是選擇器不對，或是元素還沒出現。",
        "Selenium 更要遵守網站規則。",
    ),
    cards3_numbered(
        "錯誤",
        "三個最常見的錯誤",
        [
            ("NoSuchElement", "找不到元素：檢查選擇器，或需要等待。"),
            ("TimeoutException", "等太久：條件寫錯，或網頁真的沒有。"),
            ("StaleElement", "換頁後舊元素失效：重新找一次。"),
        ],
        src="p6",
    ),
    compare2(
        "點擊之後，讀到舊頁面",
        ("立刻讀", "可能還是舊頁面", "新頁面還沒載入，讀到舊內容，而且時好時壞。", "最常見的錯誤"),
        ("先等再讀", "確認新頁面來了", "等網址或新元素出現，再去讀資料。", "穩定"),
        src="p9",
    ),
    checks5(
        "Selenium 的使用檢查清單",
        [
            ("用 with", "確保瀏覽器一定會關閉。"),
            ("先等待", "換頁與動態內容都要等。"),
            ("先用 F12", "選擇器先在瀏覽器確認。"),
            ("能不用就不用", "有 API 或 requests 就夠，就別開瀏覽器。"),
            ("守則照舊", "頻率、條款與授權仍然適用。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能用程式操作瀏覽器，\n並等到動態內容出現再取資料。",
        "完成：Selenium＋找元素＋輸入點擊＋明確等待＋截圖",
    ),
]
