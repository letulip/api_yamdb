from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    IsAdminUser
)

from users.models import USER, ADMIN


class IsOwnerModerAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.id is not None
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role != USER


class IsAdminOrReadOnlyIldar(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN


class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.is_staff or request.user.role == ADMIN
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.role == ADMIN


class IsOwnerModerAdminOrReadOnlyKonstantin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.id is not None
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role != USER
