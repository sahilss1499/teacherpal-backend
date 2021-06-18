from rest_framework import permissions, status, filters
from rest_framework.generics import ListAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

from batches.models import (Batch, BatchStudent)
from .batches_serializers import BatchSerializer




class BatchCreateListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BatchSerializer

    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['created_by']

    def get_queryset(self):
        queryset = Batch.objects.all().order_by('-id')
        return queryset

    def post(self,request,format=None):
        serializer = BatchSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


