"""Lesson 08 slide content. Build with: python tools/slides_kit.py slides/lesson08.py --out-dir <dir>"""

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

LESSON = "08"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "JSON API、開放資料與登入",
        "找到資料的來源，直接取用",
        "{ }\nJSON",
        "不用解析\nHTML",
        "F12 → API → JSON → DataFrame",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("找到 API", "用 F12 找出網頁背後的資料來源。"),
            ("JSON 變表格", "response.json 再 json_normalize。"),
            ("開放資料分析", "用 YouBike 資料算各區的車輛。"),
            ("Session 登入", "登入後抓會員才看得到的頁面。"),
        ],
    ),
    statement(
        "有 API，就不要爬網頁",
        "資料常常不在 HTML 裡，\n而在網頁背後的 API。",
        "找到來源，比解析畫面更簡單，也更穩。",
    ),
    flow5(
        "取得資料的流程",
        "從找到來源到可以分析",
        [
            ("找來源", "F12\nNetwork"),
            ("呼叫", "requests\n.get"),
            ("轉換", ".json()\n變 dict"),
            ("展平", "json_\nnormalize"),
            ("分析", "Data\nFrame"),
        ],
    ),
    section(
        "A",
        "JSON 與 API",
        "JSON 長得像 dict 與 list，取值的方法一樣。",
        "先看結構，再取值。",
    ),
    code(
        "呼叫 API，取出巢狀的值",
        "PYTHON",
        'response = requests.get(\n    "https://quotes.toscrape.com/api/quotes",\n    params={"page": 1},\n)\ndata = response.json()\n\nprint(data["quotes"][0]["author"]["name"])',
        "三個重點",
        "json() 轉成 Python 物件\n\n一層一層用 [ ] 取值\n\n不確定有沒有用 get",
        note="先印出 data.keys() 看結構。",
        src="p15",
    ),
    cards3_labeled(
        "JSON 與 Python 對照",
        [
            ("物件", "{ ... } → dict", "用 key 取值：data[\"name\"]。"),
            ("陣列", "[ ... ] → list", "用位置取值：data[0]。"),
            ("空值", "null → None", "true 與 false 變成 True 與 False。"),
        ],
        kicker="資料型態",
    ),
    checks5(
        "用 F12 找 API 的五個步驟",
        [
            ("開 Network", "先打開，再重新整理。"),
            ("點 Fetch/XHR", "只留下資料請求。"),
            ("捲動或操作", "讓網頁去要資料。"),
            ("找 JSON 請求", "名稱常有 api 或 json。"),
            ("看 Response", "確認內容，複製網址。"),
        ],
    ),
    section(
        "B",
        "開放資料與展平",
        "授權、格式、更新頻率，用之前先看。",
        "即時資料每次都不一樣，分析用快照。",
        src="p11",
    ),
    compare2(
        "解析 HTML 與呼叫 API",
        ("解析 HTML", "要寫選擇器", "網頁改版就壞，還要處理缺值。", "最後的選擇"),
        ("呼叫 API", "直接拿資料", "格式固定，常有網頁上看不到的欄位。", "優先選擇"),
        src="p9",
    ),
    code(
        "YouBike：展平、分組、統計",
        "PYTHON",
        'df = pd.DataFrame(stations)\n\nby_area = df.groupby("sarea").agg(\n    bikes=("available_rent_bikes", "sum"),\n    docks=("Quantity", "sum"),\n)\nby_area["rate"] = by_area.bikes / by_area.docks\nprint(by_area.sort_values("bikes").tail())',
        "先看欄位說明",
        "Quantity 是總車位\n\navailable_rent_bikes 可借\n\nact 是字串 1 或 0",
        note="欄位名稱不要用猜的。",
        src="p19",
    ),
    cards3_numbered(
        "開放資料",
        "使用開放資料前的三個問題",
        [
            ("授權", "能不能重製、改作，要不要標示出處？"),
            ("格式", "JSON、CSV 還是 XML，要不要金鑰？"),
            ("更新頻率", "每分鐘、每天，還是每年？"),
        ],
    ),
    section(
        "C",
        "登入與 Cookies",
        "登入後伺服器給你一個識別碼，之後每次都帶著它。",
        "只登入自己有帳號、條款允許的網站。",
    ),
    code(
        "用 Session 登入並抓會員頁",
        "PYTHON",
        'session = requests.Session()\npage = session.get(f"{base}/login")\ntoken = BeautifulSoup(page.text, "html.parser")\\\n    .select_one("input[name=csrf_token]")["value"]\n\nsession.post(f"{base}/login", data={\n    "csrf_token": token,\n    "username": user, "password": password,\n})\nmembers = session.get(f"{base}/members")',
        "三個設計",
        "GET 取得隱藏欄位\n\nPOST 送出表單\n\n同一個 session 抓頁面",
        note="密碼不要寫進程式碼。",
        src="p21",
    ),
    compare2(
        "requests.get 與 Session",
        ("requests.get", "每次都是陌生人", "不會記得 Cookie，登入後的頁面會被導回登入頁。", "只適合公開頁面"),
        ("Session", "自動帶著 Cookie", "登入一次，之後的請求都帶著識別碼。", "適合需要登入的頁面"),
        src="p12",
    ),
    cards3_numbered(
        "登入",
        "登入的三個步驟",
        [
            ("取得表單", "GET 登入頁，找出隱藏的 csrf_token。"),
            ("送出登入", "POST 帳號、密碼與 csrf_token。"),
            ("抓會員頁", "用同一個 session 請求需要登入的頁面。"),
        ],
        src="p6",
    ),
    checks5(
        "使用 API 與登入的守則",
        [
            ("優先用 API", "有開放資料就不要爬網頁。"),
            ("看授權", "標示出處，遵守使用條款。"),
            ("只登自己的", "不登入不屬於你的帳號。"),
            ("密碼不入程式", "真實帳密不要寫進檔案或 repo。"),
            ("控制頻率", "sleep 與 timeout 仍然要做。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能找到資料的 API，\n也能登入後抓取需要權限的頁面。",
        "完成：JSON＋json_normalize＋開放資料＋Session 登入",
    ),
]
