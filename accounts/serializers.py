from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'User Response',
            value={
                'id': 1,
                'username': 'john_doe',
                'email': 'john@example.com',
                'role': 'USER'
            }
        )
    ]
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = ["id", "role"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Regular User Registration',
            value={
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'securepassword123',
                'role': 'USER'
            }
        ),
        OpenApiExample(
            'Recruiter Registration',
            value={
                'username': 'recruiter_jane',
                'email': 'jane@company.com',
                'password': 'securepassword123',
                'role': 'RECRUITER'
            }
        )
    ]
)
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        help_text="Username must be unique and between 1-150 characters"
    )
    email = serializers.EmailField(
        required=False, 
        allow_blank=True,
        help_text="Email address (optional)"
    )
    password = serializers.CharField(
        write_only=True, 
        style={"input_type": "password"},
        help_text="Password must meet Django's password validation requirements"
    )
    role = serializers.ChoiceField(
        choices=[("USER", "User"), ("RECRUITER", "Recruiter")], 
        required=False,
        default="USER",
        help_text="User role: USER (default) or RECRUITER"
    )

    def validate_password(self, value: str) -> str:
        """Validate password using Django's password validation."""
        validate_password(value)
        return value

    def validate_username(self, value: str) -> str:
        """Check that username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

    def validate_email(self, value: str) -> str:
        """Check that email is unique if provided."""
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        """Create a new user with the specified role."""
        role = validated_data.get("role", "USER")
        
        # Ensure role is valid
        if role not in ("USER", "RECRUITER"):
            role = "USER"
        
        # Create user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        
        # Set role and activate user
        user.role = role
        user.is_active = True
        user.save()
        
        return user
 