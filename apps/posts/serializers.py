from rest_framework import serializers
from django.utils.text import slugify

from apps.posts.models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes post categories.
    Model: Category
    Fields: id, name, slug, description, created_at
    Read-only: id, slug, created_at
    - slug should be auto-generated from name if not provided
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def create(self, validated_data):
        validated_data['slug']=slugify(validated_data['name'])
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes tags.
    Model: Tag
    Fields: id, name, slug
    Read-only: id, slug
    - slug should be auto-generated from name if not provided
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for post list views.
    Model: Post
    Fields: id, title, slug, excerpt, cover_image, status, is_featured,
            views_count, author (nested: id, username), category (nested: id, name),
            tags (nested: id, name), published_at, created_at
    - author, category, tags should display nested info (not just IDs)
    """
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image', 'status',
            'is_featured', 'views_count', 'author', 'category', 'tags',
            'published_at', 'created_at',
        ]

    def get_author(self, obj):
        return {'id': obj.author.id, 'username': obj.author.username}
    def get_category(self, obj):
        if obj.category is None:
            return None
        return {'id': obj.category.id, 'name': obj.category.name}

    def get_tags(self, obj):
        return [{'id': tag.id, 'name': tag.name} for tag in obj.tags.all()]

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for post detail view.
    Model: Post
    Fields: all fields from PostListSerializer + content + updated_at
    - author, category, tags should display nested info
    """
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image', 'status',
            'is_featured', 'views_count', 'author', 'category', 'tags',
            'published_at', 'created_at', 'content', 'updated_at',  # extra fields
        ]

    def get_author(self, obj):
        return {'id': obj.author.id, 'username': obj.author.username}

    def get_category(self, obj):
        if obj.category is None:
            return None
        return {'id': obj.category.id, 'name': obj.category.name}

    def get_tags(self, obj):
        return [{'id': tag.id, 'name': tag.name} for tag in obj.tags.all()]

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Validates input for post creation and update.
    Model: Post
    Fields: title, content, excerpt, cover_image, category, tags, status, is_featured
    - author is automatically set from request.user (not in input)
    - slug auto-generated from title
    - If status changes to 'published' and published_at is null, set published_at = now
    """
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'cover_image',
            'category', 'tags', 'status', 'is_featured',
        ]
