from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.user.useraccount.role == 'customer':
            return True
        else:
            return False
       

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.useraccount.role == 'admin':
            return True
        else:
            return False