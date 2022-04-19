# from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        Захешировать пустой пароль.
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
        return get_object_or_404(CustomUser, username=username)


class UserSelfSerializer(UsersSerializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    role = serializers.CharField(read_only=True)


class UserKeySerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(UserKeySerializer, self).validate(attrs)
