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
        "BeautifulSoup（一）：解析 HTML",
        "把網頁變成你能取用的資料",
        "find\nselect",
        "用標籤\n找資料",
        "HTML → soup → 找元素 → 取值 → dict",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("建立 soup", "把 HTML 字串變成可以查詢的物件。"),
            ("找到元素", "用 find、find_all、select 找到目標。"),
            ("取出資料", "取出文字與 href 等屬性。"),
            ("整理成 dict", "一頁名言變成 list of dict。"),
        ],
    ),
    statement(
        "上一堂只能用字串搜尋",
        "這一堂改用標籤找資料，\n不再靠 find 字串碰運氣。",
        "BeautifulSoup 把 HTML 變成一棵可以查詢的樹。",
    ),
    flow5(
        "解析流程",
        "從 HTML 到資料，固定五步",
        [
            ("取得 HTML", "fetch\n或讀檔"),
            ("建立 soup", "html.\nparser"),
            ("找元素", "find\nselect"),
            ("取值", "文字\n屬性"),
            ("整理", "dict\nlist"),
        ],
    ),
    section(
        "A",
        "認識 BeautifulSoup",
        "先把 HTML 交給它，再用標籤與 class 去找。",
        "先會找，才會取。",
    ),
    code(
        "建立 soup，從標籤開始找",
        "PYTHON",
        'from bs4 import BeautifulSoup\n\nhtml = "<h1>本週推薦</h1>"\nsoup = BeautifulSoup(html, "html.parser")\n\nprint(soup.h1.get_text())',
        "三個重點",
        "第二個參數指定解析器\n\nsoup.h1 找第一個 h1\n\nget_text 取出文字",
        note="html.parser 是內建的，不必安裝。",
        src="p15",
    ),
    cards3_labeled(
        "找的結果，有三種長相",
        [
            ("單個", "find、select_one", "回傳一個元素，找不到是 None。"),
            ("多個", "find_all、select", "回傳類似 list 的結果，可以 for。"),
            ("文字", "get_text、屬性", "取出文字或 href 這類屬性。"),
        ],
        kicker="回傳型態",
    ),
    section(
        "B",
        "找元素與取值",
        "用 class、選擇器與屬性，精準找到要的資料。",
        "一次只解析一筆，確認對了再跑全部。",
        src="p11",
    ),
    code(
        "find 與 find_all：用標籤和 class 找",
        "PYTHON",
        'first = soup.find("li", class_="book")\nprint(first.get_text())\n\nbooks = soup.find_all("li", class_="book")\nprint(len(books))\n\nlink = soup.find("a")\nprint(link["href"])\nprint(link.get("title"))',
        "容易錯的地方",
        "class 要寫成 class_\n\n找不到 find 回 None\n\n屬性缺少 get 回 None",
        note="tag[\"href\"] 缺屬性會報錯。",
        src="p19",
    ),
    compare2(
        "find_all 與 select，怎麼選？",
        ("find_all", "用標籤與屬性找", "find_all(\"span\", class_=\"text\")，條件簡單時好讀。", "class 要加底線"),
        ("select", "用 CSS 選擇器找", "select(\"div.quote span.text\")，和 F12 看到的寫法相同。", "select_one 找第一個"),
        src="p9",
    ),
    cards3_numbered(
        "取值",
        "取值的三種寫法",
        [
            ("get_text(strip=True)", "取出文字，並去掉前後空白。"),
            ("tag[\"href\"]", "取屬性；沒有這個屬性會 KeyError。"),
            ("tag.get(\"href\")", "取屬性；沒有時回傳 None。"),
        ],
    ),
    section(
        "C",
        "整理成資料",
        "一則名言一個 dict，整頁就是 list of dict。",
        "缺值要先檢查，不要讓程式當掉。",
    ),
    code(
        "parse_quotes：整頁變成 list of dict",
        "PYTHON",
        'def parse_quotes(html):\n    page = BeautifulSoup(html, "html.parser")\n    rows = []\n    for quote in page.select("div.quote"):\n        rows.append({\n            "text": text_or_none(quote, "span.text"),\n            "author": text_or_none(quote, "small.author"),\n            "tags": [t.get_text(strip=True)\n                     for t in quote.select("a.tag")],\n        })\n    return rows',
        "三個設計",
        "輸入 HTML，輸出資料\n\n缺值交給 text_or_none\n\n標籤用 list 收集",
        note="一個函式做一件事。",
        src="p21",
    ),
    compare2(
        "找不到的時候",
        ("直接取值", "find 回傳 None", "再 get_text 會 AttributeError，整個程式停住。", "最常見的錯誤"),
        ("先檢查", "None 就給預設值", "if tag is None 回傳 None，其餘照常處理。", "資料常有缺值"),
        src="p12",
    ),
    cards3_numbered(
        "F12",
        "用 F12 找選擇器的三步",
        [
            ("點選元素", "Elements 裡對目標按右鍵檢查。"),
            ("Copy selector", "右鍵 Copy → Copy selector。"),
            ("簡化再試", "貼進 select_one，改成短的選擇器。"),
        ],
        src="p6",
    ),
    checks5(
        "解析前後的檢查清單",
        [
            ("有拿到 HTML", "狀態碼 200，長度合理。"),
            ("找到目標", "F12 確認標籤與 class。"),
            ("先試一筆", "一筆對了，再跑全部。"),
            ("數量對得上", "名言頁應該有 10 則。"),
            ("缺值有處理", "None 不會讓程式停住。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能把一頁 HTML，\n解析成一份乾淨的資料。",
        "完成：soup＋find、select＋文字與屬性＋parse_quotes",
    ),
]
