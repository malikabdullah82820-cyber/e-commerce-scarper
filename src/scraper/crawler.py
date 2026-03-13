from .utils import safe_request, url_join
from bs4 import BeautifulSoup

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def get_categories():
    """Discover category URLs from the main page."""
    response = safe_request(BASE_URL)
    if not response:
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/computers' in href or '/phones' in href:
            full_url = url_join(BASE_URL, href)
            if full_url not in categories:
                categories.append(full_url)
    return categories

def get_subcategories(category_url):
    """Discover subcategory URLs from a category page."""
    response = safe_request(category_url)
    if not response:
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    subs = []
    cat = category_url.replace(BASE_URL, '').strip('/')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if f'/{cat}/' in href and not href.endswith(f'/{cat}') and '/product/' not in href:
            full_url = url_join(BASE_URL, href)
            if full_url not in subs:
                subs.append(full_url)
    return subs

def get_product_links(subcategory_url):
    """Collect all product URLs from a subcategory, handling pagination."""
    links = []
    page = 1
    while True:
        if page == 1:
            url = subcategory_url
        else:
            url = f"{subcategory_url}?page={page}"
        response = safe_request(url)
        if not response:
            break
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find product links
        for a in soup.select('h4 a[href*="/product/"]'):
            href = a['href']
            full_url = url_join(BASE_URL, href)
            if full_url not in links:
                links.append(full_url)
        # Check for next page
        next_link = soup.find('a', string='Next »')
        if not next_link:
            break
        page += 1
    return links

def get_cat_sub_from_url(url):
    """Extract category and subcategory from URL."""
    parts = url.replace(BASE_URL, '').strip('/').split('/')
    if len(parts) == 1:
        return parts[0], ''
    elif len(parts) >= 2:
        return parts[0], parts[1]
    return '', ''