from django.db import models

# Create your models here.

from django.db import models

class Wappen(models.Model):
    name = models.CharField(max_length=100)
    bild = models.ImageField(upload_to='wappen/')
    blasonierung = models.TextField()
    koordinaten = models.CharField(max_length=100, blank=True)
    bbox = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Tinktur(models.Model):
    wappen = models.ForeignKey(Wappen, related_name='tinkturen', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    farbe = models.CharField(max_length=20) 
    textfarbe = models.CharField(max_length=20, default='#FFFFFF')  # Standardmäßig weißer Text

    def __str__(self):
        return self.name
