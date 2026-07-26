import base64
import mimetypes
from pathlib import Path

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from accounts.models import Seller, Customer
from Product.models import Product, Category
from .models import Ad, SideAd, BannerAd, CardAd
from blog.models import Blog


def home(request):
    selected_category = request.GET.get('category', '').strip()

    base_products = Product.objects.select_related('category').filter(is_approved=True)
    categories = Category.objects.all()

    for cat in categories:
        cat.inline_icon = None
        if not cat.icon:
            continue

        image_path = Path(settings.MEDIA_ROOT) / cat.icon.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        cat.inline_icon = f"data:{mime_type};base64,{encoded}"

    if selected_category:
        base_products = base_products.filter(category__name=selected_category)

    products = base_products.order_by('?')[:8]
    newest_products = base_products.order_by('-created_at')[:8]
    budget_products = base_products.order_by('price')[:8]
    ads = list(Ad.objects.filter(is_active=True).exclude(image=''))

    for ad in ads:
        ad.inline_image = None
        if not ad.image:
            continue

        image_path = Path(settings.MEDIA_ROOT) / ad.image.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        ad.inline_image = f"data:{mime_type};base64,{encoded}"

    side_ads = list(SideAd.objects.filter(is_active=True).exclude(image=''))

    for ad in side_ads:
        ad.inline_image = None
        if not ad.image:
            continue

        image_path = Path(settings.MEDIA_ROOT) / ad.image.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        ad.inline_image = f"data:{mime_type};base64,{encoded}"

    banner_ads = list(BannerAd.objects.filter(is_active=True).exclude(image=''))

    for ad in banner_ads:
        ad.inline_image = None
        if not ad.image:
            continue

        image_path = Path(settings.MEDIA_ROOT) / ad.image.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        ad.inline_image = f"data:{mime_type};base64,{encoded}"

    card_ads = list(CardAd.objects.filter(is_active=True).exclude(image='')[:3])

    for ad in card_ads:
        ad.inline_image = None
        if not ad.image:
            continue

        image_path = Path(settings.MEDIA_ROOT) / ad.image.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        ad.inline_image = f"data:{mime_type};base64,{encoded}"

    blogs = list(Blog.objects.filter(is_active=True).exclude(image='')[:3])

    for blog in blogs:
        blog.inline_image = None
        if not blog.image:
            continue

        image_path = Path(settings.MEDIA_ROOT) / blog.image.name
        if not image_path.exists():
            continue

        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = 'image/jpeg'

        try:
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
        except OSError:
            continue

        blog.inline_image = f"data:{mime_type};base64,{encoded}"

    return render(request, 'core/home.html', {
        'products': products,
        'newest_products': newest_products,
        'budget_products': budget_products,
        'ads': ads,
        'side_ads': side_ads,
        'banner_ads': banner_ads,
        'card_ads': card_ads,
        'blogs': blogs,
        'categories': categories,
        'selected_category': selected_category,
    })


def deals(request):
    return render(request, 'core/deals.html')


def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        user_type = request.POST.get('user_type', 'customer')
        shop_name = request.POST.get('shop_name', '')
        phone = request.POST.get('phone', '')
        image = request.FILES.get('image')

        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        username = email.split('@')[0]

        base_username = username
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{suffix}"
            suffix += 1

        errors = []
        if User.objects.filter(email=email).exists():
            errors.append('Email is already registered.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if user_type == 'seller' and not shop_name.strip():
            errors.append('Business name is required for sellers.')

        if errors:
            return render(request, 'core/register.html', {
                'errors': errors,
                'values': request.POST,
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        if user_type == 'seller':
            Seller.objects.create(
                user=user,
                phone=phone,
                image=image,
                shop_name=shop_name,
            )
            seller_group, _ = Group.objects.get_or_create(name='Seller')
            user.groups.add(seller_group)
        else:
            Customer.objects.create(
                user=user,
                phone=phone,
                image=image,
            )
            customer_group, _ = Group.objects.get_or_create(name='Customer')
            user.groups.add(customer_group)

        login(request, user)
        messages.success(request, f'Welcome {first_name}! Your account has been created.')
        return redirect('home')

    return render(request, 'core/register.html')


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['username'].strip()
        password = request.POST['password']

        if '@' in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                username = identifier
        else:
            username = identifier

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'core/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
