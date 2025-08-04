from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_resume = models.TextField()
    top_job = models.CharField(max_length=255)
    job_summary = models.TextField()
    predictions = models.JSONField()
    keywords = models.JSONField(null=True, blank=True)
    strengths = models.TextField(null=True, blank=True)
    weaknesses = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.user.username} on {self.created_at}"

