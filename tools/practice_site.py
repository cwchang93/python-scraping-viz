"""A tiny local practice site for lessons 07 to 10.

It only listens on 127.0.0.1 and uses the Python standard library, so no extra
install is needed. Pages:

    /           index with links
    /login      login form with a hidden CSRF token
    /members    members-only page (needs the session cookie from /login)
    /logout     clears the session
    /search     search form; results are filtered on the server
    /delayed    content that appears two seconds after the page loads (JavaScript)
    /js-list    a list that only exists after JavaScript runs (not in the raw HTML)
    /feed       infinite scroll: 10 posts at a time, loaded when you scroll to the bottom
    /load-more  first 10 posts in the HTML, a "載入更多" button fetches the rest (25 in total)
    /api/feed   the JSON behind both pages: ?offset=0&limit=10 (&max=25)
    /gallery    pictures to download: relative src, a lazy-loaded one (data-src), a 404 and a fake one
    /images/<file>        the pictures (lessons/lesson11_images_and_files/fixtures/gallery)
    /files/price_list.csv a small CSV sent as an attachment
    /files/big.bin        a 2 MiB file, for streaming downloads

Run it by hand to look around in a browser:

    python tools/practice_site.py          # http://127.0.0.1:8000

The lessons start it themselves with start_server(), on a free port.
The login below is a test value that only works on this local site.
"""

from __future__ import annotations

import csv
import html
import json
import secrets
import threading
from http.cookies import SimpleCookie
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

TEST_USER = "student"
TEST_PASSWORD = "practice-pass"

ORDERS = [
    ("A-1001", "Python 入門課", 1200, "已付款"),
    ("A-1002", "爬蟲實作課", 1800, "已付款"),
    ("A-1003", "資料視覺化課", 1500, "待付款"),
    ("A-1004", "Git 與 GitHub", 900, "已付款"),
    ("A-1005", "專題工作坊", 2400, "待付款"),
]

COURSES = [
    ("Python 入門課", "初級"),
    ("Python 資料分析", "中級"),
    ("Python 爬蟲實作", "中級"),
    ("Python 資料視覺化", "中級"),
    ("Git 與 GitHub", "初級"),
    ("SQL 入門", "初級"),
    ("Excel 資料整理", "初級"),
    ("Python 自動化", "中級"),
    ("機器學習入門", "進階"),
    ("網頁前端基礎", "初級"),
    ("API 與開放資料", "中級"),
    ("專題工作坊", "進階"),
]

POST_TOPICS = [
    "requests 入門",
    "BeautifulSoup 解析",
    "CSS 選擇器",
    "翻頁與迴圈",
    "pandas 整理",
    "資料清理",
    "JSON 與 API",
    "Selenium 基礎",
    "明確等待",
    "無限捲動",
    "圖片下載",
    "Matplotlib 繪圖",
]
POST_TAGS = ["爬蟲", "資料", "視覺化", "工具"]
POST_TOTAL = 60  # /feed
LOAD_MORE_TOTAL = 25  # /load-more
PAGE_SIZE = 10


def make_post(number: int) -> dict:
    return {
        "id": number,
        "title": f"第 {number:02d} 篇：{POST_TOPICS[(number - 1) % len(POST_TOPICS)]}",
        "tag": POST_TAGS[(number - 1) % len(POST_TAGS)],
        "views": (number * 37) % 200 + 50,
    }


POSTS = [make_post(number) for number in range(1, POST_TOTAL + 1)]


def post_html(post: dict) -> str:
    return (
        f'<article class="post" data-id="{post["id"]}">'
        f'<h3 class="post-title">{html.escape(post["title"])}</h3>'
        f'<p class="post-meta"><span class="post-tag">{post["tag"]}</span> · 閱讀 <span class="post-views">{post["views"]}</span> 次</p>'
        f'<p>這是第 {post["id"]} 篇文章的摘要。</p></article>'
    )


# The same markup as post_html(), built in the browser from the JSON of /api/feed.
POST_JS = """
function renderPost(p) {
  return '<article class="post" data-id="' + p.id + '"><h3 class="post-title">' + p.title + '</h3>' +
    '<p class="post-meta"><span class="post-tag">' + p.tag + '</span> · 閱讀 <span class="post-views">' + p.views +
    '</span> 次</p><p>這是第 ' + p.id + ' 篇文章的摘要。</p></article>';
}
"""

