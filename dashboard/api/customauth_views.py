from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

from customauth.models import (User, FCMToken, WebPushToken)
from django.http import Http404

from .customauth_serializers import (SignUpSerializer, LoginSerializer, FCMTokenSerializer, WebPushTokenSerializer)


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



# for frontend to save FCM token of a user
class SaveFCMToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FCMTokenSerializer

    def post(self,request,format=None):
        serializer = FCMTokenSerializer(data=request.data,partial=True)
        
        if serializer.is_valid():
            try:
                fcm_token_obj = FCMToken.objects.get(user=serializer.validated_data['user'], fcm_token=serializer.validated_data['fcm_token'])
                return Response("FCM token for this user and device already exists", status=status.HTTP_200_OK)
            except FCMToken.DoesNotExist:
                serializer.save()
                return Response("FCM token for the user created", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateWebPushTokenObject(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WebPushTokenSerializer

    def post(self,request, format=None):
        serializer = WebPushTokenSerializer(data=request.data)
        try:
            obj = WebPushToken.objects.get(email=request.data['email'])
            if obj is not None:
                obj.meet_link = request.data['meet_link']
                obj.token1 = request.data['token1']
                obj.token2 = request.data['token2']
                obj.token3 = request.data['token3']
                obj.save()
                return Response('Updated', status=status.HTTP_201_CREATED)

        except:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)