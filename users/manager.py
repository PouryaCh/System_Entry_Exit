# from django.contrib.auth.models import BaseUserManager


# class UserManagement(BaseUserManager):
#     def create_user(self, email, password=None,is_admin=False,is_staff=False, is_active=True):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")

#         user = self.model(
#             email=self.normalize_email(email)
#         )
        
#         user.set_password(password)  # change password to hash
#         user.is_superuser = is_admin
#         user.is_staff = is_staff
#         user.is_active = is_active
#         user.save(using=self._db)
#         return user
        