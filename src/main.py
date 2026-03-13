import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scraper.crawler import get_categories, get_subcategories, get_product_links, get_cat_sub_from_url
from scraper.parsers import parse_product_detail
from scraper.exporters import export_products, export_summary
from scraper.utils import deduplicate

def main():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    all_products = []
    categories = get_categories()
    for cat_url in categories:
        cat, _ = get_cat_sub_from_url(cat_url)
        subs = get_subcategories(cat_url)
        for sub_url in subs:
            _, sub = get_cat_sub_from_url(sub_url)
            product_urls = get_product_links(sub_url)
            page_num = 1  # approximate
            for url in product_urls:
                product = parse_product_detail(url, cat, sub, page_num)
                if product:
                    all_products.append(product)
    # deduplicate
    unique_products = deduplicate(all_products)
    dup_removed = len(all_products) - len(unique_products)
    # export products
    export_products(unique_products, os.path.join(data_dir, 'products.csv'))
    # generate summary
    summary = {}
    for p in unique_products:
        key = f"{p['category']}_{p['subcategory']}"
        if key not in summary:
            summary[key] = {'prices': [], 'missing_desc': 0, 'count': 0, 'dup_removed': dup_removed}
        summary[key]['prices'].append(p['price'])
        if not p['description']:
            summary[key]['missing_desc'] += 1
        summary[key]['count'] += 1
    for key, data in summary.items():
        prices = data['prices']
        data['avg_price'] = round(sum(prices) / len(prices), 2) if prices else 0
        data['min_price'] = min(prices) if prices else 0
        data['max_price'] = max(prices) if prices else 0
    export_summary(summary, os.path.join(data_dir, 'category_summary.csv'))

if __name__ == "__main__":
    main()
