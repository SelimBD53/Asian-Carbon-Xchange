from dj_rest_auth.views import LoginView, APIView
from accounts.models import UserAccount
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

class UserLoginview(LoginView):
    
    def post(self, request, *args, **kwargs):
        userdata = self.request.data.get('user')
        
        useracc = None
        if '@' in userdata:
            useracc = UserAccount.objects.filter(user__email=userdata).first()
        else:
            useracc = UserAccount.objects.filter(phone=userdata).first()

        if not useracc:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        self.request.data['username'] = useracc.user.username
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        response = {
            "access": self.get_response().data["access"],
            "refresh": self.get_response().data["refresh"],
            "user": {
                "id": useracc.id,
                "username": useracc.user.username,
                "first_name": useracc.user.first_name,
            },
            "phone": useracc.phone,
            "nric_number": useracc.nric_number,
        }
        return Response(response)
    
class CustomLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"})