from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # works for Post and Comment; both have .author or .user field
        owner_id = getattr(obj, "author_id", None) or getattr(obj, "user_id", None)
        return owner_id == request.user.id
