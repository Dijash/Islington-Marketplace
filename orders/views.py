from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from .models import Order


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('my_orders')
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def seller_orders(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, 'You do not have a seller profile.')
        return redirect('home')
    seller = request.user.seller_profile
    orders = Order.objects.filter(items__seller=seller).distinct().prefetch_related('items__product')
    return render(request, 'orders/seller_orders.html', {'orders': orders})


@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().prefetch_related('items__product')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/admin_orders.html', {'orders': orders, 'status_filter': status_filter})


@staff_member_required
def admin_order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} updated to {order.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('admin_orders')
