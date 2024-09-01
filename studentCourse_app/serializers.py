from rest_framework import serializers
from django.contrib.auth import get_user_model
from studentCourse_app.models import Student,Module,Courses,Admin,Notification,FeedBackStudent,ContactMessage,Registration
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


CustomUser = get_user_model()


class StudentSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=2
        )
        # The Student profile is automatically created via the post_save signal.
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        if not username_or_email or not password:
            raise serializers.ValidationError("Must include both username or email and password")

        # First, try to authenticate with the username
        user = authenticate(username=username_or_email, password=password)

        if user is None:
            # If authentication with username fails, check if the provided username_or_email is an email
            try:
                # Attempt to get the user by email
                user = CustomUser.objects.get(email=username_or_email)
                # Now, manually check the password
                if not user.check_password(password):
                    user = None
            except CustomUser.DoesNotExist:
                user = None

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        # At this point, the user is authenticated
        data["user"] = user
        return data

class AdminStudentSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(required=False, allow_null=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'id','first_name', 'last_name', 'username', 'email', 'password',
            'gender', 'profile_pic', 'city', 'country', 'date_of_birth', 'address'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id':{'read_only' : True}
        }

    def create(self, validated_data):
        # Create the CustomUser
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=2
        )
        
        # Update the Student instance that was created via post_save signal
        student_data = {
            'gender': validated_data.get('gender'),
            'profile_pic': validated_data.get('profile_pic'),
            'address': validated_data.get('address'),
            'city': validated_data.get('city'),
            'country': validated_data.get('country'),
            'date_of_birth': validated_data.get('date_of_birth'),
        }

        student = Student.objects.get(custom_user=user)
        for attr, value in student_data.items():
            if value is not None:
                setattr(student, attr, value)
        student.save()

        return user
        
    def update(self, instance, validated_data):
        student_data = {
            'gender': validated_data.get('gender'),
            'profile_pic': validated_data.get('profile_pic'),
            'address': validated_data.get('address'),
            'city': validated_data.get('city'),
            'country': validated_data.get('country'),
            'date_of_birth': validated_data.get('date_of_birth'),
        }

        # Prevent updating email and username
        if 'email' in validated_data or 'username' in validated_data:
            raise serializers.ValidationError("Cannot update email or username.")

        for attr, value in validated_data.items():
            if attr in ['first_name', 'last_name', 'password']:
                setattr(instance, attr, value)
        instance.save()

        # Update the Student instance
        student = Student.objects.get(custom_user=instance)
        for attr, value in student_data.items():
            if value is not None:
                setattr(student, attr, value)
        student.save()

        return instance

    def delete(self, instance):
        custom_user = CustomUser.objects.get(id=instance.custom_user.id)
        custom_user.delete()  
        instance.delete()
    
   
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        student = Student.objects.filter(custom_user=instance).first()
        if student:
            representation.update({
                'gender': student.gender if student.gender else '',
                'profile_pic': student.profile_pic.url if student.profile_pic else None,
                'address': student.address if student.address else '',
                'city': student.city if student.city else '',
                'country': student.country if student.country else '',
                'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else None,
            })
        else:
            representation.update({
                'gender': '',
                'profile_pic': None,
                'address': '',
                'city': '',
                'country': '',
                'date_of_birth': None,
            })
        
        return representation



class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type']

        
class AdminSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='custom_user.first_name')
    last_name = serializers.CharField(source='custom_user.last_name')
    username = serializers.CharField(source='custom_user.username', read_only=True)
    email = serializers.EmailField(source='custom_user.email', read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Admin
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'created_at', 'updated_at', 'password'
        ]

    def update(self, instance, validated_data):
        custom_user_data = validated_data.pop('custom_user', {})
        custom_user = instance.custom_user

        # Update related CustomUser fields
        if 'first_name' in custom_user_data:
            custom_user.first_name = custom_user_data['first_name']
        if 'last_name' in custom_user_data:
            custom_user.last_name = custom_user_data['last_name']
        if 'password' in validated_data:
            custom_user.password = make_password(validated_data['password'])
        custom_user.save()

        # Update Admin fields
        return super().update(instance, validated_data)
    
class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='custom_user.first_name')
    last_name = serializers.CharField(source='custom_user.last_name')
    username = serializers.CharField(source='custom_user.username', read_only=True)
    email = serializers.EmailField(source='custom_user.email', read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Student
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'gender', 'profile_pic', 'city', 'country', 
            'date_of_birth', 'address', 'created_at', 'updated_at', 'password'
        ]

    def update(self, instance, validated_data):
        custom_user_data = validated_data.pop('custom_user', {})
        custom_user = instance.custom_user

        # Update related CustomUser fields
        if 'first_name' in custom_user_data:
            custom_user.first_name = custom_user_data['first_name']
        if 'last_name' in custom_user_data:
            custom_user.last_name = custom_user_data['last_name']
        if 'password' in validated_data:
            custom_user.password = make_password(validated_data['password'])
        custom_user.save()

        # Update Student fields
        return super().update(instance, validated_data)

    

class FeedBackStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = FeedBackStudent
        fields = ['id', 'student_id', 'student_name', 'feedback', 'feedback_reply', 'created_at', 'updated_at']
        extra_kwargs = {
            'feedback_reply': {'required': False}  
        }

    def get_student_name(self, obj):
        return f"{obj.student_id.custom_user.first_name} {obj.student_id.custom_user.last_name}"

    def validate(self, attrs):
        user = self.context['request'].user
        if user.user_type == '1':  # Admin
            if 'feedback_reply' not in attrs or not attrs['feedback_reply']:
                raise serializers.ValidationError({'feedback_reply': 'This field is required.'})
        return attrs
    

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'student_id', 'message', 'created_at', 'updated_at']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'student', 'module', 'registration_date']