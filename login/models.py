from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10 , null=True)
    display_picture = models.ImageField(upload_to='displaypictures', null=True, default='default_profile_pic.png')
    is_approved = models.BooleanField(default=False)
    is_requested = models.BooleanField(default=True)

    def __str__(self):
        return self.student_user.username
    
