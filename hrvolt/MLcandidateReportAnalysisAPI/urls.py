from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('MLcandidateReportGeneration', views.MLcandidateReportGenerationAPI.as_view(), name="MLcandidateReportGenerationPage"),
    # path('MLCandidateEducationPrediction', views.MLCandidateEducationPredictionAPI.as_view(), name="MLCandidateEducationPredictionPage"),
    # path('MLCandidateExperiencePrediction', views.MLCandidateExperiencePredictionAPI.as_view(), name="MLCandidateExperiencePredictionPage"),
    # path('MLCandidateTechnicalPrediction', views.MLCandidateTechnicalPredictionAPI.as_view(), name="MLCandidateTechnicalPredictionPage"),
    # path('MLCandidateSoftSkillPrediction', views.MLCandidateSoftSkillPredictionAPI.as_view(), name="MLCandidateSoftSkillPredictionPage"),
    # path('MLCandidateCurricularActPrediction', views.MLCandidateCurricularActPredictionAPI.as_view(), name="MLCandidateCurricularActPredictionPage"),
    # path('MLProjectPrediction', views.MLProjectPredictionAPI.as_view(), name="MLProjectPredictionPage"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)