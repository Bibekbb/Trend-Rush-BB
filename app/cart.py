class Cart:
    def __init__(self, request):
        # Access the session data from the request directly
        self.session = request.session
        # Get the cart data from the session
        cart = self.session.get('cart')
        if cart is None:
            # If cart data doesn't exist in the session, initialize an empty cart
            cart = self.session['cart'] = {}
        self.cart = cart

    # Rest of the Cart class methods (e.g., add, remove, clear, etc.)
