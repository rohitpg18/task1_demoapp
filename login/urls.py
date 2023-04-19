from django.urls import path
from .views import *

urlpatterns = [
    
    # Rest API urls
    path('all-students/', AllUsersView.as_view(), name='all_student'),
    path('delete/', DeleteAPI.as_view(), name='delete'),
    path('update-api/<str:pk>/', UpdateAPI.as_view(), name='update'),
    path('create/', CreateStudent.as_view(), name = 'create'),
    path('approve-user-list/', ApproveUserList.as_view(), name = 'approve_user'),
    path('approve/<str:pk>/', ApproveStudent.as_view(), name = 'approve'),
    path('rejected-list/', RejectedStudentList.as_view(), name = 'rejected_list'),

    
    
    
    # urls for rendering templates
    path('api-data/', api_data, name = 'api'),
    path('api-login/', login_api, name = 'api_login'),
    path('approve-student/', approve_user, name = 'approve_student'),
    path('rejected-users/', rejected_user, name = 'rejected_users'),
    
    
    
    # old urls
    path('' , home, name = 'home'),
    path('add-student/', add , name = 'add-student'),
    path('delete-student/<int:id>', delete_student , name = 'delete-student'),
    path('update-student/<int:id>' , update_student , name = 'update-student'),
    path('do-update/<int:id>' , update_student_details, name = 'do-update'),
    path('signup/',signup,name='signup'), 
    path('login/',login,name='login'), 
    path('signout/',signout,name='signout'),     
]





