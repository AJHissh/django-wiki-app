from django.db import models

# Create your models here.
class Entries(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=500)
    
