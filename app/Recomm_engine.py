from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from .models import Product
def get_item_recommendations(cart, products, num_recommendations=5):
    # Extract and prepare data for KNN
    X = [[Product.category.id, Product.subcategory.id, Product.brand.id, Product.price] for product in Product]

    # Normalize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create a NearestNeighbors model
    knn = NearestNeighbors(n_neighbors=num_recommendations)
    knn.fit(X_scaled)

    # Prepare input data (features of the items in the cart)
    input_features = []
    for item in cart:
        product = item.product
        input_features.append([Product.category.id, product.subcategory.id, product.brand.id, product.price])

    input_features_scaled = scaler.transform(input_features)

    # Find K-nearest neighbors
    recommended_indices = knn.kneighbors(input_features_scaled, return_distance=False)

    # Get the recommended products based on indices
    recommended_products = [products[i] for i in recommended_indices]

    return recommended_products
