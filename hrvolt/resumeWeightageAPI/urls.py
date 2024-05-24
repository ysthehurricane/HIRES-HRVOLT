from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('MainEducationWeightageRegister', views.MainEducationWeightageRegisterAPI.as_view(), name="MainEducationWeightageRegisterPage"),
    path('MainEducationWeightageUpdate', views.MainEducationWeightageUpdateAPI.as_view(), name="MainEducationWeightageUpdatePage"),
    path('MainEducationWeightageGet', views.MainEducationWeightageGetAPI.as_view(), name="MainEducationWeightageGetPage"),
    path('MainEducationWeightageDelete', views.MainEducationWeightageDeleteAPI.as_view(), name="MainEducationWeightageDeletePage"),

    path('EducationCategoriesWeightageRegister', views.EducationCategoriesWeightageRegisterAPI.as_view(), name="EducationCategoriesWeightageRegisterPage"),
    path('EducationCategoriesWeightageUpdate', views.EducationCategoriesWeightageUpdateAPI.as_view(), name="EducationCategoriesWeightageUpdatePage"),
    path('EducationCategoriesWeightageGet', views.EducationCategoriesWeightageGetAPI.as_view(), name="EducationCategoriesWeightageGetPage"),
    path('EducationCategoriesWeightageDelete', views.EducationCategoriesWeightageDeleteAPI.as_view(), name="EducationCategoriesWeightageDeletePage"),

    path('MainExperienceWeightageRegister', views.MainExperienceWeightageRegisterAPI.as_view(), name="MainExperienceWeightageRegisterPage"),
    path('MainExperienceWeightageUpdate', views.MainExperienceWeightageUpdateAPI.as_view(), name="MainExperienceWeightageUpdatePage"),
    path('MainExperienceWeightageGet', views.MainExperienceWeightageGetAPI.as_view(), name="MainExperienceWeightageGetPage"),
    path('MainExperienceWeightageDelete', views.MainExperienceWeightageDeleteAPI.as_view(), name="MainExperienceWeightageDeletePage"),

    path('TechnicalSkillWeightage', views.TechnicalSkillWeightageAPI.as_view(), name="TechnicalSkillWeightagePage"),
    path('MaintechnicalSkillWeightageUpdate', views.MaintechnicalSkillWeightageUpdateAPI.as_view(), name="MaintechnicalSkillWeightageUpdatePage"),
    path('MaintechnicalSkillWeightageGet', views.MaintechnicalSkillWeightageGetAPI.as_view(), name="MaintechnicalSkillWeightageGetPage"),
    path('MaintechnicalSkillWeightageDelete', views.MaintechnicalSkillWeightageDeleteAPI.as_view(), name="MaintechnicalSkillWeightageDeletePage"),

    path('SoftSkillWeightage', views.SoftSkillWeightageAPI.as_view(), name="SoftSkillWeightagePage"),
    path('MainSoftSkillWeightageUpdate', views.MainSoftSkillWeightageUpdateAPI.as_view(), name="MainSoftSkillWeightageUpdatePage"),
    path('MainSoftSkillWeightageGet', views.MainSoftSkillWeightageGetAPI.as_view(), name="MainSoftSkillWeightageGetPage"),
    path('MainSoftSkillWeightageDelete', views.MainSoftSkillWeightageDeleteAPI.as_view(), name="MainSoftSkillWeightageDeletePage"),

    path('CurricularActivitiesWeightage', views.CurricularActivitiesWeightageAPI.as_view(), name="CurricularActivitiesWeightagePage"),
    path('MainCurricularActivitiesWeightageUpdate', views.MainCurricularActivitiesWeightageUpdateAPI.as_view(), name="MainCurricularActivitiesWeightageUpdatePage"),
    path('MainCurricularActivitiesWeightageGet', views.MainCurricularActivitiesWeightageGetAPI.as_view(), name="MainCurricularActivitiesWeightageGetPage"),
    path('MainCurricularActivitiesWeightageDelete', views.MainCurricularActivitiesWeightageDeleteAPI.as_view(), name="MainCurricularActivitiesWeightageDeletePage"),

    path('AnyDropWeightage', views.AnyDropWeightageAPI.as_view(), name="AnyDropWeightagePage"),
    path('MainAnyDropWeightageUpdate', views.MainAnyDropWeightageUpdateAPI.as_view(), name="MainAnyDropWeightageUpdatePage"),
    path('MainAnyDropWeightageGet', views.MainAnyDropWeightageGetAPI.as_view(), name="MainAnyDropWeightageGetPage"),
    path('MainAnyDropWeightageDelete', views.MainAnyDropWeightageDeleteAPI.as_view(), name="MainAnyDropWeightageWeightageDeletePage"),

    path('ProjectWeightage', views.ProjectWeightageAPI.as_view(), name="ProjectWeightagePage"),
    path('MainProjectWeightageUpdate', views.MainProjectWeightageUpdateAPI.as_view(), name="MainProjectWeightageUpdatePage"),
    path('MainProjectWeightageGet', views.MainProjectWeightageGetAPI.as_view(), name="MainProjectWeightageGetPage"),
    path('MainProjectWeightageDelete', views.MainProjectWeightageDeleteAPI.as_view(), name="MainProjectWeightageDeletePage"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

