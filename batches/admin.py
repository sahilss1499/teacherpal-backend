from django.contrib import admin
from .models import BatchStudent, Batch
# Register your models here.
admin.site.register(Batch)
admin.site.register(BatchStudent)