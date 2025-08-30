from django.contrib import admin

# Register your models here.
from .models import SolarDevice, InverterBrand, Inverter, DeviceLocation, GenerationData

admin.site.register(SolarDevice)
admin.site.register(InverterBrand)
admin.site.register(Inverter)
admin.site.register(DeviceLocation)
admin.site.register(GenerationData)
