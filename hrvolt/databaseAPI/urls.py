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
    path('sectorRegister',views.SectorAPI.as_view() , name="sectorPage"),
    path('sectorUpdate',views.SectorUpdateAPI.as_view() , name="sectorUpdatePage"),
    path('sectorGet',views.SectorGetAPI.as_view() , name="sectorGetPage"),
    path('sectorGetOne',views.SectorGetOneAPI.as_view() , name="sectorGetOnePage"),
    path('sectorGetAction',views.SectorGetActionAPI.as_view() , name="sectorGetActionPage"),
    path('sectorDelete',views.SectorDeleteAPI.as_view() , name="sectorDeletePage"),
    path('SectorGetBySearch',views.SectorGetBySearchAPI.as_view() , name="SectorGetBySearchPage"),

    path('jobPositionRegister',views.JobPositionAPI.as_view() , name="jobPositionRegisterPage"),
    path('jobPositionUpdate',views.JobPositionUpdateAPI.as_view() , name="jobPositionUpdatePage"),
    path('jobPositionGet',views.JobPositionGetAPI.as_view() , name="jobPositionGetPage"),
    path('jobPositionGetOne',views.JobPositionGetOneAPI.as_view() , name="jobPositionGetOnePage"),
    path('jobPositionGetSector',views.JobPositionGetSectorAPI.as_view() , name="jobPositionGetSectorPage"),
    path('jobPositionDelete',views.JobPositionDeleteAPI.as_view() , name="jobPositionDeletePage"),
    path('JobPositionGetBySearch',views.JobPositionGetBySearchAPI.as_view() , name="JobPositionGetBySearchPage"),

    path('jobLevelRegister',views.JobLevelAPI.as_view() , name="jobLevelRegisterPage"),
    path('jobLevelUpdate',views.JobLevelUpdateAPI.as_view() , name="jobLevelUpdatePage"),
    path('jobLevelGet',views.JobLevelGetAPI.as_view() , name="jobLevelGetPage"),
    path('jobLevelGetOne',views.JobLevelGetOneAPI.as_view() , name="jobLevelGetOnePage"),
    path('jobLevelGetAction',views.JobLevelGetActionAPI.as_view() , name="jobLevelGetActionPage"),
    path('jobLevelDelete',views.JobLevelDeleteAPI.as_view() , name="jobLevelDeletePage"),
    path('JobLevelGetBySearch',views.JobLevelGetBySearchAPI.as_view() , name="JobLevelGetBySearchPage"),

    path('locationRegister',views.LocationAPI.as_view() , name="locationRegisterPage"),
    path('locationUpdate',views.LocationUpdateAPI.as_view() , name="locationUpdatePage"),
    path('locationGet',views.LocationGetAPI.as_view() , name="locationGetPage"),
    path('locationGetOne',views.LocationGetOneAPI.as_view() , name="locationGetOnePage"),
    path('locationGetAction',views.LocationGetActionAPI.as_view() , name="locationGetActionPage"),
    path('locationDelete',views.LocationDeleteAPI.as_view() , name="locationDeletePage"),
    path('LocationGetBySearch',views.LocationGetBySearchAPI.as_view() , name="LocationGetBySearchPage"),

    path('companyTypeRegister',views.CompanyTypeAPI.as_view() , name="companyTypeRegisterPage"),
    path('companyTypeUpdate',views.CompanyTypeUpdateAPI.as_view() , name="companyTypeUpdatePage"),
    path('companyTypeGet',views.CompanyTypeGetAPI.as_view() , name="companyTypeGetPage"),
    path('companyTypeGetOne',views.CompanyTypeGetOneAPI.as_view() , name="companyTypeGetOnePage"),
    path('companyTypeGetAction',views.CompanyTypeGetActionAPI.as_view() , name="companyTypeGetActionPage"),
    path('companyTypeDelete',views.CompanyTypeDeleteAPI.as_view() , name="companyTypeDeletePage"),
    path('CompanyTypeGetBySearch',views.CompanyTypeGetBySearchAPI.as_view() , name="CompanyTypeGetBySearchPage"),

    path('workPlaceRegister',views.WorkPlaceAPI.as_view() , name="workPlaceRegisterPage"),
    path('workPlaceGet',views.WorkPlaceGetAPI.as_view() , name="workPlaceGetPage"),
    path('workPlaceGetOne',views.WorkPlaceGetOneAPI.as_view() , name="workPlaceGetOnePage"),
    path('workPlaceUpdate',views.WorkPlaceUpdateAPI.as_view() , name="workPlaceUpdatePage"),
    path('workPlaceGetAction',views.WorkPlaceGetActionAPI.as_view() , name="workPlaceGetActionPage"),
    path('workPlaceDelete',views.WorkPlaceDeleteAPI.as_view() , name="workPlaceDeletePage"),
    path('WorkPlaceGetBySearch',views.WorkPlaceGetBySearchAPI.as_view() , name="WorkPlaceGetBySearchPage"),

    path('employmentTypeRegister',views.EmploymentTypeAPI.as_view() , name="employmentTypeRegisterPage"),
    path('employmentTypeUpdate',views.EmploymentTypeUpdateAPI.as_view() , name="employmentTypeUpdatePage"),
    path('employmentTypeGet',views.EmploymentTypeGetAPI.as_view() , name="employmentTypeGetPage"),
    path('employmentTypeGetOne',views.EmploymentTypeGetOneAPI.as_view() , name="employmentTypeGetOnePage"),
    path('employmentTypeGetAction',views.EmploymentTypeActionAPI.as_view() , name="employmentTypeGetActionPage"),
    path('employmentTypeDelete',views.EmploymentTypeDeleteAPI.as_view() , name="employmentTypeDeletePage"),
    path('EmploymentTypeGetBySearch',views.EmploymentTypeGetBySearchAPI.as_view() , name="EmploymentTypeGetBySearchPage"),

    path('joiningPeriodRegister',views.JoiningPeriodAPI.as_view() , name="joiningPeriodRegisterPage"),
    path('joiningPeriodGet',views.JoiningPeriodGetAPI.as_view() , name="joiningPeriodGetPage"),
    path('joiningPeriodGetOne',views.JoiningPeriodGetOneAPI.as_view() , name="joiningPeriodGetOnePage"),
    path('joiningPeriodUpdate',views.JoiningPeriodUpdateAPI.as_view() , name="joiningPeriodUpdatePage"), 
    path('joiningPeriodGetAction',views.JoiningPeriodGetActionAPI.as_view() , name="joiningPeriodGetActionPage"),
    path('joiningPeriodDelete',views.JoiningPeriodDeleteAPI.as_view() , name="joiningPeriodDeletePage"),
    path('JoiningPeriodGetBySearch',views.JoiningPeriodGetBySearchAPI.as_view() , name="JoiningPeriodGetBySearchPage"),

    path('technicalSkillsRegister',views.TechnicalSkillsAPI.as_view() , name="technicalSkillsRegisterPage"),
    path('technicalSkillsUpdate',views.TechnicalSkillsUpdateAPI.as_view() , name="technicalSkillsUpdatePage"),
    path('technicalSkillsGet',views.TechnicalSkillsGetAPI.as_view() , name="technicalSkillsGetPage"),
    path('technicalSkillsGetOne',views.TechnicalSkillsGetOneAPI.as_view() , name="technicalSkillsGetOnePage"),
    path('technicalSkillsGetfromJobPosition',views.TechnicalSkillsGetfromJobPositionAPI.as_view() , name="technicalSkillsGetfromJobPositionPage"),
    path('technicalSkillsGetfromJobLevel',views.TechnicalSkillsGetfromJobLevelAPI.as_view() , name="technicalSkillsGetfromJobLevelPage"),
    path('technicalSkillsGetfromJobPositionJobLevel',views.TechnicalSkillsGetfromJobPositionJobLevelAPI.as_view() , name="technicalSkillsGetfromJobPositionJobLevelPage"),
    path('technicalSkillsDelete',views.TechnicalSkillsDeleteAPI.as_view() , name="technicalSkillsDeletePage"),
    path('technicalSkillsGetUnique',views.TechnicalSkillsGetUniqueAPI.as_view() , name="technicalSkillsGetUniquePage"),

    path('uniquetechnicalSkillsRegister',views.UniqueTechnicalSkillsAPI.as_view() , name="uniquetechnicalSkillsRegisterPage"),
    path('UniqueTechnicalSkillsUpdate',views.UniqueTechnicalSkillsUpdateAPI.as_view() , name="UniqueTechnicalSkillsUpdatePage"),
    path('UniqueTechnicalSkillsGet',views.UniqueTechnicalSkillsGetAPI.as_view() , name="UniqueTechnicalSkillsGetPage"),
    path('UniqueTechnicalSkillsDelete',views.UniqueTechnicalSkillsDeleteAPI.as_view() , name="UniqueTechnicalSkillsDeletePage"),
    path('UniqueTechnicalSkillsGetOne',views.UniqueTechnicalSkillsGetOneAPI.as_view() , name="UniqueTechnicalSkillsGetOnePage"),
    path('UniqueTechnicalSkillsGetOneByName',views.UniqueTechnicalSkillsGetOneByNameAPI.as_view() , name="UniqueTechnicalSkillsGetOneByNamePage"),
    path('UniqueTechnicalSkillsGetBySearch',views.UniqueTechnicalSkillsGetBySearchAPI.as_view() , name="UniqueTechnicalSkillsGetBySearchPage"),


    path('MainTechnicalSkillsRegister',views.MainTechnicalSkillsAPI.as_view() , name="MainTechnicalSkillsRegisterPage"),
    path('MainTechnicalSkillsGet',views.MainTechnicalSkillsGetAPI.as_view() , name="MainTechnicalSkillsGetPage"),
    path('MainTechnicalSkillsGetOne',views.MainTechnicalSkillsGetOneAPI.as_view() , name="MainTechnicalSkillsGetOnePage"),
    path('MainTechnicalSkillsGetfromJobPosition',views.MainTechnicalSkillsGetfromJobPositionAPI.as_view() , name="MainTechnicalSkillsGetfromJobPositionPage"),
    path('MainTechnicalSkillsGetfromJobLevel',views.MainTechnicalSkillsGetfromJobLevelAPI.as_view() , name="MainTechnicalSkillsGetfromJobLevelPage"),
    path('MainTechnicalSkillsGetfromJobPositionJobLevel',views.MainTechnicalSkillsGetfromJobPositionJobLevelAPI.as_view() , name="MainTechnicalSkillsGetfromJobPositionJobLevelPage"),
    path('MainTechnicalSkillsUpdate',views.MainTechnicalSkillsUpdateAPI.as_view() , name="MainTechnicalSkillsUpdatePage"),
    path('MainTechnicalSkillsDelete',views.MainTechnicalSkillsDeleteAPI.as_view() , name="MainTechnicalSkillsDeletePage"),
    path('MainTechnicalSkillsGetBySearch',views.MainTechnicalSkillsGetBySearchAPI.as_view() , name="MainTechnicalSkillsGetBySearchPage"),


    path('havetotechnicalSkillsRegister',views.HaveToTechnicalSkillsAPI.as_view() , name="havetotechnicalSkillsRegisterPage"),
    path('havetotechnicalSkillsGetfromJobLevel',views.HaveToTechnicalSkillsGetfromJobLevelAPI.as_view() , name="havetotechnicalSkillsGetfromJobLevelPage"),
    path('havetotechnicalSkillsGet',views.HaveToTechnicalSkillsGetAPI.as_view() , name="havetotechnicalSkillsGetPage"),
    path('havetotechnicalSkillsGetOne',views.HaveToTechnicalSkillsGetOneAPI.as_view() , name="havetotechnicalSkillsGetOnePage"),
    path('havetotechnicalSkillsGetfromJobPosition',views.HaveToTechnicalSkillsGetfromJobPositionAPI.as_view() , name="havetotechnicalSkillsGetfromJobPositionPage"),
    path('havetotechnicalSkillsGetfromJobPositionJobLevel',views.HaveToTechnicalSkillsGetfromJobPositionJobLevelAPI.as_view() , name="havetotechnicalSkillsGetfromJobPositionJobLevelPage"),
    path('havetotechnicalSkillsDelete',views.HaveToTechnicalSkillsDeleteAPI.as_view() , name="havetotechnicalSkillsDeletePage"),
    path('havetoOptionaltechnicalSkills',views.HaveToOptionalTechnicalSkillsAPI.as_view() , name="havetoOptionaltechnicalSkillsPage"),

    path('optionaltechnicalSkillsRegister',views.OptionalTechnicalSkillsAPI.as_view() , name="optionaltechnicalSkillsRegisterPage"),
    path('optionaltechnicalSkillsGetfromJobLevel',views.OptionalTechnicalSkillsGetfromJobLevelAPI.as_view() , name="optionaltechnicalSkillsGetfromJobLevelPage"),
    path('optionaltechnicalSkillsGet',views.OptionalTechnicalSkillsGetAPI.as_view() , name="optionaltechnicalSkillsGetPage"),
    path('optionaltechnicalSkillsGetOne',views.OptionalTechnicalSkillsGetOneAPI.as_view() , name="optionaltechnicalSkillsGetOnePage"),
    path('optionaltechnicalSkillsGetfromJobPosition',views.OptionalTechnicalSkillsGetfromJobPositionAPI.as_view() , name="optionaltechnicalSkillsGetfromJobPositionPage"),
    path('optionaltechnicalSkillsGetfromJobPositionJobLevel',views.OptionalTechnicalSkillsGetfromJobPositionJobLevelAPI.as_view() , name="optionaltechnicalSkillsGetfromJobPositionJobLevelPage"),
    path('optionaltechnicalSkillsDelete',views.OptionalTechnicalSkillsDeleteAPI.as_view() , name="optionaltechnicalSkillsDeletePage"),
    path('OptionalHaveTotechnicalSkillsDelete',views.OptionalHaveToTechnicalSkillsAPI.as_view() , name="OptionalHaveTotechnicalSkillsDeletePage"),
    
    path('softSkillsRegister',views.SoftSkillsAPI.as_view() , name="softSkillsRegisterPage"),
    path('softSkillsUpdate',views.SoftSkillsUpdateAPI.as_view() , name="softSkillsUpdatePage"),
    path('softSkillsGet',views.SoftSkillsGetAPI.as_view() , name="softSkillsGetPage"),
    path('softSkillsGetOne',views.SoftSkillsGetOneAPI.as_view() , name="softSkillsGetOnePage"),
    path('softSkillsGetAction',views.SoftSkillsGetActionAPI.as_view() , name="softSkillsGetActionPage"),
    path('softSkillsDelete',views.SoftSkillsDeleteAPI.as_view() , name="softSkillsDeletePage"),
    path('SoftSkillsGetBySearch',views.SoftSkillsGetBySearchAPI.as_view() , name="SoftSkillsGetBySearchPage"),
    
    path('LanguageRegister',views.LanguageRegisterAPI.as_view() , name="LanguageRegisterPage"),
    path('LanguageUpdate',views.LanguageUpdateAPI.as_view() , name="LanguageUpdatePage"),
    path('LanguageGet',views.LanguageGetAPI.as_view() , name="LanguageGetAPIPage"),
    path('LanguageGetOne',views.LanguageGetOneAPI.as_view() , name="LanguageGetOnePage"),
    path('LanguageGetAction',views.LanguageGetActionAPI.as_view() , name="LanguageGetActionPage"),
    path('LanguageDelete',views.LanguageDeleteAPI.as_view() , name="LanguageDeletePage"),
    path('LanguageGetBySearch',views.LanguageGetBySearchAPI.as_view() , name="LanguageGetBySearchPage"),

    path('jobRequirementRegister',views.JobRequirementAPI.as_view() , name="jobRequirementRegisterPage"),
    path('jobRequirementUpdate',views.JobRequirementUpdateAPI.as_view() , name="jobRequirementUpdatePage"),
    path('jobRequirementGet',views.JobRequirementGetAPI.as_view() , name="jobRequirementGetPage"),
    path('jobRequirementGetOne',views.JobRequirementGetOneAPI.as_view() , name="jobRequirementGetOnePage"),
    # path('jobRequirementGetAction',views.jobRequirementGetActionAPI.as_view() , name="jobRequirementGetActionPage"),
    path('jobRequirementDelete',views.JobRequirementDeleteAPI.as_view() , name="jobRequirementDeletePage"),
    path('jobRequirementGetfromJobPosition',views.JobRequirementGetfromJobPositionAPI.as_view() , name="jobRequirementGetfromJobPositionPage"),
    path('jobRequirementGetfromJobPositionJobLevel',views.JobRequirementGetfromJobPositionJobLevelAPI.as_view() , name="jobRequirementGetfromJobPositionJobLevelPage"),
    path('JobRequirementGetBySearch',views.JobRequirementGetBySearchAPI.as_view() , name="JobRequirementGetBySearchPage"),
    

    path('jobBenefitRegister',views.JobBenefitAPI.as_view() , name="jobBenefitRegisterPage"),
    path('jobBenefitUpdate',views.JobBenefitUpdateAPI.as_view() , name="jobBenefitUpdatePage"),
    path('jobBenefitGet',views.JobBenefitGetAPI.as_view() , name="jobBenefitGetPage"),
    path('jobBenefitGetOne',views.JobBenefitGetOneAPI.as_view() , name="jobBenefitGetOnePage"),
    # path('jobBenefitGetAction',views.jobBenefitGetActionAPI.as_view() , name="jobBenefitGetActionPage"),
    path('jobBenefitDelete',views.JobBenefitDeleteAPI.as_view() , name="jobBenefitDeletePage"),
    path('jobBenefitGetfromJobPosition',views.JobBenefitGetfromJobPositionAPI.as_view() , name="jobBenefitGetfromJobPositionPage"),
    path('jobBenefitGetfromJobPositionJobLevel',views.JobBenefitGetfromJobPositionJobLevelAPI.as_view() , name="jobBenefitGetfromJobPositionJobLevelPage"),
    path('JobBenefitGetBySearch',views.JobBenefitGetBySearchAPI.as_view() , name="JobBenefitGetBySearchPage"),

    path('jobResponsibilityRegister',views.JobResponsibilityAPI.as_view() , name="jobResponsibilityRegisterPage"),
    path('jobResponsibilityUpdate',views.JobResponsibilityUpdateAPI.as_view() , name="jobResponsibilityUpdatePage"),
    path('jobResponsibilityGet',views.JobResponsibilityGetAPI.as_view() , name="jobResponsibilityGetPage"),
    path('jobResponsibilityGetOne',views.JobResponsibilityGetOneAPI.as_view() , name="jobResponsibilityGetOnePage"),
    path('jobResponsibilityDelete',views.JobResponsibilityDeleteAPI.as_view() , name="jobResponsibilityDeletePage"),
    path('jobResponsibilityGetfromJobPositionJobLevel',views.JobResponsibilityGetfromJobPositionJobLevelAPI.as_view() , name="jobResponsibilityGetfromJobPositionJobLevelPage"),
    path('jobResponsibilityGetfromJobPosition',views.JobResponsibilityGetfromJobPositionAPI.as_view() , name="jobResponsibilityGetfromJobPositionPage"),
    path('JobResponsibilityGetBySearch',views.JobResponsibilityGetBySearchAPI.as_view() , name="JobResponsibilityGetBySearchPage"),

    path('educationRegister', views.EducationAPI.as_view(), name="educationRegisterPage"),
    path('educationUpdate', views.EducationUpdateAPI.as_view(), name="educationUpdatePage"),
    path('educationGet', views.EducationGetAPI.as_view(), name="educationGetPage"),
    path('educationGetOne', views.EducationGetOneAPI.as_view(), name="educationGetOnePage"),
    path('educationDelete', views.EducationDeleteAPI.as_view(), name="educationDeletePage"),
    path('educationGetAction', views.EducationGetActionAPI.as_view(), name="educationGetActionPage"),
    path('EducationGetBySearch', views.EducationGetBySearchAPI.as_view(), name="EducationGetBySearchPage"),

    path('educationFieldRegister', views.EducationFieldAPI.as_view(), name="educationFieldRegisterPage"),
    path('educationFieldUpdate', views.EducationFieldUpdateAPI.as_view(), name="educationFieldUpdatePage"),
    path('educationFieldGet', views.EducationFieldGetAPI.as_view(), name="educationFieldGetPage"),
    path('educationFieldGetOne', views.EducationFieldGetOneAPI.as_view(), name="educationFieldGetOnePage"),
    path('educationFieldGetSector', views.EducationFieldGetSectorAPI.as_view(), name="educationFieldGetSectorPage"),
    path('educationFieldDelete', views.EducationFieldDeleteAPI.as_view(), name="educationFieldDeletePage"),
    path('EducationFieldGetBySearch', views.EducationFieldGetBySearchAPI.as_view(), name="EducationFieldGetBySearchPage"),

   
    path('nationalityRegister',views.NationalityRegisterAPI.as_view() , name="nationalityRegisterPage"),
    path('nationalityUpdate',views.NationalityUpdateAPI.as_view() , name="nationalityUpdatePage"),
    path('nationalityGet',views.NationalityGetAPI.as_view() , name="nationalityGetPage"),
    path('nationalityGetOne',views.NationalityGetOneAPI.as_view() , name="nationalityGetOnePage"),
    path('nationalityGetAction',views.NationalityGetActionAPI.as_view() , name="nationalityGetActionPage"),
    path('nationalityDelete',views.NationalityDeleteAPI.as_view() , name="nationalityDeletePage"),
    path('NationalityGetBySearch',views.NationalityGetBySearchAPI.as_view() , name="NationalityGetBySearchPage"),


    path('UniversityRegister',views.UniversityRegisterAPI.as_view() , name="UniversityRegisterPage"),
    path('UniversityGet',views.UniversityGetAPI.as_view() , name="UniversityGetPage"),
    path('UniversityGetBySearch',views.UniversityGetBySearchAPI.as_view() , name="UniversityGetBySearchPage"),

    path('DegreeRegister',views.DegreeRegisterAPI.as_view() , name="DegreeRegisterPage"),
    path('DegreeGet',views.DegreeGetAPI.as_view() , name="DegreeGetPage"),
    path('DegreeGetBySearch',views.DegreeGetBySearchAPI.as_view() , name="DegreeGetBySearchPage"),





] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
