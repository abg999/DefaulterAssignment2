from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.validators import UniqueValidator

class AccountsCreateSerializer(serializers.ModelSerializer):
    '''
        A serializer class defined to match the structure of incoming requests
        to create a new Account.
        Appuser(user, firstname, lastname, email, username, password, )
    '''

    def create(self, validated_data):
        # this method has been overrided to change hash the password
        # manually, as the form would simply dump the normal string 
        # and would cause problems with the related user object
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
