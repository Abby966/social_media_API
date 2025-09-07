# posts/views.py
from django.db.models import Q
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Follow, Like, Comment, Bookmark
from .serializers import (
    PostSerializer,
    FollowSerializer,
    LikeSerializer,
    CommentSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "author", None) or getattr(obj, "user", None)
        return owner == request.user


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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

    # -------- Likes --------
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        POST /api/posts/{id}/like/
        Idempotent: 201 on first like, 200 if already liked.
        """
        post = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response(LikeSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "already liked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        DELETE /api/posts/{id}/unlike/
        """
        post = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "not liked"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def likes(self, request, pk=None):
        """
        GET /api/posts/{id}/likes/
        """
        post = self.get_object()
        qs = Like.objects.filter(post=post).select_related("user")
        return Response(LikeSerializer(qs, many=True).data)

    # -------- Bookmarks --------
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        """
        POST /api/posts/{id}/bookmark/
        """
        post = self.get_object()
        _, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({"detail": "bookmarked"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "already bookmarked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], permission_classes=[permissions.IsAuthenticated])
    def unbookmark(self, request, pk=None):
        """
        DELETE /api/posts/{id}/unbookmark/
        """
        post = self.get_object()
        deleted, _ = Bookmark.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "not bookmarked"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def bookmarks(self, request):
        """
        GET /api/posts/bookmarks/  -> list my bookmarked posts (paginated)
        """
        qs = (
            Post.objects.filter(bookmarks__user=request.user)
            .select_related("author")
            .order_by("-bookmarks__created_at")
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin):

    queryset = Comment.objects.select_related("user", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(content__icontains=q)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    POST /api/follow/           -> follow (body: {"following": <user_id>})
    DELETE /api/follow/<id>/    -> unfollow by relation id
    GET /api/follow/            -> my follow relations
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following_id", flat=True)

        qs = (
            Post.objects.filter(Q(author_id__in=following_ids) | Q(author=self.request.user))
            .select_related("author")
        )

        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(content__icontains=q)
        return qs
