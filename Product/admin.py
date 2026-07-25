from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'seller', 'is_approved', 'created_at')
    list_filter = ('category', 'created_at', 'is_approved')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    actions = ['approve_products', 'disapprove_products']

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Seller').exists():
            return True
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Seller').exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'seller_profile'):
            return qs.filter(seller=request.user.seller_profile)
        return qs.none()

    @admin.action(description='Approve selected products')
    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Disapprove selected products')
    def disapprove_products(self, request, queryset):
        queryset.update(is_approved=False)
