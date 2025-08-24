from django.shortcuts import render
from .models import UserAccount, BankAccount
from .serializers import UserRegistrationSerializer, BankAccountSerializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
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
    
    @action(detail=False, methods=['post'], url_path='verify-otp')
    def Verify_otp(self, request):
        otp_mail = request.data.get('email')
        otp_code = request.data.get('otp')
        
        if not otp_mail or not otp_code:
            return Response({"message": "Email and OTP is Required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_account = UserAccount.objects.get(user__email=otp_mail)
            
            if user_account.otp == otp_code:
                user_account.user.is_active = True
                user_account.user.save()
                
                user_account.otp = None
                user_account.save()
                return Response({"message": "OTP verified successfully. User is now active!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid OTP!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
    
class BankAccountView(viewsets.GenericViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializers
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            accountends = serializer.save()
            return Response({"Message": "Bank Account Created Successfully!", "account_id": accountends.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

