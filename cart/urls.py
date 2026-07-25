from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/', views.add_to_cart, name='cart_add'),
    path('cart/remove/', views.remove_from_cart, name='cart_remove'),
    path('cart/update/', views.update_cart_quantity, name='cart_update'),
    path('cart/detail/', views.cart_detail, name='cart_detail'),
]
