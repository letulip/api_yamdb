from rest_framework import viewsets, filters

from .models import CustomUser
from .serializers import UsersSerializer
from .pagination import CustomPagination


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (AdminOnly) TODO
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        '^username',
        '$username'
    )
