from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from users import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('',views.UserActivityView)




urlpatterns = [
    
    path('signup/', views.SignupUserView.as_view(), name= 'signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('activity/', include(router.urls)),
    path('activityexcel/', views.UserActivityView.as_view({'get': 'excelreport'}),name="activityexcel"),
    # path('activityresource/', views.ImportUserActivityView.as_view(), name='activityresource'),
    
    path('auth/', obtain_auth_token, name='auth'),

    
]

