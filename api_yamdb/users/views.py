# from django.shortcuts import get_object_or_404
# from django.core.mail import send_mail
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

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
    lookup_field = 'username'

    # def perform_create(self, serializer):
    #     username = self.request.user.username
    #     email = self.request.user.email
    #     serializer.save(
    #         username=username,
    #         email=email
    #     )
    #     user = get_object_or_404(CustomUser, username=username)
    #     code = PasswordResetTokenGenerator.make_token(user)
    #     print(code)

