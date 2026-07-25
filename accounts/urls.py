from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/product/add/', views.seller_product_add, name='seller_product_add'),
    path('dashboard/product/<int:product_id>/edit/', views.seller_product_edit, name='seller_product_edit'),
    path('dashboard/product/<int:product_id>/delete/', views.seller_product_delete, name='seller_product_delete'),
    path('profile/', views.profile_view, name='profile'),
]
