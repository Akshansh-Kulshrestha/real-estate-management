# content/admin.py

from django.contrib import admin
from .models import BlogPost, Notification, Message


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'is_published')
    search_fields = ('title', 'author__username')
    list_filter = ('is_published', 'published_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'title')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'content')
