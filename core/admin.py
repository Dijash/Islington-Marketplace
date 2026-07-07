from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('description',)
    list_display = ('id','name', 'description')
    search_fields = ('name',)
    
class ProductAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at')
    list_display = ('id', 'name', 'stock', 'status', 'price', 'category', 'created_at', 'updated_at')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
