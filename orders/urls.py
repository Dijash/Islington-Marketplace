from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('manage/orders/', views.admin_orders, name='admin_orders'),
    path('manage/orders/<int:order_id>/update/', views.admin_order_update, name='admin_order_update'),
]
