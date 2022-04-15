from rest_framework import viewsets, filters

from .models import CustomUser
from .serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (AdminOnly) TODO
    filter_backends = (filters.SearchFilter,)
    paginations_class = None
    search_fields = (
        '^username',
        '$username'
    )
