from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('CandidateReportAnalysis', views.CandidateReportAnalysisAPI.as_view(), name="CandidateReportAnalysisPage"),
    path('candidateReportGeneration', views.candidateReportGenerationAPI.as_view(), name="candidateReportGenerationPage"),
    path('CandidateEducationPrediction', views.CandidateEducationPredictionAPI.as_view(), name="CandidateEducationPredictionPage"),
    path('CandidateExperiencePrediction', views.CandidateExperiencePredictionAPI.as_view(), name="CandidateExperiencePredictionPage"),
    path('CandidateSoftSkillPrediction', views.CandidateSoftSkillPredictionAPI.as_view(), name="CandidateSoftSkillPredictionPage"),
    path('CandidateTechnicalPrediction', views.CandidateTechnicalPredictionAPI.as_view(), name="CandidateTechnicalPredictionPage"),
    path('CandidateCurricularActivitiesPrediction', views.CandidateCurricularActivitiesPredictionAPI.as_view(), name="CandidateCurricularActivitiesPredictionPage"),
    path('AnyDropPrediction', views.AnyDropPredictionAPI.as_view(), name="AnyDropPredictionPage"),
    path('ProjectPrediction', views.ProjectPredictionAPI.as_view(), name="ProjectPredictionPage"),
    path('CandidateReportGet', views.CandidateReportGetAPI.as_view(), name="CandidateReportGetPage"),
    path('CandidateReportGetOne', views.CandidateReportGetOneAPI.as_view(), name="CandidateReportGetOnePage"),
    path('CandidateProfileScore', views.CandidateProfileScoreAPI.as_view(), name="CandidateProfileScorePage"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)