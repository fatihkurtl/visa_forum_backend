from django.contrib import admin
from .models import Category, Thread, Comments, Replies

class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 0
    fields = ('content', 'author', 'created_at')
    readonly_fields = ('created_at', 'content', 'author')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_title', 'created_at', 'updated_at')
    search_fields = ('name', 'sub_title')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'comments', 'likes')
    inlines = [CommentsInline]

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('content', 'thread', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('thread', 'author')
    readonly_fields = ('created_at', 'updated_at', 'replies', 'likes')

@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    list_display = ('content', 'comment', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('comment', 'author')
    readonly_fields = ('created_at', 'updated_at')