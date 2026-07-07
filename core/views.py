from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Category, Profile

def home(request):
    return render(request, 'core/home.html')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/product_list.html', {
        'products': products,
        'categories': categories,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {
        'product': product,
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'core/category_list.html', {
        'categories': categories,
    })

def deals(request):
    products = Product.objects.filter(status='available')
    return render(request, 'core/deals.html', {
        'products': products,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'core/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        user_type = request.POST.get('user_type', 'customer')
        shop_name = request.POST.get('shop_name', '') if user_type == 'seller' else ''
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
        Profile.objects.create(
            user=user,
            user_type=user_type,
            phone=phone,
            image=image,
            shop_name=shop_name,
        )

        login(request, user)
        return redirect('home')

    return render(request, 'core/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')
