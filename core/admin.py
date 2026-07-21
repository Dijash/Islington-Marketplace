from django.contrib import admin
from .models import Ad, SideAd, BannerAd, CardAd


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active', 'order')


@admin.register(SideAd)
class SideAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active', 'order')


@admin.register(BannerAd)
class BannerAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active', 'order')


@admin.register(CardAd)
class CardAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discount_price', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active', 'order')
