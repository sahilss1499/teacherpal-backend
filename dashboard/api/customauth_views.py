from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

from customauth.models import User
from django.http import Http404

from .customauth_serializers import SignUpSerializer, LoginSerializer


class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        user = request.data
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data

            return Response(user_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)