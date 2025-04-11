from django.db import models

# Create your models here.

class BlogPost (models.Model):
    title =       models.CharField(max_length = 200)
    content =     models.TextField()
    author_name = models.CharField(max_length=100)
    pub_date =    models.DateTimeField('date published')

    def __str__(self):
        return self.title




