import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Product

def get_item_recommendations(cart, num_recommendations=5):
    product_ids = list(cart.keys())
    product_ids = list(map(int, product_ids))

    logging.debug("Product IDs in cart: %s", product_ids)

    products = Product.objects.filter(id__in=product_ids)
    sub_categories = products.values_list('subcategory', flat=True)
    recommended_products = Product.objects.filter(subcategory__in=sub_categories).exclude(
        id__in=products
    )[:5]
    product_descriptions = [product.descriptions for product in products]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(product_descriptions)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    logging.debug("Cosine Similarities: %s", cosine_similarities)

    product_indices = list(range(len(products)))

    recommendations = []
    for product_id in product_ids:
        product_index = product_ids.index(product_id)
        similarity_scores = cosine_similarities[product_index]

        logging.debug("Similarity Scores: %s", similarity_scores)

        similar_indices = sorted(product_indices, key=lambda x: similarity_scores[x], reverse=True)
        similar_indices = [idx for idx in similar_indices if idx != product_index]
        top_similar_indices = similar_indices[:num_recommendations]

        logging.debug("Top Similar Indices: %s", top_similar_indices)

        recommended_product_ids = [product_ids[idx] for idx in top_similar_indices]

        logging.debug("Recommended Product IDs: %s", recommended_product_ids)

        recommended_products = Product.objects.filter(id__in=recommended_product_ids)
        recommendations.extend(recommended_products)

    recommendations = list(set(recommendations))

    logging.debug("Final Recommendations: %s", recommendations)

    return recommended_products[:num_recommendations]
