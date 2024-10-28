# # utils.py
# from .models import Product
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from collections import defaultdict

# def get_item_recommendations(session_cart, num_recommendations=5):
#     # Extract the product IDs and quantities from the session cart
#     product_ids_in_cart = list(session_cart.keys())
#     cart_quantities = [int(quantity) for quantity in session_cart.values()]

#     # Get all product IDs in the database
#     all_product_ids = Product.objects.values_list('id', flat=True)

#     # Create a user-item interaction vector (1 if product in cart, 0 if not)
#     interaction_vector = [1 if str(product_id) in product_ids_in_cart else 0 for product_id in all_product_ids]

#     # Get the product names and their corresponding features
#     product_names = Product.objects.values_list('name', flat=True)
#     product_features = [f"{product.category_id} {product.brand_id}" for product in Product.objects.all()]

#     # Compute TF-IDF vectors for the product features
#     tfidf_vectorizer = TfidfVectorizer()
#     tfidf_matrix = tfidf_vectorizer.fit_transform(product_features)

#     # Compute cosine similarity between products based on their features
#     cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#     # Calculate the mean similarity score for each product
#     mean_similarity_scores = cosine_sim.dot(interaction_vector) / interaction_vector.sum()

#     # Sort products based on mean similarity scores and get top-N recommended products
#     related_product_indices = mean_similarity_scores.argsort()[-num_recommendations:][::-1]
#     recommended_product_ids = [all_product_ids[idx] for idx in related_product_indices]

#     # Retrieve the recommended products from the database
#     recommended_products = Product.objects.filter(id__in=recommended_product_ids)

#     # Sort recommended products based on cart quantities
#     recommended_products = sorted(recommended_products, key=lambda product: cart_quantities[product_ids_in_cart.index(str(product.id))], reverse=True)

#     return recommended_products
