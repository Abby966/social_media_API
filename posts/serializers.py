from rest_framework import serializers
from .models import Post, Follow, Like, Comment, Bookmark  # ⬅️ added Bookmark

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    # NEW 👇
    bookmarks_count = serializers.IntegerField(source="bookmarks.count", read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "content",
            "media_url",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "bookmarks_count",  # NEW
            "is_bookmarked",    # NEW
        ]
        read_only_fields = [
            "author",
            "author_username",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "bookmarks_count",
            "is_bookmarked",
        ]

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.bookmarks.filter(user=request.user).exists()

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content is required.")
        return value


class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source="follower.username")
    following_username = serializers.ReadOnlyField(source="following.username")

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "following",
            "follower_username",
            "following_username",
            "created_at",
        ]
        read_only_fields = ["follower", "created_at"]


class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Like
        fields = ["id", "user", "user_username", "post", "created_at"]
        read_only_fields = ["user", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "user_username",
            "post",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "user_username", "created_at", "updated_at"]

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value
