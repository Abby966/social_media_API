# posts/serializers.py
from rest_framework import serializers
from .models import Post, Follow

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "author", "author_username", "content", "media_url", "created_at"]
        read_only_fields = ["author", "author_username", "created_at"]

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content is required.")
        return value

class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source="follower.username")
    following_username = serializers.ReadOnlyField(source="following.username")

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "follower_username", "following_username", "created_at"]
        read_only_fields = ["follower", "created_at"]
