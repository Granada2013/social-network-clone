from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import PermissionsMixin

from django.db import models


class User(AuthUser, PermissionsMixin):

    def __str__(self):
        return f'@{self.username}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, upload_to='accounts')

    def __str__(self):
        return f'@{self.user.username}'


