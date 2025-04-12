from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)

class Listing(models.Model):
    title = models.CharField(max_length=200, unique=False)
    description = models.CharField(max_length=500, unique=False)
    price = models.IntegerField()
    condition = models.CharField(max_length=100, unique=False)
    status = models.CharField(max_length=50, unique=False)
    photo = models.ImageField(upload_to='images/')