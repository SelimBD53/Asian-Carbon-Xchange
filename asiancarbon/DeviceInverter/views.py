from django.shortcuts import render
from .models import SolarDevice, InverterBrand, Inverter, DeviceLocation, GenerationData
from .serializers import SolarDeviceSerializer, InverterBrandSerializer, InverterSerializer, DeviceLocationSerializer, GenerationDataSerializer, ConfirmDeviceSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class SolarDeviceView(viewsets.GenericViewSet):
    queryset = SolarDevice.objects.all()
    serializer_class = SolarDeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
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
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
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
            inervt = serializer.save()
            return Response({"message": "Inverter Created Successfully!", "Inverter_id": inervt.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceLocationView(viewsets.GenericViewSet):
    queryset = DeviceLocation.objects.all()
    serializer_class = DeviceLocationSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            locat = serializer.save()
            return Response({"message": "Device Location Created Successfully!", "device_id": locat.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerationDataView(viewsets.GenericViewSet):
    queryset = GenerationData.objects.all()
    serializer_class = GenerationDataSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            gent = serializer.save()
            return Response({"message": "Generation Data Created Successfully!", "gent_id": gent.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmDeviceView(viewsets.GenericViewSet):
    serializer_class = ConfirmDeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SolarDevice.objects.filter(owner=self.request.user)

    def retrieve(self, request, pk=None):
        deva = self.get_object()
        serializer = self.get_serializer(deva)
        return Response(serializer.data, status=status.HTTP_200_OK)