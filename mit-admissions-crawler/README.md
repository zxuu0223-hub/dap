# MIT Admissions dual-engine crawler

Two independent implementations crawl `https://mitadmissions.org/blogs/` and write the required columns:

`Title | Author | Comment Count | Time | Article Content | Images In Article`

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
python -m mit_crawler.playwright_crawler --limit 10 --output output/playwright_results.csv
python -m mit_crawler.drissionpage_crawler --limit 10 --output output/drissionpage_results.csv
python merge_results.py output/playwright_results.csv output/drissionpage_results.csv --output output/mit_admissions_articles.csv
```

The CSV is UTF-8 with BOM for direct Excel compatibility. Duplicate titles are removed during merge.
