from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Available")
    photo = models.ImageField(upload_to='listing_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class ListingPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)  # Number of additional listings purchased
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} listings"
