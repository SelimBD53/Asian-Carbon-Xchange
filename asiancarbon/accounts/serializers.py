from rest_framework import serializers
from .models import UserAccount, BankAccount
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from asiancarbon.settings import EMAIL_HOST_USER

class UserSerializers(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=False)
    full_named = serializers.SerializerMethodField(read_only=True)

    
    class Meta:
        model = User
        fields = ['id', 'username','full_named', 'email', 'full_name', 'password']
        extra_kwargs = {
            'username': {'read_only': True},
            'full_name': {'write_only': True}
        }
    def get_full_named(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class UserRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserAccount
        fields = ['user', 'phone', 'confirm_password', 'nric_number', 'role']
    
    def validate_role(self, value):
        if value == 'admin':
            raise serializers.ValidationError({"message": "Cann't Create role Admin!"})
        
    def validate(self, data):
        user_data = data.get('user')
        password = user_data.get('password')
        confirm_password = data.get('confirm_password')
        try:
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Confirm Password did not match!"})
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                {"message: Error Validat in Password And Confirm Password"})
        data.pop('confirm_password', None)
        return data

    def create(self, validated_data):
        try:
            otp_code = str(random.randint(100000, 999999))
            validated_data['role'] = 'customer'
            user = validated_data.pop('user')
            
            full_name = user.pop('full_name')
            phone = validated_data.get('phone')
            name_part = full_name.split(' ')
            first_name = name_part[0]
            
            last_name = name_part[1] if len(name_part) > 1 else ''
            username = f"{first_name}_{last_name}_{phone[-2:]}"
            user_instance = User.objects.create(username=username, first_name=first_name, last_name=last_name, **user)
            user_instance.set_password(user.get('password'))
            user_instance.save() 
            
            user_account = UserAccount.objects.create(user=user_instance, otp=otp_code)
            for key, value in validated_data.items():
                setattr(user_account, key, value)
            user_account.save()
            subject = f"Welcome {full_name} to our Platform"
            message = f"""
Hello {first_name},

Welcome to our platform! Your account has been Create Successfully.
Verify to the account . Your OTP code {otp_code}


Best regards,
Asian Carbon Xchangs"""
            send_mail(subject, message, EMAIL_HOST_USER, [user_instance.email], fail_silently=False)
            return user_account

        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                {'message : Error Creating Student! {e}'})
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            full_name = user_data.pop('full_name', None)
            
            if full_name:
                phone = validated_data.get('phone', instance.phone)
                name_part = full_name.split(' ')
                instance.user.first_name = name_part[0]
                instance.user.last_name = name_part[1] if len(name_part) > 1 else ''
                instance.user.username = f"{instance.user.first_name}_{instance.user.last_name}_{phone[-2:]}"
                
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
        instance.user.save()
        
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance   
        

class BankAccountSerializers(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ['full_name', 'email', 'phone', 'nric_number', 'bank_name', 'account_number',
                  'account_type', 'branch_name_code', 'terms_accepted', 'created_at']
        read_only_fields = ['created_at']

        def validate(self, data):
            if '@' not in data.get('email'):
                raise serializers.ValidationError(
                    {"email": "Email Address Not Valied!"})
            if len(data.get('phone')) <= 10:
                raise serializers.ValidationError(
                    {"Phone": "Invalid Phone Number!"})
            if not data.get('terms_accepted', False):
                raise serializers.ValidationError(
                    {"terms_accepted": "You must accept the terms and conditions"})
            account_number = data.get('account_number', '')
            if not account_number.isdigit() or len(account_number) < 10:
                raise serializers.ValidationError(
                    {"account_number": "Account Number Must be Numeric and at least 10 digits"})

        def create(self, validated_data):
            try:
                bank_data = {
                    'full_name': validated_data.get('full_name'),
                    'email': validated_data.get('email'),
                    'phone': validated_data.get('phone'),
                    'nric_number': validated_data.get('nric_number'),
                    'account_number': validated_data.get('account_number'),
                    'account_type': validated_data.get('account_type'),
                    'branch_name_code': validated_data.get('branch_name_code'),
                    'terms_accepted': validated_data.get('terms_accepted')
                }

                bank_account = BankAccount.objects.create(**bank_data)
                bank_account.save()
                return bank_account
            except Exception as e:
                print(e)
                raise serializers.ValidationError(
                    {"message": "Bank Account Create Problem in Serializers!"})
