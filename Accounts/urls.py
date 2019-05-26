from django.urls import path
from .views import CreateAccountAPI
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='login'), 
    path('signup/', CreateAccountAPI.as_view(), name='signup'), 
]