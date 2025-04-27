from django.db import models

# Create your models here.class 

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)
    
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    condition = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Available")
    photo = models.ImageField(upload_to='images/')
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='listings')
