from django.contrib import admin
from .models import UserActivity, Users, UserManagement

admin.site.register(Users)
admin.site.register(UserActivity)
# admin.site.register(UserManagement)
