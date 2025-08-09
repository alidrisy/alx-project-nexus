from django.shortcuts import render
from django.db import models
from rest_framework import viewsets, permissions, decorators, response, status
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Job, Application
from .serializers import CategorySerializer, JobSerializer, ApplicationSerializer
from accounts.permissions import IsAdmin, IsRecruiterOrAdmin, IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.AllowAny()]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related('category', 'posted_by')
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'job_type', 'location']
    search_fields = ['title', 'description', 'company', 'location']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [IsRecruiterOrAdmin()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        job = self.get_object()
        if request.user == job.posted_by:
            raise PermissionDenied('You cannot apply to your own job.')
        data = {"job": job.id, "candidate": request.user.id, **request.data}
        serializer = ApplicationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=request.user, job=job)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'ADMIN':
            return Application.objects.select_related('job', 'candidate')
        # Non-admins: see only own applications or applications to own jobs
        return Application.objects.select_related('job', 'candidate').filter(
            models.Q(candidate=user) | models.Q(job__posted_by=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticated()]
