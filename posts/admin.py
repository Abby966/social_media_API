from django.contrib import admin
from .models import Post, Follow, Like, Comment, Bookmark

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id","user","post","created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username","post__id")


# Register your models here.
