from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

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


class CurrentUserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'

    def get_queryset(self):
        return CustomUser.objects.filter(username=self.request.user)


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
        print(f'--->>> {request.data}')
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
# 601-c13e492d7f2dc54de868
#  {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDM1OTA2MSwiaWF0IjoxNjUwMjcyNjYxLCJqdGkiOiJhZGYzYWExM2U4NDQ0ZGYyYjk0ZjE3Mzc2ZmNkYjUyYiIsInVzZXJfaWQiOjF9.EVD-4o-ruA9EgX7EZ89A-5Gh6AVCHtuZA1YgJsuD3J8",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwMzU5MDYxLCJpYXQiOjE2NTAyNzI2NjEsImp0aSI6IjQzOTkzZmFiOGE1YTRkMDFhMGYwZTY0ZDc5MzMzMjg2IiwidXNlcl9pZCI6MX0.Nu1__3Ywq8z-1awN4hEAYo_6QJI6Br4Nm-hVN-DAotw"
# }


# tulip
# 601-248f8b311d65f5726604
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDM1OTIzMywiaWF0IjoxNjUwMjcyODMzLCJqdGkiOiI3OGExMjU2MzQyNjY0YmEwYWY1ZWMxMzA1ZTg3ODUzYyIsInVzZXJfaWQiOjJ9.qAh3pmqpk0bgbcq3VlPhvz84lX7brIO1R9IxVoQqrcI",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwMzU5MjMzLCJpYXQiOjE2NTAyNzI4MzMsImp0aSI6IjVlMTJmMTBjZjQ5YTQ5ZWNiOTJiY2VlMDI0NmI0NjI3IiwidXNlcl9pZCI6Mn0.-SYev3JUmoxJOmehOKL7sb9rVmhSWUpReEkrbnDo0X4"
# }