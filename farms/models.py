from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    farm_name = models.CharField(max_length=100, default="My Farm")
    intended_crop = models.CharField(max_length=100, default="Rice")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    location_name = models.CharField(max_length=255, default="Unknown Village")
    soil_type = models.CharField(max_length=100, default="Loamy")
    nitrogen = models.IntegerField(default=0)
    phosphorus = models.IntegerField(default=0)
    potassium = models.IntegerField(default=0)
    ph_level = models.FloatField(default=7.0)
    soil_moisture = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.farm_name