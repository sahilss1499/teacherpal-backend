from django.db.models import fields
from rest_framework import serializers

from batches.models import (Batch, BatchStudent)

from .customauth_serializers import UserDetailSerializer

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('__all__')

class BatchStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchStudent
        fields = ('batch', 'student')

class BatchStudentShowSerializer(serializers.ModelSerializer):
    student = UserDetailSerializer()
    class Meta:
        model = BatchStudent
        fields = ('__all__')


class AttendanceRequestSerializer(serializers.Serializer):
    meet_link = serializers.URLField()
    duration = serializers.IntegerField(required=False)
    sender = serializers.UUIDField(required=False)

    class Meta:
        fields = ('meet_link', 'duration', 'sender')


class AttendanceResponseSerializer(serializers.Serializer):
    meet_link = serializers.URLField()
    student_id = serializers.UUIDField()

    class Meta:
        fields = ('meet_link', 'student_id')


class AttendanceDetailSerializer(serializers.Serializer):
    date = serializers.DateField()

    class Meta:
        fields = ('date',)