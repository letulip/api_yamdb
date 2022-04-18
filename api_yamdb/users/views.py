from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from rest_framework import viewsets, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import UsersSerializer, UserKeySerializer
from .pagination import CustomPagination
from .tokens import get_check_hash
from api.permissions import (
    IsOwnerModerAdminOrReadOnly,
    IsAdminOrReadOnly
)


class CurrentUserDetailView(DetailView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer

    def get_object(self):
        print(self.request.user)
        user = get_object_or_404(CustomUser, username=self.request.user)
        print(user)
        return user


class CurrentUserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    lookup_field = 'username'
    # http_method_names = ['patch', 'get', ]

    def get_queryset(self):
        return CustomUser.objects.filter(username=self.request.user)
        return get_object_or_404(CustomUser, username=self.request.user)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOrReadOnly,)
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
    http_method_names = ['post', ]


class UserKeyView(TokenObtainPairView):
    queryset = CustomUser.objects.all()
    serializer_class = UserKeySerializer

    def post(self, request: HttpRequest):
        try:
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
            return JsonResponse(
                {
                    'confirmation_code': 'Unexeptable',
                }
            )
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return Response(status=HTTP_404_NOT_FOUND)
            # return JsonResponse()



# admin


# tulip
# 601-c5126a7b0b34aef7ce17
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDM3MzU1NywiaWF0IjoxNjUwMjg3MTU3LCJqdGkiOiJjNWUyNmIxM2QzZTc0OGQ3ODBmMmQ5NTAxOTliMjlkYSIsInVzZXJfaWQiOjN9.Cs_p5ka57vMda1UOtp18-WOQkAMvSy5RJp-ReXmKaLw",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwMzczNTU3LCJpYXQiOjE2NTAyODcxNTcsImp0aSI6ImM0ZDczMDZlNTNmZDQxODBiNDQyZGQ2OTA1ZDVmYWE1IiwidXNlcl9pZCI6M30.jgC2V6f3_LTmqLAhtjLmuM64bKWrBWuE6YbLkQmcMrw"
# }