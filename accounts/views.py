from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Product.models import Product
from Product.forms import ProductForm


@login_required
def seller_dashboard(request):
    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller).select_related('category')
    return render(request, 'accounts/seller_dashboard.html', {
        'products': products,
    })


@login_required
def seller_product_add(request):
    seller = request.user.seller_profile
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.is_approved = False
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'accounts/seller_product_form.html', {
        'form': form,
        'action': 'Add',
    })


@login_required
def seller_product_edit(request, product_id):
    seller = request.user.seller_profile
    product = get_object_or_404(Product, id=product_id, seller=seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.is_approved = False
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'accounts/seller_product_form.html', {
        'form': form,
        'product': product,
        'action': 'Edit',
    })


@login_required
def seller_product_delete(request, product_id):
    seller = request.user.seller_profile
    product = get_object_or_404(Product, id=product_id, seller=seller)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')
    return render(request, 'accounts/seller_product_delete.html', {
        'product': product,
    })
