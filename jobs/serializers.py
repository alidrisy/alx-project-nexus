from rest_framework import serializers
from .models import Category, Job, Application


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Category.objects.all(), source='category'
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company', 'location', 'job_type',
            'category', 'category_id', 'posted_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['posted_by', 'created_at', 'updated_at']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job', 'candidate', 'resume', 'cover_letter', 'created_at']
        read_only_fields = ['candidate', 'created_at'] 