from django.shortcuts import render
from .models import UserAccount, BankAccount
from .serializers import UserRegistrationSerializer, BankAccountSerializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class UserRegView(viewsets.GenericViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserRegistrationSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_acc = serializer.save()
            return Response({"message": "User Account Created Successfully", "user_id": user_acc.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BankAccountView(viewsets.GenericViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializers
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            accountends = serializer.save()
            return Response({"Message": "Bank Account Created Successfully!", "account_id": accountends.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

