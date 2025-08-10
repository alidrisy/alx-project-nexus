from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
        read_only_fields = ["id", "role"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    role = serializers.ChoiceField(choices=[("USER", "User"), ("RECRUITER", "Recruiter")], required=False)

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

    def create(self, validated_data):
        role = validated_data.get("role") or "USER"
        if role not in ("USER", "RECRUITER"):
            role = "USER"
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        user.role = role
        user.is_active = True
        user.save()
        return user
 