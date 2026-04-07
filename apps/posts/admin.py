from django.contrib import admin

from apps.posts.models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category.
    list_display: name, slug, created_at
    search_fields: name
    prepopulated_fields: {'slug': ('name',)}
    """
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag.
    list_display: name, slug, created_at
    search_fields: name
    prepopulated_fields: {'slug': ('name',)}
    """
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post.
    list_display: title, author, category, status, is_featured, views_count, published_at, created_at
    list_filter: status, is_featured, category, created_at
    search_fields: title, content, author__username
    prepopulated_fields: {'slug': ('title',)}
    """
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views_count', 'published_at', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}