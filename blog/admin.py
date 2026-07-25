from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'topic', 'created_at')
    search_fields = ('title', 'topic')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at',)

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
