from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    # Added null=True, blank=True so the form doesn't crash
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    farm_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='farm_pics/', null=True, blank=True)
    
    # Added null=True, blank=True here to fix your specific IntegrityError
    intended_crop = models.CharField(max_length=100, null=True, blank=True)
    
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    soil_type = models.CharField(max_length=100, default="Loamy")
    nitrogen = models.IntegerField(default=0)
    phosphorus = models.IntegerField(default=0)
    potassium = models.IntegerField(default=0)
    ph_level = models.FloatField(default=7.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.farm_name