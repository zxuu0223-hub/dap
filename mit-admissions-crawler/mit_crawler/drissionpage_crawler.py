import argparse
import re
from urllib.parse import urljoin

from DrissionPage import ChromiumOptions, ChromiumPage

from .common import Article, normalize_text, parse_comment_count, write_csv

BASE_URL = "https://mitadmissions.org/blogs/"


def first_text(page: ChromiumPage, selectors: list[str]) -> str:
    for selector in selectors:
        element = page.ele(selector, timeout=1)
        if element:
            return normalize_text(element.text)
    return ""


def crawl(limit: int) -> list[Article]:
    options = ChromiumOptions().headless().auto_port()
    page = ChromiumPage(options)
    page.get(BASE_URL)
    links: list[str] = []
    for anchor in page.eles("css:a[href*='/blogs/entry/']"):
        href = urljoin(BASE_URL, anchor.attr("href")).split("#")[0]
        if href not in links:
            links.append(href)
        if len(links) >= limit:
            break

    records: list[Article] = []
    for link in links:
        page.get(link)
        article = page.ele("css:main article", timeout=3)
        author = first_text(page, ["css:main article h1 a[href*='/blogs/author/']"])
        author = re.sub(r"^by\s+", "", author, flags=re.IGNORECASE)
        title = first_text(page, ["css:main article h1"])
        if author:
            title = normalize_text(re.sub(rf"\s*by\s+{re.escape(author)}\s*$", "", title, flags=re.IGNORECASE))
        time_element = page.ele("css:main article time", timeout=1)
        published = (time_element.attr("datetime") or normalize_text(time_element.text)) if time_element else ""
        content_elements = article.eles("css:p, h2, h3") if article else []
        content = normalize_text("\n".join(element.text for element in content_elements))
        images = [urljoin(link, image.attr("src")) for image in article.eles("tag:img") if image.attr("src")] if article else []
        comments = first_text(page, ["css:a[href*='#comments']", "css:.comments-link", "css:.comment-count"])
        records.append(Article(title, author, parse_comment_count(comments), published, content, " | ".join(images)))
    page.quit()
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", default="output/drissionpage_results.csv")
    args = parser.parse_args()
    write_csv(crawl(args.limit), args.output)


if __name__ == "__main__":
    main()
