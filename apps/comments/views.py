from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.permissions import IsAuthorOrReadOnly
from apps.comments.models import Comment, Like
from apps.comments.serializers import CommentCreateSerializer,CommentListSerializer,CommentUpdateSerializer,LikeSerializer
from apps.posts.models import Post


class CommentListCreateAPIView(ListCreateAPIView):
    """
    GET /api/v1/comments/?post=<id> — List comments for a post (top-level only, with nested replies).
    POST /api/v1/comments/ — Create a new comment.

    - serializer: CommentListSerializer for GET, CommentCreateSerializer for POST
    - permission_classes: AllowAny for GET, IsAuthenticated for POST
    - perform_create: set author = request.user
    - get_queryset: filter by post query param, only top-level (parent=None), only approved
    - filterset_fields: ['post']
    """
    filterset_fields = ['post']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentListSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.filter(status='published')
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# get queryset???

class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET /api/v1/comments/<pk>/ — Retrieve a comment.
    PUT/PATCH /api/v1/comments/<pk>/ — Update a comment (author only).
    DELETE /api/v1/comments/<pk>/ — Delete a comment (author only).

    - serializer: CommentUpdateSerializer for PUT/PATCH, CommentListSerializer for GET
    - permission_classes: IsAuthenticated, IsAuthorOrReadOnly
    """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentUpdateSerializer
        return CommentListSerializer


class LikeToggleAPIView(GenericAPIView):
    """
    POST /api/v1/comments/like/ — Toggle like on a post.
    - If user already liked the post → unlike (delete the Like), return {"status": "unliked"}
    - If user hasn't liked the post → like (create the Like), return {"status": "liked"}

    - serializer_class: LikeSerializer
    - permission_classes: [IsAuthenticated]
    - Accepts: {"post": <post_id>}
    """
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post')
        existing_like = Like.objects.filter(post=post_id, user=request.user).first()

        if existing_like:
            existing_like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)


class PostLikesListAPIView(ListAPIView):
    """
    GET /api/v1/comments/likes/?post=<id> — List all likes for a post.

    - serializer_class: LikeSerializer
    - permission_classes: [AllowAny]
    - filterset_fields: ['post']
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['post']