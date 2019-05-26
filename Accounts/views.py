from rest_framework import generics
from .serializers import AccountsCreateSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response


class CreateAccountAPI(generics.CreateAPIView):
    serializer_class = AccountsCreateSerializer