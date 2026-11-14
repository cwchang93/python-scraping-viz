"""Rebuild the scraped datasets used by lessons 05 and 06 from the practice sites.

    python tools/build_fixtures.py books     # lesson 05: 1000 raw book rows + one detail page
    python tools/build_fixtures.py quotes    # lesson 06: raw quotes and author pages
    python tools/build_fixtures.py api       # lesson 07: JSON snapshots (quotes API, YouBike)
    python tools/build_fixtures.py selenium  # lessons 08, 09: rendered HTML from the local practice site (needs Chrome)
    python tools/build_fixtures.py images    # lesson 10: 12 book covers plus 3 generated pictures (needs Pillow)
    python tools/build_fixtures.py all

Both sites are built for scraping practice. Requests are spaced one second apart.
The raw text is kept as scraped on purpose: cleaning it is what the lessons teach.
"""

from __future__ import annotations

import csv
import json
import logging
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BOOKS_DIR = ROOT / "lessons/lesson06_tidy_scraped_data/fixtures"
QUOTES_DIR = ROOT / "lessons/lesson07_cleaning_scraped_data/fixtures"
API_DIR = ROOT / "lessons/lesson08_json_api_and_sessions/fixtures"
SELENIUM_DIR = ROOT / "lessons/lesson09_selenium_basics/fixtures"
FEED_DIR = ROOT / "lessons/lesson10_scroll_and_load_more/fixtures"
GALLERY_DIR = ROOT / "lessons/lesson11_images_and_files/fixtures/gallery"
YOUBIKE_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
YOUBIKE_SAMPLE_STEP = 6  # keep every 6th station so all districts are covered
USER_AGENT = "python-scraping-viz-class/0.1 (student project)"
DELAY = 1.0

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("fixtures")


def get(url: str) -> requests.Response:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    response.raise_for_status()
    return response


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.info("wrote %s (%d rows)", path.relative_to(ROOT), len(rows))


def build_books() -> None:
    rows: list[dict] = []
    url: str | None = "https://books.toscrape.com/"
    page = 0
    while url:
        page += 1
        response = get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        for pod in soup.select("article.product_pod"):
            link = pod.select_one("h3 a")
            rows.append(
                {
                    "title": link["title"],
                    "price_text": pod.select_one("p.price_color").get_text(),
                    "rating_word": pod.select_one("p.star-rating")["class"][1],
                    "availability": pod.select_one("p.availability").get_text(strip=True),
                    "url": urljoin(url, link["href"]),
                }
            )
        log.info("books page %d: total %d", page, len(rows))
        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None
        if url:
            time.sleep(DELAY)
    write_csv(BOOKS_DIR / "books_raw.csv", ["title", "price_text", "rating_word", "availability", "url"], rows)

    detail_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    time.sleep(DELAY)
    (BOOKS_DIR / "book_detail.html").write_bytes(get(detail_url).content)
    log.info("wrote book_detail.html")


def build_quotes() -> None:
    quotes: list[dict] = []
    url: str | None = "https://quotes.toscrape.com/"
    page = 0
    while url:
        page += 1
        soup = BeautifulSoup(get(url).content, "html.parser")
        for quote in soup.select("div.quote"):
            keywords = quote.select_one("meta.keywords")
            quotes.append(
                {
                    "page": page,
                    "text": quote.select_one("span.text").get_text(),
                    "author": quote.select_one("small.author").get_text(),
                    "tags_text": keywords["content"] if keywords else "",
                    "author_url": quote.select_one("a")["href"],
                }
            )
        log.info("quotes page %d: total %d", page, len(quotes))
        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None
        if url:
            time.sleep(DELAY)
    write_csv(QUOTES_DIR / "quotes_raw.csv", ["page", "text", "author", "tags_text", "author_url"], quotes)

    authors: list[dict] = []
    seen: set[str] = set()
    for quote in quotes:
        author_url = quote["author_url"]
        if author_url in seen:
            continue
        seen.add(author_url)
        time.sleep(DELAY)
        soup = BeautifulSoup(get(urljoin("https://quotes.toscrape.com/", author_url)).content, "html.parser")
        authors.append(
            {
                "author_url": author_url,
                "name": soup.select_one("h3.author-title").get_text(),
                "born_date_text": soup.select_one("span.author-born-date").get_text(),
                "born_location_text": soup.select_one("span.author-born-location").get_text(),
                "description": soup.select_one("div.author-description").get_text(),
            }
        )
        log.info("author %d: %s", len(authors), authors[-1]["name"].strip())
    write_csv(
        QUOTES_DIR / "authors_raw.csv",
        ["author_url", "name", "born_date_text", "born_location_text", "description"],
        authors,
    )


