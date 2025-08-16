from django.contrib import admin

from .models import Profile, Tag, Post, Comment, Like, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("body", "author__username")
    date_hierarchy = "created_at"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at")
    search_fields = ("content", "author__username")
    list_filter = ("created_at",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    search_fields = ("follower__username", "following__username")


