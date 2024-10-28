import heapq
import logging
from .models import  Product, UserInteraction
from datetime import datetime
from collections import Counter


def get_item_recommend(cart, num_recommendations=5):
    product_ids = list(cart.keys())
    product_ids = list(map(int, product_ids))

    logging.debug("Product IDs in cart: %s", product_ids)

    products = Product.objects.filter(id__in=product_ids)
    sub_categories = products.values_list('subcategory', flat=True)
    recommended_products = Product.objects.filter(subcategory__in=sub_categories).exclude(
        id__in=products
    )[:5]

    user_interactions = UserInteraction.objects.filter(product__id__in=product_ids).values_list('user_id', 'product_id')

    user_similarity = {}
    for user_id, product_id in user_interactions:
        if user_id not in user_similarity:
            user_similarity[user_id] = Counter()
        user_similarity[user_id][product_id] += 1

    most_similar_users = Counter()
    for user_id, items in user_similarity.items():
        most_similar_users.update(items)

    for product_id in product_ids:
        most_similar_users[product_id] = 0

    recommended_product_ids = [product_id for product_id, _ in most_similar_users.most_common(num_recommendations)]
    logging.debug("Recommended Product IDs: %s", recommended_product_ids)

    cart_subcategories = set(products.values_list('subcategory', flat=True))
    recommended_products = Product.objects.filter(
        subcategory__in=cart_subcategories
    ).exclude(
        id__in=products
    )[:num_recommendations]

    logging.debug("Recommended Products: %s", recommended_products)

    return recommended_products