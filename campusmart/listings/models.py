from django.db import models

# Create your models here.class 

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)
    
from django.db import models
from django.contrib.auth.models import User  # or your custom User

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Available")
    photo = models.ImageField(upload_to='listing_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
