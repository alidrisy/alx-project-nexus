from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="jobs")
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posted_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} @ {self.company}"


class Application(models.Model):
    job = models.ForeignKey(Job, related_name="applications", on_delete=models.CASCADE)
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    resume = models.TextField()
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "candidate")

    def __str__(self) -> str:
        return f"Application by {self.candidate} for {self.job}"
