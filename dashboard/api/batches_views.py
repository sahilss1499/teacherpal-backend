from rest_framework import permissions, status, filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from batches.models import (Attendance, Batch, BatchStudent, AttendanceResponse, Quiz, QuizResponse)
from customauth.models import (User, FCMToken, WebPushToken)
from .batches_serializers import (BatchSerializer, BatchStudentSerializer, 
                                    BatchStudentShowSerializer, AttendanceRequestSerializer, AttendanceResponseSerializer,
                                    AttendanceDetailSerializer, QuizRequestSerializer, QuizResponseSerializer, QuizSerializer)

from .notification_service import send_notification, send_attendance_notification, send_quiz_notification


from django.utils import timezone
import datetime


# Frontend website APIs
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
            data=serializer.validated_data
            user=User.objects.get(id=self.request.user.id)
            data['created_by']=user
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

    def post(self, request,pk,format=None):
        serializer = BatchStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AttendanceDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AttendanceDetailSerializer

    def post(self,request,pk,format=None):
        serializer = AttendanceDetailSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            attendance_request_qs = Attendance.objects.filter(batch=pk,created_by=self.request.user.id,created_at__date=data['date'])
            total_attendance_requests = attendance_request_qs.count()
            if total_attendance_requests==0:
                return Response("No Attendance were taken on this date", status=status.HTTP_400_BAD_REQUEST)
            attendace_response_qs = AttendanceResponse.objects.filter(batch=pk,created_at__date=data['date'])
            # to get student list
            batch_student_qs = BatchStudent.objects.filter(batch=pk)
            student_att_count = {}
            
            for batch_student in batch_student_qs:
                student_att_count[batch_student.student.email] = 0
            
            for attendance_response in attendace_response_qs:
                student_att_count[attendance_response.student.email] += 1


            for key, value in student_att_count.items():
                student_att_count[key] = (value/total_attendance_requests)*100

            student_att_count["total_attendance_requests"] = total_attendance_requests
            return Response(student_att_count, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class QuizListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuizSerializer

    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['created_by', 'batch']

    def get_queryset(self):
        queryset = Quiz.objects.all().order_by('-id')
        return queryset


class QuizDetailView(APIView):
    def get(self,request,pk,format=None):
        quiz_obj = Quiz.objects.get(id=pk)
        batch_student_qs = BatchStudent.objects.filter(batch=quiz_obj.batch)
        quiz_response_qs = QuizResponse.objects.filter(quiz=pk)

        student_quiz_response = {}
            
        for batch_student in batch_student_qs:
            student_quiz_response[batch_student.student.email] = {"is_correct": None, "response": None}
        
        
        for quiz_response in quiz_response_qs:
            student_quiz_response[quiz_response.student.email]["is_correct"] = quiz_response.is_correct
            student_quiz_response[quiz_response.student.email]["response"] = quiz_response.answer

        return Response(student_quiz_response, status=status.HTTP_200_OK)








# Extension side APIs
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

            batch_students = BatchStudent.objects.filter(batch=batch_obj.id)

            receivers = WebPushToken.objects.filter(meet_link=serializer.validated_data['meet_link'])
            token_list = []
            
            for receiver in receivers:
                token_list_item = {}
                token_list_item["token1"]=receiver.token1
                token_list_item["token2"]=receiver.token2
                token_list_item["token3"]=receiver.token3
                token_list.append(token_list_item)
            
            send_attendance_notification(token_list)
            

            return Response({"response": "Attendance Request created"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AttendanceResponseView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AttendanceResponseSerializer

    def post(self,request,format=None):
        serializer = AttendanceResponseSerializer(data=request.data)

        if serializer.is_valid():
            try:
                batch_obj = Batch.objects.get(meet_link=serializer.validated_data['meet_link'])
            except:
                return Response("No batch with given meet link exists", status=status.HTTP_400_BAD_REQUEST)

            try:
                attendance_request_obj = Attendance.objects.filter(batch=batch_obj).last()
            except:
                return Response("No such meeting link found", status=status.HTTP_400_BAD_REQUEST)
            
            attendance_response_obj = AttendanceResponse(
                attendance=attendance_request_obj,
                student=self.request.user,
                batch=batch_obj
            )

            if(attendance_request_obj.created_at + datetime.timedelta(seconds=attendance_request_obj.duration) > timezone.now()):
                attendance_response_obj.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response("The attendance got expired",status=status.HTTP_406_NOT_ACCEPTABLE)
            
        return Response("Some Error encountered",status=status.HTTP_400_BAD_REQUEST)





class QuizRequestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuizRequestSerializer

    def post(self,request,format=None):
        serializer = QuizRequestSerializer(data=request.data,partial=True)

        if serializer.is_valid():
            try:
                batch_obj = Batch.objects.get(meet_link=serializer.validated_data['meet_link'])
            except:
                return Response("No batch with given meet link exists", status=status.HTTP_400_BAD_REQUEST)
            duration = 120
            if serializer.validated_data['duration'] is None:
                duration=serializer.validated_data['duration']

            quiz = Quiz.objects.create(
                batch=batch_obj,
                duration=duration,
                question=serializer.validated_data['question'],
                option_a=serializer.validated_data['option_a'],
                option_b=serializer.validated_data['option_b'],
                option_c=serializer.validated_data['option_c'],
                option_d=serializer.validated_data['option_d'],
                answer=serializer.validated_data['answer'],
                created_by=self.request.user
            )

            batch_students = BatchStudent.objects.filter(batch=batch_obj.id)

            receivers = WebPushToken.objects.filter(meet_link=serializer.validated_data['meet_link'])
            token_list = []
            
            for receiver in receivers:
                token_list_item = {}
                token_list_item["token1"]=receiver.token1
                token_list_item["token2"]=receiver.token2
                token_list_item["token3"]=receiver.token3
                token_list.append(token_list_item)
            
            send_quiz_notification(serializer.validated_data,token_list)
            

            return Response({"response": "Quiz Request created"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class QuizResponseView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuizResponseSerializer

    def post(self,request,format=None):
        serializer = QuizResponseSerializer(data=request.data)

        if serializer.is_valid():
            try:
                batch_obj = Batch.objects.get(meet_link=serializer.validated_data['meet_link'])
            except:
                return Response("No batch with given meet link exists", status=status.HTTP_400_BAD_REQUEST)

            try:
                quiz_request_obj = Quiz.objects.filter(batch=batch_obj).last()
            except:
                return Response("No such meeting link found", status=status.HTTP_400_BAD_REQUEST)
            
            quiz_response_obj = QuizResponse(
                quiz=quiz_request_obj,
                answer=serializer.validated_data['answer'],
                student=self.request.user,
                is_correct=False,
                batch=batch_obj
            )

            if(quiz_request_obj.created_at + datetime.timedelta(seconds=quiz_request_obj.duration) > timezone.now()):
                if quiz_response_obj.answer == quiz_request_obj.answer:
                    print("Correct answer")
                    quiz_response_obj.is_correct=True
                else:
                    print("Wrong answer")
                quiz_response_obj.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response("The Quiz got expired",status=status.HTTP_406_NOT_ACCEPTABLE)
            
        return Response("Some Error encountered",status=status.HTTP_400_BAD_REQUEST)