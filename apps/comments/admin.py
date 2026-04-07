from django.contrib import admin

from apps.comments.models import Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment.
    list_display: id, author, post, parent, is_approved, created_at
    list_filter: is_approved, created_at
    search_fields: content, author__username, post__title
    """
    list_display = ['id', 'author', 'post', 'parent', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Like.
    list_display: id, user, post, created_at
    search_fields: user__username, post__title
    """
    list_display = ['id', 'user', 'post', 'created_at']
    search_fields = ['user__username', 'post__title']