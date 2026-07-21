from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'seller', 'is_approved', 'created_at')
    list_filter = ('category', 'created_at', 'is_approved')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('is_approved',)
    actions = ['approve_products', 'disapprove_products']

    @admin.action(description='Approve selected products')
    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Disapprove selected products')
    def disapprove_products(self, request, queryset):
        queryset.update(is_approved=False)
