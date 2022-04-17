from rest_framework import permissions


class IsOwnerModerAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Вернуться позже на тему того, как заведён модер 
        return obj.author == request.user or request.user.is_staff
