# from django.db.models import Count
# from collections import Counter
# from .models import Product, UserInteraction

# def get_item_recommendations(user_id, num_recommendations=5):
#     # Get user interactions for the given user
#     user_interactions = UserInteraction.objects.filter(user__id=user_id)

#     # Create an interaction matrix (user x product) with counts of interactions
#     interaction_matrix = user_interactions.values('user__id', 'product__id').annotate(interaction_count=Count('id')).values_list('interaction_count', 'user__id', 'product__id')

#     # Convert the interaction matrix to a dictionary
#     interaction_dict = {}
#     for count, user_id, product_id in interaction_matrix:
#         if user_id not in interaction_dict:
#             interaction_dict[user_id] = {}
#         interaction_dict[user_id][product_id] = count

#     # Calculate similarity between users based on their interactions
#     similarity_scores = {}
#     for user_id, items in interaction_dict.items():
#         similarity_scores[user_id] = Counter(items)

#     # Get the most common products among the similar users
#     most_common_products = Counter()
#     for items in similarity_scores.values():
#         most_common_products.update(items)

#     # Get the recommended product IDs
#     recommended_product_ids = [product_id for product_id, _ in most_common_products.most_common(num_recommendations)]

#     # Fetch the recommended products from the database
#     recommended_products = Product.objects.filter(id__in=recommended_product_ids)

#     return recommended_products
