from django.contrib import admin
from .models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
