from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField
    date = models.DateTimeField(auto_now_add=True)
    star = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    imageURL = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url