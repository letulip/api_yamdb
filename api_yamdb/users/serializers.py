# from django.core.mail import send_mail
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .tokens import get_check_hash

class UsersSerializer(serializers.ModelSerializer):

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

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def create(self, validated_data):
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
        return new_user


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