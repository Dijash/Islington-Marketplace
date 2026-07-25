from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max
from .models import Product, Category

PRODUCTS_PER_PAGE = 15


def product_list(request):
    products = Product.objects.select_related('category').filter(is_approved=True).order_by('-created_at')
    categories = Category.objects.filter(products__is_approved=True).distinct().order_by('name')

    category = request.GET.get('category')
    search = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    price_stats = products.aggregate(price_min=Min('price'), price_max=Max('price'))
    slider_min = int(price_stats['price_min'] or 0)
    slider_max = int(price_stats['price_max'] or 0)

    if slider_min == slider_max:
        slider_max = slider_min + 1

    if category:
        products = products.filter(category__name=category)
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Product/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
        'min_price': min_price or slider_min,
        'max_price': max_price or slider_max,
        'slider_min': slider_min,
        'slider_max': slider_max,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_approved=True)
    return render(request, 'Product/product_detail.html', {'product': product})
