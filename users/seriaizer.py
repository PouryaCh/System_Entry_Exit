from rest_framework import serializers
from .models import Users, UserActivity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [ 'username', 'password', 'email']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # email = serializers.EmailField()
    
    
class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['user', 'login', 'logout']
        

        