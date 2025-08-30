from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register('Device-create', views.SolarDeviceView, basename='device_create')
router.register('Inverter-Brand', views.InverterBrandView, basename='inverterBrand_create')
router.register('Inverter-create', views.InverterView, basename='inverter_create')
router.register('DeviceLocation-create', views.DeviceLocationView, basename='DeviceLocation_create')
router.register('Generation-Create', views.GenerationDataView, basename="Generation_data")
urlpatterns = [
    path('', include(router.urls)),
]