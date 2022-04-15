from rest_framework import serializers

from .models import CustomUser

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
