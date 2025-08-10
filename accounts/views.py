from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    tags=['Authentication'],
    summary='User Registration',
    description='Register a new user account with either USER or RECRUITER role',
    request=RegisterSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            'Regular User Registration',
            value={
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'securepassword123',
                'role': 'USER'
            },
            description='Register a regular user account'
        ),
        OpenApiExample(
            'Recruiter Registration',
            value={
                'username': 'recruiter_jane',
                'email': 'jane@company.com',
                'password': 'securepassword123',
                'role': 'RECRUITER'
            },
            description='Register a recruiter account'
        )
    ]
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user account.
        
        Accepts username, email, password, and optional role.
        Role can be either 'USER' (default) or 'RECRUITER'.
        Returns user data and JWT tokens upon successful registration.
        """
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': 'Registration failed',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['User Management'],
    summary='Get/Update Current User',
    description='Retrieve or update the currently authenticated user profile',
    responses={
        200: UserSerializer,
        401: OpenApiTypes.OBJECT,
    }
)
class MeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Create your views here.
