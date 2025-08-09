from django.contrib import admin
from .models import Category, Job, Application


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "location", "job_type", "category", "posted_by", "created_at")
    list_filter = ("job_type", "category", "location")
    search_fields = ("title", "company", "location")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "candidate", "created_at")
    search_fields = ("job__title", "candidate__username")
