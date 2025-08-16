# social_media_API/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, FollowViewSet, FeedViewSet
from users.views import RegisterView, MeView, ObtainAuthTokenView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"follow", FollowViewSet, basename="follow")
router.register(r"feed", FeedViewSet, basename="feed")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/token/", ObtainAuthTokenView.as_view(), name="token"),
    path("api/auth/me/", MeView.as_view(), name="me"),
]
