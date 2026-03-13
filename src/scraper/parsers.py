import re
from .utils import clean_text, normalize_price, url_join, safe_request, BASE_URL
from bs4 import BeautifulSoup

def parse_product_detail(url, category, subcategory, page_num):
    response = safe_request(url)
    if not response:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    # Title and Price
    h4s = soup.find_all('h4')
    title = ""
    price_str = ""
    for h4 in h4s:
        text = clean_text(h4.text)
        if '$' in text:
            price_str = text
        else:
            title = text
    price = normalize_price(price_str)
    # Description
    desc_elem = soup.find('p', {'class': 'description'}) or soup.find('p')
    description = clean_text(desc_elem.text) if desc_elem else ""
    # Image
    img_elem = soup.find('img', {'class': 'card-img-top'})
    img_src = img_elem.get('src') if img_elem else ""
    image_url = url_join(BASE_URL, img_src) if img_src else ""
    # Reviews
    review_elem = soup.find('p', string=lambda x: x and 'reviews' in x)
    review_text = clean_text(review_elem) if review_elem else "0 reviews"
    review_count = int(re.search(r'(\d+)', review_text).group(1)) if re.search(r'(\d+)', review_text) else 0
    # Rating
    rating = len(soup.select('.glyphicon-star'))
    # Specs
    specs_elem = soup.find('p', string=lambda x: x and ('HDD' in x or 'RAM' in x))
    specs = clean_text(specs_elem) if specs_elem else ""
    return {
        'category': category,
        'subcategory': subcategory,
        'title': title,
        'price': price,
        'product_url': url,
        'image_url': image_url,
        'description': description,
        'review_count': review_count,
        'rating': rating,
        'specs': specs,
        'source_page': page_num
    }