# social_media_API/urls.py  (PROJECT-LEVEL)
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import (
    PostViewSet,
    CommentViewSet,   # ← make sure this import resolves
    FollowViewSet,
    FeedViewSet,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")  # ← THIS LINE
router.register(r"follow", FollowViewSet, basename="follow")
router.register(r"feed",  FeedViewSet,  basename="feed")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
