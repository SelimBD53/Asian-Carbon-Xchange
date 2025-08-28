from django.contrib import admin

# Register your models here.
from .models import SolarDevice, InverterBrand,Inverter

admin.site.register(SolarDevice)
admin.site.register(InverterBrand)
admin.site.register(Inverter)
