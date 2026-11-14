import argparse
import csv
from pathlib import Path

from mit_crawler.common import CSV_HEADERS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", default="output/mit_admissions_articles.csv")
    args = parser.parse_args()
    by_title: dict[str, dict[str, str]] = {}
    for input_name in args.inputs:
        with open(input_name, encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("Title"):
                    by_title[row["Title"]] = row
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(by_title.values())


if __name__ == "__main__":
    main()
