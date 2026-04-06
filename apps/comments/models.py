from django.conf import settings
from django.db import models

from apps.posts.models import Post


class Comment(models.Model):
    """
    Represents a comment on a blog post.

    Fields:
    - post: ForeignKey → Post, on_delete=CASCADE, related_name='comments'
    - author: ForeignKey → settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='comments'
    - parent: ForeignKey → 'self', on_delete=CASCADE, null=True, blank=True,
              related_name='replies' (for nested/threaded comments)
    - content: TextField
    - is_approved: BooleanField, default=True
    - created_at: DateTimeField, auto_now_add=True
    - updated_at: DateTimeField, auto_now=True

    __str__ returns: f"Comment by {self.author.username} on {self.post.title}"
    Meta: ordering = ['-created_at']
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
    )

    content = models.TextField(default='')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['-created_at']

class Like(models.Model):
    """
    Represents a like/reaction on a post.

    Fields:
    - post: ForeignKey → Post, on_delete=CASCADE, related_name='likes'
    - user: ForeignKey → settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='likes'
    - created_at: DateTimeField, auto_now_add=True

    __str__ returns: f"{self.user.username} liked {self.post.title}"
    Meta:
        unique_together = ['post', 'user']   # One like per user per post
        ordering = ['-created_at']
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-created_at']