GALLERY_DIR = Path(__file__).resolve().parents[1] / "lessons/lesson11_images_and_files/fixtures/gallery"
IMAGE_TYPES = {".jpg": "image/jpeg", ".png": "image/png", ".gif": "image/gif"}
# a 1x1 transparent GIF: the placeholder that lazy-loaded pictures show before the real one arrives
PLACEHOLDER_GIF = bytes.fromhex("47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b")
PRICE_LIST_CSV = "課程,價格\n" + "".join(f"{name},{price}\n" for _, name, price, _ in ORDERS)
BIG_FILE = bytes(range(256)) * 8192  # 2 MiB


def gallery_page() -> bytes | None:
    manifest = GALLERY_DIR / "manifest.csv"
    if not manifest.exists():
        return None
    with open(manifest, encoding="utf-8-sig", newline="") as file:
        items = list(csv.DictReader(file))
    books, extras = [], []
    for item in items:
        name, title = item["file"], html.escape(item["title"])
        if item["kind"] == "book":
            src = f'src="images/{name}"'
            if name == "cover_02.jpg":
                src = f'src="images/{name}?v=3"'  # a version number after the file name
            elif name == "cover_12.jpg":
                src = f'class="lazy" src="images/loading.gif" data-src="images/{name}"'  # lazy loading
            books.append(
                f'<figure class="book" data-rating="{item["rating"]}"><img {src} alt="{title}">'
                f"<figcaption>{title}</figcaption></figure>"
            )
        else:
            extras.append(f'<figure class="extra"><img src="images/{name}" alt="{title}"><figcaption>{title}</figcaption></figure>')
    body = f"""
<style>figure {{ display: inline-block; margin: .5rem; vertical-align: top; width: 150px; }} figure img {{ max-width: 150px; }}</style>
<h1>圖庫</h1>
<h2>書籍封面</h2>
<div id="books">{"".join(books)}</div>
<h2>其他圖片</h2>
<div id="extras">{"".join(extras)}</div>
<h2>舊資料</h2>
<div id="old">
<figure><img src="images/missing.jpg" alt="已下架的封面"><figcaption>已下架的封面</figcaption></figure>
<figure><img src="images/fake.jpg" alt="舊圖片"><figcaption>舊圖片</figcaption></figure>
</div>
<h2>檔案下載</h2>
<p><a href="/files/price_list.csv" id="csv-link">價目表（CSV）</a>　<a href="/files/big.bin" id="big-link">大型檔案（2 MB）</a></p>"""
    return render("圖庫", body)


FEED_STYLE = "<style>.post { min-height: 140px; border-bottom: 1px solid #ddd; padding: .5rem 0; } .post-meta { color: #666; }</style>"

