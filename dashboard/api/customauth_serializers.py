from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework_jwt.settings import api_settings

from customauth.models import (User, FCMToken)
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import auth
import jwt
from django.conf import settings
from rest_framework.response import Response
import random
from rest_framework import permissions


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'role',
                  'full_name')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=4, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    token = serializers.CharField(
        max_length=68, min_length=6, read_only=True)
    full_name = serializers.CharField(
        max_length=68, min_length=6, read_only=True)


    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'token',
                  'id','full_name','role']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        try:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token,
            'id': user.id,
            'role': user.role,
        }
        return super().validate(attrs)




class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ('__all__')