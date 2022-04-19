from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

from api_yamdb.settings import USER, MODERATOR, ADMIN


class IsOwnerModerAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.id is not None
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role != USER


class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_staff or request.user.role == ADMIN
        return False
        # is_admin = super().has_permission(request, view)
        # return request.method in SAFE_METHODS or is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.role == ADMIN


class IsModerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == MODERATOR
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == MODERATOR
