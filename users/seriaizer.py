from rest_framework import serializers
from .models import Users, UserActivity
# from django.utils import timezone, dateformat
# import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # email = serializers.EmailField()


class UserActivitySerializer(serializers.ModelSerializer):

    user = serializers.CharField(read_only=True)
    login = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S")
    logout = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserActivity
        fields = ['user', 'login', 'logout']


# class MySerializer(serializers.ModelSerializer):
#     start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

#     class Meta:
#         model = UserActivity
#         fields = ['start_time']
