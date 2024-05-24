from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('ProjectCountPerUser',views.ProjectCountPerUserAPI.as_view() , name="ProjectCountPerUserPage"),
    path('TotalUniqueEducation',views.TotalUniqueEducationAPI.as_view() , name="TotalUniqueEducationPage"),
    path('TotalEducation',views.TotalEducationAPI.as_view() , name="TotalEducationPage"),
    path('TotalDegree',views.TotalDegreeAPI.as_view() , name="TotalDegreePage"),
    path('TotalEducationField',views.TotalEducationFieldAPI.as_view() , name="TotalEducationFieldPage"),
    path('TotalUniversity',views.TotalUniversityAPI.as_view() , name="TotalUniversityPage"),
    path('TotalWorkPlacePreference',views.TotalWorkPlacePreferenceAPI.as_view() , name="TotalWorkPlacePreferencePage"),
    path('TotalTechSkillPreference',views.TotalTechSkillPreferenceAPI.as_view() , name="TotalTechSkillPreferencePage"),
    path('TotalSoftSkillPreference',views.TotalSoftSkillPreferenceAPI.as_view() , name="TotalSoftSkillPreferencePage"),
    path('TotalLanguage',views.TotalLanguageAPI.as_view() , name="TotalLanguagePage"),
    path('EmployTypePref',views.EmployTypePrefAPI.as_view() , name="EmployTypePrefPage"),
    path('Nationality',views.NationalityAPI.as_view() , name="NationalityPage"),
    path('JobPositionPrefer',views.JobPositionPreferAPI.as_view() , name="JobPositionPreferPage"),
    path('TotalJobPosition',views.TotalJobPositionAPI.as_view() , name="TotalJobPositionPage"),
    path('JobLevelPrefer',views.JobLevelPreferAPI.as_view() , name="JobLevelPreferPage"),
    path('TotalJobLevel',views.TotalJobLevelAPI.as_view() , name="TotalJobLevelPage"),
    path('EducationbyJobLevel',views.EducationbyJobLevelAPI.as_view() , name="EducationbyJobLevelPage"),
    path('EducationbyJobPosition',views.EducationbyJobPositionAPI.as_view() , name="EducationbyJobPositionPage"),
    path('EducationFieldbyJobLevel',views.EducationFieldbyJobLevelAPI.as_view() , name="EducationFieldbyJobLevelPage"),
    path('EducationFieldbyJobPosition',views.EducationFieldbyJobPositionAPI.as_view() , name="EducationFieldbyJobPositionPage"),
    path('EducationDashboard',views.EducationDashboardAPI.as_view() , name="EducationDashboardPage"),
    path('EducationFieldDashboard',views.EducationFieldDashboardAPI.as_view() , name="EducationFieldDashboardPage"),
    path('MainEducationDashboard',views.MainEducationDashboardAPI.as_view() , name="MainEducationDashboardPage"),
    path('TechnicalSkillDashboard',views.TechnicalSkillDashboardAPI.as_view() , name="TechnicalSkillDashboardPage"),
    path('ProjectDurationDashboard',views.ProjectDurationDashboardAPI.as_view() , name="ProjectDurationDashboardPage"),
    path('ExperienceDurationDashboard',views.ExperienceDurationDashboardAPI.as_view() , name="ExperienceDurationDashboardPage"),
    path('JoiningPeriodDashboard',views.JoiningPeriodDashboardAPI.as_view() , name="JoiningPeriodDashboardPage"),
    path('WorkPlaceDashboard',views.WorkPlaceDashboardAPI.as_view() , name="WorkPlaceDashboardPage"),


    path('AllCandidateListBasedOnJobDescription',views.JobDescriptionCandidateListAPI.as_view() , name="AllCandidateListBasedOnJobDescriptionPage"),
    
    path('JobDescriptionTotalCandidateList',views.JobDescriptionTotalCandidateListAPI.as_view() , name="JobDescriptionTotalCandidateListAPIPage"),

    path('JobPositionOnTimeBasis',views.JobPositionOnTimeBasisAPI.as_view() , name="JobPositionOnTimeBasisPage"),
    path('JobPositionLevelLastSixMonths',views.JobPositionLevelLastSixMonthsAPI.as_view() , name="JobPositionLevelLastSixMonthsPage"),






] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)