def build_api() -> None:
    API_DIR.mkdir(parents=True, exist_ok=True)
    for page in (1, 2):
        data = get(f"https://quotes.toscrape.com/api/quotes?page={page}").json()
        (API_DIR / f"quotes_api_page{page}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        log.info("wrote quotes_api_page%d.json (%d quotes)", page, len(data["quotes"]))
        time.sleep(DELAY)

    stations = get(YOUBIKE_URL).json()
    sample = stations[::YOUBIKE_SAMPLE_STEP]
    (API_DIR / "youbike_sample.json").write_text(json.dumps(sample, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info("wrote youbike_sample.json (%d of %d stations, updated %s)", len(sample), len(stations), sample[0].get("srcUpdateTime"))


def build_selenium() -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    from practice_site import start_server, stop_server
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    SELENIUM_DIR.mkdir(parents=True, exist_ok=True)
    FEED_DIR.mkdir(parents=True, exist_ok=True)
    server, base = start_server()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    try:
        with webdriver.Chrome(options=options) as driver:
            driver.get(f"{base}/delayed")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result")))
            (SELENIUM_DIR / "delayed_rendered.html").write_text(driver.page_source, encoding="utf-8")
            log.info("wrote delayed_rendered.html")

            # lesson 09: scroll /feed until the end message appears, then keep the rendered page
            driver.get(f"{base}/feed")
            while True:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.post")))
                if driver.find_elements(By.ID, "end-message"):
                    break
                before = len(driver.find_elements(By.CSS_SELECTOR, "article.post"))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                WebDriverWait(driver, 10).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, "article.post")) > before
                )
            (FEED_DIR / "feed_rendered.html").write_text(driver.page_source, encoding="utf-8")
            log.info("wrote feed_rendered.html")
    finally:
        stop_server(server)


def build_images() -> None:
    """lesson 10: 12 real book covers from books.toscrape.com plus 3 generated pictures."""
    from PIL import Image, ImageDraw, ImageFont

    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    start_url = "https://books.toscrape.com/"
    soup = BeautifulSoup(get(start_url).content, "html.parser")
    rows: list[dict] = []
    for number, pod in enumerate(soup.select("article.product_pod")[:12], start=1):
        # the list page only has ~100px thumbnails; the detail page has the larger cover (about 318x395)
        detail_url = urljoin(start_url, pod.select_one("h3 a")["href"])
        time.sleep(DELAY)
        detail = BeautifulSoup(get(detail_url).content, "html.parser")
        image = detail.select_one("div.item.active img")
        name = f"cover_{number:02d}.jpg"
        time.sleep(DELAY)
        (GALLERY_DIR / name).write_bytes(get(urljoin(detail_url, image["src"])).content)
        rows.append(
            {
                "file": name,
                "title": image["alt"],
                "rating": pod.select_one("p.star-rating")["class"][1],
                "kind": "book",
            }
        )
        log.info("cover %d: %s", number, image["alt"])

    try:
        font = ImageFont.load_default(size=72)
    except TypeError:  # Pillow older than 10.1 cannot choose the size
        font = ImageFont.load_default()

    # banner.png: RGBA with transparent corners (saving it as JPEG needs convert("RGB"))
    layer = Image.new("RGBA", (1200, 400))
    draw = ImageDraw.Draw(layer)
    for x in range(1200):
        draw.line([(x, 0), (x, 399)], fill=(20 + x // 8, 90 + x // 20, 160 - x // 12, 255))
    draw.text((60, 150), "SCRAPING CLASS", fill=(255, 255, 255, 255), font=font)
    mask = Image.new("L", (1200, 400), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 1199, 399), radius=60, fill=255)
    banner = Image.new("RGBA", (1200, 400), (0, 0, 0, 0))  # the corners stay fully transparent black
    banner.paste(layer, (0, 0), mask)
    banner.save(GALLERY_DIR / "banner.png")

    # landscape.jpg: a big, wide picture (1600x900)
    landscape = Image.new("RGB", (1600, 900))
    draw = ImageDraw.Draw(landscape)
    for y in range(900):
        if y < 600:
            draw.line([(0, y), (1599, y)], fill=(120 + y // 8, 170 + y // 12, 230))
        else:
            draw.line([(0, y), (1599, y)], fill=(40, 120 - (y - 600) // 8, 60))
    draw.ellipse((1150, 90, 1350, 290), fill=(255, 220, 90))
    landscape.save(GALLERY_DIR / "landscape.jpg", quality=90)

    # icon.png: a tiny 64x64 RGBA picture
    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ImageDraw.Draw(icon).ellipse((4, 4, 59, 59), fill=(231, 76, 60, 255), outline=(255, 255, 255, 255), width=3)
    icon.save(GALLERY_DIR / "icon.png")

    for name, title in (("banner.png", "Banner"), ("landscape.jpg", "Landscape"), ("icon.png", "Icon")):
        rows.append({"file": name, "title": title, "rating": "", "kind": "other"})
    write_csv(GALLERY_DIR / "manifest.csv", ["file", "title", "rating", "kind"], rows)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target not in {"books", "quotes", "api", "selenium", "images", "all"}:
        print(__doc__)
        return 2
    if target in {"books", "all"}:
        build_books()
    if target in {"quotes", "all"}:
        build_quotes()
    if target in {"api", "all"}:
        build_api()
    if target in {"selenium", "all"}:
        build_selenium()
    if target in {"images", "all"}:
        build_images()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
