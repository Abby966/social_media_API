from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    media_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # NEW: track edits
    updated_at = models.DateTimeField(auto_now=True)  # ← added

    class Meta:
        ordering = ["-created_at"]
        # Helpful indexes for common queries (feed & recent lookups)
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["author", "-created_at"]),
        ]

    def __str__(self):
        return f"Post({self.id}) by {self.author.username}"

    # Convenience properties (no DB change)
    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def comments_count(self) -> int:
        return self.comments.count()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="uniq_follow"),
            models.CheckConstraint(check=~models.Q(follower=models.F("following")), name="no_self_follow"),
        ]
        indexes = [
            models.Index(fields=["follower", "following"]),
            models.Index(fields=["following"]),
        ]

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"


# NEW: Like model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="uniq_like"),  # one like per user per post
        ]
        indexes = [
            models.Index(fields=["post", "-created_at"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Like(user={self.user.username}, post={self.post_id})"


# NEW: Comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post", "-created_at"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"Comment({self.id}) by {self.user.username} on Post({self.post_id})"
