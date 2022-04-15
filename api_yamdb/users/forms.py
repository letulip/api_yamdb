# from django import forms
# from django.shortcuts import get_object_or_404
# from django.core.mail import send_mail
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta():
        model = CustomUser
        fields = ('username', 'email',)

    # def post(self, serializer):
    #     username = self.request.user.username
    #     email = self.request.user.email
    #     serializer.save(
    #         username=username,
    #         email=email
    #     )
    #     user = get_object_or_404(CustomUser, username=username)
    #     code = PasswordResetTokenGenerator.make_token(user)
    #     return code


class CustomUserChangeForm(UserChangeForm):

    class Meta():
        model = CustomUser
        fields = ('username', 'email',)
