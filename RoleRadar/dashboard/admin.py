from django.contrib import admin

# Register your models here.
from dashboard.models import ResumeAnalysis


class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'top_job', 'created_at')
    list_filter = ('user', 'created_at', 'top_job')
    search_fields = ('user__username', 'resume_text', 'top_job', 'suggestion')
    readonly_fields = ('created_at',)


admin.site.register(ResumeAnalysis, ResumeAnalysisAdmin)
