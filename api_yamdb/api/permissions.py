from rest_framework.permissions import BasePermission, SAFE_METHODS

from api_yamdb.settings import USER, MODERATOR, ADMIN


class IsOwnerModerAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.id is not None
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role != USER


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.role != ADMIN

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role != ADMIN


class IsModerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.role != MODERATOR

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role != MODERATOR
