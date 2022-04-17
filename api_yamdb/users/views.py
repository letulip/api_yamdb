from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UsersSerializer, UserKeySerializer
from .pagination import CustomPagination
from .tokens import get_check_hash
from api.permissions import IsOwnerModerAdminOrReadOnly


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (AdminOnly) TODO
    permission_classes = (IsOwnerModerAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    search_fields = (
        '^username',
        '$username'
    )
    lookup_field = 'username'


class UserAuthViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = (AdminOnly) TODO
    permission_classes = (IsOwnerModerAdminOrReadOnly,)


class UserKeyView(TokenObtainPairView):
    queryset = CustomUser.objects.all()
    serializer_class = UserKeySerializer

    def post(self, request: HttpRequest):
        username = request.data['username']
        user = get_object_or_404(CustomUser, username=username)
        code = request.data['confirmation_code']
        if (get_check_hash.check_token(user=user, token=code)):
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            )
        else:
            return JsonResponse(
                {
                    'confirmation_code': 'Unexeptable',
                }
            )
