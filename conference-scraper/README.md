# Conference Scraper Pipeline

## 🧩 Overview

This project extracts conference listings and enriches them with detailed data.

Pipeline:

1. Copy HTML table → `input.html`
2. Extract → `conferences.csv`
3. Enrich → `conferences_enriched.csv`

---

## ⚙️ Setup (using uv)

Install dependencies:

```bash
uv add beautifulsoup4 playwright
uv run playwright install
```

---

## 🪜 Step 1: Extract table data

Paste `<tbody>` HTML into:

```
input.html
```

Run:

```bash
uv run extract_table.py
```

Output:

```
conferences.csv
```

---

## 🪜 Step 2: Enrich data (Cloudflare-safe)

Run:

```bash
uv run enrich_playwright.py
```

Output:

```
conferences_enriched.csv
```

---

## ⚠️ Notes

- Uses Playwright to bypass Cloudflare
- Browser runs in visible mode (`headless=False`)
- Expect ~2–5 seconds per URL

---

## 🚀 Future Improvements

- Async scraping (10x faster)
- Resume from failures
- Direct DB ingestion
- Deduplication

---

## 🧠 Pipeline Summary

```
HTML → CSV → Enriched CSV
```
