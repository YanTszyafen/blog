from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    #account
    username=models.CharField(max_length=15,unique=True, blank=False)
    #Avatar
    avatar=models.ImageField(upload_to='avatar/%Y%M%D', blank=True)
    #Introduction
    user_desc=models.CharField(max_length=500, blank=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']


    class Meta:
        db_table='tb_users'
        verbose_name='User_Management' #admin background display
        verbose_name_plural=verbose_name #admin background display

    def __str__(self):
        return self.username
