from django.db import models

from customauth.models import User

# Create your models here.
class Batch(models.Model):
    name = models.CharField(max_length=200)
    meet_link = models.URLField(unique=True)
    created_by= models.ForeignKey(User,related_name='batch_created_by',blank=True,null=True,on_delete=models.CASCADE)
    modified_by= models.ForeignKey(User,related_name='batch_modeified_by',blank=True,null=True,on_delete=models.CASCADE)
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