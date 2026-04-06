from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only the author of an object can edit/delete it.
    Everyone can read (GET, HEAD, OPTIONS).

    - has_object_permission checks if request.method is safe OR obj.author == request.user
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user