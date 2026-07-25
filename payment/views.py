import json
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from Product.models import Product


def checkout(request):
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
    payment = {}

    if request.user.is_authenticated:
        user = request.user
        contact['first_name'] = user.first_name
        contact['last_name'] = user.last_name
        contact['email'] = user.email

        profile = getattr(user, 'seller_profile', None) or getattr(user, 'customer_profile', None)
        if profile:
            contact['phone'] = profile.phone

    payment_cookie = request.COOKIES.get('checkout_payment')
    if payment_cookie:
        try:
            payment = json.loads(payment_cookie)
        except (json.JSONDecodeError, TypeError):
            payment = {}

    return render(request, 'payment/checkout.html', {
        'items': items,
        'subtotal': str(subtotal),
        'shipping': str(shipping),
        'total': str(total),
        'item_count': sum(i['quantity'] for i in items),
        'contact': contact,
        'payment': payment,
    })


def checkout_success(request):
    from orders.models import Order, OrderItem

    cart = request.session.get('cart', {})
    checkout_data = request.session.get('checkout_data', {})

    if cart and request.user.is_authenticated:
        subtotal = Decimal('0')
        for item in cart.values():
            subtotal += Decimal(item['price']) * item['quantity']
        shipping = Decimal('0') if subtotal == 0 else Decimal('150')
        total = subtotal + shipping

        order = Order.objects.create(
            user=request.user,
            first_name=checkout_data.get('first_name', request.user.first_name),
            last_name=checkout_data.get('last_name', request.user.last_name),
            email=checkout_data.get('email', request.user.email),
            phone=checkout_data.get('phone', ''),
            address=checkout_data.get('address', ''),
            city=checkout_data.get('city', ''),
            zip_code=checkout_data.get('zip', ''),
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
