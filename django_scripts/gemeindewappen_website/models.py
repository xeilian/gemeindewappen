from django.db import models

class Entity(models.Model):
    TYPE_CHOICES = [
        ('landkreis', 'Landkreis'),
        ('ehem_landkreis', 'Ehemalige Gemeinde'),
        ('gemeinde_ohne_stadtstatus', 'Gemeinde'),
        ('kreisstadt', 'Kreisstadt'),
        ('kreisfreie_stadt', 'Kreisfreie Stadt')
    ]

    types = {'landkreis': 'Landkreis',
    'ehem_landkreis': 'Ehemalige Gemeinde',
    'gemeinde_ohne_stadtstatus': 'Gemeinde',
    'kreisstadt': 'Kreisstadt',
    'kreisfreie_stadt': 'Kreisfreie Stadt'
    }

    wikidata_id = models.CharField(max_length=255)
    database_id = models.CharField(max_length=255, primary_key=True, default='default_value')
    name = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True)
    coordinates = models.CharField(max_length=255)
    insignia = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    bundesland = models.CharField(max_length=255)
    landkreis = models.CharField(max_length=255)
    online = models.CharField(max_length=255)

    class Meta:
        db_table = 'entities'

    @property
    def type_in_header(self):
        return self.types.get(self.type, None)

    def __str__(self):
        return self.name

class Normdaten(models.Model):
    wikidata_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    district_key = models.CharField(max_length=255)
    municipality_key = models.CharField(max_length=255)
    regional_key = models.CharField(max_length=255)
    gnd = models.CharField(max_length=255)
    geonames_id = models.CharField(max_length=255)
    openstreetmap_rel_id = models.CharField(max_length=255)
    leobw_link = models.CharField(max_length=255)
    sitelink_de = models.CharField(max_length=255)
    sitelink_en = models.CharField(max_length=255)
    sitelink_fr = models.CharField(max_length=255)

    class Meta:
        db_table = 'normdaten'

    def __str__(self):
        return self.name
    

class Wappen(models.Model):
    wikidata_id = models.CharField(max_length=255)
    coat_of_arms_image = models.CharField(max_length=255)
    blasionierung = models.CharField(max_length=255)

    # Tinkturen
    schwarz = models.CharField(max_length=1)
    weiß = models.CharField(max_length=1)
    gelb = models.CharField(max_length=1)
    rot = models.CharField(max_length=1)
    grün = models.CharField(max_length=1)
    blau = models.CharField(max_length=1)

    class Meta:
        db_table = 'wappen'

    def __str__(self):
        return self.name


class Population(models.Model):
    wikidata_id = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    population_value = models.CharField(max_length=255)

    class Meta:
        db_table = "population"

    def __str__(self):
        return self.name
    

class Area(models.Model):
    wikidata_id = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    area_value = models.CharField(max_length=255)

    class Meta:
        db_table = "area"

    def __str__(self):
        return self.name

