from django.urls import path, include
from . import views
from .auth_app import UserLoginview, CustomLogoutView

from rest_framework import routers
router = routers.DefaultRouter()
router.register('user-registration', views.UserRegView, basename='user_registration')
router.register('bank-account', views.BankAccountView, basename='bank_account')
urlpatterns = [
    path('', include(router.urls)),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('add-bank-account/', views.BankAccountView.as_view(), name='create-account'),
    path('login/', UserLoginview.as_view()),
    path('logout/', CustomLogoutView.as_view()),
]
