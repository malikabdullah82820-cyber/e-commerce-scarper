# Setup and Installation Guide

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)
- Git
- A text editor or IDE (VS Code, PyCharm, etc.)
- Chrome or Firefox browser

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/malikabdullah82820/job-market-analysis.git
cd job-market-analysis
```

### 2. Create Virtual Environment

It's recommended to create a virtual environment to avoid conflicts with other Python projects.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **Selenium** - Browser automation
- **Scrapy** - Web scraping framework
- **Pandas** - Data analysis
- **Matplotlib/Seaborn** - Visualizations

### 4. Download WebDriver

#### For Chrome:
1. Visit https://chromedriver.chromium.org/
2. Download ChromeDriver matching your Chrome version
3. Extract it to your project root or add to PATH

#### For Firefox:
1. Visit https://github.com/mozilla/geckodriver/releases
2. Download GeckoDriver for your OS
3. Extract it to your project root or add to PATH

### 5. Project Structure Verification

Verify that all directories exist:
```
.
├── selenium/
├── scrapy_project/
├── analysis/
├── data/
│   ├── raw/
│   └── final/
├── docs/
└── README.md
```

## Running the Project

### Full Workflow

```bash
# Step 1: Run Selenium to collect job links
python -m selenium.job_search

# Step 2: Run Scrapy to extract job details
cd scrapy_project
scrapy crawl jobs -o ../data/final/jobs.csv

# Step 3: Run analysis
cd ..
python -m analysis.analyze_jobs
```

### Individual Components

#### Selenium Only
```bash
python -m selenium.job_search
```

#### Scrapy Only
```bash
cd scrapy_project
scrapy crawl jobs
```

#### Analysis Only
```bash
python -m analysis.analyze_jobs
```

## Troubleshooting

### WebDriver Issues

**Error: "ChromeDriver not found"**
- Ensure ChromeDriver is in your PATH
- Or place it in the project root directory
- Or update the path in the code

**Error: "Chrome crashes during automation"**
- Update Chrome browser
- Update ChromeDriver to matching version
- Try running with `--no-sandbox` flag

### Selenium Issues

**Element not found errors**
- Website structure might have changed
- Update CSS selectors in `selenium/job_search.py`
- Increase wait timeouts in `selenium/config.py`

### Scrapy Issues

**No data being extracted**
- Ensure `job_links.csv` exists in `data/raw/`
- Check that links are accessible
- Update CSS selectors in spider if site structure changed
- Check Scrapy logs for errors

**Rate limiting/403 errors**
- Increase DOWNLOAD_DELAY in `scrapy_project/settings.py`
- Add random delays between requests
- Respect robots.txt

## Configuration

### Selenium Config (`selenium/config.py`)

```python
JOB_TITLES = ["Software Engineer", ...]  # Search terms
LOCATIONS = ["New York", ...]             # Location filters
HEADLESS = False                          # Run browser in headless mode
TIMEOUT = 30                              # Element wait timeout (seconds)
POLITE_DELAY = 2                          # Delay between requests (seconds)
```

### Scrapy Config (`scrapy_project/settings.py`)

```python
DOWNLOAD_DELAY = 1                        # Delay between requests
CONCURRENT_REQUESTS = 16                  # Parallel requests
ROBOTSTXT_OBEY = True                    # Respect robots.txt
```

## Expected Output

After running the full workflow, you should have:

1. **data/raw/job_links.csv** - List of job URLs collected by Selenium
2. **data/final/jobs.csv** - Structured job data extracted by Scrapy
3. **analysis/report.md** - Analysis report with insights

## Performance Notes

- Initial run may take 10-30 minutes depending on network
- Number of jobs collected depends on search parameters
- Scrapy processes faster than Selenium collection
- Analysis runs are typically < 1 minute

## Next Steps

1. Review the README.md for project overview
2. Check analysis/report.md for findings
3. Explore data/final/jobs.csv for raw data
4. Modify scripts for different data sources
5. Extend analysis with additional metrics

## Support

For issues or questions:
1. Check this setup guide
2. Review project README.md
3. Check Scrapy documentation: https://docs.scrapy.org/
4. Check Selenium documentation: https://www.selenium.dev/documentation/
