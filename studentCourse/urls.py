
from django.contrib import admin
from django.urls import path
from studentCourse_app.views import (
    AdminAddStudentView, GetStudentView, UpdateStudentView, 
    DeleteStudentView,CoursesAPIView,ModuleAPIView,
    StudentSignupView, LoginView,LogoutView,ProfileView,
    FeedBackStudentListView, FeedBackStudentDetailView, 
    FeedBackStudentReplyView,NotificationListView, NotificationDetailView,
    ContactMessageListView, ContactMessageDetailView,RegistrationListCreateView,
    RegistrationDetailView,check_email_exist,check_username_exist,RegistrationDeleteView,
    user_type_check)
from studentCourse_app.templateViews import (
    LoginPage,SignupStudent,AdminHome,AdminProfile,AddStudent,
    AddModule,AddCourse,ManageCourse,ManageModule,ManageStudent,
    StudentFeedbackMessage,StudentContactUs,NotificationStudent,
    StudentHome,StudentProfile,About,Contact,CourseShow,ModuleShow)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('login_page',LoginPage,name="login_page"),
    path('signup_student',SignupStudent,name="signup_student"),
    path('api/auth/user-status/', user_type_check, name='user-status'),
    
    path('api/signup/', StudentSignupView.as_view(), name='student-signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    #Admin Api
    path('api/admin/students/add/', AdminAddStudentView.as_view(), name='admin_add_student'),
    path('api/admin/students/', GetStudentView.as_view(), name='admin_get_all_students'),
    path('api/admin/students/update/<int:student_id>', UpdateStudentView.as_view(), name='admin_update_student'),
    path('api/admin/students/delete/<int:student_id>', DeleteStudentView.as_view(), name='admin_delete_student'),
    path('api/admin/courses/', CoursesAPIView.as_view()),  # Handles GET all, POST new course
    path('api/admin/courses/<int:pk>', CoursesAPIView.as_view()),  # Handles GET, PUT, DELETE for a specific course

    path('api/admin/modules/', ModuleAPIView.as_view()),  # Handles GET all, POST new module
    path('api/admin/modules/<int:pk>/', ModuleAPIView.as_view()),  # Handles GET, PUT, DELETE for a specific module
    
    path('api/profile/', ProfileView.as_view(), name='profile'),

    path('api/feedback/', FeedBackStudentListView.as_view(), name='feedback-list'),
    path('api/feedback/<int:pk>', FeedBackStudentDetailView.as_view(), name='feedback-detail'),
    path('api/feedback/reply/<int:pk>', FeedBackStudentReplyView.as_view(), name='feedback-reply'),
    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/notifications/<int:pk>', NotificationDetailView.as_view(), name='notification-detail'),
    path('api/contact-messages/', ContactMessageListView.as_view(), name='contact-message-list'),
    path('api/contact-messages/<int:pk>', ContactMessageDetailView.as_view(), name='contact-message-detail'),
    path('api/registrations/', RegistrationListCreateView.as_view(), name='registration-list-create'),
    path('api/registrations/<int:pk>/', RegistrationDetailView.as_view(), name='registration-detail'),
    path('api/registrations/delete_by_module/<int:module_id>', RegistrationDeleteView.as_view(), name='delete_registration_by_module'),

    path('check_email_exist', check_email_exist,name="check_email_exist"),
    path('check_username_exist', check_username_exist,name="check_username_exist"),
    #Admin
    path('admin/admin_home',AdminHome,name="admin_home"),
    path('admin/admin_profile', AdminProfile,name="admin_profile"),
    path('admin/add_student', AddStudent,name="add_student"),
    path('admin/add_course', AddCourse, name='add_course'),
    path('admin/add_module', AddModule, name='add_module'),
    path('admin/manage_student', ManageStudent,name="manage_student"),
    path('admin/manage_course', ManageCourse,name="manage_course"),
    path('admin/manage_module', ManageModule,name="manage_module"),
    path('admin/student_feedback_message', StudentFeedbackMessage,name="student_feedback_message"),
    path('admin/student_contact_message', StudentContactUs,name="student_contact_message"),
    path('admin/admin_notification_student', NotificationStudent,name="admin_notification_student"),

    #Student
    path('',StudentHome,name="student_home"),
    path('student/student_profile',StudentProfile,name="student_profile"),
    path('student/about',About,name="about"),
    path('student/contact',Contact,name="contact"),
    path('student/courseshow',CourseShow,name='courseshow'),
    path('student/moduleshow/',ModuleShow,name='moduleshow')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
