"""Lesson 06 slide content. Build with: python tools/slides_kit.py slides/lesson06.py --out-dir <dir>"""

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

LESSON = "06"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "爬回來的資料整理：pandas",
        "把字串變成能計算、能排名的表格",
        "1000\n本書",
        "整理成\n排行榜",
        "讀入 → 轉型 → 篩選 → 排序 → 存檔",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("讀入並檢查", "幾筆、哪些欄位、什麼型態。"),
            ("轉成可計算", "價格、評分從字串變成數字。"),
            ("篩選與排序", "找出條件符合的書，做成排行榜。"),
            ("乾淨的 CSV", "存成 books_clean.csv 再讀回驗證。"),
        ],
    ),
    statement(
        "先看清楚資料的型態",
        "原始價格是 £51.77，評分是 Three，\n先轉型，才能計算。",
        "整理資料的第一步，是看清楚它現在是什麼型態。",
    ),
    flow5(
        "整理流程",
        "從原始字串到乾淨表格",
        [
            ("讀入", "read_\ncsv"),
            ("檢查", "info\nhead"),
            ("轉型", "astype\nmap"),
            ("篩選排序", "條件\nsort"),
            ("存檔", "to_\ncsv"),
        ],
    ),
    section(
        "A",
        "讀入與檢查",
        "拿到資料，先看幾筆、哪些欄位、什麼型態。",
        "還沒看懂資料，不要急著算。",
    ),
    code(
        "讀進來，先看一眼",
        "PYTHON",
        'import pandas as pd\n\ndf = pd.read_csv(\n    "books_raw.csv", encoding="utf-8-sig"\n)\nprint(df.shape)\nprint(df.head(3))\ndf.info()',
        "先確認三件事",
        "shape：幾列幾欄\n\nhead：資料長什麼樣\n\ninfo：每欄是什麼型態",
        note="全部是字串，要先轉型。",
        src="p15",
    ),
    cards3_labeled(
        "資料進 pandas 的三種路",
        [
            ("檔案", "read_csv", "讀進存好的 CSV，記得 encoding。"),
            ("表格", "read_html", "網頁的 table 一行變成 DataFrame。"),
            ("字典", "DataFrame(rows)", "上一堂的 list of dict 直接轉換。"),
        ],
        kicker="資料來源",
    ),
    code(
        "網頁上的表格：read_html",
        "PYTHON",
        'from io import StringIO\n\ntables = pd.read_html(StringIO(html))\ninfo = tables[0]\ninfo.columns = ["item", "value"]',
        "什麼時候用它",
        "網頁本身是 table\n\n不用寫 BeautifulSoup\n\n需要安裝 lxml",
        note="傳入 StringIO，不要直接傳字串。",
        src="p16",
    ),
    section(
        "B",
        "轉型與新欄位",
        "價格去掉符號、評分用字典對照，欄位才能計算。",
        "轉完型態，先檢查一次。",
        src="p11",
    ),
    code(
        "價格與評分：字串轉數字",
        "PYTHON",
        'df["price"] = (\n    df["price_text"]\n    .str.replace("£", "", regex=False)\n    .astype(float)\n)\n\nRATING = {"One": 1, "Two": 2, "Three": 3}\ndf["rating"] = df["rating_word"].map(RATING)',
        "三個重點",
        "str 讓整欄一起處理\n\nastype 轉成 float\n\nmap 用字典對照",
        note="map 對照失敗會變 NaN。",
        src="p19",
    ),
    compare2(
        "字串與數字，差在哪裡？",
        ("字串", "\"£51.77\"", "不能比大小，相加只是把文字接起來。", "還不能分析"),
        ("數字", "51.77", "能加總、平均、排名、畫圖。", "float"),
        src="p12",
    ),
    cards3_numbered(
        "轉型",
        "轉型的三個工具",
        [
            ("str.replace", "先清掉符號或多餘文字。"),
            ("astype", "把整欄轉成指定的型態。"),
            ("map", "用字典把文字對照成數字。"),
        ],
    ),
    section(
        "C",
        "篩選、排序與輸出",
        "用條件選出資料，排出名次，存成乾淨的檔案。",
        "每一步都數一下筆數。",
    ),
    code(
        "篩選與排序",
        "PYTHON",
        'cheap5 = df[\n    (df["rating"] == 5) & (df["price"] < 15)\n]\n\nranked = df.sort_values(\n    ["rating", "price"],\n    ascending=[False, True],\n)\ntop3 = df.nlargest(3, "price")',
        "三個重點",
        "條件要加括號\n\n多個條件用 & 與 |\n\nnlargest 取前幾名",
        note="評分高到低，同分價格低到高。",
        src="p21",
    ),
    compare2(
        "兩個條件怎麼寫？",
        ("& 與 |", "DataFrame 的條件", "每個條件加括號：(a) & (b)，逐列比較。", "整欄一起判斷"),
        ("and 與 or", "單一的布林值", "用在 if 判斷，不能直接放在整欄條件上。", "會出現 ValueError"),
        src="p9",
    ),
    cards3_numbered(
        "排名",
        "做排行榜的三種寫法",
        [
            ("sort_values", "排序後用 head 取前幾筆。"),
            ("nlargest", "直接取最大或最小的前幾名。"),
            ("groupby + head", "每個分組各取第一名。"),
        ],
        src="p6",
    ),
    checks5(
        "整理完成的檢查清單",
        [
            ("保留原始值", "保留價格與評分原文，方便查錯。"),
            ("轉換失敗", "無法轉成數字時，檢查缺值。"),
            ("對照失敗", "map 找不到評分會產生缺值。"),
            ("範圍合理", "價格大於 0，評分應在 1 到 5。"),
            ("存檔再讀回", "筆數、欄位與總價要一致。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能把爬回來的字串，\n整理成能計算、能排名的表格。",
        "完成：read_csv＋轉型＋篩選排序＋books_clean.csv",
    ),
]
