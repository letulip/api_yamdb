from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import viewsets, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import UsersSerializer, UserKeySerializer, UserSelfSerializer, UserCreateSerializer
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

    def perform_create(self, serializer):
        print('we can create here ad well')
        # new_user = CustomUser.objects.create(**validated_data)
        username = self.request.data['username']
        email = self.request.data['email']
        print(self.request.user)
        # serializer.save(user=self.request.user)
        new_user = CustomUser.objects.create(username=username, email=email)
        print(new_user)
        code = get_check_hash.make_token(new_user)
        # send_mail(
        #     from_email='from@example.com',
        #     subject=f'Hello, {username} Confirm your email',
        #     message=f'Your confirmation code: {code}.',
        #     recipient_list=[
        #         email,
        #     ],
        #     fail_silently=False,
        # )
        message = (
            f'Hello, {username} Confirm your email {email}',
            f'Your confirmation code: {code}.',
        )
        print(code)
        return get_object_or_404(CustomUser, username=username)
        # return new_user
        # user = get_object_or_404(CustomUser, username=username)
        response = Response(data=new_user, status=HTTP_200_OK)
        print(response.__dict__)
        return response
        return Response(data=new_user, status=HTTP_200_OK)


class UserAuthView(APIView):
    queryset = CustomUser.objects.all()
    # serializer_class = UsersSerializer
    serializer_class = UserCreateSerializer
    http_method_names = ['post', ]

    def post(self, validated_data):
        try:
            username = self.request.data['username']
            email = self.request.data['email']

            serializer = UserCreateSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                # new_user = CustomUser.objects.create(user)
                new_user = get_object_or_404(CustomUser, username=username)
                code = get_check_hash.make_token(new_user)
                # send_mail(
                #     from_email='from@example.com',
                #     subject=f'Hello, {username} Confirm your email',
                #     message=f'Your confirmation code: {code}.',
                #     recipient_list=[
                #         email,
                #     ],
                #     fail_silently=False,
                # )
                print(code)
                return Response(data=serializer.data, status=HTTP_200_OK)
            return Response(data=serializer.data, status=HTTP_400_BAD_REQUEST)
        except BaseException as err:
            return Response(data=err.args[0], status=HTTP_400_BAD_REQUEST)


class UserKeyView(TokenObtainPairView):
    queryset = CustomUser.objects.all()
    serializer_class = UserKeySerializer

    def post(self, request: HttpRequest):
        print(request.data)
        if not request.data or 'username' not in request.data:
            print("we have no data")
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            username = request.data['username']
            print(username)
            user = get_object_or_404(CustomUser, username=username)
            code = request.data['confirmation_code']
            if (get_check_hash.check_token(user=user, token=code)):
                refresh = RefreshToken.for_user(user)
                return Response(data=refresh, status=HTTP_200_OK)
            data = {
                'confirmation_code': 'Unexeptable',
            }
            return Response(data=data, status=HTTP_400_BAD_REQUEST)
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            error = {
                'error': f'{err}'
            }
            return Response(data=error, status=HTTP_404_NOT_FOUND)


# admin


# tulip
# 601-c5126a7b0b34aef7ce17
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDQ0ODY4MCwiaWF0IjoxNjUwMzYyMjgwLCJqdGkiOiI5YjBhYjRjOGVjNTg0MGJlYTBjYjU1MDdlMTE3Y2VhYyIsInVzZXJfaWQiOjN9.o5SyNTvbPQKPJaI2bflNljV-pY9fW87xaiS_0I_Aqdw",
    # "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwNDQ4NjgwLCJpYXQiOjE2NTAzNjIyODAsImp0aSI6IjJlZjBlNTljZjI4MTQ0ZWE4NGVmNWE0YTczNzQ3NTk5IiwidXNlcl9pZCI6M30.RwRH8fvbi61FDaYcZJjexF-7skZXvgQgYNZh9eH8vJA"
# }


# somenewuser
# 601-4248fe442dc514c3cb17
# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDM4OTczNywiaWF0IjoxNjUwMzAzMzM3LCJqdGkiOiJmYmIxNDNmMTk0MTc0MWY3YmFmOTY2ZTdiOWIzZTVkYSIsInVzZXJfaWQiOjV9.C4tkYZqcy4fy1gv260PsIxzGG-jps99B34YuccnKP74",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwMzg5NzM3LCJpYXQiOjE2NTAzMDMzMzcsImp0aSI6ImZiZTNhMDgwODk2MDQ3YzViYzYzYTQ1NDA3NWE5ODg4IiwidXNlcl9pZCI6NX0.vX_nr-oidSM2rWkapEgg7f_oHo0t_4t-Z0GZ6919YRY"
# }