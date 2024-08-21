from django.shortcuts import render
from users.models import Users, UserManagement, UserActivity
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate, TokenAuthentication
from .seriaizer import UserSerializer, LoginSerializer, UserActivitySerializer
# from .models import UserActivity
from django.utils import timezone, dateformat
import pytz
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter




formatted_date = dateformat.format(timezone.localtime(), 'Y-m-d H:i')

# date_ = datetime.now()
# format_change = (date_.strftime("%Y/%m/%d _ %H:%M"))
class SignupUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            password = data['password']
            email = data['email']
            username = data['username']
            user = Users(email=email, username=username)
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
            # email = serializer.validated_data['email']
                user = Users.objects.filter(username=username)
                
            except Users.DoesNotExist:
                
                return Response({'message': 'invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user and user[0].check_password(password):
                user = user[0]
                check_last_activity = UserActivity.objects.filter(user=user).order_by('-login').first()
                
                # print("test",check_last_activity)
                if check_last_activity and check_last_activity.is_active:
                    check_last_activity.is_active = False
                    check_last_activity.save()
                    logout_time = check_last_activity.logout
                    logout_time = logout_time + datetime.timedelta(hours=3, minutes=30)
                    logout_time = dateformat.format(logout_time, 'Y-m-d H:i')
                    return Response({'success': 'Exit Successfully', "time":logout_time})

                else:
                    obj = UserActivity(
                        user = user
                    )
                    obj.save()
                login_time = obj.login
                login_time = login_time + datetime.timedelta(hours=3, minutes=30)
                login_time = dateformat.format(login_time, 'Y-m-d H:i')
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'success': 'Enter Successfully',
                    "time": login_time,
                }, status=status.HTTP_200_OK)

            return Response({'message': 'Invalid Username or Password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivityView(ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    serach_fields = ['user', 'activity_type', 'timestamp']
    ordering_fields = ['timestamp', 'activity_type']
    http_method_names = ['get', 'post', 'put', 'delete']
    
    
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return UserActivity.objects.filter(user=self.request.user)    
    