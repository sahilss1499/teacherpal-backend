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