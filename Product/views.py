from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product


def product_list(request):
    products = Product.objects.select_related('category').filter(is_approved=True).order_by('-created_at')
    categories = Product.objects.filter(category__isnull=False).values_list('category__name', flat=True).distinct().order_by('category__name')

    category = request.GET.get('category')
    search = request.GET.get('q', '').strip()

    if category:
        products = products.filter(category__name=category)
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return render(request, 'Product/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_approved=True)
    return render(request, 'Product/product_detail.html', {'product': product})
