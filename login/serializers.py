from rest_framework import serializers
from login.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'password']

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class UserStudentSerializer(serializers.ModelSerializer):
    student_user = StudentSerializers(many = False, read_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','is_active','is_superuser', 'student_user']
        
# class LoginSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = ['username', 'password']
    