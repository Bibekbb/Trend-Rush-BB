# import heapq
# import logging
# from .models import  Product, UserInteraction
# from datetime import datetime
# from collections import Counter


# def get_item_recommendations(cart, num_recommendations=5):
#     product_ids = list(cart.keys())
#     product_ids = list(map(int, product_ids))

#     logging.debug("Product IDs in cart: %s", product_ids)

#     products = Product.objects.filter(id__in=product_ids)
#     sub_categories = products.values_list('subcategory', flat=True)
#     recommended_products = Product.objects.filter(subcategory__in=sub_categories).exclude(
#         id__in=products
#     )[:5]

#     user_interactions = UserInteraction.objects.filter(product__id__in=product_ids).values_list('user_id', 'product_id')

#     user_similarity = {}
#     for user_id, product_id in user_interactions:
#         if user_id not in user_similarity:
#             user_similarity[user_id] = Counter()
#         user_similarity[user_id][product_id] += 1

#     most_similar_users = Counter()
#     for user_id, items in user_similarity.items():
#         most_similar_users.update(items)

#     for product_id in product_ids:
#         most_similar_users[product_id] = 0

#     recommended_product_ids = [product_id for product_id, _ in most_similar_users.most_common(num_recommendations)]
#     logging.debug("Recommended Product IDs: %s", recommended_product_ids)

#     cart_subcategories = set(products.values_list('subcategory', flat=True))
#     recommended_products = Product.objects.filter(
#         subcategory__in=cart_subcategories
#     ).exclude(
#         id__in=products
#     )[:num_recommendations]

#     logging.debug("Recommended Products: %s", recommended_products)

#     print("The Recommended Product is:", recommended_products )
#     return recommended_products


# Recommended Products

# import logging
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from .models import Product
# import nltk


# def get_item_recommendations(cart, num_recommendations=5):
#     product_ids = list(cart.keys())
#     product_ids = list(map(int, product_ids))

#     logging.info("Product IDs in cart: %s", product_ids)

#     products = Product.objects.filter(id__in=product_ids)
#     sub_categories = products.values_list('subcategory', flat=True)
#     recommended_products = Product.objects.filter(subcategory__in=sub_categories).exclude(
#         id__in=products
#     )[:5]

    
#     product_descriptions = [product.descriptions for product in products]

#     logging.info("Product Descriptions (Before Preprocessing): %s",
#                  product_descriptions)

#     tfidf_vectorizer = TfidfVectorizer(stop_words=None)
#     tfidf_matrix = tfidf_vectorizer.fit_transform(product_descriptions)

#     logging.info("Product Descriptions (After Preprocessing): %s",
#                  tfidf_vectorizer.get_feature_names_out())

#     cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

#     logging.info("Cosine Similarities: %s", cosine_similarities)
#     product_indices = list(range(len(products)))

#     recommendations = []
#     for product_id in product_ids:
#         product_index = product_ids.index(product_id)
#         similarity_scores = cosine_similarities[product_index]

#         logging.info("Similarity Scores: %s", similarity_scores)

#         similar_indices = sorted(
#             product_indices, key=lambda x: similarity_scores[x], reverse=True)
#         similar_indices = [
#             idx for idx in similar_indices if idx != product_index]
#         top_similar_indices = similar_indices[:num_recommendations]

#         print("similar Item:", similar_indices)
#         logging.info("Top Similar Indices: %s", top_similar_indices)

#         recommended_product_ids = [product_ids[idx]
#                                    for idx in top_similar_indices]
        

#         print("The Recommended product is:",recommended_product_ids)

#         logging.info("Recommended Product IDs: %s", recommended_product_ids)

#         recommended_products = Product.objects.filter(
#             id__in=recommended_product_ids)
#         recommendations.extend(recommended_products)

#         print("the bibej uss :", recommended_products)
    
#     recommendations = list(set(recommendations))

#     logging.info("Final Recommendations: %s", recommendations)

#     return recommended_products[:num_recommendations]






# import logging
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from .models import Product, UserInteraction
# from collections import Counter
# import nltk
# from nltk.corpus import stopwords
# nltk.download('stopwords')

# def get_item_recommendations(cart, num_recommendations=5):
#     product_ids = list(cart.keys())
#     product_ids = list(map(int, product_ids))

#     logging.debug("Product IDs in cart: %s", product_ids)

#     products = Product.objects.filter(id__in=product_ids)
#     sub_categories = products.values_list('subcategory', flat=True)

#     # Recommendation based on user interactions
#     user_interactions = UserInteraction.objects.filter(product__id__in=product_ids).values_list('user_id', 'product_id')
#     user_similarity = {}
    
#     for user_id, product_id in user_interactions:
#         if user_id not in user_similarity:
#             user_similarity[user_id] = Counter()
#         user_similarity[user_id][product_id] += 1

#     most_similar_users = Counter()
#     for user_id, items in user_similarity.items():
#         most_similar_users.update(items)

#     for product_id in product_ids:
#         most_similar_users[product_id] = 0

#     recommended_product_ids = [product_id for product_id, _ in most_similar_users.most_common(num_recommendations)]
#     logging.debug("Recommended Product IDs (User Interaction): %s", recommended_product_ids)

#     # Recommendation based on product descriptions
#     product_descriptions = [product.descriptions for product in products]

#     logging.debug("Product Descriptions (Before Preprocessing): %s", product_descriptions)

#     tfidf_vectorizer = TfidfVectorizer(stop_words=None)
#     tfidf_matrix = tfidf_vectorizer.fit_transform(product_descriptions)

