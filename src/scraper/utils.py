import requests
from urllib.parse import urljoin
import re

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def safe_request(url):
    """Make a safe HTTP request."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException:
        return None

def clean_text(text):
    """Clean and strip text."""
    if text:
        return text.strip()
    return ""

def normalize_price(price_str):
    """Extract numeric price from string."""
    if not price_str:
        return 0.0
    match = re.search(r'(\d+\.?\d*)', price_str)
    if match:
        return float(match.group(1))
    return 0.0

def deduplicate(products):
    """Remove duplicate products based on title and url."""
    seen = set()
    unique = []
    for p in products:
        key = (p.get('title', ''), p.get('url', ''))
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique

def url_join(base, url):
    """Join base URL with relative URL."""
    return urljoin(base, url)