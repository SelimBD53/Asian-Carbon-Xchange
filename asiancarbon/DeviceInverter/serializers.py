from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SolarDevice, InverterBrand, Inverter, DeviceLocation, GenerationData
from drf_extra_fields.fields import Base64ImageField

class SolarDeviceSerializer(serializers.ModelSerializer):
    class  Meta:
        model = SolarDevice
        fields = ['id', 'code', 'device_type', 'capacity_kWp', 'cop_date', 'status', 'tier']
        
        read_only_fields = ['id', 'status']
    
    def create(self, validated_data):
        try:
            user = SolarDevice.objects.create(**validated_data)
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError({"message: Error From Device creation! {e}"})

class InverterBrandSerializer(serializers.ModelSerializer):
    logo_pic = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = InverterBrand
        fields = "__all__"
        # ['id', 'name', 'logo_pic', 'is_immediate_connection']
        
    
    def create(self, validated_data):
        try: 
            img = validated_data.get('logo_pic')
            print(img)
            inverter = InverterBrand.objects.create(**validated_data)
            inverter.save()
            return inverter
        except Exception as e:
            raise serializers.ValidationError({"message": f"Inverter Brand Creation Error! {e}"})
        
class InverterSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    class Meta:
        model = Inverter
        fields = ['id', 'device', 'brand_name', 'serial_no', 'capacity_kwp']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        try:
            invertes = Inverter.objects.create(**validated_data)
            invertes.save()
            return invertes
        except Exception as e:
            return serializers.ValidationError({"message": f"Error From Inverter Creation {e}"})
    
class DeviceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLocation
        fields = "__all__"
    
    def create(self, validated_data):
        try:
            deviceloc = DeviceLocation.objects.create(**validated_data)
            deviceloc.save()
            return deviceloc
        except Exception as e:
            return serializers.ValidationError({"message": f"Error Creation from Device Location! {e}"})

class GenerationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationData
        fields = "__all__"
    
    def create(self, validated_data):
        try:
            data_user = GenerationData.objects.create(**validated_data)
            data_user.save()
            return data_user
        except Exception as e:
            return serializers.ValidationError({"message": f"Error From Generation Data Create! {e}"})

class ConfirmDeviceSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)
    inverter = InverterSerializer(source="Inverters", many=True, read_only=True)
    device_location = serializers.SerializerMethodField()
    
    class Meta:
        model = SolarDevice
        fields = ['owner_name', 'device_type', 'capacity_kWp', 'cop_date', 'inverter', 'device_location']
    
    def get_device_location(self, inst):
        location = inst.solar_device
        return {
            "address": location.address,
            "country": location.country,
            "province": location.province 
        }
    