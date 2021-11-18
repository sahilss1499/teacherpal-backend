from django.db import models

from customauth.models import User

# Create your models here.
class Batch(models.Model):
    name = models.CharField(max_length=200)
    meet_link = models.URLField(unique=True)
    created_by= models.ForeignKey(User,related_name='batch_created_by',blank=True,null=True,on_delete=models.CASCADE)
    modified_by= models.ForeignKey(User,related_name='batch_modified_by',blank=True,null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name



class BatchStudent(models.Model):

    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.PROTECT)
    created_by=models.ForeignKey(User,related_name='batch_student_created_by', on_delete=models.PROTECT,blank=True,null=True)
    modified_by=models.ForeignKey(User,related_name='batch_student_modified_by', on_delete=models.PROTECT,blank=True,null=True)

    class Meta:
        unique_together = ('batch','student')




class Attendance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    duration = models.IntegerField(default=120)
    created_by= models.ForeignKey(User,related_name='attendance_created_by',blank=True,null=True,on_delete=models.CASCADE)
    modified_by= models.ForeignKey(User,related_name='attendance_modified_by',blank=True,null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) :
        return f"Batch: {str(self.batch.name)}; Created At: {str(self.created_at)}"

class AttendanceResponse(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self) :
        return f"Attendendance: {self.attendance.id}; Student: {self.student.email}; Batch: {str(self.batch.name)}"


class Quiz(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    duration = models.IntegerField(default=300)

    question=models.TextField()
    option_a=models.CharField(max_length=300,blank=True,null=True)
    option_b=models.CharField(max_length=300,blank=True,null=True)
    option_c=models.CharField(max_length=300,blank=True,null=True)
    option_d=models.CharField(max_length=300,blank=True,null=True)
    answer = models.CharField(max_length=300,blank=True,null=True)

    created_by= models.ForeignKey(User,related_name='Quiz_created_by',blank=True,null=True,on_delete=models.CASCADE)
    modified_by= models.ForeignKey(User,related_name='Quiz_modified_by',blank=True,null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.question



class QuizResponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self) :
        return f"Quiz: {self.quiz.id}; Student: {self.student.email}; Batch: {str(self.batch.name)}"