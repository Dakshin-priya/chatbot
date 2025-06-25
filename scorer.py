def compute_match_score(product, context):
    budget_score = 1 if product['price'] <= int(context.get('budget', 0)) else 0.5
    brand_score = 1 if context.get('brand', '').lower() in product['name'].lower() else 0.5
    feature_score = 1 if context.get('features', '').lower() in product['features'].lower() else 0.5
    purpose_score = 1 if context.get('purpose', '').lower() in product['features'].lower() else 0.5
    return (budget_score + brand_score + feature_score + purpose_score) / 4

def select_best_product(products, context):
    for product in products:
        product['match_percent'] = round(compute_match_score(product, context) * 100, 2)
    return max(products, key=lambda x: x['match_percent'])