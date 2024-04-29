from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    star = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    image = models.ImageField(null=True, default=None)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=10)
    Gender=models.CharField(max_length=100)
    

