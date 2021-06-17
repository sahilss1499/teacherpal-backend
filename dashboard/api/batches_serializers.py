from rest_framework import serializers

from batches.models import (Batch, BatchStudent)


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('__all__')

