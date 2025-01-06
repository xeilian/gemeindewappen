from django.db import models

# Create your models here.

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

class Landkreis(models.Model):
    TYPE_CHOICES = [
        ('landkreis', 'Landkreis'),
        ('other_type', 'Other Type'),
    ]

    wikidata_id = models.CharField(max_length=255, primary_key=True, default='default_value')
    name = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True)


    class Meta:
        db_table = 'landkreise'

    def __str__(self):
        return self.name
    

class Entity(models.Model):
    TYPE_CHOICES = [
        ('landkreis', 'Landkreis'),
        ('ehem_landkreis', 'Ehemalige Gemeinde'),
        ('gemeinde_ohne_stadtstatus', 'Gemeinde'),
        ('kreisstadt', 'Kreisstadt'),
        ('kreisfreie_stadt', 'Kreisfreie Stadt')
    ]

    wikidata_id = models.CharField(max_length=255, primary_key=True, default='default_value')
    name = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True)
    coordinates = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    bundesland = models.CharField(max_length=255)
    landkreis = models.CharField(max_length=255)

    class Meta:
        db_table = 'entities'

    def __str__(self):
        return self.name

class Normdaten(models.Model):
    wikidata_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    district_key = models.CharField(max_length=255)
    gnd = models.CharField(max_length=255)
    geonames_id = models.CharField(max_length=255)
    openstreetmap_rel_id = models.CharField(max_length=255)
    sitelink_de = models.CharField(max_length=255)
    sitelink_en = models.CharField(max_length=255)
    sitelink_fr = models.CharField(max_length=255)

    class Meta:
        db_table = 'normdaten'

    def __str__(self):
        return self.name