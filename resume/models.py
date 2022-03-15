from django.db import models

# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    