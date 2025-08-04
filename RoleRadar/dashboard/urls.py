from django.urls import path
from dashboard import views

# app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('key-skills/', views.key_skills, name='key_skills'),
    path('resume/<int:id>/', views.resume_detail, name='resume_detail'),
    path('resume-analysis/<int:id>/delete/', views.delete_resume_analysis_view, name='delete_resume_analysis'),
    path('resume-analysis/<int:id>/pdf/', views.download_resume_analysis_pdf, name='resume_pdf'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('resume/', views.resume, name='resume'),
    path('advice/', views.advice, name='advice'),
    path('resume-summerize/', views.resume_summerize, name='resume_summerize'),
    path('resume/download/pdf/', views.download_generated_resume_pdf, name='download_generated_resume_pdf'),
    path('resume/download/word/', views.download_generated_resume_word, name='download_generated_resume_word'),
]
