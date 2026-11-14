import csv
import re
from dataclasses import asdict, dataclass
from pathlib import Path


CSV_HEADERS = ["Title", "Author", "Comment Count", "Time", "Article Content", "Images In Article"]


@dataclass(frozen=True)
class Article:
    title: str
    author: str
    comment_count: int
    time: str
    article_content: str
    images_in_article: str


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def parse_comment_count(value: str) -> int:
    match = re.search(r"\d+", value or "")
    return int(match.group()) if match else 0


def write_csv(records: list[Article], output: str | Path) -> None:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for record in records:
            writer.writerow({
                "Title": record.title,
                "Author": record.author,
                "Comment Count": record.comment_count,
                "Time": record.time,
                "Article Content": record.article_content,
                "Images In Article": record.images_in_article,
            })
