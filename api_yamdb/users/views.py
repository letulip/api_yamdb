import json
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from rest_framework import viewsets, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .models import CustomUser
from .serializers import UsersSerializer, UserKeySerializer
from .pagination import CustomPagination
from .tokens import get_check_hash
from api.permissions import (
    IsOwnerModerAdminOrReadOnly,
    IsAdminOrReadOnly
)


class CurrentUserDetailView(GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer
    # http_method_names = ['patch', 'get', ]
    # lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data)

    def get_object(self):
        # queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        user = get_object_or_404(CustomUser, username=self.request.user)
        self.check_object_permissions(self.request, user)
        return user

    def patch(self, request):
        upd_user = self.get_object()
        serializer = UsersSerializer(upd_user, data=request.data, partial=True)
        # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                status=HTTP_200_OK,
                data=serializer.data
            )
        return JsonResponse(
            status=HTTP_400_BAD_REQUEST,
            data='wrong parameters'
        )


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