from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group, Permission
# import pandas
# from import_export import resources






class UserManagement(BaseUserManager):
    def create_user(self, username,  email, password=None, is_admin=False, is_staff=False, is_active=True, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # change password to hash
        user.is_superuser = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)
        # if not email:
        #     raise ValueError("User must have an email")
        # if not password:
        #     raise ValueError("User must have a password")
        
        # user = self.model(
        #     email=self.normalize_email(email)
        # )
        # user.set_password(password)
        # user.is_superuser = True
        # user.is_staff = True
        # user.is_active = True
        # user.save(using=self._db)




class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(
    ("username"),
    max_length=150,
    unique=False,
    null=True,
    blank=True
    )
    
    
    
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username or self.email

    objects = UserManagement()


class UserActivity(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    login = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    logout = models.DateTimeField(auto_now=True,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user} - {self.login} - {self.logout}"




    
    
