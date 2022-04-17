from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Действие доступно только администратору!'

    def has_permission(self, request, view):
        return (
            request.user in permissions.SAFE_METHODS
            or request.user.is_staff or request.user.role == 'admin'
        )