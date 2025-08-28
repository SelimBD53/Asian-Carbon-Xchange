from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SolarDevice, InverterBrand, Inverter
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
    class Meta:
        model = Inverter
        fields = ['id', 'serial_no', 'capacity_kwp']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        try:
            invertes = Inverter.objects.create(**validated_data)
            invertes.save()
            return invertes
        except Exception as e:
            return serializers.ValidationError({"message": f"Error From Inverter Creation {e}"})
        