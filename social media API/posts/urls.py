
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import (
    PostViewSet,
    CommentViewSet,
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
router.register(r"posts", PostViewSet, basename="posts")          # /api/posts/...
router.register(r"comments", CommentViewSet, basename="comments") # /api/comments/...
router.register(r"follow", FollowViewSet, basename="follow")      # /api/follow/...
router.register(r"feed", FeedViewSet, basename="feed")            # /api/feed/ (list-only)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # JWT auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# serve media/static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # If you run collectstatic and have STATIC_ROOT set, uncomment the next line:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
