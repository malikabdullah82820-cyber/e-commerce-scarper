# Job Market Analysis - Web Scraping Project

## Project Overview
This project uses Selenium and Scrapy to collect and analyze job listings from multiple public career boards. It demonstrates a professional web scraping workflow with proper data extraction, cleaning, and analysis.

## Objective
- Automate browser interactions to discover job listings using Selenium
- Extract structured job data using Scrapy
- Generate insights about hiring trends, required skills, and market demand

## Data Sources
The project scrapes public career pages from:
1. **GitHub Job Board** - Tech roles in software development
2. **LinkedIn Jobs** (public filtered listings) - Diverse roles across sectors
3. **Company Career Pages** (Greenhouse/Lever powered) - Direct company listings
4. **Government Job Portals** - Public sector opportunities

All sources are publicly accessible without authentication.

## Project Structure
```
.
├── selenium/                 # Browser automation scripts
│   ├── job_search.py        # Main Selenium search and link collection
│   ├── config.py            # Configuration for search parameters
│   └── utils.py             # Helper functions for Selenium
├── scrapy_project/          # Scrapy spider and configuration
│   ├── scrapy.cfg           # Scrapy project configuration
│   ├── settings.py          # Scrapy settings
│   ├── spiders/
│   │   └── job_spider.py    # Main spider for job extraction
│   ├── items.py             # Item definitions
│   ├── pipelines.py         # Data processing pipelines
│   └── middlewares.py       # Custom middlewares
├── data/
│   ├── raw/                 # Raw job links from Selenium
│   │   └── job_links.csv    # Collected job URLs
│   └── final/               # Final processed data
│       └── jobs.csv         # Final cleaned dataset
├── analysis/
│   ├── analyze_jobs.py      # Analysis and insights generation
│   └── report.md            # Analysis findings and visualizations
├── docs/
│   ├── setup.md             # Setup and installation guide
│   └── approach.md          # Methodology documentation
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore patterns
```

## Required Data Fields
Each job record includes:
- **Job Title** - Exact posting title
- **Company** - Employer name
- **Location** - City/Country/Region (or Remote/Hybrid designation)
- **Department** - Team or functional area
- **Employment Type** - Full-time, Contract, Internship, Part-time
- **Posted Date** - When the job was listed
- **Job URL** - Link to full job posting
- **Job Description** - Full or summarized description
- **Required Skills** - Extracted or parsed skills list
- **Experience Level** (optional) - Junior/Mid/Senior
- **Salary** (optional) - If publicly available

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Chrome or Firefox browser
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/malikabdullah82820/job-market-analysis.git
   cd job-market-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download WebDriver**
   - For Chrome: Download ChromeDriver from https://chromedriver.chromium.org/
   - For Firefox: Download GeckoDriver from https://github.com/mozilla/geckodriver/releases
   - Place in project root or add to PATH

## Usage

### Step 1: Run Selenium to Collect Job Links
```bash
python -m selenium.job_search
```
This will:
- Open a browser session
- Search for target job roles
- Collect job detail URLs
- Export to `data/raw/job_links.csv`

### Step 2: Run Scrapy to Extract Job Details
```bash
cd scrapy_project
scrapy crawl jobs -o ../data/final/jobs.csv
```
This will:
- Read job links from `job_links.csv`
- Visit each job page
- Extract structured data
- Export to `data/final/jobs.csv`

### Step 3: Run Analysis
```bash
python -m analysis.analyze_jobs
```
This will:
- Analyze the collected data
- Generate insights report
- Create visualizations
- Save findings to `analysis/report.md`

## Analysis Output

The analysis generates insights on:
- **Top Skills** - Most frequently required skills
- **Location Trends** - Cities/regions with most openings
- **Company Activity** - Most active hiring companies
- **Entry-level Opportunities** - Internship and junior positions
- **Job Titles** - Most common role families

## Git Workflow

This project follows a professional branching strategy:

### Branches
- **main** - Stable, production-ready code (protected)
- **develop** - Integration branch for tested features
- **feature/\*** - Individual feature development
- **bugfix/\*** - Bug fixes
- **release/\*** - Release preparation

### Making Changes
1. Create a feature branch from develop:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit with clear messages:
   ```bash
   git add .
   git commit -m "Add Selenium filtering for location"
   ```

3. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

4. After review and approval, merge into develop and eventually main

## Compliance & Ethics
- ✅ Only scrapes publicly available pages
- ✅ No authentication bypass or CAPTCHA solving
- ✅ Respects site terms of service and robots.txt
- ✅ Implements polite request delays
- ✅ No collection of personal candidate data
- ✅ Transparent source attribution

## Results Summary

Upon completion, the project provides:
1. **job_links.csv** - Index of 1,000+ job URLs (intermediate output)
2. **jobs.csv** - Clean, structured dataset with 1,000+ job records
3. **Analysis Report** - Hiring trend insights and interpretations
4. **GitHub History** - Professional commit history with feature branches and PRs

## Troubleshooting

### Selenium Issues
- **WebDriver not found**: Ensure ChromeDriver/GeckoDriver is in PATH
- **Element not found**: Increase wait times in config
- **Site blocks requests**: Add longer delays between requests

### Scrapy Issues
- **Links not opening**: Check job_links.csv exists and is properly formatted
- **Missing fields**: Adjust CSS selectors in spider for target site
- **Memory issues**: Process in smaller batches

### Analysis Issues
- **Empty results**: Ensure jobs.csv has data
- **Missing columns**: Check that all required fields were extracted

## Dependencies
See `requirements.txt` for complete list. Key packages:
- Selenium - Browser automation
- Scrapy - Web scraping framework
- Pandas - Data analysis
- Matplotlib/Seaborn - Visualizations

## Author
Submitted for: Tools & Techniques for Data Science (Assignment 1)
Account: malikabdullah82820@gmail.com
Date: March 2026

## License
This project is for educational purposes as part of university coursework.
