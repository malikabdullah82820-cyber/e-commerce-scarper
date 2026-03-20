"""
Configuration for Selenium job search automation
"""

# Job search parameters
JOB_TITLES = ["Software Engineer", "Data Analyst", "Product Manager", "QA Engineer", "DevOps Engineer"]
LOCATIONS = ["New York", "San Francisco", "Austin", "Seattle", "Remote"]

# Browser settings
HEADLESS = False  # Set to True to run in headless mode
WINDOW_SIZE = (1920, 1080)
TIMEOUT = 30  # seconds

# Job boards to scrape
JOB_BOARDS = {
    "github_jobs": {
        "url": "https://github.com/jobs",
        "search_selector": "input[aria-label='Job search']",
        "search_parameter": "q",
        "results_selector": ".Box-row",
        "link_selector": "a.Link--primary",
        "enabled": True
    },
    "greenhouse": {
        "url": "https://boards.greenhouse.io",
        "description": "Greenhouse job boards (multiple companies)",
        "search_enabled": False  # Limited search capability
    },
    "lever": {
        "url": "https://www.lever.co/jobs",
        "description": "Lever job boards (multiple companies)",
        "search_enabled": False  # Limited search capability
    }
}

# Request settings
POLITE_DELAY = 2  # seconds between requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Output settings
OUTPUT_FILE = "data/raw/job_links.csv"
