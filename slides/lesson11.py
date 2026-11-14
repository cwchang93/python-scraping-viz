"""Lesson 11 slide content. Build with: python tools/slides_kit.py slides/lesson11.py --out-dir <dir>"""

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

LESSON = "11"
SERIES = "PYTHON 爬蟲與資料視覺化"

SLIDES = [
    title_slide(
        "圖片與檔案下載",
        "把圖片抓回來，再用 Pillow 整理成縮圖",
        "圖片\n下載",
        "縮圖 整理\n檔案 CSV",
        "bytes → 存檔 → Pillow → 縮圖 → 整理",
    ),
    cards4(
        "課堂任務",
        "今天下課前，要留下四個看得見的成果",
        [
            ("下載圖片", "找出圖片網址，一張一張存檔。"),
            ("避開壞圖", "檢查狀態碼與 Content-Type。"),
            ("大檔案", "串流下載，先問大小再決定。"),
            ("縮圖與整理", "用 Pillow 縮圖，依評分整理。"),
        ],
    ),
    statement(
        "圖片不是文字",
        "圖片是二進位資料，\n用 bytes 取得、用 wb 存檔。",
        "用 response.text 存圖片，只會得到壞檔。",
    ),
    flow5(
        "下載圖片的流程",
        "從找到網址到處理完成",
        [
            ("找網址", "img\nsrc"),
            ("補完整", "url\njoin"),
            ("檢查", "狀態碼\nType"),
            ("存檔", "write_\nbytes"),
            ("處理", "Pillow\n縮圖"),
        ],
    ),
    section(
        "A",
        "下載圖片",
        "圖片網址在 img 的 src，可能是相對路徑或懶載入。",
        "檢查 Content-Type，避開 404 與假圖。",
    ),
    code(
        "取得圖片，存成檔案",
        "PYTHON",
        'response = requests.get(url, timeout=10)\n\nprint(response.headers["Content-Type"])\nprint(len(response.content))\n\nPath("cover.jpg").write_bytes(response.content)',
        "三個重點",
        "content 是 bytes\n\nContent-Type 看類型\n\nwrite_bytes 二進位寫入",
        note="不要用 response.text。",
        src="p15",
    ),
    cards3_labeled(
        "圖片網址的三種寫法",
        [
            ("相對", "images/a.jpg", "用 urljoin 接上頁面網址。"),
            ("懶載入", "data-src", "src 是佔位圖，真網址在 data-src。"),
            ("參數", "a.jpg?v=3", "檔名要用 urlparse 取出。"),
        ],
        kicker="網址",
    ),
    compare2(
        "兩種失敗的圖片",
        ("404", "找不到圖片", "狀態碼不是 200，直接略過。", "容易發現"),
        ("200 的假圖", "內容是錯誤網頁", "要檢查 Content-Type 是不是 image/。", "容易漏掉"),
        src="p12",
    ),
    section(
        "B",
        "大檔案與批次",
        "先問大小、串流下載，批次要略過已存在的檔案。",
        "每張之間要 sleep，對網站有禮貌。",
        src="p11",
    ),
    code(
        "批次下載：已存在就略過",
        "PYTHON",
        'for url in urls:\n    path = folder / filename_from_url(url)\n    if path.exists():\n        summary["skipped"] += 1\n        continue\n    ok = download_image(url, folder)\n    summary["ok" if ok else "failed"] += 1\n    time.sleep(1)',
        "三個好習慣",
        "檔案存在就略過\n\n每張之間 sleep\n\n最後印出統計",
        note="中斷後重跑，不會重抓。",
        src="p19",
    ),
    cards3_numbered(
        "大檔案",
        "大檔案的三個做法",
        [
            ("先問大小", "requests.head 只拿標頭。"),
            ("串流下載", "stream=True，一塊一塊寫。"),
            ("看建議檔名", "Content-Disposition 有檔名。"),
        ],
    ),
    compare2(
        "一般 get 與串流",
        ("一般 get", "整個讀進記憶體", "小圖與小檔案適合，簡單直接。", "小檔案"),
        ("stream", "一塊一塊讀寫", "大檔案用，記憶體只需要一塊。", "大檔案"),
        src="p20",
    ),
    code(
        "用 Pillow 做縮圖",
        "PYTHON",
        'with Image.open("cover.jpg") as picture:\n    print(picture.size, picture.mode)\n\n    if picture.mode == "RGBA":\n        bg = Image.new("RGB", picture.size, "white")\n        bg.paste(picture, mask=picture.getchannel("A"))\n        picture = bg\n    thumb = ImageOps.fit(picture, (120, 160))\nthumb.save("thumb.jpg", quality=85)',
        "三個設計",
        "with 開圖，自動關檔\n\nRGBA 先貼白底\n\nfit 裁成剛好大小",
        note="RGBA 不能直接存成 JPEG。",
        src="p21",
    ),
    section(
        "C",
        "Pillow 與整理",
        "縮圖有三種做法，差別在比例與裁切。",
        "最後把圖片整理成資料夾，做出縮圖牆。",
    ),
    cards3_numbered(
        "縮圖",
        "三種縮圖方法",
        [
            ("thumbnail", "依比例縮小，不放大，會改動原圖。"),
            ("resize", "硬拉成指定大小，會變形。"),
            ("ImageOps.fit", "縮放後裁切，剛好又不變形。"),
        ],
        src="p6",
    ),
    compare2(
        "RGBA 轉成 JPEG 的兩種做法",
        ("convert(RGB)", "透明變黑色", "快，但透明的地方會變成黑色。", "要小心"),
        ("貼到白底", "透明變白色", "先建白底，再用透明通道當遮罩貼上。", "建議"),
        src="p9",
    ),
    checks5(
        "圖片下載的檢查清單",
        [
            ("驗證類型", "200 也可能是假圖。"),
            ("存檔用二進位", "write_bytes 或 wb。"),
            ("檔名要安全", "去掉參數與非法字元。"),
            ("先問大小", "大檔案先 HEAD 或串流。"),
            ("版權與頻率", "自己用可以，別重新發布。"),
        ],
        src="p23",
    ),
    checkpoint(
        "我能下載圖片與檔案，\n並用 Pillow 縮圖、整理成資料夾。",
        "完成：bytes＋下載函式＋串流＋Pillow＋整理",
    ),
]
