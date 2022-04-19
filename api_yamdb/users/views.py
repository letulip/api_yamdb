from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import UsersSerializer, UserKeySerializer, UserSelfSerializer
from .pagination import CustomPagination
from .tokens import get_check_hash
from api.permissions import IsAdminOrReadOnly


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

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_account_information(self, request):
        try:
            user = CustomUser.objects.get(username=request.user)
        except CustomUser.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = UsersSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            if request.user.role == 'admin':
                serializer = UsersSerializer(user, data=request.data)
            else:
                serializer = UserSelfSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)


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


# admin


# tulip
# 601-c5126a7b0b34aef7ce17
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDM3MzU1NywiaWF0IjoxNjUwMjg3MTU3LCJqdGkiOiJjNWUyNmIxM2QzZTc0OGQ3ODBmMmQ5NTAxOTliMjlkYSIsInVzZXJfaWQiOjN9.Cs_p5ka57vMda1UOtp18-WOQkAMvSy5RJp-ReXmKaLw",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwMzczNTU3LCJpYXQiOjE2NTAyODcxNTcsImp0aSI6ImM0ZDczMDZlNTNmZDQxODBiNDQyZGQ2OTA1ZDVmYWE1IiwidXNlcl9pZCI6M30.jgC2V6f3_LTmqLAhtjLmuM64bKWrBWuE6YbLkQmcMrw"
# }


# somenewuser
# 601-4248fe442dc514c3cb17
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDM4OTczNywiaWF0IjoxNjUwMzAzMzM3LCJqdGkiOiJmYmIxNDNmMTk0MTc0MWY3YmFmOTY2ZTdiOWIzZTVkYSIsInVzZXJfaWQiOjV9.C4tkYZqcy4fy1gv260PsIxzGG-jps99B34YuccnKP74",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwMzg5NzM3LCJpYXQiOjE2NTAzMDMzMzcsImp0aSI6ImZiZTNhMDgwODk2MDQ3YzViYzYzYTQ1NDA3NWE5ODg4IiwidXNlcl9pZCI6NX0.vX_nr-oidSM2rWkapEgg7f_oHo0t_4t-Z0GZ6919YRY"
# }