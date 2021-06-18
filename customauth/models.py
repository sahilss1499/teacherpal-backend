from django.db import models

import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other','other'),
    )

    role_choices = (
        ('is_superadmin', 'is_superadmin'),
        ('is_teacher', 'is_teacher'),
        ('is_student', 'is_student'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, blank=True, null=True,)
    role = models.CharField(max_length=100,choices=role_choices, blank=True, null=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=50, choices=gender_choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.id)



class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_fcm_token')
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.fcm_token