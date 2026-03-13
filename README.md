# E-commerce Scraper

## Project Purpose

This project is a mini web scraper for the static e-commerce test site at https://webscraper.io/test-sites/e-commerce/static. It navigates categories, subcategories, paginated listing pages, and product detail pages to extract product data and generate CSV reports.

## Setup Instructions

### Prerequisites

- Python (managed by uv)
- uv package manager

### Installation

1. Install uv if not already installed:

   ```bash
   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Clone the repository and navigate to the project directory.

3. Install dependencies:

   ```bash
   uv sync
   ```

## How to Run the Scraper

Run the scraper using uv:

```bash
uv run python src/main.py
```

This will generate `data/products.csv` and `data/category_summary.csv`.

## Branching Workflow Followed

This project follows Git branching best practices as required:

1. **Repository Initialization**:
   - Created repository with `main` branch.
   - Initial commit with uv project setup.

2. **Development Branch**:
   - Created `dev` branch from `main`.

3. **Feature Branches**:
   - Created `feature/catalog-navigation` for category and subcategory discovery, pagination handling.
   - Created `feature/product-details` for product detail page scraping and data extraction.
   - Merged both feature branches into `dev`.

4. **Fix Branches**:
   - Created `fix/url-resolution` for proper URL joining and relative link handling.
   - Created `fix/deduplication` for removing duplicate products from the dataset.
   - Merged both fix branches into `dev`.

5. **Final Merge**:
   - After testing, merged `dev` into `main`.

All work was done on appropriate branches, not directly on `main`.

## Assumptions

- The target website structure remains static as of the development time.
- Internet connection is available for scraping.
- The site does not have anti-scraping measures (as it's a test site).
- Product pages have consistent HTML structure.

## Limitations

- Scraping is done sequentially, not in parallel, so it may be slow for large sites.
- Error handling is basic; some edge cases may not be covered.
- No retry mechanism for failed requests beyond the initial attempt.
- Assumes English content; no internationalization support.

## Project Structure

```
project/
├── pyproject.toml
├── README.md
├── data/
│   ├── products.csv
│   └── category_summary.csv
├── src/
│   ├── main.py
│   └── scraper/
│       ├── crawler.py
│       ├── parsers.py
│       ├── exporters.py
│       └── utils.py
└── tests/
```

## Dependencies

- requests: For HTTP requests
- beautifulsoup4: For HTML parsing

Managed by uv in `pyproject.toml`.
