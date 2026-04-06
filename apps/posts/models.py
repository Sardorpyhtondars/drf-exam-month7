from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Blog post category (e.g., Technology, Lifestyle, Education, Travel).

    Fields:
    - name: CharField, max_length=100, unique=True
    - slug: SlugField, max_length=120, unique=True
    - description: TextField, blank=True, null=True
    - created_at: DateTimeField, auto_now_add=True
    - updated_at: DateTimeField, auto_now=True

    __str__ returns: self.name
    Meta: ordering = ['name']
    """
    pass


class Tag(models.Model):
    """
    Tag for categorizing posts (e.g., python, django, api).

    Fields:
    - name: CharField, max_length=50, unique=True
    - slug: SlugField, max_length=70, unique=True
    - created_at: DateTimeField, auto_now_add=True

    __str__ returns: self.name
    Meta: ordering = ['name']
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    """
    Represents a blog post.

    Fields:
    - author: ForeignKey → settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='posts'
    - category: ForeignKey → Category, on_delete=SET_NULL, null=True, blank=True, related_name='posts'
    - tags: ManyToManyField → Tag, blank=True, related_name='posts'
    - title: CharField, max_length=255
    - slug: SlugField, max_length=280, unique=True
    - content: TextField (main blog content)
    - excerpt: TextField, max_length=500, blank=True, null=True (short summary)
    - cover_image: ImageField, upload_to='posts/covers/', blank=True, null=True
    - status: CharField with choices (draft / published / archived), default='draft'
    - is_featured: BooleanField, default=False
    - views_count: PositiveIntegerField, default=0
    - published_at: DateTimeField, blank=True, null=True
    - created_at: DateTimeField, auto_now_add=True
    - updated_at: DateTimeField, auto_now=True
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='posts',
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='posts/covers/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']