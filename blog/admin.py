from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'topic', 'created_at')
    search_fields = ('title', 'topic')
    list_editable = ('is_active', 'order')