PAGE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }}
table {{ border-collapse: collapse; }} td, th {{ border: 1px solid #ccc; padding: .3rem .6rem; }}
.error {{ color: #b00020; }} nav a {{ margin-right: 1rem; }}
</style>
</head>
<body>
<nav><a href="/">首頁</a><a href="/login">登入</a><a href="/members">會員頁</a><a href="/search">搜尋</a><a href="/delayed">延遲載入</a></nav>
{body}
</body>
</html>
"""


def render(title: str, body: str) -> bytes:
    return PAGE.format(title=html.escape(title), body=body).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server: "PracticeServer"

    def log_message(self, *args) -> None:  # keep the terminal quiet
        pass

    def send(
        self,
        status: int,
        body: bytes,
        headers: dict[str, str] | None = None,
        content_type: str = "text/html; charset=utf-8",
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":  # a HEAD request gets the same headers, without the body
            self.wfile.write(body)

    def redirect(self, location: str, headers: dict[str, str] | None = None) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()

    def session_user(self) -> str | None:
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        if "session" in cookie:
            return self.server.sessions.get(cookie["session"].value)
        return None

    def login_page(self, error: str = "") -> bytes:
        token = secrets.token_hex(8)
        self.server.tokens.add(token)
        message = f'<p id="message" class="error">{html.escape(error)}</p>' if error else ""
        body = f"""
<h1>會員登入</h1>
{message}
<form method="post" action="/login" id="login-form">
  <input type="hidden" name="csrf_token" value="{token}">
  <p><label>帳號 <input type="text" name="username" id="username"></label></p>
  <p><label>密碼 <input type="password" name="password" id="password"></label></p>
  <p><button type="submit" id="login-button">登入</button></p>
</form>"""
        return render("會員登入", body)

    def do_GET(self) -> None:
        url = urlparse(self.path)
        query = parse_qs(url.query)

        if url.path == "/":
            body = (
                "<h1>本機練習站</h1><p>登入、Cookies、搜尋與動態載入的練習頁面。</p>"
                '<p><a href="/js-list">JavaScript 清單</a></p>'
                '<p><a href="/feed">無限捲動</a>　<a href="/load-more">載入更多按鈕</a></p>'
            )
            self.send(200, render("練習站", body))
        elif url.path == "/login":
            self.send(200, self.login_page())
        elif url.path == "/members":
            user = self.session_user()
            if user is None:
                self.redirect("/login")
                return
            rows = "".join(
                f"<tr><td>{order_id}</td><td>{html.escape(name)}</td><td>{price}</td><td>{status}</td></tr>"
                for order_id, name, price, status in ORDERS
            )
            body = f"""
<h1 id="welcome">歡迎回來，{html.escape(user)}</h1>
<table id="orders">
<thead><tr><th>訂單</th><th>課程</th><th>金額</th><th>狀態</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p><a href="/logout" id="logout">登出</a></p>"""
            self.send(200, render("會員頁", body))
        elif url.path == "/logout":
            cookie = SimpleCookie(self.headers.get("Cookie", ""))
            if "session" in cookie:
                self.server.sessions.pop(cookie["session"].value, None)
            self.redirect("/", {"Set-Cookie": "session=; Max-Age=0; Path=/"})
        elif url.path == "/search":
            keyword = query.get("q", [""])[0].strip()
            hits = [item for item in COURSES if keyword.lower() in item[0].lower()] if keyword else COURSES
            items = "".join(
                f'<li class="result"><span class="title">{html.escape(title)}</span> <span class="level">{level}</span></li>'
                for title, level in hits
            )
            body = f"""
<h1>課程搜尋</h1>
<form method="get" action="/search" id="search-form">
  <input type="text" name="q" id="q" value="{html.escape(keyword)}">
  <button type="submit" id="search-button">搜尋</button>
</form>
<p id="count">共 {len(hits)} 筆</p>
<ul id="results">{items}</ul>"""
            self.send(200, render("課程搜尋", body))
        elif url.path == "/js-list":
            body = """
<h1>JavaScript 清單</h1>
<ul id="list"></ul>
<script>
var items = ["Python 入門", "網頁爬蟲", "資料清理", "資料視覺化", "Selenium", "GitHub Pages"];
items.forEach(function (name) {
  var li = document.createElement("li");
  li.className = "course";
  li.textContent = name;
  document.getElementById("list").appendChild(li);
});
</script>"""
            self.send(200, render("JavaScript 清單", body))
        elif url.path == "/delayed":
            body = """
<h1>延遲載入</h1>
<div id="content">載入中……</div>
<script>
setTimeout(function () {
  document.getElementById("content").innerHTML =
    '<div id="result">資料載入完成：共 3 筆</div><ul id="items"><li>Alpha</li><li>Beta</li><li>Gamma</li></ul>';
}, 2000);
</script>"""
            self.send(200, render("延遲載入", body))
        elif url.path == "/feed":
            body = f"""{FEED_STYLE}
<h1>文章動態</h1>
<div id="feed"></div>
<p id="status">載入中……</p>
<script>
{POST_JS}
var offset = 0, loading = false, done = false;
function loadMore() {{
  if (loading || done) return;
  loading = true;
  fetch("/api/feed?offset=" + offset + "&limit={PAGE_SIZE}")
    .then(function (response) {{ return response.json(); }})
    .then(function (data) {{
      setTimeout(function () {{  // pretend the network is a little slow
        document.getElementById("feed").insertAdjacentHTML("beforeend", data.items.map(renderPost).join(""));
        if (data.next_offset === null) {{
          done = true;
          document.getElementById("status").outerHTML = '<p id="end-message">已載入全部 ' + data.total + ' 篇</p>';
        }} else {{
          offset = data.next_offset;
        }}
        loading = false;
      }}, 300);
    }});
}}
window.addEventListener("scroll", function () {{
  if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 100) loadMore();
}});
loadMore();
</script>"""
            self.send(200, render("文章動態", body))
        elif url.path == "/load-more":
            shown = "".join(post_html(post) for post in POSTS[:PAGE_SIZE])
            body = f"""{FEED_STYLE}
<h1>文章列表</h1>
<div id="feed">{shown}</div>
<button type="button" id="load-more">載入更多</button>
<script>
{POST_JS}
var offset = {PAGE_SIZE};
var button = document.getElementById("load-more");
button.addEventListener("click", function () {{
  button.disabled = true;
  fetch("/api/feed?offset=" + offset + "&limit={PAGE_SIZE}&max={LOAD_MORE_TOTAL}")
    .then(function (response) {{ return response.json(); }})
    .then(function (data) {{
      setTimeout(function () {{
        document.getElementById("feed").insertAdjacentHTML("beforeend", data.items.map(renderPost).join(""));
        if (data.next_offset === null) {{
          button.remove();
        }} else {{
          offset = data.next_offset;
          button.disabled = false;
        }}
      }}, 300);
    }});
}});
</script>"""
            self.send(200, render("文章列表", body))
        elif url.path == "/api/feed":
            try:
                offset = int(query.get("offset", ["0"])[0])
                limit = min(int(query.get("limit", [str(PAGE_SIZE)])[0]), 100)
                cap = min(int(query.get("max", [str(POST_TOTAL)])[0]), POST_TOTAL)
            except ValueError:
                self.send(400, json.dumps({"error": "offset、limit、max 都要是整數"}, ensure_ascii=False).encode("utf-8"),
                          content_type="application/json; charset=utf-8")
                return
            items = POSTS[offset : min(offset + limit, cap)] if offset >= 0 else []
            next_offset = offset + len(items) if offset + len(items) < cap else None
            payload = {"items": items, "next_offset": next_offset, "total": cap}
            self.send(200, json.dumps(payload, ensure_ascii=False).encode("utf-8"), content_type="application/json; charset=utf-8")
        elif url.path == "/gallery":
            page = gallery_page()
            if page is None:
                self.send(404, render("圖庫", "<h1>圖庫還沒建立</h1><p>先執行 python tools/build_fixtures.py images</p>"))
            else:
                self.send(200, page)
        elif url.path.startswith("/images/"):
            self.send_image(url.path.removeprefix("/images/"))
        elif url.path == "/files/price_list.csv":
            self.send(
                200,
                PRICE_LIST_CSV.encode("utf-8"),
                {"Content-Disposition": 'attachment; filename="price_list.csv"'},
                content_type="text/csv; charset=utf-8",
            )
        elif url.path == "/files/big.bin":
            self.send(
                200,
                BIG_FILE,
                {"Content-Disposition": 'attachment; filename="big.bin"'},
                content_type="application/octet-stream",
            )
        else:
            self.send(404, render("找不到頁面", "<h1>404</h1><p>找不到這個頁面。</p>"))

    do_HEAD = do_GET

    def send_image(self, name: str) -> None:
        if name == "loading.gif":
            self.send(200, PLACEHOLDER_GIF, content_type="image/gif")
        elif name == "fake.jpg":  # looks like a picture, but the server answers 200 with a web page
            self.send(200, render("錯誤", "<h1>這不是圖片</h1><p>圖片已移除，請見首頁。</p>"))
        else:
            path = GALLERY_DIR / Path(name).name  # Path(...).name keeps only the file name
            if path.suffix in IMAGE_TYPES and path.is_file():
                self.send(200, path.read_bytes(), content_type=IMAGE_TYPES[path.suffix])
            else:
                self.send(404, render("找不到圖片", "<h1>404</h1><p>找不到這張圖片。</p>"))

    def do_POST(self) -> None:
        url = urlparse(self.path)
        if url.path != "/login":
            self.send(404, render("找不到頁面", "<h1>404</h1>"))
            return
        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        token = form.get("csrf_token", [""])[0]
        username = form.get("username", [""])[0]
        password = form.get("password", [""])[0]

        if token not in self.server.tokens:
            self.send(403, render("拒絕", "<h1>403</h1><p>表單已失效，請重新整理登入頁。</p>"))
            return
        self.server.tokens.discard(token)

        if username == TEST_USER and password == TEST_PASSWORD:
            session_id = secrets.token_hex(16)
            self.server.sessions[session_id] = username
            self.redirect("/members", {"Set-Cookie": f"session={session_id}; Path=/; HttpOnly"})
        else:
            self.send(200, self.login_page("帳號或密碼錯誤"))


class PracticeServer(ThreadingHTTPServer):
    tokens: set[str]
    sessions: dict[str, str]


def start_server(port: int = 0, host: str = "127.0.0.1") -> tuple[PracticeServer, str]:
    """Start the site in a background thread. Returns (server, base_url)."""
    server = PracticeServer((host, port), Handler)
    server.tokens = set()
    server.sessions = {}
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://{host}:{server.server_address[1]}"


def stop_server(server: PracticeServer) -> None:
    server.shutdown()
    server.server_close()


if __name__ == "__main__":
    running, base = start_server(port=8000)
    print(f"練習站已啟動：{base}　（Ctrl+C 結束）")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        stop_server(running)
