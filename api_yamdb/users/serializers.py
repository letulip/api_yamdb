# from django.core.mail import send_mail
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK
# from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .tokens import get_check_hash
from api_yamdb.settings import USER, MODERATOR, ADMIN, ROLE_CHOICES


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta():
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = CustomUser

    def get_role(self, obj):
        print()
        return obj.role

    def validate_password(self, value: str) -> str:
        """
        Захешировать пустой пароль.
        """
        return make_password(value)

    # def validate_username(self, value: str) -> bool:
    #     return value != 'me'

    def post(self, validated_data):
        new_user = CustomUser.objects.create(**validated_data)
        username = validated_data.pop('username')
        email = validated_data.pop('email')
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
        # return Response(data=new_user, status=HTTP_200_OK)
        # return new_user
        return get_object_or_404(CustomUser, username=username)
        # return JsonResponse()


class UserKeySerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        # del self.fields['password']
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(UserKeySerializer, self).validate(attrs)
