from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
choise = (
    ('customer', 'Customer'),
    ('admin', 'Admin')
)
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    nric_number = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=7, blank=True, null=True)
    role = models.CharField(max_length=20, choices=choise, null=True, blank=True, default='customer')
    
    def __str__(self):
        return self.user.username

bank_choise = (
    ('UCB', 'UCB'),
    ('NRBC', 'NRBC'),
    ('City', 'City'),
    ('Dhaka Bank', 'Dhaka Bank'),
)
account_type_choise = (
    ('Savings Account', 'Savings Account'),
    ('Current Account', 'Current Account'),
    ('Fixed Deposit Account', 'Fixed Deposit Account'),
)

class BankAccount(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=15)
    nric_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100, choices=bank_choise)
    account_number = models.CharField(max_length=100, unique=True)
    account_type = models.CharField(max_length=100, choices=account_type_choise)
    branch_name_code = models.CharField(max_length=100)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    