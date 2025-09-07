from rest_framework import serializers
from .models import Post, Follow, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    # NEW: show number of likes & comments
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "content",
            "media_url",
            "created_at",
            "updated_at",     # NEW: added updated_at from model
            "likes_count",    # NEW
            "comments_count", # NEW
        ]
        read_only_fields = [
            "author",
            "author_username",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
        ]

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


# NEW: Like serializer
class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Like
        fields = ["id", "user", "user_username", "post", "created_at"]
        read_only_fields = ["user", "created_at"]


# NEW: Comment serializer
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
