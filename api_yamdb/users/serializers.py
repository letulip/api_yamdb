from rest_framework import serializers

from .models import CustomUser

class UsersSerializer(serializers.ModelSerializer):

    class Meta():
        fields = '__all__'
        model = CustomUser
