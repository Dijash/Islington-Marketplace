from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/place-order/', views.place_order, name='place_order'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/save-data/', views.save_checkout_data, name='save_checkout_data'),
]
