from rest_framework import serializers

from apps.comments.models import Comment, Like


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Validates input for creating a comment.
    Model: Comment
    Fields: post, parent, content
    - author is automatically set from request.user
    - Validate that parent comment belongs to the same post (if provided)
    """
    class Meta:
        model = Comment
        fields = ['post', 'parent', 'content']

    def validate(self, data):
        if data.get('parent') and data['parent'].post != data['post']:
            raise serializers.ValidationError("Parent comment does not belong to this post.")
        return data


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing comments.
    Model: Comment
    Fields: id, post, author (nested: id, username), parent, content,
            is_approved, replies (nested list of same serializer), created_at
    - replies = serializers.SerializerMethodField()
    - get_replies: return child comments (where parent=self)
    """
    author = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'parent', 'content', 'is_approved', 'replies', 'created_at']
    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
        }

    def get_replies(self, obj):
        child_comments = obj.replies.all()
        return CommentListSerializer(child_comments, many=True).data


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a comment (only content can be changed).
    Model: Comment
    Fields: content
    """
    class Meta:
        model = Comment
        fields = ['content']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for liking a post.
    Model: Like
    Fields: id, post, user, created_at
    Read-only: id, user, created_at
    - user is automatically set from request.user
    - Validate that user hasn't already liked the post
    """
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']