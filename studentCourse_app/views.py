from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from studentCourse_app.serializers import StudentSignupSerializer
from studentCourse_app.serializers import LoginSerializer
from studentCourse_app.serializers import AdminStudentSerializer
from studentCourse_app.serializers import CoursesSerializer
from studentCourse_app.serializers import ModuleSerializer
from rest_framework.permissions import IsAuthenticated
from studentCourse_app.models import CustomUser,Student,Admin,FeedBackStudent,ContactMessage,Notification,Registration
from studentCourse_app.models import Courses,Module
from django.shortcuts import get_object_or_404
from django.http import Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import AdminSerializer, StudentSerializer,FeedBackStudentSerializer,NotificationSerializer,ContactMessageSerializer,RegistrationSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class StudentSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StudentSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)  
            if hasattr(user, 'admin'):
                user_role = 'admin'
            elif hasattr(user, 'student'):
                user_role = 'student'
                
            return Response({"token": token.key,"user_role": user_role}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "No active token found."}, status=status.HTTP_400_BAD_REQUEST)


class AdminAddStudentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AdminStudentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Successfully Added Student"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Failed to Add Student: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStudentView(APIView):
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = AdminStudentSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateStudentView(APIView):
    def put(self, request, student_id, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=student_id)
        serializer = AdminStudentSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteStudentView(APIView):
    def delete(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, custom_user=student_id)
        serializer = AdminStudentSerializer()
        serializer.delete(student)
        return Response({"message": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class CoursesAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            course = get_object_or_404(Courses, pk=pk)
            serializer = CoursesSerializer(course)
            return Response({"message": "Course retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            courses = Courses.objects.all()
            serializer = CoursesSerializer(courses, many=True)
            return Response({"message": "Courses retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create course.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        course = get_object_or_404(Courses, pk=pk)
        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to update course.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Courses, pk=pk)
        course.delete()
        return Response({"message": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ModuleAPIView(APIView):
    def get(self, request):
        course_id = request.query_params.get('course_id') 
        
        if course_id:
            modules = Module.objects.filter(course=course_id)
            if not modules.exists():
                return Response({"message": "No modules found for the given course ID."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ModuleSerializer(modules, many=True)
            return Response({"message": "Modules retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            modules = Module.objects.all()
            if not modules.exists():
                return Response({"message": "No modules found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ModuleSerializer(modules, many=True)
            return Response({"message": "Modules retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Module created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create module.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        module = get_object_or_404(Module, pk=pk)
        serializer = ModuleSerializer(module, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Module updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to update module.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        module = get_object_or_404(Module, pk=pk)
        module.delete()
        return Response({"message": "Module deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']  
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '1':  # Admin
            try:
                admin = Admin.objects.get(custom_user=user)
                serializer = AdminSerializer(admin)
                message = "Admin profile retrieved successfully."
            except Admin.DoesNotExist:
                return Response({"error": "Admin profile not found."}, status=status.HTTP_404_NOT_FOUND)
        elif user.user_type == '2':  # Student
            try:
                student = Student.objects.get(custom_user=user)
                serializer = StudentSerializer(student)
                message = "Student profile retrieved successfully."
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        profile_pic = request.FILES.get('profile_pic', None)

        if user.user_type == '1':  # Admin
            try:
                admin = Admin.objects.get(custom_user=user)
                if profile_pic:
                    admin.profile_pic = profile_pic
                serializer = AdminSerializer(admin, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    message = "Admin profile updated successfully."
                    return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid data.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Admin.DoesNotExist:
                return Response({"error": "Admin profile not found."}, status=status.HTTP_404_NOT_FOUND)

        elif user.user_type == '2':  # Student
            try:
                student = Student.objects.get(custom_user=user)
                if profile_pic:
                    student.profile_pic = profile_pic
                serializer = StudentSerializer(student, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    message = "Student profile updated successfully."
                    return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid data.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

class FeedBackStudentListView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '1':  # Admin
            feedback = FeedBackStudent.objects.all()
        elif user.user_type == '2':  # Student
            feedback = FeedBackStudent.objects.filter(student_id=user.student.id)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FeedBackStudentSerializer(feedback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '2':  # Student
            data = request.data.copy()
            data['student_id'] = user.student.id  # Automatically set the student_id
            serializer = FeedBackStudentSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # student_id is already set in the data
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Only students can create feedback."}, status=status.HTTP_403_FORBIDDEN)

class FeedBackStudentDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            feedback = FeedBackStudent.objects.get(pk=pk)
            if user.user_type == '1' or feedback.student_id == user.student:
                serializer = FeedBackStudentSerializer(feedback)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except FeedBackStudent.DoesNotExist:
            return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            feedback = FeedBackStudent.objects.get(pk=pk)
            if user.user_type == '1' or feedback.student_id == user.student:
                serializer = FeedBackStudentSerializer(feedback, data=request.data, context={'request': request},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except FeedBackStudent.DoesNotExist:
            return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

class FeedBackStudentReplyView(APIView):
    def put(self, request, pk, *args, **kwargs):
        user = request.user
        print(user)
        if user.user_type == '1':  # Admin
            try:
                feedback = FeedBackStudent.objects.get(pk=pk)
                serializer = FeedBackStudentSerializer(feedback, data=request.data, partial=True,context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except FeedBackStudent.DoesNotExist:
                return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Only admins can reply to feedback."}, status=status.HTTP_403_FORBIDDEN)
    

class NotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '1':  # Admin
            notifications = Notification.objects.all()
        elif user.user_type == '2':  # Student
            notifications = Notification.objects.filter(student_id=user.student.id)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '1':  # Admin
            student_ids = request.data.get('student_ids')
            message = request.data.get('message')

            if student_ids:
                # Sending notifications to specific students
                students = Student.objects.filter(id__in=student_ids)
                for student in students:
                    Notification.objects.create(student_id=student, message=message)
                return Response({"message": "Notifications sent to specified students."}, status=status.HTTP_201_CREATED)
            else:
                # Sending notification to all students
                students = Student.objects.all()
                for student in students:
                    Notification.objects.create(student_id=student, message=message)
                return Response({"message": "Notification sent to all students."}, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Only admins can create notifications."}, status=status.HTTP_403_FORBIDDEN)

class NotificationDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            notification = Notification.objects.get(pk=pk)
            if user.user_type == '1' or notification.student_id == user.student:
                serializer = NotificationSerializer(notification)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ContactMessageListView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '1':  # Admin
            messages = ContactMessage.objects.all()
        elif user.user_type == '2':  # Student
            messages = ContactMessage.objects.filter(student=user.student)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == '2':  # Student
            serializer = ContactMessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(student=user.student)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Only students can create contact messages."}, status=status.HTTP_403_FORBIDDEN)

class ContactMessageDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            message = ContactMessage.objects.get(pk=pk)
            if user.user_type == '1':
                serializer = ContactMessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Contact message not found."}, status=status.HTTP_404_NOT_FOUND)
        

class RegistrationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_type == '1':  # Admin
            registrations = Registration.objects.all()
        elif user.user_type == '2':  # Student
            try:
                student = Student.objects.get(custom_user=user)
                registrations = Registration.objects.filter(student=student)
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.user_type == '2':  # Student
            try:
                student = Student.objects.get(custom_user=user)
                request.data['student'] = student.id  # Automatically assign the logged-in student's ID
                serializer = RegistrationSerializer(data=request.data)
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        elif user.user_type == '1':  # Admin
            serializer = RegistrationSerializer(data=request.data)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegistrationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            if user.user_type == '1':  # Admin
                return Registration.objects.get(pk=pk)
            elif user.user_type == '2':  # Student
                student = Student.objects.get(custom_user=user)
                return Registration.objects.get(pk=pk, student=student)
            else:
                raise Http404
        except Registration.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        registration = self.get_object(pk, user)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)


class RegistrationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_by_module(self, module_id, user):
        try:
            if user.user_type == '1':  # Admin
                return Registration.objects.get(module=module_id)
            elif user.user_type == '2':  # Student
                student = Student.objects.get(custom_user=user)
                return Registration.objects.get(module=module_id, student=student)
            else:
                raise Http404
        except Registration.DoesNotExist:
            raise Http404

    def delete(self, request, module_id, *args, **kwargs):
        user = request.user
        registration = self.get_object_by_module(module_id, user)

        if user.user_type == '1':  # Admin can delete any registration
            registration.delete()
        elif user.user_type == '2':  # Student can only delete their own registration
            try:
                student = Student.objects.get(custom_user=user)
                if registration.student != student:
                    return Response({"error": "You can only delete your own registrations."}, status=status.HTTP_403_FORBIDDEN)
                registration.delete()
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_type_check(request):
    user = request.user
    response_data = {
        "is_superuser": user.is_superuser,
        "is_admin": user.user_type == "1",  # Assuming user_type 1 is Admin
        "is_student": user.user_type == "2"  # Assuming user_type 2 is Student
    }
    return Response(response_data, status=status.HTTP_200_OK)