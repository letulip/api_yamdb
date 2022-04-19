from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta():
        fields = (
            'email',
            'username',
        )
        model = CustomUser


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

    # def create(self, validated_data):
    #     print('we can create')
    #     new_user = CustomUser.objects.create(**validated_data)
    #     username = validated_data.pop('username')
    #     email = validated_data.pop('email')
    #     code = get_check_hash.make_token(new_user)
    #     # send_mail(
    #     #     from_email='from@example.com',
    #     #     subject=f'Hello, {username} Confirm your email',
    #     #     message=f'Your confirmation code: {code}.',
    #     #     recipient_list=[
    #     #         email,
    #     #     ],
    #     #     fail_silently=False,
    #     # )
    #     message = (
    #         f'Hello, {username} Confirm your email {email}',
    #         f'Your confirmation code: {code}.',
    #     )
    #     print(code)
    #     return get_object_or_404(CustomUser, username=username)
    #     # return new_user
    #     # user = get_object_or_404(CustomUser, username=username)
    #     response = Response(data=new_user, status=HTTP_200_OK)
    #     print(response.__dict__)
    #     return response
    #     return Response(data=new_user, status=HTTP_200_OK)


class UserSelfSerializer(UsersSerializer):
    username = serializers.CharField(
        max_length=150,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="""This value may contain only letters,
                digits and @/./+/-/_ characters."""
            ),
            RegexValidator(
                regex=r'^\b(m|M)e\b',
                inverse_match=True,
                message="""Username Me registration not allowed."""
            )
        ],
    )
    email = serializers.EmailField(
        required=False,
        max_length=255
    )
    role = serializers.CharField(read_only=True)


class UserKeySerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(required=True)
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(UserKeySerializer, self).validate(attrs)
