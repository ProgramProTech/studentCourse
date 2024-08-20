from django.shortcuts import render
from studentCourse_app.models import  Student


def LoginPage(request):
    return render(request,"login_page.html")

def SignupStudent(request):
    return render(request,"signup_student_page.html")

def AdminHome(request):
    return render(request, "admin_template/home_content.html")

def AdminProfile(request):
    return render(request,"admin_template/admin_profile.html")


def AddStudent(request):
    return render(request,"admin_template/add_student_template.html")

def AddCourse(request):
    return render(request,"admin_template/add_course_template.html")

def AddModule(request):
    return render(request,"admin_template/add_module_template.html")

def ManageStudent(request):
    return render(request,"admin_template/manage_student.html")

def ManageCourse(request):
    return render(request,"admin_template/manage_course.html")

def ManageModule(request):
    return render(request,"admin_template/manage_module.html")

def StudentFeedbackMessage(request):
    return render(request,"Admin_template/student_feedback.html")


def StudentContactUs(request):
    return render(request,"admin_template/student_contact_messages.html")

def NotificationStudent(request):
    students=Student.objects.all()
    return render(request,"Admin_template/student_notification.html",{"students":students})


def StudentHome(request):
    return render(request, "student_template/home_content.html")

def StudentProfile(request):
    return render(request, "student_template/student_profile.html") 


def About(request):
    return render(request, "student_template/about.html") 


def Contact(request):
    return render(request, "student_template/contact.html") 