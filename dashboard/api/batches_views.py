from rest_framework import permissions, status, filters
from rest_framework.generics import ListAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from batches.models import (Attendance, Batch, BatchStudent, AttendanceResponse)
from .batches_serializers import (BatchSerializer, BatchStudentSerializer, BatchStudentShowSerializer, AttendanceRequestSerializer)




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


class BatchDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BatchSerializer
    def get_object(self, pk):
        try:
            return Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        batch = self.get_object(pk)
        serializer = BatchSerializer(batch)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        batch = self.get_object(pk)
        serializer = BatchSerializer(
            batch, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        batch = self.get_object(pk)
        batch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class BatchStudentList(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BatchStudentSerializer

    def get(self, request,pk,format=None):
        try:
            students = BatchStudent.objects.filter(batch=pk)
            serializer=BatchStudentShowSerializer(students,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise Http404

    def post(self, request, format=None):
        serializer = BatchStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AttendanceRequestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AttendanceRequestSerializer

    def post(self,request,format=None):
        serializer = AttendanceRequestSerializer(data=request.data,partial=True)

        if serializer.is_valid():
            try:
                batch_obj = Batch.objects.get(meet_link=serializer.validated_data['meet_link'])
            except:
                return Response("No batch with given meet link exists", status=status.HTTP_400_BAD_REQUEST)
            duration = 120
            if serializer.validated_data['duration'] is None:
                duration=serializer.validated_data['duration']

            attendance = Attendance.objects.create(
                batch=batch_obj,
                duration=duration,
                created_by=self.request.user
            )

            return Response("Attendance Request created", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class AttendanceResponse(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
