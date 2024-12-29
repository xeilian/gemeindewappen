from django.db import models

# Create your models here.

class Wappen(models.Model):
    name = models.CharField(max_length=100)
    bild = models.ImageField(upload_to='wappen/')
    beschreibung = models.TextField()

    def __str__(self):
        return self.name
