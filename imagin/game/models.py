from django.db import models


class Gameuser(models.Model):
    login = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=250)
    image = models.ImageField(upload_to='user_images',null=True,blank=True)
    sids = models.TextField(default='')