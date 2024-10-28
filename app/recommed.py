import logging
from django.db.models import Q
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Product, UserInteraction
import nltk
from nltk.corpus import stopwords


def get_item_recommendations(cart, num_recommendations=5):

    product_ids = list(map(int, cart.keys()))

    cart_products = Product.objects.filter(id__in=product_ids)

    cart_descriptions = [product.descriptions for product in cart_products]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = tfidf_vectorizer.fit_transform(cart_descriptions)

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    product_index_mapping = {product_id: index for index,
                             product_id in enumerate(product_ids)}

    recommended_product_ids = set()

    for product_id in product_ids:
        product_index = product_index_mapping[product_id]
        similarity_scores = cosine_similarities[product_index]

        similar_indices = np.argsort(similarity_scores)[::-1]

        cart_product_ids = set(product_ids)
        top_recommendations = [
            idx for idx in similar_indices if product_index_mapping[product_ids[idx]] not in cart_product_ids]

        recommended_product_ids.update(
            product_ids[idx] for idx in top_recommendations)

        if len(recommended_product_ids) >= num_recommendations:
            break

    recommended_products_tfidf = Product.objects.filter(
        id__in=list(recommended_product_ids))

    products = Product.objects.filter(id__in=product_ids)
    sub_categories = products.values_list('subcategory', flat=True)
    recommended_products_nn = Product.objects.filter(
        Q(subcategory__in=sub_categories) & ~Q(id__in=products)
    )[:num_recommendations]

    prod_recomm = list(
        recommended_products_tfidf) + list(recommended_products_nn)
    recommended_product_ids = [product.id for product in prod_recomm]

    print("The recommended Product IDs are:", recommended_product_ids)


    # print("The recommended Items is:", prod_recomm)
    logger = logging.getLogger(__name__)
    logger.info("The Recommendation items: %s", prod_recomm)
    return prod_recomm[:num_recommendations]
