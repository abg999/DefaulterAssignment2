from django.db import models
# Create your models here.

class ProcessedImage(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=50)