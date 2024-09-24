from django.contrib import admin
from .models import Category, Thread, Comments, Replies

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_title', 'created_at', 'updated_at')
    search_fields = ('name', 'sub_title')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('category',)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('content', 'thread', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('thread', 'author')

@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    list_display = ('content', 'comment', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('comment', 'author')