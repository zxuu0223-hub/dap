import argparse
import re
from urllib.parse import urljoin

from playwright.sync_api import Page, sync_playwright

from .common import Article, normalize_text, parse_comment_count, write_csv

BASE_URL = "https://mitadmissions.org/blogs/"


def collect_links(page: Page, limit: int) -> list[str]:
    page.goto(BASE_URL, wait_until="domcontentloaded")
    anchors = page.locator("article a[href*='/blogs/entry/'], a[href*='/blogs/entry/']")
    links: list[str] = []
    for href in anchors.evaluate_all("els => els.map(el => el.href)"):
        clean = href.split("#")[0]
        if clean not in links:
            links.append(clean)
        if len(links) >= limit:
            break
    return links


def parse_article(page: Page, url: str) -> Article:
    page.goto(url, wait_until="domcontentloaded")
    article = page.locator("main article").first
    author_locator = article.locator("h1 a[href*='/blogs/author/']").first
    author = normalize_text(author_locator.inner_text()) if author_locator.count() else ""
    author = re.sub(r"^by\s+", "", author, flags=re.IGNORECASE)
    title = normalize_text(article.locator("h1").first.inner_text())
    if author:
        title = normalize_text(re.sub(rf"\s*by\s+{re.escape(author)}\s*$", "", title, flags=re.IGNORECASE))
    time_locator = article.locator("time").first
    published = (time_locator.get_attribute("datetime") or normalize_text(time_locator.inner_text())) if time_locator.count() else ""
    content_nodes = article.locator("p, h2, h3")
    content = normalize_text("\n".join(content_nodes.all_text_contents()))
    images = [urljoin(url, src) for src in article.locator("img").evaluate_all("els => els.map(el => el.currentSrc || el.src)") if src]
    comment_locator = page.locator("a[href*='#comments'], .comments-link, .comment-count").first
    comment_text = comment_locator.inner_text(timeout=2_000) if comment_locator.count() else "0"
    return Article(title, author, parse_comment_count(comment_text), published, content, " | ".join(images))


def crawl(limit: int) -> list[Article]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        links = collect_links(page, limit)
        records = [parse_article(page, link) for link in links]
        browser.close()
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", default="output/playwright_results.csv")
    args = parser.parse_args()
    write_csv(crawl(args.limit), args.output)


if __name__ == "__main__":
    main()
