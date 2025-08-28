from django.shortcuts import render
from .models import SolarDevice, InverterBrand, Inverter
from .serializers import SolarDeviceSerializer, InverterBrandSerializer, InverterSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class SolarDeviceView(viewsets.GenericViewSet):
    queryset = SolarDevice.objects.all()
    serializer_class = SolarDeviceSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(owner=self.request.user)
            return Response({"message": "Device Created Successfully!", 'Device_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class InverterBrandView(viewsets.GenericViewSet):
    queryset = InverterBrand.objects.all()
    serializer_class = InverterBrandSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            inverter = serializer.save()
            return Response({"message": "Inverter Brand Created Successfully!", "Inverter_logo": inverter.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class InverterView(viewsets.GenericViewSet):
    queryset = Inverter.objects.all()
    serializer_class = InverterSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            inervt = serializer.save(device=self.request.device, brand=self.request.brand)
            return Response({"message": "Inverter Created Successfully!", "Inverter_id": inervt.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)