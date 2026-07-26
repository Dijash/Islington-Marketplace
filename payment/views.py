import json
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from Product.models import Product


def _is_customer(user):
    return user.is_authenticated and not user.is_staff and not hasattr(user, 'seller_profile')


@login_required
def checkout(request):
    if not _is_customer(request.user):
        messages.error(request, 'Only customers can place orders.')
        return redirect('home')

    cart = request.session.get('cart', {})

    items = []
    subtotal = Decimal('0')
    for pid, item in cart.items():
        line_total = Decimal(item['price']) * item['quantity']
        subtotal += line_total
        items.append({
            'product_id': pid,
            'name': item['name'],
            'price': item['price'],
            'image': item.get('image', ''),
            'quantity': item['quantity'],
            'line_total': str(line_total),
        })

    shipping = Decimal('0') if subtotal == 0 else Decimal('150')
    total = subtotal + shipping

    if not items:
        return redirect('product_list')

    contact = {}
    if request.user.is_authenticated:
        user = request.user
        contact['first_name'] = user.first_name
        contact['last_name'] = user.last_name
        contact['email'] = user.email

        profile = getattr(user, 'seller_profile', None) or getattr(user, 'customer_profile', None)
        if profile:
            contact['phone'] = profile.phone

    return render(request, 'payment/checkout.html', {
        'items': items,
        'subtotal': str(subtotal),
        'shipping': str(shipping),
        'total': str(total),
        'item_count': sum(i['quantity'] for i in items),
        'contact': contact,
    })


@require_POST
@login_required
def place_order(request):
    if not _is_customer(request.user):
        return JsonResponse({'status': 'error', 'message': 'Only customers can place orders.'}, status=403)

    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'status': 'error', 'message': 'Cart is empty.'}, status=400)

    payment_method = request.POST.get('payment_method', 'cod')
    if payment_method not in ('cod', 'card'):
        return JsonResponse({'status': 'error', 'message': 'Invalid payment method.'}, status=400)

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    zip_code = request.POST.get('zip', '').strip()

    if not all([first_name, last_name, email, address, city, zip_code]):
        return JsonResponse({'status': 'error', 'message': 'All required fields must be filled.'}, status=400)

    if payment_method == 'card':
        card_name = request.POST.get('card_name', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        card_expiry = request.POST.get('card_expiry', '').strip()
        card_cvv = request.POST.get('card_cvv', '').strip()
        if not all([card_name, card_number, card_expiry, card_cvv]):
            return JsonResponse({'status': 'error', 'message': 'All card details are required.'}, status=400)

    subtotal = Decimal('0')
    for item in cart.values():
        subtotal += Decimal(item['price']) * item['quantity']
    shipping = Decimal('0') if subtotal == 0 else Decimal('150')
    total = subtotal + shipping

    from orders.models import Order, OrderItem
    order = Order.objects.create(
        user=request.user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        zip_code=zip_code,
        payment_method=payment_method,
        subtotal=subtotal,
        shipping=shipping,
        total=total,
    )

    for pid, item in cart.items():
        product = None
        seller = None
        try:
            product = Product.objects.get(id=pid)
            seller = product.seller
        except Product.DoesNotExist:
            pass

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=item['name'],
            product_price=Decimal(item['price']),
            quantity=item['quantity'],
            seller=seller,
        )

    request.session['cart'] = {}
    request.session['checkout_data'] = {}
    request.session.modified = True

    return JsonResponse({'status': 'ok', 'order_id': order.id})


def checkout_success(request):
    return render(request, 'payment/checkout_success.html')


@require_POST
def save_checkout_data(request):
    data = {
        'first_name': request.POST.get('first_name', ''),
        'last_name': request.POST.get('last_name', ''),
        'email': request.POST.get('email', ''),
        'phone': request.POST.get('phone', ''),
        'address': request.POST.get('address', ''),
        'city': request.POST.get('city', ''),
        'zip': request.POST.get('zip', ''),
    }
    request.session['checkout_data'] = data
    request.session.modified = True
    return JsonResponse({'status': 'ok'})
