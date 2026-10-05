"""Rebuild the scraped datasets used by lessons 05 and 06 from the practice sites.

    python tools/build_fixtures.py books     # lesson 05: 1000 raw book rows + one detail page
    python tools/build_fixtures.py quotes    # lesson 06: raw quotes and author pages
    python tools/build_fixtures.py all

Both sites are built for scraping practice. Requests are spaced one second apart.
The raw text is kept as scraped on purpose: cleaning it is what the lessons teach.
"""

from __future__ import annotations

import csv
import logging
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BOOKS_DIR = ROOT / "lessons/lesson05_tidy_scraped_data/fixtures"
QUOTES_DIR = ROOT / "lessons/lesson06_cleaning_scraped_data/fixtures"
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


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target not in {"books", "quotes", "all"}:
        print(__doc__)
        return 2
    if target in {"books", "all"}:
        build_books()
    if target in {"quotes", "all"}:
        build_quotes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
