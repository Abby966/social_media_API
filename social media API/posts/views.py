from django.shortcuts import render
# posts/views.py
from django.db.models import Q
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from .models import Post, Follow
from .serializers import PostSerializer, FollowSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Read: anyone. Write: only the author of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "author", None) == request.user

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts.
    - Auth required to create/update/delete.
    - Only the author can update/delete.
    - Filtering: ?author=<user_id>
    - Search: ?q=keyword (in content)
    """
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        author = self.request.query_params.get("author")
        q = self.request.query_params.get("q")
        if author:
            qs = qs.filter(author_id=author)
        if q:
            qs = qs.filter(Q(content__icontains=q))
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    POST /api/follow/      {"following": <user_id>}
    DELETE /api/follow/<id>/    (unfollow by relation id)
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET /api/feed/ -> posts from users I follow
    Optional: ?q=keyword
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following_id", flat=True)
        qs = Post.objects.filter(author_id__in=following_ids).select_related("author")
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(content__icontains=q)
        return qs


# Create your views here.
