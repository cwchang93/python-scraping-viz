"""Lesson 07 slide content. Build with: python tools/slides_kit.py slides/lesson07.py --out-dir <dir>"""

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

LESSON = "07"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "網頁資料清理",
        "缺值、重複、格式不一致，一項一項做決策",
        "NaN\nNaT",
        "找問題\n做決策",
        "找問題 → 做決策 → 驗證 → 留紀錄",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("問題清單", "列出資料裡的缺值、重複與格式問題。"),
            ("文字與日期", "清掉引號、切開標籤、解析日期。"),
            ("合併兩張表", "用 author_url 把名言與作者接起來。"),
            ("驗證與紀錄", "寫下驗證條件與清理決策。"),
        ],
    ),
    statement(
        "清理不是按一個按鈕",
        "而是一連串決策，\n每一個都要有理由。",
        "資料動過什麼，要留下紀錄，才能被信任。",
    ),
    flow5(
        "清理流程",
        "從髒資料到可以分析的資料",
        [
            ("找問題", "isna\nduplicated"),
            ("統一格式", "strip\ntitle"),
            ("轉型別", "to_numeric\nto_datetime"),
            ("缺值重複", "dropna\ndrop_dup"),
            ("驗證", "assert\n留紀錄"),
        ],
    ),
    section(
        "A",
        "找出問題",
        "先列出所有問題，再逐項決定怎麼處理。",
        "看得見的問題，才處理得了。",
    ),
    code(
        "用兩行程式找問題",
        "PYTHON",
        'print(toy.isna().sum())\n\nprint(toy.duplicated().sum())',
        "找什麼",
        "每欄有幾個缺值\n\n有幾列完全重複\n\n型態是否符合預期",
        note="先找問題，再動手改。",
        src="p16",
    ),
    cards3_labeled(
        "常見的三種問題",
        [
            ("缺值", "NaN 與空字串", "網頁沒有資料時，常是空字串而不是 NaN。"),
            ("重複", "寫法不同的同一筆", "大小寫與空白不同，其實是同一個人。"),
            ("格式", "空白、引號、大小寫", "文字裡夾帶符號，日期是一句英文。"),
        ],
        kicker="問題類型",
    ),
    compare2(
        "先統一格式，再找重複",
        ("先找重複", "看不出重複", "\" Alice \" 和 \"alice\" 寫法不同，duplicated 不算重複。", "漏掉了"),
        ("先統一", "才看得出重複", "strip 與 title 之後，兩筆變成一樣，才找得到。", "順序很重要"),
        src="p12",
    ),
    section(
        "B",
        "文字、標籤與日期",
        "把夾在文字裡的資料，一項一項拆出來。",
        "轉不了的，讓它變成看得見的缺值。",
        src="p11",
    ),
    code(
        "標籤：切開、展開、統計",
        "PYTHON",
        'q["tags"] = q["tags_text"].str.split(",")\n\nlong = q[["text", "tags"]].explode("tags")\n\nprint(long["tags"].value_counts().head())',
        "三步",
        "split 切成 list\n\nexplode 一列一個標籤\n\nvalue_counts 排名",
        note="一則名言會變成多筆。",
        src="p15",
    ),
    cards3_numbered(
        "日期",
        "日期與出生地的處理",
        [
            ("to_datetime", "用 format 指定「月 日, 年」的格式。"),
            ("str.replace", "用規則去掉開頭的 in 與 The。"),
            ("str.split", "取最後一段逗號後的文字當國家。"),
        ],
    ),
    code(
        "日期轉型：用 NaT 標記失敗",
        "PYTHON",
        'authors["born_date"] = pd.to_datetime(\n    authors["born_date_text"],\n    format="%B %d, %Y",\n    errors="coerce",\n)\nprint(authors["born_date"].isna().sum())\nauthors["born_year"] = authors["born_date"].dt.year',
        "三個重點",
        "format 對應 March 14, 1879\n\ncoerce 失敗變 NaT\n\ndt.year 取出年份",
        note="NaT 是日期的缺值。",
        src="p19",
    ),
    section(
        "C",
        "合併與驗證",
        "兩張表接起來，再把應該成立的事寫成 assert。",
        "不驗證，就不知道有沒有壞。",
    ),
    code(
        "合併兩張表，並驗證",
        "PYTHON",
        'merged = quotes.merge(\n    authors[["author_url", "born_year", "country"]],\n    on="author_url",\n    how="left",\n    validate="many_to_one",\n)\nassert len(merged) == 100\nassert merged["born_year"].notna().all()\nassert merged["country"].notna().all()',
        "三個設計",
        "left 保留所有名言\n\nvalidate 檢查對應關係\n\nassert 寫下應成立的事",
        note="資料更新後，一跑就知道。",
        src="p21",
    ),
    compare2(
        "errors=coerce 與 raise",
        ("coerce", "轉不了就變缺值", "NaN 或 NaT 讓問題看得見，再決定怎麼處理。", "資料不乾淨時用"),
        ("raise", "轉不了就報錯", "程式立刻停下來，適合資料來源很可靠時。", "預設行為"),
        src="p20",
    ),
    cards3_numbered(
        "缺值",
        "缺值的三種決策",
        [
            ("刪除", "缺少計算必要的欄位，這列無法使用。"),
            ("補值", "有依據才補，並說明補的是什麼。"),
            ("保留", "標成未知，不要補成 0 拉低平均。"),
        ],
        src="p6",
    ),
    checks5(
        "清理完成的檢查清單",
        [
            ("筆數", "合併前後筆數沒有意外變動。"),
            ("型態", "日期是 datetime，數字是數字。"),
            ("缺值", "NaN、NaT 與空字串都檢查過。"),
            ("範圍", "年份、字數等數值在合理範圍。"),
            ("紀錄", "每個決策都寫進 cleaning_log。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能列出資料的問題，\n逐項處理，並證明它處理對了。",
        "完成：問題清單＋文字日期清理＋merge＋驗證＋紀錄",
    ),
]
