from django.db import models
from django_resized import ResizedImageField

# Create your models here.

from django.contrib.auth.models import User

class SolarDevice(models.Model):
    STATUS = (("PENDING", "Pending"), ("APPROVED", "Approved"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10) # DEVOT436
    device_type = models.CharField(max_length=20)  # Redicial/Commercial
    capacity_kWp = models.DecimalField(max_digits=8, decimal_places=2)
    cop_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default="PENDING")
    tier = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.owner.username} - {self.code}"

class InverterBrand(models.Model):
    name = models.CharField(max_length=50)
    logo_pic = ResizedImageField(size=[300, 300], upload_to='logo_pics', null=True, blank=True, force_format='webp', quality=100)
    is_immediate_connection = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Inverter(models.Model):
    device = models.ForeignKey(SolarDevice, on_delete=models.CASCADE, related_name="Inverters")
    brand = models.ForeignKey(InverterBrand, on_delete=models.CASCADE, related_name="Inverterbrand")
    serial_no = models.CharField(max_length=100)
    capacity_kwp = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.serial_no