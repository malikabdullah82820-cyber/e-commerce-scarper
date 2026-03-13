import csv

def export_products(products, filepath):
    if not products:
        return
    fieldnames = ['category', 'subcategory', 'title', 'price', 'product_url', 'image_url', 'description', 'review_count', 'rating', 'specs', 'source_page']
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            writer.writerow(p)

def export_summary(summary, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category_subcategory', 'total_products', 'avg_price', 'min_price', 'max_price', 'missing_descriptions', 'duplicates_removed'])
        for key, data in summary.items():
            writer.writerow([key, data['count'], data['avg_price'], data['min_price'], data['max_price'], data['missing_desc'], data['dup_removed']])