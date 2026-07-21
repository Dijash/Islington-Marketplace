from django.contrib import admin
from .models import Seller, Customer


class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shop_name', 'phone', 'created_at')
    search_fields = ('shop_name', 'user__username', 'user__email')
    list_filter = ('created_at',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)


admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer, CustomerAdmin)
