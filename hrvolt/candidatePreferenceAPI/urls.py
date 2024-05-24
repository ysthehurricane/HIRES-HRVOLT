"""hrvolt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('candidatePreferenceRegister', views.CandidatePreferenceAPI.as_view(), name="candidatePreferenceRegisterPage"),
    path('candidatePreferenceUpdate', views.CandidatePreferenceUpdateAPI.as_view(), name="candidatePreferenceUpdatePage"),
    path('candidatePreferenceGet', views.CandidatePreferenceGetAPI.as_view(), name="candidatePreferenceGetPage"),
    path('candidatePreferenceGetOne', views.CandidatePreferenceGetOneAPI.as_view(), name="candidatePreferenceGetOnePage"),
    path('CandidatePreferenceDelete', views.CandidatePreferenceDeleteAPI.as_view(), name="CandidatePreferenceDeletePage"),

    path('candidateEmploymentTypePreferenceRegister', views.CandidateEmploymentTypePreferenceAPI.as_view(), name="candidateEmploymentTypePreferenceRegisterPage"),
    path('candidateEmploymentTypePreferenceGet', views.CandidateEmploymentTypePreferenceGetAPI.as_view(), name="candidateEmploymentTypePreferenceGetPage"),
    path('candidateEmploymentTypePreferenceGetOne', views.CandidateEmploymentTypePreferenceGetOneAPI.as_view(), name="candidateEmploymentTypePreferenceGetOnePage"),
    path('candidateEmploymentTypePreferenceDelete', views.CandidateEmploymentTypePreferenceDeleteAPI.as_view(), name="candidateEmploymentTypePreferenceDeletePage"),

    path('candidatePreferenceLocationRegister', views.CandidatePreferenceLocationAPI.as_view(), name="candidatePreferenceLocationRegisterPage"),
    path('candidatePreferenceLocationGet', views.CandidatePreferenceLocationGetAPI.as_view(), name="candidatePreferenceLocationGetPage"),
    path('candidatePreferenceLocationGetOne', views.CandidatePreferenceLocationGetOneAPI.as_view(), name="candidatePreferenceLocationGetOnePage"),
    path('candidatePreferenceLocationDelete', views.CandidatePreferenceLocationDeleteAPI.as_view(), name="candidatePreferenceLocationDeletePage"),

    path('candidateCompanyPreferenceRegister', views.CandidateCompanyPreferenceAPI.as_view(), name="candidateCompanyPreferenceRegisterPage"),
    path('candidateCompanyPreferenceGetOne', views.CandidateCompanyPreferenceGetOneAPI.as_view(), name="candidateCompanyPreferenceGetOnePage"),
    path('candidateCompanyPreferenceDelete', views.CandidateCompanyPreferenceDeleteAPI.as_view(), name="candidateCompanyPreferenceDeletePage"),
    
    path('candidateCompanySectorPreferenceRegister', views.CandidateCompanySectorPreferenceAPI.as_view(), name="candidateCompanySectorPreferenceRegisterPage"),
    path('candidateCompanySectorPreferenceGetOne', views.CandidateCompanySectorPreferenceGetOneAPI.as_view(), name="candidateCompanySectorPreferenceGetOnePage"),
    path('candidateCompanySectorPreferenceDelete', views.CandidateCompanySectorPreferenceDeleteAPI.as_view(), name="candidateCompanySectorPreferenceDeletePage"),

    path('candidateWorkPlacePreferenceRegister', views.CandidateWorkplacePreferenceAPI.as_view(), name="candidateWorkPlacePreferenceRegisterPage"),
    path('candidateWorkPlacePreferenceGetOne', views.CandidateWorkplacePreferenceGetOneAPI.as_view(), name="candidateWorkPlacePreferenceGetOnePage"),
    path('candidateWorkPlacePreferenceDelete', views.CandidateWorkplacePreferenceDeleteAPI.as_view(), name="candidateWorkPlacePreferenceDeletePage"),

    path('candidateJoiningPeriodPreferenceRegister', views.CandidateJoiningPeriodPreferenceAPI.as_view(), name="candidateJoiningPeriodPreferenceRegisterPage"),
    path('candidateJoiningPeriodPreferenceGetOne', views.CandidateJoiningPeriodPreferenceGetOneAPI.as_view(), name="candidateJoiningPeriodPreferenceGetOnePage"),
    path('candidateJoiningPeriodPreferenceDelete', views.CandidateJoiningPeriodPreferenceDeleteAPI.as_view(), name="candidateJoiningPeriodPreferenceDeletePage"),

    path('candidatePreferenceResetDelete', views.CandidatePreferenceResetDeleteAPI.as_view(), name="candidatePreferenceResetDeletePage"),

    path('CandidatePreferenceGetAll', views.CandidatePreferenceGetAllAPI.as_view(), name="CandidatePreferenceGetAllPage"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
