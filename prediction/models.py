import email
from django.db import models

# Create your models here.
class userDetails(models.Model):
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)