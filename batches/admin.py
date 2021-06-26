from django.contrib import admin
from .models import BatchStudent, Batch, Attendance, AttendanceResponse, Quiz
# Register your models here.
admin.site.register(Batch)
admin.site.register(BatchStudent)
admin.site.register(Attendance)
admin.site.register(AttendanceResponse)
admin.site.register(Quiz)