from django.shortcuts import render
from users.models import Users, UserManagement, UserActivity
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate, TokenAuthentication
from .seriaizer import UserSerializer, LoginSerializer, UserActivitySerializer
# from .models import UserActivity
from django.utils import timezone, dateformat
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
import xlsxwriter
import pandas as pd
from django.http import FileResponse
# import io
from django.http import HttpResponse
from django.utils.timezone import is_aware




# formatted_date = dateformat.format(timezone.localtime(), 'Y-m-d H:i')


class SignupUserView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# date_ = datetime.now()
# format_change = (date_.strftime("%Y/%m/%d _ %H:%M"))
# class SignupUserView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
#             password = data['password']
#             email = data['email']
#             username = data['username']
#             user = Users(email=email, username=username)
#             user.set_password(password)
#             user.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                # email = serializer.validated_data['email']
                user = Users.objects.get(username=username)

            except Users.DoesNotExist:

                return Response({'message': 'invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

            if user.check_password(password):
                check_last_activity = UserActivity.objects.filter(
                    user=user).order_by('-login').first()

                # print("test",check_last_activity)
                if check_last_activity and check_last_activity.is_active:
                    check_last_activity.is_active = False
                    check_last_activity.save()
                    logout_time = check_last_activity.logout
                    logout_time = logout_time + \
                        datetime.timedelta(hours=3, minutes=30)
                    logout_time = dateformat.format(logout_time, 'Y-m-d H:i')
                    return Response({'success': 'Exit Successfully', "time": logout_time})

                else:
                    obj = UserActivity(
                        user=user
                    )
                    obj.save()
                login_time = obj.login
                login_time = login_time + \
                    datetime.timedelta(hours=3, minutes=30)
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
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    serach_fields = ['user', 'activity_type', 'timestamp']
    ordering_fields = ['timestamp', 'activity_type']
    http_method_names = ['get', 'post', 'put', 'delete']
    
   


    # def perform_create(self, serializer):

    #     super().perform_create(serializer)

    #     check_last_activity = UserActivity.objects.all().order_by('-login').first()

    #     if check_last_activity and check_last_activity.is_active:
    #         check_last_activity.is_active = False
    #         check_last_activity.save()
    #         logout_time = check_last_activity.logout
    #         logout_time = logout_time + datetime.timedelta(hours=3, minutes=30)
    #         logout_time = dateformat.format(logout_time, 'Y-m-d H:i')
    #         # return Response({'success': 'Exit Successfully', "time":logout_time})

    def get_queryset(self):
        
        #     # formatted_date = dateformat.format(timezone.localtime(), 'Y-m-d H:i')

        if self.request.user.is_superuser:
            
            #         # check_last_activity =UserActivity.objects.all().order_by('-login').first()
            #         # logout_time = check_last_activity.logout
            #         # logout_time = logout_time + datetime.timedelta(hours=3, minutes=30)
            #         # logout_time = dateformat.format(logout_time, 'Y-m-d H:i')
            #         # return ({'success': 'Exit Successfully', "time":logout_time})
            return super().get_queryset()
        return UserActivity.objects.filter(user=self.request.user)
    
  
    

    #  data = {
    #     queryset.values('user', 'login', 'logout')
    # }
    # # 
    # # df = pd.DataFrame(data)    
    # # df.to_excel('activity.xlsx', index=False)
    
    
    
    
    # def excelreport(request, _):
    #     queryset = UserActivity.objects.all()  
    #     data = {
    #         queryset
    #     }
        
    #     df = pd.DataFrame(data)
    #     df.to_csv('activity.csv', index=False)
        
    
    
    # def excelreport(request,_):

    #     buffer = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(buffer)
    #     worksheet = workbook.add_worksheet()
    #     worksheet.write('A1', '')
    #     workbook.close()
    #     buffer.seek(0)
    #     queryset = UserActivity.objects.all().values_list('user', 'login', 'logout')
        
    #     for query in queryset:
            
    #         return FileResponse(buffer,as_attachment=True, filename='report.xlsx')
    
    
    def excelreport(self, request):
        # دریافت تمامی رکوردهای UserActivity به صورت دیکشنری
        activity_data = UserActivity.objects.all().values()
        
        # تبدیل datetime های دارای timezone به بدون timezone
        for item in activity_data:
            for key, value in item.items():
                if isinstance(value, datetime) and is_aware(value):
                    item[key] = value.replace(tzinfo=None)
        
        # تبدیل داده‌ها به یک DataFrame
        df = pd.DataFrame(activity_data)
        
        # ایجاد یک پاسخ HTTP با نوع محتوای اکسل
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=activity.xlsx'
        
        # نوشتن DataFrame به فایل اکسل
        df.to_excel(response, index=False)
        
        return response
    
    