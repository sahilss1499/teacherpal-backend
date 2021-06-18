from django.contrib import admin
from .models import BatchStudent, Batch, Attendance, AttendanceResponse
# Register your models here.
admin.site.register(Batch)
admin.site.register(BatchStudent)
admin.site.register(Attendance)
admin.site.register(AttendanceResponse)