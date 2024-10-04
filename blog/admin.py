from django.contrib import admin
from .models import BlogPost as Blog

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'view_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('view_count',)