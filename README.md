# Trend Rush

**Trend Rush** is a fashion recommendation system designed to provide users with personalized fashion item suggestions. Using content-based filtering, this Django-powered application recommends five similar items to users, enhancing their shopping experience by suggesting items that match their preferences and style.

## Features

- **Personalized Fashion Recommendations**: Provides a list of five similar fashion items based on the user’s preferences.
- **Content-Based Filtering**: Uses item attributes to suggest similar fashion products.
- **Shopping Cart**: Integrated with Django Cart for a seamless shopping experience.
- **Intuitive Interface**: Easy-to-navigate interface for browsing recommended items and adding them to the cart.

## Tech Stack

- **Django**: The primary framework for developing the backend.
- **Django Cart**: Manages the shopping cart functionality.
- **NumPy**: Efficient numerical computations, primarily for handling data arrays.
- **Scikit-Learn**: Implements content-based filtering algorithms.
- **NLTK**: Processes and tokenizes text data for better recommendation accuracy.

## Installation

To set up **Trend Rush** on your local machine:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/trend-rush.git
   cd trend-rush
   ```

2. **Install required packages**:

   Ensure you have Python installed, then install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

5. Open your browser and go to `http://127.0.0.1:8000` to start using Trend Rush.

## Usage

1. **Browse Fashion Items**: View fashion items available in the catalog.
2. **Get Recommendations**: Receive recommendations based on item features, including style, color, and type.
3. **Add to Cart**: Add recommended items to your cart using Django Cart for easy checkout.

## How It Works

**Content-Based Filtering**: 
- The recommendation engine uses content-based filtering to suggest items similar to the one the user is currently viewing. This is achieved by analyzing item features and calculating similarity scores with other products using Scikit-Learn.
- **Recommendation Logic**: Based on the selected item, the system identifies five items with the highest similarity scores, which are then presented as recommendations.

## Libraries Used

- **Django**: Backend framework.
- **Django Cart**: Cart functionality.
- **NumPy**: Array manipulation for efficient data handling.
- **Scikit-Learn**: Similarity calculations for recommendation engine.
- **NLTK**: Text preprocessing for handling item descriptions and metadata.

## Future Improvements

- **Collaborative Filtering**: Incorporate user-based recommendations to suggest items that users with similar tastes have liked.
- **Advanced NLP Techniques**: Use advanced NLP models for better understanding of item descriptions.

## Contributing

Feel free to submit pull requests, report issues, or suggest features! Contributions are welcome and appreciated.

---

Enjoy creating a fashion-forward experience with **Trend Rush**!