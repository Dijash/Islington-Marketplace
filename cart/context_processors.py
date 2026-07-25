def cart_context(request):
    cart = request.session.get('cart', {})
    return {'cart_product_ids': set(cart.keys())}
