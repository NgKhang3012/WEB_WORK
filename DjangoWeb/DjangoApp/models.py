from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.
class UserInfo(models.Model):
    id=models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    phonenumber = models.CharField(max_length=10,null=True)
    gender = models.CharField(max_length=100,null=True)
    avatar = models.ImageField(null=True, default=None)
    introduction=models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.firstname    

class Post(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    star = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    image = models.ImageField(null=True, default=None)
    idUser = models.ForeignKey("UserInfo", on_delete=models.CASCADE, null= True)

    def __str__(self):
        return self.title

