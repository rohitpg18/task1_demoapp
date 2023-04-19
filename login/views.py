from django.shortcuts import render, redirect
from login.models import *
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from login.serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q

from itertools import chain

# Views for Rest APIS

# To view all users

class AllUsersView(APIView):
    
    permission_classes = [IsAuthenticated,]
    
    def get (self, request):
        
        if request.user.is_superuser == True and request.user.username == 'admin':
            
            student_users = User.objects.filter(is_superuser = False)
            
            serializer = UserStudentSerializer(student_users, many = True)
            
            return Response(serializer.data)
        
        elif request.user.is_superuser == False or request.user.username != 'admin':
            
            student_user = User.objects.filter(id = request.user.id)
            
            serializer = UserStudentSerializer(student_user, many=True)
            
            return Response(serializer.data)
        
        
        
# List of students to be approved
  
class ApproveUserList(APIView):
    
    def get(self, request):
        
        student_users = User.objects.filter(Q(is_active = False) & Q(student_user__is_requested = True) )
        
        serializer = UserStudentSerializer(student_users, many = True)
            
        return Response(serializer.data)
    
        
        
# Delete Student    
class DeleteAPI(APIView):
    
    permission_classes = [IsAuthenticated,]
    
    def get(self,request):
        
        return Response('api call')
    
    def post(self, request):
        
        id = request.POST.get('id')
        user = User.objects.get(id = id)
        user.delete()
        
        return Response('User is deleted')
    

# approve user with specific id 
class ApproveStudent(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request, pk):
        pk = int(pk)
        
        student_users = User.objects.get(id = pk)
        
        serializer = UserStudentSerializer(student_users, many = False)
        
        return Response(serializer.data)

    
    def post(self, request, pk):
        
        pk = int(pk)
        
        
        
        action = request.POST.get('is_active')
        user = User.objects.get(id=pk)
        student = Student.objects.get(student_user_id = pk)
        
        if action == 'True':
            user.is_active = True
            student.is_requested = False
            student.is_approved = True
            
        else:
            student.is_requested = False
            user.is_active = False
            student.is_approved = False
            
            
        user.save()
        student.save()
        
        
        
        
        
        return Response('Updated Successfully')
    

# Login approval rejected users    
class RejectedStudentList(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        
        if request.user.is_superuser == True and request.user.username == 'admin':
            student_users = User.objects.filter(Q(is_active = False) & Q(student_user__is_requested = False) )
            serializer = UserSerializer(student_users, many = True)
            
            
        return Response(serializer.data)
    

# update user details   
class UpdateAPI(APIView):
    
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, pk):
        pk = int(pk)
        
        student_users = User.objects.get(id = pk)
        
        serializer = UserStudentSerializer(student_users, many = False)
        
        return Response(serializer.data)
    
    def post(self, request, pk):
        
        pk = int(pk)
        
        user = User.objects.get(id=pk)
        student = Student.objects.get(student_user_id = pk)
        
        if request.POST.get('is_active') == 'true':
            user.is_active = True
        else:
            user.is_active = False
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone_number')
        
        
        user.save()
        student.save()
        
        return Response('Updated Successfully')
    
    
    
# add new student/user with this
class CreateStudent(APIView):

    
    def post(self, request):
        
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        
        user = User.objects.create(username = username, first_name=first_name, last_name=last_name, email= email)
        user.set_password(password)
        user.is_active = False
        user.save()
        
        student = Student.objects.create(student_user_id=user.id, phone_number = phone_number, is_approved = False)
        
        admin_user = User.objects.get(username = 'admin')
        
        # if student is not None:
        
        #     send_mail("New Student added",
        #               f'''New student added - 
        #               Username - {user.username}
        #               First Name - {user.first_name}
        #               Last Name - {user.last_name}
        #               Email - {user.email}
        #               Phone Number - {student.phone_number}
        #               ''', 
        #               'rpgunjegaonkar@gmail.com',[f'{admin_user.email}'])
            
        #     print('mail_sent')
        
        return Response('Student created successfully')
    
    
        
    
    
# Views for Rendering Templates       
        
def api_data(request):
    
    return render (request, 'api_data.html')

def login_api(request):
    return render (request, 'api-login.html')

def approve_user(request):
    return render(request, 'approve_user.html')

def rejected_user(request):
    return render(request, 'rejected_list.html')
            
    
    


















































# OLD VIEWS

# for signing up in app
def signup(request):
    
    if request.method == "POST":
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return redirect('signup')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get('first_name')
        user.save()
        
        return redirect('login')
    
    return render(request,'signup.html')



# authenticate user 
def login(request):
    
    if request.method == "POST":
        
        user = authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("home")
        else:

            return redirect('login')
        
    return render(request, "login.html")

# authenticate user logout

@login_required(login_url="/login/")
def signout(request):
    auth.logout(request)
    return redirect("login")
    

# All students list.
@login_required(login_url="/login/")
def home (request):
    s = Student.objects.all().values()

    users= None
    if request.user.is_superuser:
        users= User.objects.all()
        
    template = loader.get_template("index.html")
    
    context = {
        's' : s ,
        'users' : users
    }

    return HttpResponse (template.render(context, request))

# add new student
@login_required(login_url="/login/")
def add (request):
    if request.method == 'POST':
        name_stu = request.POST.get("student-name")
        number = request.POST.get("student-number")
        emailid = request.POST.get("student-email")
        profile_pic= request.FILES.get('img', None)
        
        

        s = Student()
        s.name = name_stu
        
        s.phone_number = number
        
        s.email = emailid
        
        if profile_pic is not None and profile_pic != '':
            s.display_picture = profile_pic
            
        s.save()
        return redirect ("/")

    return render (request , "add-student.html")

# delete student
@login_required(login_url="/login/")
def delete_student (request , id):
    s = Student.objects.get(pk = id)
    s.delete()
    return redirect ("/")

# get student which we want to update
@login_required(login_url="/login/")
def update_student(request,id):
    s = Student.objects.get(pk = id)
    return render (request, "update-student.html" ,{
        "s" : s
    })

# update required details
@login_required(login_url="/login/")
def update_student_details(request, id):
    if request.method == 'POST':
        name_stu = request.POST.get("student-name")
        number = request.POST.get("student-number")
        emailid = request.POST.get("student-email")
        profile_pic= request.FILES.get('img', None)

        s = Student.objects.get(pk = id)
        s.name = name_stu
        s.phone_number = number
        s.email = emailid
        s.display_picture = profile_pic
        s.save()
        return redirect ("/")












    