#     logging.debug("Product Descriptions (After Preprocessing): %s", tfidf_vectorizer.get_feature_names_out())

#     cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
#     product_indices = list(range(len(products)))

#     descriptions_recommendations = []
#     for product_id in product_ids:
#         product_index = product_ids.index(product_id)
#         similarity_scores = cosine_similarities[product_index]

#         logging.debug("Similarity Scores (Product Descriptions): %s", similarity_scores)

#         similar_indices = sorted(
#             product_indices, key=lambda x: similarity_scores[x], reverse=True)
#         similar_indices = [
#             idx for idx in similar_indices if idx != product_index]
#         top_similar_indices = similar_indices[:num_recommendations]

#         logging.debug("Top Similar Indices (Product Descriptions): %s", top_similar_indices)

#         recommended_product_ids = [product_ids[idx]
#                                    for idx in top_similar_indices]

#         logging.debug("Recommended Product IDs (Product Descriptions): %s", recommended_product_ids)

#         recommended_products = Product.objects.filter(
#             id__in=recommended_product_ids)
#         descriptions_recommendations.extend(recommended_products)

#     descriptions_recommendations = list(set(descriptions_recommendations))
#     logging.debug("Final Recommendations (Product Descriptions): %s", descriptions_recommendations)

#     # Combine recommendations from both approaches
#     combined_recommendations = list(set(recommended_product_ids) | set([product.id for product in descriptions_recommendations]))

#     # Fetch the recommended products based on indices
#     recommended_products = Product.objects.filter(id__in=combined_recommendations)

#     logging.debug("Combined Recommendations: %s", recommended_products)

#     return recommended_products[:num_recommendations]






# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from .models import Product

# def get_item_recommendations(cart, num_recommendations=5):
#     product_ids = list(map(int, cart.keys()))
    
#     # Fetch products based on cart items
#     cart_products = Product.objects.filter(id__in=product_ids)
    
#     # Extract descriptions of products in the cart
#     cart_descriptions = [product.descriptions for product in cart_products]

#     # Initialize TF-IDF vectorizer
#     tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    
#     # Fit and transform product descriptions
#     tfidf_matrix = tfidf_vectorizer.fit_transform(cart_descriptions)
    

#     print("the cart desc::", tfidf_matrix)
#     # Compute cosine similarities for all products
#     cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
#     print("The similar:::", cosine_similarities)

#     # Create an empty list to store recommended product IDs
#     recommended_product_ids = []
#     print("The id is", recommended_product_ids)
#     for product_id in product_ids:
#         product_index = product_ids.index(product_id)
#         similarity_scores = cosine_similarities[product_index]

#         # Sort product indices by similarity scores in descending order
#         similar_indices = np.argsort(similarity_scores)[::-1]

#         # Exclude products already in the cart
#         top_recommendations = [idx for idx in similar_indices if product_ids[idx] not in product_ids][:num_recommendations]
        
#         recommended_product_ids.extend([product_ids[idx] for idx in top_recommendations])
#         print("the top recomm", top_recommendations)
#         print("the prod:",similarity_scores)
#     # Fetch the recommended products based on indices
#     recommended_products = Product.objects.filter(id__in=recommended_product_ids)
#     print("the last is", recommended_products)
#     return recommended_products


# # Import necessary libraries and models
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from .models import Product, UserInteraction

# def get_item_recommendations(cart, num_recommendations=5):
#     # Extract product IDs from the cart
#     product_ids = list(map(int, cart.keys()))

#     # Fetch products based on cart items
#     cart_products = Product.objects.filter(id__in=product_ids)

#     # Extract descriptions of products in the cart
#     cart_descriptions = [product.descriptions for product in cart_products]

#     # Initialize TF-IDF vectorizer
#     tfidf_vectorizer = TfidfVectorizer(stop_words='english')

#     # Fit and transform product descriptions
#     tfidf_matrix = tfidf_vectorizer.fit_transform(cart_descriptions)

#     # Compute cosine similarities for all products
#     cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

#     # Create a dictionary mapping product_id to index
#     product_index_mapping = {product_id: index for index, product_id in enumerate(product_ids)}

#     # Create a set to store recommended product IDs
#     recommended_product_ids = set()

#     for product_id in product_ids:
#         product_index = product_index_mapping[product_id]
#         similarity_scores = cosine_similarities[product_index]

#         # Sort product indices by similarity scores in descending order
#         similar_indices = np.argsort(similarity_scores)[::-1]

#         # Exclude products already in the cart
#         cart_product_ids = set(product_ids)
#         top_recommendations = [idx for idx in similar_indices if product_index_mapping[product_ids[idx]] not in cart_product_ids]

#         recommended_product_ids.update(product_ids[idx] for idx in top_recommendations)

#         # Break the loop when you have 5 different recommendations
#         if len(recommended_product_ids) >= num_recommendations:
#             break

#     # Fetch the recommended products based on indices
#     recommended_products_tfidf = Product.objects.filter(id__in=list(recommended_product_ids))

#     # Now, let's add the recommendations based on subcategories
#     products = Product.objects.filter(id__in=product_ids)
#     sub_categories = products.values_list('subcategory', flat=True)
#     recommended_products_nn = Product.objects.filter(subcategory__in=sub_categories).exclude(
#         id__in=products
#     )[:num_recommendations]

#     # Combine the two sets of recommendations and ensure that you get 5 different products
#     combined_recommendations = list(recommended_products_tfidf) + list(recommended_products_nn)

#     print("The Recommendation items: ",combined_recommendations)
#     return combined_recommendations[:num_recommendations]




