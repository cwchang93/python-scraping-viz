"""Lesson 01 slide content. Build with: python tools/slides_kit.py slides/lesson01.py --out-dir <dir>"""

from slides_kit import cards4, cards3_numbered, checkpoint, flow5, statement, title_slide

LESSON = "01"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "Python 語法暖身與爬蟲先備",
        "先把常用語法找回來，再開始抓網頁",
        "15",
        "題小試身手",
        "讀懂程式 → 動手練習 → 準備爬蟲",
    ),
    statement(
        "今天不是考試，是找回手感",
        "忘了語法很正常，\n先練習再一起補回來。",
        "先自己寫，卡住時讀提示；重點是看懂資料怎麼一步步變成結果。",
    ),
    cards4(
        "用 Colab 線上暖身",
        "先開教材，再建立自己的練習副本",
        [
            ("開啟教材", "點擊此處開啟 Lesson 01 筆記本。"),
            ("儲存副本", "選「檔案 → 在雲端硬碟中儲存副本」。"),
            ("逐格執行", "閱讀題目、填入程式，按 Shift + Enter。"),
            ("練習與檢查", "從 Core 開始，完成後看 assert 與解答。"),
        ],
    ),
    flow5(
        "15 題練習路線",
        "從 Python 基礎一路接到爬蟲常用操作",
        [
            ("01–05", "變數、型別、字串、條件、List、Dict"),
            ("06–10", "迴圈、函式、HTML 字串、例外處理"),
            ("11–12", "拆解 URL、搜尋 HTML 資料"),
            ("13–14", "requests、timeout、狀態碼與回應文字"),
            ("15", "整合：整理網頁文字成資料清單"),
        ],
    ),
    cards4(
        "練習節奏",
        "依照自己的熟悉程度分段完成",
        [
            ("Core｜1–5", "先喚回 Python 基本語法。"),
            ("Practice｜6–10", "用容器、迴圈和函式處理資料。"),
            ("Challenge｜11–15", "練習網址、HTML 與 requests。"),
            ("看解答", "先完成再對照 Solutions，找出需要複習的地方。"),
        ],
    ),
    cards3_numbered(
        "爬蟲會一直用到的語法",
        "基礎語法會變成資料處理工具",
        [
            ("List / Dict", "保存多筆資料，並用欄位名稱取值。"),
            ("For / If", "逐筆檢查內容，保留符合條件的資料。"),
            ("函式 / 例外", "重用步驟，妥善處理缺值與請求錯誤。"),
        ],
    ),
    checkpoint(
        "我能讀懂常見 Python 語法，\n也知道爬蟲程式如何整理回應。",
        "完成 15 題 Learning Exercise；不熟的部分記下來，後面課程會再用到。",
    ),
]
