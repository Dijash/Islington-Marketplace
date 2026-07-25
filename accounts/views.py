from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Product.models import Product
from Product.forms import ProductForm
from .forms import SellerProfileForm, CustomerProfileForm


@login_required
def seller_dashboard(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'You do not have a seller profile.')
        return redirect('home')
    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller).select_related('category')
    approved_count = products.filter(is_approved=True).count()
    pending_count = products.filter(is_approved=False).count()
    return render(request, 'accounts/seller_dashboard.html', {
        'products': products,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'total_count': products.count(),
    })


@login_required
def seller_product_add(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'You do not have a seller profile.')
        return redirect('home')
    seller = request.user.seller_profile
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.is_approved = False
            product.save()
            messages.success(request, 'Product added successfully! Awaiting admin approval.')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'accounts/seller_product_form.html', {
        'form': form,
        'action': 'Add',
    })


@login_required
def seller_product_edit(request, product_id):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'You do not have a seller profile.')
        return redirect('home')
    seller = request.user.seller_profile
    product = get_object_or_404(Product, id=product_id, seller=seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.is_approved = False
            product.save()
            messages.success(request, 'Product updated! Awaiting re-approval.')
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
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'You do not have a seller profile.')
        return redirect('home')
    seller = request.user.seller_profile
    product = get_object_or_404(Product, id=product_id, seller=seller)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('seller_dashboard')
    return render(request, 'accounts/seller_product_delete.html', {
        'product': product,
    })


@login_required
def profile_view(request):
    if hasattr(request.user, 'seller_profile'):
        return seller_profile(request)
    elif hasattr(request.user, 'customer_profile'):
        return customer_profile(request)
    messages.info(request, 'Please complete your profile setup.')
    return redirect('home')


@login_required
def seller_profile(request):
    seller = request.user.seller_profile
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES, instance=seller, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = SellerProfileForm(instance=seller, user=request.user)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': seller,
        'user_type': 'seller',
    })


@login_required
def customer_profile(request):
    customer = request.user.customer_profile
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=customer, user=request.user)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': customer,
        'user_type': 'customer',
    })
