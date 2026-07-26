from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from Product.models import Product


def _get_cart(session):
    return session.get('cart', {})


def _save_cart(session, cart):
    session['cart'] = cart
    session.modified = True


def _cart_summary(cart):
    total = Decimal('0')
    count = 0
    for item in cart.values():
        total += Decimal(item['price']) * item['quantity']
        count += item['quantity']
    return {'count': count, 'total': str(total)}


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id, is_approved=True)

    user = request.user
    if user.is_authenticated and (user.is_staff or hasattr(user, 'seller_profile')):
        return JsonResponse({'status': 'error', 'message': 'Sellers and admins cannot add items to cart.'}, status=403)

    cart = _get_cart(request.session)
    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        image_url = product.image.url if product.image else ''
        cart[pid] = {
            'name': product.name,
            'price': str(product.price),
            'image': image_url,
            'quantity': 1,
        }

    _save_cart(request.session, cart)
    summary = _cart_summary(cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', **summary})

    return JsonResponse({'status': 'ok', **summary})


@require_POST
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    cart = _get_cart(request.session)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        _save_cart(request.session, cart)

    summary = _cart_summary(cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', **summary})

    return JsonResponse({'status': 'ok', **summary})


@require_POST
def update_cart_quantity(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    cart = _get_cart(request.session)
    pid = str(product_id)

    if pid not in cart:
        return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=400)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)

    if quantity < 1:
        del cart[pid]
    else:
        cart[pid]['quantity'] = quantity

    _save_cart(request.session, cart)
    summary = _cart_summary(cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', **summary})

    return JsonResponse({'status': 'ok', **summary})


def cart_detail(request):
    cart = _get_cart(request.session)
    items = []
    for pid, item in cart.items():
        items.append({
            'product_id': pid,
            'name': item['name'],
            'price': item['price'],
            'image': item['image'],
            'quantity': item['quantity'],
        })
    summary = _cart_summary(cart)
    return JsonResponse({'items': items, **summary})
