from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (
    UsersSerializer,
    UserKeySerializer,
    UserSelfSerializer,
    UserCreateSerializer
)
from .pagination import CustomPagination
from .tokens import get_check_hash
from api.permissions import IsAdminOrReadOnly


class UsersViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
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
        user = get_object_or_404(CustomUser, username=request.user)

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


class UserAuthView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    http_method_names = ['post', ]

    def post(self, request: HttpRequest):
        if not request.data:
            resp_obj = {
                'email': [
                    'This field is required.'
                ],
                'username': [
                    'This field is required.'
                ]
            }
            return Response(data=resp_obj, status=HTTP_400_BAD_REQUEST)

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data['username']
            email = request.data['email']
            serializer.save()
            new_user = get_object_or_404(CustomUser, username=username)
            code = get_check_hash.make_token(new_user)
            send_mail(
                from_email='from@example.com',
                subject=f'Hello, {username} Confirm your email',
                message=f'Your confirmation code: {code}.',
                recipient_list=[
                    email,
                ],
                fail_silently=False,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(
            data=serializer.data,
            status=HTTP_400_BAD_REQUEST
        )


class UserKeyView(TokenObtainPairView):
    queryset = CustomUser.objects.all()
    serializer_class = UserKeySerializer

    def post(self, request: HttpRequest):
        if not request.data or 'username' not in request.data:
            return Response(status=HTTP_400_BAD_REQUEST)

        username = request.data['username']
        user = get_object_or_404(CustomUser, username=username)
        code = request.data['confirmation_code']
        if (get_check_hash.check_token(user=user, token=code)):
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data=token, status=HTTP_200_OK)
        data = {
            'confirmation_code': 'Unexeptable',
        }
        return Response(data=data, status=HTTP_400_BAD_REQUEST)
