from django.urls import path
from . import views

from  django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings

urlpatterns = [

    path('platformGenerateAuthToken', views.CustomTokenObtainPairView.as_view(), name='customTokenObtainPair'),

    path('UserLoggedInValidate', views.UserLoggedInValidateAPI.as_view(), name="UserLoggedInValidatePage"),
    path('UserLoggedOutUpdate', views.UserLoggedOutUpdateAPI.as_view(), name="UserLoggedOutUpdatePage"),
    path('JobDescriptionPlatform', views.JobDescriptionPlatformAPI.as_view(), name="JobDescriptionPlatformPage"),
    path('jobDescriptionUpdatePlatform',views.JobDescriptionUpdatePlatformAPI.as_view() , name="jobDescriptionUpdatePlatformPage"),
    path('jobDescriptionGetPlatform',views.JobDescriptionGetPlatformAPI.as_view() , name="jobDescriptionGetPlatformPage"),
    path('jobDescriptionGetOnePlatform',views.JobDescriptionGetOnePlatformAPI.as_view() , name="jobDescriptionGetOnePlatformPage"),
    path('jobDescriptionGetUserPlatform',views.JobDescriptionGetUserPlatformAPI.as_view() , name="jobDescriptionGetUserPlatformPage"),
    path('jobDescriptionGetfromJobPositionJobLevelPlatform',views.JobDescriptionGetfromJobPositionJobLevelPlatformAPI.as_view() , name="jobDescriptionGetfromJobPositionJobLevelPlatformPage"),
    path('jobDescriptionDeletePlatform',views.JobDescriptionDeletePlatformAPI.as_view() , name="jobDescriptionDeletePlatformPage"),    
    
    
    path('educationJobDescriptionRegisterPlatform',views.EducationJobDescriptionPlatformAPI.as_view() , name="educationJobDescriptionRegisterPlatformPage"),
    path('educationJobDescriptionGetPlatform',views.EducationJobDescriptionGetPlatformAPI.as_view() , name="educationJobDescriptionGetPlatformPage"),
    path('educationjobDescriptionGetOnePlatform',views.EducationJobDescriptionGetOnePlatformAPI.as_view() , name="educationjobDescriptionGetOnePlatformPage"),
    path('educationjobDescriptionDeletePlatform',views.EducationJobDescriptionDeletePlatformAPI.as_view() , name="educationjobDescriptionDeletePlatformPage"),  
    path('EducationJobDescriptionGetbyDescpPlatform',views.EducationJobDescriptionGetbyDescpPlatformAPI.as_view() , name="EducationJobDescriptionGetbyDescpPlatformPage"),


    path('educationFieldJobDescriptionRegisterPlatform',views.EducationFieldJobDescriptionPlatformAPI.as_view() , name="educationFieldJobDescriptionRegisterPlatformPage"),
    path('educationFieldJobDescriptionGetPlatform',views.EducationFieldJobDescriptionGetPlatformAPI.as_view() , name="educationFieldJobDescriptionGetPlatformPage"),
    path('educationFieldjobDescriptionGetOnePlatform',views.EducationFieldJobDescriptionGetOnePlatformAPI.as_view() , name="educationFieldjobDescriptionGetOnePlatformPage"),
    path('educationFieldjobDescriptionDeletePlatform',views.EducationFieldJobDescriptionDeletePlatformAPI.as_view() , name="educationFieldjobDescriptionDeletePlatformPage"),  
    path('EducationFieldJobDescriptionGetbyDescpPlatform',views.EducationFieldJobDescriptionGetbyDescpPlatformAPI.as_view() , name="EducationFieldJobDescriptionGetbyDescpPlatformPage"),

    path('softskillsJobDescriptionRegisterPlatform',views.SoftSkillsJobDescriptionPlatformAPI.as_view() , name="softskillsJobDescriptionRegisterPlatformPage"),
    path('softskillsJobDescriptionGetPlatform',views.SoftSkillsJobDescriptionGetPlatformAPI.as_view() , name="softskillsJobDescriptionGetPlatformPage"),
    path('softskillsjobDescriptionGetOnePlatform',views.SoftSkillsJobDescriptionGetOnePlatformAPI.as_view() , name="softskillsjobDescriptionGetOnePlatformPage"),
    path('softskillsjobDescriptionDeletePlatform',views.SoftSkillsJobDescriptionDeletePlatformAPI.as_view() , name="softskillsjobDescriptionDeletePlatformPage"),    
    path('SoftSkillsJobDescriptionGetbyDescpPlatform',views.SoftSkillsJobDescriptionGetbyDescpPlatformAPI.as_view() , name="SoftSkillsJobDescriptionGetbyDescpPlatformPage"),    
    
    
    path('technicalskillsJobDescriptionRegisterPlatform',views.TechnicalSkillsJobDescriptionPlatformAPI.as_view() , name="technicalskillsJobDescriptionRegisterPlatformPage"),
    path('technicalskillsJobDescriptionGetPlatform',views.TechnicalSkillsJobDescriptionGetPlatformAPI.as_view() , name="technicalskillsJobDescriptionGetPlatformPage"),
    path('technicalskillsjobDescriptionGetOnePlatform',views.TechnicalSkillsJobDescriptionGetOnePlatformAPI.as_view() , name="technicalskillsjobDescriptionGetOnePlatformPage"),
    path('technicalskillsjobDescriptionDeletePlatform',views.TechnicalSkillsJobDescriptionDeletePlatformAPI.as_view() , name="technicalskillsjobDescriptionDeletePlatformPage"),  
    path('TechnicalSkillsJobDescriptionGetbyDescpPlatform',views.TechnicalSkillsJobDescriptionGetbyDescpPlatformAPI.as_view() , name="TechnicalSkillsJobDescriptionGetbyDescpPlatformPage"),  
    
    
    path('customjobDescriptionResponsibilityRegisterPlatform',views.CustomJobDescriptionResponsibilityPlatformAPI.as_view() , name="customJobDescriptionResponsibilityRegisterPlatformPage"),
    path('customjobDescriptionResponsibilityGetPlatform',views.CustomJobDescriptionResponsibilityGetPlatformAPI.as_view() , name="customJobDescriptionResponsibilityGetPlatformPage"),
    path('customjobDescriptionResponsibilityGetOnePlatform',views.CustomJobDescriptionResponsibilityGetOnePlatformAPI.as_view() , name="customjobDescriptionResponsibilityGetOnePlatformPage"),
    path('customjobDescriptionResponsibilityGetfromUserJobDescriptionPlatform',views.CustomJobDescriptionResponsibilityGetfromUserJobDescriptionPlatformAPI.as_view() , name="customjobDescriptionResponsibilityGetfromUserJobDescriptionPlatformPage"),
    path('customjobDescriptionResponsibilityGetfromJobPositionJobLevelPlatform',views.CustomJobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformAPI.as_view() , name="customjobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformPage"),
    path('customjobDescriptionResponsibilityGetfromJobPositionPlatform',views.CustomJobDescriptionResponsibilityGetfromJobPositionPlatformAPI.as_view() , name="customjobDescriptionResponsibilityGetfromJobPositionPlatformPage"),
    path('customjobDescriptionResponsibilityDeletePlatform',views.CustomJobDescriptionResponsibilityDeletePlatformAPI.as_view() , name="customjobDescriptionResponsibilityDeletePlatformPage"), 
    
    
    path('customjobDescriptionRequirementRegisterPlatform',views.CustomJobDescriptionRequirementPlatformAPI.as_view() , name="customJobDescriptionRequirementRegisterPlatformPage"),
    path('customjobDescriptionRequirementGetPlatform',views.CustomJobDescriptionRequirementGetPlatformAPI.as_view() , name="customJobDescriptionRequirementGetPlatformPage"),
    path('customjobDescriptionRequirementGetOnePlatform',views.CustomJobDescriptionRequirementGetOnePlatformAPI.as_view() , name="customjobDescriptionRequirementGetOnePlatformPage"),
    path('customjobDescriptionRequirementGetfromUserJobDescriptionPlatform',views.CustomJobDescriptionRequirementGetfromUserJobDescriptionPlatformAPI.as_view() , name="customjobDescriptionRequirementGetfromUserJobDescriptionPlatformPage"),
    path('customjobDescriptionRequirementGetfromJobPositionJobLevelPlatform',views.CustomJobDescriptionRequirementGetfromJobPositionJobLevelPlatformAPI.as_view() , name="customjobDescriptionRequirementGetfromJobPositionJobLevelPlatformPage"),
    path('customjobDescriptionRequirementGetfromJobPositionPlatform',views.CustomJobDescriptionRequirementGetfromJobPositionPlatformAPI.as_view() , name="customjobDescriptionRequirementGetfromJobPositionPlatformPage"),
    path('customjobDescriptionRequirementDeletePlatform',views.CustomJobDescriptionRequirementDeletePlatformAPI.as_view() , name="customjobDescriptionRequirementDeletePlatformPage"), 
    
    path('customjobDescriptionBenefitRegisterPlatform',views.CustomJobDescriptionBenefitPlatformAPI.as_view() , name="customJobDescriptionBenefitRegisterPlatformPage"),
    path('customjobDescriptionBenefitGetPlatform',views.CustomJobDescriptionBenefitGetPlatformAPI.as_view() , name="customJobDescriptionBenefitGetPlatformPage"),
    path('customjobDescriptionBenefitGetOnePlatform',views.CustomJobDescriptionBenefitGetOnePlatformAPI.as_view() , name="customjobDescriptionBenefitGetOnePlatformPage"),
    path('customjobDescriptionBenefitGetfromUserJobDescriptionPlatform',views.CustomJobDescriptionBenefitGetfromUserJobDescriptionPlatformAPI.as_view() , name="customjobDescriptionBenefitGetfromUserJobDescriptionPlatformPage"),
    path('customjobDescriptionBenefitGetfromJobPositionJobLevelPlatform',views.CustomJobDescriptionBenefitGetfromJobPositionJobLevelPlatformAPI.as_view() , name="customjobDescriptionBenefitGetfromJobPositionJobLevelPlatformPage"),
    path('customjobDescriptionBenefitGetfromJobPositionPlatform',views.CustomJobDescriptionBenefitGetfromJobPositionPlatformAPI.as_view() , name="customjobDescriptionBenefitGetfromJobPositionPlatformPage"),
    path('customjobDescriptionBenefitDeletePlatform',views.CustomJobDescriptionBenefitDeletePlatformAPI.as_view() , name="customjobDescriptionBenefitDeletePlatformPage"), 
    
    
    path('jobDescriptionResponsibilityRegisterPlatform',views.JobDescriptionResponsibilityPlatformAPI.as_view() , name="jobDescriptionResponsibilityRegisterPlatformPage"),
    path('jobDescriptionResponsibilityGetOnePlatform',views.JobDescriptionResponsibilityGetOnePlatformAPI.as_view() , name="jobDescriptionResponsibilityGetOnePlatformPage"),
    path('jobDescriptionResponsibilityGetfromUserJobDescriptionPlatform',views.JobDescriptionResponsibilityGetfromUserJobDescriptionPlatformAPI.as_view() , name="jobDescriptionResponsibilityGetfromUserJobDescriptionPlatformPage"),
    path('jobDescriptionResponsibilityGetfromJobPositionJobLevelPlatform',views.JobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformAPI.as_view() , name="jobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformPage"),
    path('jobDescriptionResponsibilityGetfromJobPositionPlatform',views.JobDescriptionResponsibilityGetfromJobPositionPlatformAPI.as_view() , name="jobDescriptionResponsibilityGetfromJobPositionPlatformPage"),
    path('jobDescriptionResponsibilityDeletePlatform',views.JobDescriptionResponsibilityDeletePlatformAPI.as_view() , name="jobDescriptionResponsibilityDeletePlatformPage"), 
    
    path('bothjobDescriptionResponsibilityGetfromUserJobDescriptionPlatform',views.BothJobDescriptionResponsibilityGetfromUserJobDescriptionPlatformAPI.as_view() , name="bothjobDescriptionResponsibilityGetfromUserJobDescriptionPlatformPage"),
    path('bothjobDescriptionResponsibilityGetfromJobPositionJobLevelPlatform',views.BothJobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformAPI.as_view() , name="bothjobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformPage"),
    path('bothjobDescriptionResponsibilityGetfromJobPositionPlatform',views.BothJobDescriptionResponsibilityGetfromJobPositionPlatformAPI.as_view() , name="bothjobDescriptionResponsibilityGetfromJobPositionPlatformPage"),
    
    path('jobDescriptionRequirementRegisterPlatform',views.JobDescriptionRequirementPlatformAPI.as_view() , name="jobDescriptionRequirementRegisterPlatformPage"),
    path('jobDescriptionRequirementGetOnePlatform',views.JobDescriptionRequirementGetOnePlatformAPI.as_view() , name="jobDescriptionRequirementGetOnePlatformPage"),
    path('jobDescriptionRequirementGetfromUserJobDescriptionPlatform',views.JobDescriptionRequirementGetfromUserJobDescriptionPlatformAPI.as_view() , name="jobDescriptionRequirementGetfromUserJobDescriptionPlatformPage"),
    path('jobDescriptionRequirementGetfromJobPositionJobLevelPlatform',views.JobDescriptionRequirementGetfromJobPositionJobLevelPlatformAPI.as_view() , name="jobDescriptionRequirementGetfromJobPositionJobLevelPlatformPage"),
    path('jobDescriptionRequirementGetfromJobPositionPlatform',views.JobDescriptionRequirementGetfromJobPositionPlatformAPI.as_view() , name="jobDescriptionRequirementGetfromJobPositionPlatformPage"),
    path('jobDescriptionRequirementDeletePlatform',views.JobDescriptionRequirementDeletePlatformAPI.as_view() , name="jobDescriptionRequirementDeletePlatformPage"), 
    
    path('bothJobDescriptionRequirementGetfromUserJobDescriptionPlatform',views.BothJobDescriptionRequirementGetfromUserJobDescriptionPlatformAPI.as_view() , name="bothJobDescriptionRequirementGetfromUserJobDescriptionPlatformPage"),
    path('bothJobDescriptionRequirementGetfromJobPositionJobLevelPlatform',views.BothJobDescriptionRequirementGetfromJobPositionJobLevelPlatformAPI.as_view() , name="bothJobDescriptionRequirementGetfromJobPositionJobLevelPlatformPage"),
    path('bothJobDescriptionRequirementGetfromJobPositionPlatform',views.BothJobDescriptionRequirementGetfromJobPositionPlatformAPI.as_view() , name="bothJobDescriptionRequirementGetfromJobPositionPlatformPage"),
        
    path('jobDescriptionBenefitRegisterPlatform',views.JobDescriptionBenefitPlatformAPI.as_view() , name="JobDescriptionBenefitRegisterPlatformPage"),
    path('jobDescriptionBenefitGetOnePlatform',views.JobDescriptionBenefitGetOnePlatformAPI.as_view() , name="jobDescriptionBenefitGetOnePlatformPage"),
    path('jobDescriptionBenefitGetfromUserJobDescriptionPlatform',views.JobDescriptionBenefitGetfromUserJobDescriptionPlatformAPI.as_view() , name="jobDescriptionBenefitGetfromUserJobDescriptionPlatformPage"),
    path('jobDescriptionBenefitGetfromJobPositionJobLevelPlatform',views.JobDescriptionBenefitGetfromJobPositionJobLevelPlatformAPI.as_view() , name="jobDescriptionBenefitGetfromJobPositionJobLevelPlatformPage"),
    path('jobDescriptionBenefitGetfromJobPositionPlatform',views.JobDescriptionBenefitGetfromJobPositionPlatformAPI.as_view() , name="jobDescriptionBenefitGetfromJobPositionPlatformPage"),
    path('jobDescriptionBenefitDeletePlatform',views.JobDescriptionBenefitDeletePlatformAPI.as_view() , name="jobDescriptionBenefitDeletePlatformPage"), 
    
    path('bothJobDescriptionBenefitGetfromUserJobDescriptionPlatform',views.BothJobDescriptionBenefitGetfromUserJobDescriptionPlatformAPI.as_view() , name="bothJobDescriptionBenefitGetfromUserJobDescriptionPlatformPage"),
    path('bothJobDescriptionBenefitGetfromJobPositionJobLevelPlatform',views.BothJobDescriptionBenefitGetfromJobPositionJobLevelPlatformAPI.as_view() , name="bothJobDescriptionBenefitGetfromJobPositionJobLevelPlatformPage"),
    path('bothJobDescriptionBenefitGetfromJobPositionPlatform',views.BothJobDescriptionBenefitGetfromJobPositionPlatformAPI.as_view() , name="bothJobDescriptionBenefitGetfromJobPositionPlatformPage"),
    
    path('companyDetailRegisterPlatform',views.CompanyDetailRegisterPlatformAPI.as_view(),name='companyDetailRegisterPlatformPage'),
    path('companyDetailsUpdatePlatform',views.CompanyDetailsUpdatePlatformAPI.as_view(),name='companyDetailsUpdatePlatformPage'),
    path('companyDetailsGetOnePlatform',views.CompanyDetailsGetOnePlatformAPI.as_view(),name='companyDetailsGetOnePlatformPage'),
    path('companyDetailsDeletePlatform',views.CompanyDetailsDeletePlatformAPI.as_view(),name='companyDetailsDeletePlatformPage'),
    
    path('companyLocationDetailRegisterPlatform',views.CompanyLocationDetailRegisterPlatformAPI.as_view(),name='companyLocationDetailRegisterPlatformPage'),
    path('companyLocationDetailsUpdatePlatform',views.CompanyLocationDetailsUpdatePlatformAPI.as_view(),name='companyLocationDetailsUpdatePlatformPage'),
    path('companyLocationDetailsCompanyGetPlatform',views.CompanyLocationDetailsCompanyGetPlatformAPI.as_view(),name='companyLocationDetailsCompanyGetPlatformPage'),
    path('companyLocationDetailsGetOnePlatform',views.CompanyLocationDetailsGetOnePlatformAPI.as_view(),name='companyLocationDetailsGetOnePlatformPage'),
    path('companyLocationDetailsDeletePlatform',views.CompanyLocationDetailsDeletePlatformAPI.as_view(),name='companyLocationDetailsDeletePlatformPage'),
    
    path('jobDescriptioncompanyLocationDetailRegisterPlatform',views.JobDescriptionCompanyLocationDetailRegisterPlatformAPI.as_view(),name='JobDescriptioncompanyLocationDetailRegisterPlatformPage'),
    path('jobDescriptioncompanyLocationDetailsUpdatePlatform',views.JobDescriptionCompanyLocationDetailsUpdatePlatformAPI.as_view(),name='jobDescriptioncompanyLocationDetailsUpdatePlatformPage'),
    path('jobDescriptioncompanyLocationDetailsGetOnePlatform',views.JobDescriptionCompanyLocationDetailsGetOnePlatformAPI.as_view(),name='jobDescriptioncompanyLocationDetailsGetOnePlatformPage'),
    path('jobDescriptioncompanyLocationDetailsDeletePlatform',views.JobDescriptionCompanyLocationDetailsDeletePlatformAPI.as_view(),name='jobDescriptioncompanyLocationDetailsDeletePlatformPage'),
            
    path('jobDescriptionEmploymentTypeDetailRegisterPlatform',views.JobDescriptionEmploymentTypeDetailRegisterPlatformAPI.as_view(),name='JobDescriptionEmploymentTypeDetailRegisterPlatformPage'),
    path('jobDescriptionEmploymentTypeDetailsUpdatePlatform',views.JobDescriptionEmploymentTypeDetailsUpdatePlatformAPI.as_view(),name='jobDescriptionEmploymentTypeDetailsUpdatePlatformPage'),
    path('jobDescriptionEmploymentTypeDetailsGetOnePlatform',views.JobDescriptionEmploymentTypeDetailsGetOnePlatformAPI.as_view(),name='jobDescriptionEmploymentTypeDetailsGetOnePlatformPage'),
    path('jobDescriptionEmploymentTypeDetailsDeletePlatform',views.JobDescriptionEmploymentTypeDetailsDeletePlatformAPI.as_view(),name='jobDescriptionEmploymentTypeDetailsDeletePlatformPage'),
    path('JobDescriptionEmploymentTypeGetbyDescpPlatform',views.JobDescriptionEmploymentTypeGetbyDescpPlatformAPI.as_view(),name='JobDescriptionEmploymentTypeGetbyDescpPlatformage'),
    
    path('userCompanyRegisterPlatform',views.UserCompanyRegisterPlatformAPI.as_view(),name='userCompanyRegisterPlatformPage'),
    path('userCompanyUpdatePlatform',views.UserCompanyUpdatePlatformAPI.as_view(),name='userCompanyUpdatePlatformPage'),
    path('userCompanyGetOnePlatform',views.UserCompanyGetOnePlatformAPI.as_view(),name='userCompanyGetOnePlatformPage'),
    path('userCompanyGetOneUserPlatform',views.UserCompanyGetOneUserPlatformAPI.as_view(),name='userCompanyGetOneUserPlatformPage'),

    path('userCompanyDeletePlatform',views.UserCompanyDeletePlatformAPI.as_view(),name='userCompanyDeletePlatformPage'),
    
    path('alljobdescriptionGetPlatform',views.AllJobDescriptionGetPlatformAPI.as_view(),name='alljobdescriptionPlatformPage'),
    
    path('nationalityJobDescriptionRegisterPlatform',views.NationalityJobDescriptionPlatformAPI.as_view() , name="nationalityJobDescriptionRegisterPlatformPage"),
    path('nationalityJobDescriptionGetPlatform',views.NationalityJobDescriptionGetPlatformAPI.as_view() , name="nationalityJobDescriptionGetPlatformPage"),
    path('nationalityjobDescriptionGetOnePlatform',views.NationalityJobDescriptionGetOnePlatformAPI.as_view() , name="nationalityjobDescriptionGetOnePlatformPage"),
    path('nationalityjobDescriptionDeletePlatform',views.NationalityJobDescriptionDeletePlatformAPI.as_view() , name="nationalityjobDescriptionDeletePlatformPage"),    
    path('NationalityJobDescriptionGetbyDescpPlatform',views.NationalityJobDescriptionGetbyDescpPlatformAPI.as_view() , name="NationalityJobDescriptionGetbyDescpPlatformPage"),
    
    path('genderJobDescriptionRegisterPlatform',views.GenderJobDescriptionPlatformAPI.as_view() , name="genderJobDescriptionRegisterPlatformPage"),
    path('genderJobDescriptionGetPlatform',views.GenderJobDescriptionGetPlatformAPI.as_view() , name="genderJobDescriptionGetPlatformPage"),
    path('genderjobDescriptionGetOnePlatform',views.GenderJobDescriptionGetOnePlatformAPI.as_view() , name="genderjobDescriptionGetOnePlatformPage"),
    path('genderjobDescriptionDeletePlatform',views.GenderJobDescriptionDeletePlatformAPI.as_view() , name="genderjobDescriptionDeletePlatformPage"),    
    path('GenderJobDescriptionGetbyDescpPlatform',views.GenderJobDescriptionGetbyDescpPlatformAPI.as_view() , name="GenderJobDescriptionGetbyDescpPlatformPage"),
        
    path('workPlaceJobDescriptionRegisterPlatform',views.WorkPlaceJobDescriptionPlatformAPI.as_view() , name="workPlaceJobDescriptionRegisterPlatformPage"),
    path('workPlaceJobDescriptionGetPlatform',views.WorkPlaceJobDescriptionGetPlatformAPI.as_view() , name="workPlaceJobDescriptionGetPlatformPage"),
    path('workPlacejobDescriptionGetOnePlatform',views.WorkPlaceJobDescriptionGetOnePlatformAPI.as_view() , name="workPlacejobDescriptionGetOnePlatformPage"),
    path('workPlacejobDescriptionDeletePlatform',views.WorkPlaceJobDescriptionDeletePlatformAPI.as_view() , name="workPlacejobDescriptionDeletePlatformPage"),    
    path('WorkPlaceJobDescriptionGetbyDescpPlatform',views.WorkPlaceJobDescriptionGetbyDescpPlatformAPI.as_view() , name="WorkPlaceJobDescriptionGetbyDescpPlatformPage"),  
        
    path('languageJobDescriptionRegisterPlatform',views.LanguageJobDescriptionPlatformAPI.as_view() , name="languageJobDescriptionRegisterPlatformPage"),
    path('languageJobDescriptionGetPlatform',views.LanguageJobDescriptionGetPlatformAPI.as_view() , name="languageJobDescriptionGetPlatformPage"),
    path('languagejobDescriptionGetOnePlatform',views.LanguageJobDescriptionGetOnePlatformAPI.as_view() , name="languagejobDescriptionGetOnePlatformPage"),
    path('languagejobDescriptionDeletePlatform',views.LanguageJobDescriptionDeletePlatformAPI.as_view() , name="languagejobDescriptionDeletePlatformPage"),    
    path('LanguageJobDescriptionGetbyDescpPlatform',views.LanguageJobDescriptionGetbyDescpPlatformAPI.as_view() , name="LanguageJobDescriptionGetbyDescpPlatformPage"),
        
    path('joiningperiodJobDescriptionRegisterPlatform',views.JoiningPeriodJobDescriptionPlatformAPI.as_view() , name="joiningperiodJobDescriptionRegisterPlatformPage"),
    path('joiningperiodJobDescriptionGetPlatform',views.JoiningPeriodJobDscriptionGetPlatformAPI.as_view() , name="joiningperiodJobDescriptionGetPlatformPage"),
    path('joiningperiodjobDescriptionGetOnePlatform',views.JoiningPeriodJobDescriptionGetOnePlatformAPI.as_view() , name="joiningperiodjobDescriptionGetOnePlatformPage"),
    path('joiningperiodjobDescriptionDeletePlatform',views.JoiningPeriodJobDescriptionDeletePlatformAPI.as_view() , name="joiningperiodjobDescriptionDeletePlatformPage"),    
    path('JoiningPeriodJobDescriptionGetbyDescpPlatform',views.JoiningPeriodJobDescriptionGetbyDescpPlatformAPI.as_view() , name="JoiningPeriodJobDescriptionGetbyDescpPlatformPage"),   

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
