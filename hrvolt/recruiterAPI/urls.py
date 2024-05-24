from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('jobDescriptionRegister',views.JobDescriptionAPI.as_view() , name="jobDescriptionRegisterPage"),
    path('jobDescriptionUpdate',views.JobDescriptionUpdateAPI.as_view() , name="jobDescriptionUpdatePage"),
    path('jobDescriptionGet',views.JobDescriptionGetAPI.as_view() , name="jobDescriptionGetPage"),
    path('jobDescriptionGetOne',views.JobDescriptionGetOneAPI.as_view() , name="jobDescriptionGetOnePage"),
    path('jobDescriptionGetUser',views.JobDescriptionGetUserAPI.as_view() , name="jobDescriptionGetUserPage"),
    path('jobDescriptionGetfromJobPositionJobLevel',views.JobDescriptionGetfromJobPositionJobLevelAPI.as_view() , name="jobDescriptionGetfromJobPositionJobLevelPage"),
    path('jobDescriptionDelete',views.JobDescriptionDeleteAPI.as_view() , name="jobDescriptionDeletePage"),    
    
    
    path('educationJobDescriptionRegister',views.EducationJobDescriptionAPI.as_view() , name="educationJobDescriptionRegisterPage"),
    path('educationJobDescriptionGet',views.EducationJobDescriptionGetAPI.as_view() , name="educationJobDescriptionGetPage"),
    path('educationjobDescriptionGetOne',views.EducationJobDescriptionGetOneAPI.as_view() , name="educationjobDescriptionGetOnePage"),
    path('educationjobDescriptionDelete',views.EducationJobDescriptionDeleteAPI.as_view() , name="educationjobDescriptionDeletePage"),  
    path('EducationJobDescriptionGetbyDescp',views.EducationJobDescriptionGetbyDescpAPI.as_view() , name="EducationJobDescriptionGetbyDescpPage"),

    path('educationFieldJobDescriptionRegister',views.EducationFieldJobDescriptionAPI.as_view() , name="educationFieldJobDescriptionRegisterPage"),
    path('educationFieldJobDescriptionGet',views.EducationFieldJobDescriptionGetAPI.as_view() , name="educationFieldJobDescriptionGetPage"),
    path('educationFieldjobDescriptionGetOne',views.EducationFieldJobDescriptionGetOneAPI.as_view() , name="educationFieldjobDescriptionGetOnePage"),
    path('educationFieldjobDescriptionDelete',views.EducationFieldJobDescriptionDeleteAPI.as_view() , name="educationFieldjobDescriptionDeletePage"),  
    path('EducationFieldJobDescriptionGetbyDescp',views.EducationFieldJobDescriptionGetbyDescpAPI.as_view() , name="EducationFieldJobDescriptionGetbyDescpPage"),

    path('softskillsJobDescriptionRegister',views.SoftSkillsJobDescriptionAPI.as_view() , name="softskillsJobDescriptionRegisterPage"),
    path('softskillsJobDescriptionGet',views.SoftSkillsJobDescriptionGetAPI.as_view() , name="softskillsJobDescriptionGetPage"),
    path('softskillsjobDescriptionGetOne',views.SoftSkillsJobDescriptionGetOneAPI.as_view() , name="softskillsjobDescriptionGetOnePage"),
    path('softskillsjobDescriptionDelete',views.SoftSkillsJobDescriptionDeleteAPI.as_view() , name="softskillsjobDescriptionDeletePage"), 
    path('SoftSkillsJobDescriptionGetbyDescp',views.SoftSkillsJobDescriptionGetbyDescpAPI.as_view() , name="SoftSkillsJobDescriptionGetbyDescpPage"),    
    
    path('technicalskillsJobDescriptionRegister',views.TechnicalSkillsJobDescriptionAPI.as_view() , name="technicalskillsJobDescriptionRegisterPage"),
    path('technicalskillsJobDescriptionGet',views.TechnicalSkillsJobDescriptionGetAPI.as_view() , name="technicalskillsJobDescriptionGetPage"),
    path('technicalskillsjobDescriptionGetOne',views.TechnicalSkillsJobDescriptionGetOneAPI.as_view() , name="technicalskillsjobDescriptionGetOnePage"),
    path('technicalskillsjobDescriptionDelete',views.TechnicalSkillsJobDescriptionDeleteAPI.as_view() , name="technicalskillsjobDescriptionDeletePage"),  
    path('TechnicalSkillsJobDescriptionGetbyDescp',views.TechnicalSkillsJobDescriptionGetbyDescpAPI.as_view() , name="TechnicalSkillsJobDescriptionGetbyDescpPage"),  
    
    
    path('customjobDescriptionResponsibilityRegister',views.CustomJobDescriptionResponsibilityAPI.as_view() , name="customJobDescriptionResponsibilityRegisterPage"),
    path('customjobDescriptionResponsibilityGet',views.CustomJobDescriptionResponsibilityGetAPI.as_view() , name="customJobDescriptionResponsibilityGetPage"),
    path('customjobDescriptionResponsibilityGetOne',views.CustomJobDescriptionResponsibilityGetOneAPI.as_view() , name="customjobDescriptionResponsibilityGetOnePage"),
    path('customjobDescriptionResponsibilityGetfromUserJobDescription',views.CustomJobDescriptionResponsibilityGetfromUserJobDescriptionAPI.as_view() , name="customjobDescriptionResponsibilityGetfromUserJobDescriptionPage"),
    path('customjobDescriptionResponsibilityGetfromJobPositionJobLevel',views.CustomJobDescriptionResponsibilityGetfromJobPositionJobLevelAPI.as_view() , name="customjobDescriptionResponsibilityGetfromJobPositionJobLevelPage"),
    path('customjobDescriptionResponsibilityGetfromJobPosition',views.CustomJobDescriptionResponsibilityGetfromJobPositionAPI.as_view() , name="customjobDescriptionResponsibilityGetfromJobPositionPage"),
    path('customjobDescriptionResponsibilityDelete',views.CustomJobDescriptionResponsibilityDeleteAPI.as_view() , name="customjobDescriptionResponsibilityDeletePage"), 
    
    
    path('customjobDescriptionRequirementRegister',views.CustomJobDescriptionRequirementAPI.as_view() , name="customJobDescriptionRequirementRegisterPage"),
    path('customjobDescriptionRequirementGet',views.CustomJobDescriptionRequirementGetAPI.as_view() , name="customJobDescriptionRequirementGetPage"),
    path('customjobDescriptionRequirementGetOne',views.CustomJobDescriptionRequirementGetOneAPI.as_view() , name="customjobDescriptionRequirementGetOnePage"),
    path('customjobDescriptionRequirementGetfromUserJobDescription',views.CustomJobDescriptionRequirementGetfromUserJobDescriptionAPI.as_view() , name="customjobDescriptionRequirementGetfromUserJobDescriptionPage"),
    path('customjobDescriptionRequirementGetfromJobPositionJobLevel',views.CustomJobDescriptionRequirementGetfromJobPositionJobLevelAPI.as_view() , name="customjobDescriptionRequirementGetfromJobPositionJobLevelPage"),
    path('customjobDescriptionRequirementGetfromJobPosition',views.CustomJobDescriptionRequirementGetfromJobPositionAPI.as_view() , name="customjobDescriptionRequirementGetfromJobPositionPage"),
    path('customjobDescriptionRequirementDelete',views.CustomJobDescriptionRequirementDeleteAPI.as_view() , name="customjobDescriptionRequirementDeletePage"), 
    
    path('customjobDescriptionBenefitRegister',views.CustomJobDescriptionBenefitAPI.as_view() , name="customJobDescriptionBenefitRegisterPage"),
    path('customjobDescriptionBenefitGet',views.CustomJobDescriptionBenefitGetAPI.as_view() , name="customJobDescriptionBenefitGetPage"),
    path('customjobDescriptionBenefitGetOne',views.CustomJobDescriptionBenefitGetOneAPI.as_view() , name="customjobDescriptionBenefitGetOnePage"),
    path('customjobDescriptionBenefitGetfromUserJobDescription',views.CustomJobDescriptionBenefitGetfromUserJobDescriptionAPI.as_view() , name="customjobDescriptionBenefitGetfromUserJobDescriptionPage"),
    path('customjobDescriptionBenefitGetfromJobPositionJobLevel',views.CustomJobDescriptionBenefitGetfromJobPositionJobLevelAPI.as_view() , name="customjobDescriptionBenefitGetfromJobPositionJobLevelPage"),
    path('customjobDescriptionBenefitGetfromJobPosition',views.CustomJobDescriptionBenefitGetfromJobPositionAPI.as_view() , name="customjobDescriptionBenefitGetfromJobPositionPage"),
    path('customjobDescriptionBenefitDelete',views.CustomJobDescriptionBenefitDeleteAPI.as_view() , name="customjobDescriptionBenefitDeletePage"), 
    
    
    path('jobDescriptionResponsibilityRegister',views.JobDescriptionResponsibilityAPI.as_view() , name="jobDescriptionResponsibilityRegisterPage"),
    path('jobDescriptionResponsibilityGetOne',views.JobDescriptionResponsibilityGetOneAPI.as_view() , name="jobDescriptionResponsibilityGetOnePage"),
    path('jobDescriptionResponsibilityGetfromUserJobDescription',views.JobDescriptionResponsibilityGetfromUserJobDescriptionAPI.as_view() , name="jobDescriptionResponsibilityGetfromUserJobDescriptionPage"),
    path('jobDescriptionResponsibilityGetfromJobPositionJobLevel',views.JobDescriptionResponsibilityGetfromJobPositionJobLevelAPI.as_view() , name="jobDescriptionResponsibilityGetfromJobPositionJobLevelPage"),
    path('jobDescriptionResponsibilityGetfromJobPosition',views.JobDescriptionResponsibilityGetfromJobPositionAPI.as_view() , name="jobDescriptionResponsibilityGetfromJobPositionPage"),
    path('jobDescriptionResponsibilityDelete',views.JobDescriptionResponsibilityDeleteAPI.as_view() , name="jobDescriptionResponsibilityDeletePage"), 
    
    path('bothjobDescriptionResponsibilityGetfromUserJobDescription',views.BothJobDescriptionResponsibilityGetfromUserJobDescriptionAPI.as_view() , name="bothjobDescriptionResponsibilityGetfromUserJobDescriptionPage"),
    path('bothjobDescriptionResponsibilityGetfromJobPositionJobLevel',views.BothJobDescriptionResponsibilityGetfromJobPositionJobLevelAPI.as_view() , name="bothjobDescriptionResponsibilityGetfromJobPositionJobLevelPage"),
    path('bothjobDescriptionResponsibilityGetfromJobPosition',views.BothJobDescriptionResponsibilityGetfromJobPositionAPI.as_view() , name="bothjobDescriptionResponsibilityGetfromJobPositionPage"),
    
    path('jobDescriptionRequirementRegister',views.JobDescriptionRequirementAPI.as_view() , name="jobDescriptionRequirementRegisterPage"),
    path('jobDescriptionRequirementGetOne',views.JobDescriptionRequirementGetOneAPI.as_view() , name="jobDescriptionRequirementGetOnePage"),
    path('jobDescriptionRequirementGetfromUserJobDescription',views.JobDescriptionRequirementGetfromUserJobDescriptionAPI.as_view() , name="jobDescriptionRequirementGetfromUserJobDescriptionPage"),
    path('jobDescriptionRequirementGetfromJobPositionJobLevel',views.JobDescriptionRequirementGetfromJobPositionJobLevelAPI.as_view() , name="jobDescriptionRequirementGetfromJobPositionJobLevelPage"),
    path('jobDescriptionRequirementGetfromJobPosition',views.JobDescriptionRequirementGetfromJobPositionAPI.as_view() , name="jobDescriptionRequirementGetfromJobPositionPage"),
    path('jobDescriptionRequirementDelete',views.JobDescriptionRequirementDeleteAPI.as_view() , name="jobDescriptionRequirementDeletePage"), 
    
    path('bothJobDescriptionRequirementGetfromUserJobDescription',views.BothJobDescriptionRequirementGetfromUserJobDescriptionAPI.as_view() , name="bothJobDescriptionRequirementGetfromUserJobDescriptionPage"),
    path('bothJobDescriptionRequirementGetfromJobPositionJobLevel',views.BothJobDescriptionRequirementGetfromJobPositionJobLevelAPI.as_view() , name="bothJobDescriptionRequirementGetfromJobPositionJobLevelPage"),
    path('bothJobDescriptionRequirementGetfromJobPosition',views.BothJobDescriptionRequirementGetfromJobPositionAPI.as_view() , name="bothJobDescriptionRequirementGetfromJobPositionPage"),
        
    path('jobDescriptionBenefitRegister',views.JobDescriptionBenefitAPI.as_view() , name="JobDescriptionBenefitRegisterPage"),
    path('jobDescriptionBenefitGetOne',views.JobDescriptionBenefitGetOneAPI.as_view() , name="jobDescriptionBenefitGetOnePage"),
    path('jobDescriptionBenefitGetfromUserJobDescription',views.JobDescriptionBenefitGetfromUserJobDescriptionAPI.as_view() , name="jobDescriptionBenefitGetfromUserJobDescriptionPage"),
    path('jobDescriptionBenefitGetfromJobPositionJobLevel',views.JobDescriptionBenefitGetfromJobPositionJobLevelAPI.as_view() , name="jobDescriptionBenefitGetfromJobPositionJobLevelPage"),
    path('jobDescriptionBenefitGetfromJobPosition',views.JobDescriptionBenefitGetfromJobPositionAPI.as_view() , name="jobDescriptionBenefitGetfromJobPositionPage"),
    path('jobDescriptionBenefitDelete',views.JobDescriptionBenefitDeleteAPI.as_view() , name="jobDescriptionBenefitDeletePage"), 
    
    path('bothJobDescriptionBenefitGetfromUserJobDescription',views.BothJobDescriptionBenefitGetfromUserJobDescriptionAPI.as_view() , name="bothJobDescriptionBenefitGetfromUserJobDescriptionPage"),
    path('bothJobDescriptionBenefitGetfromJobPositionJobLevel',views.BothJobDescriptionBenefitGetfromJobPositionJobLevelAPI.as_view() , name="bothJobDescriptionBenefitGetfromJobPositionJobLevelPage"),
    path('bothJobDescriptionBenefitGetfromJobPosition',views.BothJobDescriptionBenefitGetfromJobPositionAPI.as_view() , name="bothJobDescriptionBenefitGetfromJobPositionPage"),
    
    path('companyDetailRegister',views.CompanyDetailRegisterAPI.as_view(),name='companyDetailRegisterPage'),
    path('companyDetailsUpdate',views.CompanyDetailsUpdateAPI.as_view(),name='companyDetailsUpdatePage'),
    # path('companyDetailsGet',views.CompanyDetailsGetAPI.as_view(),name='companyDetailsGetPage'),
    path('companyDetailsGetOne',views.CompanyDetailsGetOneAPI.as_view(),name='companyDetailsGetOnePage'),
    path('CompanyDetailsGetOneByUser',views.CompanyDetailsGetOneByUserAPI.as_view(),name='CompanyDetailsGetOneByUserPage'),


    
    path('companyDetailsDelete',views.CompanyDetailsDeleteAPI.as_view(),name='companyDetailsDeletePage'),
    
    path('companyLocationDetailRegister',views.CompanyLocationDetailRegisterAPI.as_view(),name='companyLocationDetailRegisterPage'),
    path('companyLocationDetailsUpdate',views.CompanyLocationDetailsUpdateAPI.as_view(),name='companyLocationDetailsUpdatePage'),
    path('companyLocationDetailsCompanyGet',views.CompanyLocationDetailsCompanyGetAPI.as_view(),name='companyLocationDetailsCompanyGetPage'),
    path('companyLocationDetailsGetOne',views.CompanyLocationDetailsGetOneAPI.as_view(),name='companyLocationDetailsGetOnePage'),
    path('companyLocationDetailsDelete',views.CompanyLocationDetailsDeleteAPI.as_view(),name='companyLocationDetailsDeletePage'),
    
    path('jobDescriptioncompanyLocationDetailRegister',views.JobDescriptionCompanyLocationDetailRegisterAPI.as_view(),name='JobDescriptioncompanyLocationDetailRegisterPage'),
    path('jobDescriptioncompanyLocationDetailsUpdate',views.JobDescriptionCompanyLocationDetailsUpdateAPI.as_view(),name='jobDescriptioncompanyLocationDetailsUpdatePage'),
    # path('jobDescriptioncompanyLocationDetailsGet',views.JobDescriptionCompanyLocationDetailsGetAPI.as_view(),name='jobDescriptioncompanyLocationDetailsGetPage'),
    path('jobDescriptioncompanyLocationDetailsGetOne',views.JobDescriptionCompanyLocationDetailsGetOneAPI.as_view(),name='jobDescriptioncompanyLocationDetailsGetOnePage'),
    path('jobDescriptioncompanyLocationDetailsDelete',views.JobDescriptionCompanyLocationDetailsDeleteAPI.as_view(),name='jobDescriptioncompanyLocationDetailsDeletePage'),
            
    path('jobDescriptionEmploymentTypeDetailRegister',views.JobDescriptionEmploymentTypeDetailRegisterAPI.as_view(),name='JobDescriptionEmploymentTypeDetailRegisterPage'),
    path('jobDescriptionEmploymentTypeDetailsUpdate',views.JobDescriptionEmploymentTypeDetailsUpdateAPI.as_view(),name='jobDescriptionEmploymentTypeDetailsUpdatePage'),
    path('JobDescriptionEmploymentTypeGetbyDescp',views.JobDescriptionEmploymentTypeGetbyDescpAPI.as_view(),name='JobDescriptionEmploymentTypeGetbyDescpPage'),
    path('jobDescriptionEmploymentTypeDetailsGetOne',views.JobDescriptionEmploymentTypeDetailsGetOneAPI.as_view(),name='jobDescriptionEmploymentTypeDetailsGetOnePage'),
    path('jobDescriptionEmploymentTypeDetailsDelete',views.JobDescriptionEmploymentTypeDetailsDeleteAPI.as_view(),name='jobDescriptionEmploymentTypeDetailsDeletePage'),
    
    path('userCompanyRegister',views.UserCompanyRegisterAPI.as_view(),name='userCompanyRegisterPage'),
    path('userCompanyUpdate',views.UserCompanyUpdateAPI.as_view(),name='userCompanyUpdatePage'),
    path('userCompanyGetOne',views.UserCompanyGetOneAPI.as_view(),name='userCompanyGetOnePage'),
    path('userCompanyGetOneUser',views.UserCompanyGetOneUserAPI.as_view(),name='userCompanyGetOneUserPage'),

    path('userCompanyDelete',views.UserCompanyDeleteAPI.as_view(),name='userCompanyDeletePage'),
    
    path('alljobdescriptionGet',views.AllJobDescriptionGetAPI.as_view(),name='alljobdescriptionPage'),
    
    path('nationalityJobDescriptionRegister',views.NationalityJobDescriptionAPI.as_view() , name="nationalityJobDescriptionRegisterPage"),
    path('nationalityJobDescriptionGet',views.NationalityJobDescriptionGetAPI.as_view() , name="nationalityJobDescriptionGetPage"),
    path('nationalityjobDescriptionGetOne',views.NationalityJobDescriptionGetOneAPI.as_view() , name="nationalityjobDescriptionGetOnePage"),
    path('nationalityjobDescriptionDelete',views.NationalityJobDescriptionDeleteAPI.as_view() , name="nationalityjobDescriptionDeletePage"),    
    path('NationalityJobDescriptionGetbyDescp',views.NationalityJobDescriptionGetbyDescpAPI.as_view() , name="NationalityJobDescriptionGetbyDescpPage"),
    
    path('genderJobDescriptionRegister',views.GenderJobDescriptionAPI.as_view() , name="genderJobDescriptionRegisterPage"),
    path('genderJobDescriptionGet',views.GenderJobDescriptionGetAPI.as_view() , name="genderJobDescriptionGetPage"),
    path('genderjobDescriptionGetOne',views.GenderJobDescriptionGetOneAPI.as_view() , name="genderjobDescriptionGetOnePage"),
    path('genderjobDescriptionDelete',views.GenderJobDescriptionDeleteAPI.as_view() , name="genderjobDescriptionDeletePage"),   
    path('GenderJobDescriptionGetbyDescp',views.GenderJobDescriptionGetbyDescpAPI.as_view() , name="GenderJobDescriptionGetbyDescpPage"),

        
    path('workPlaceJobDescriptionRegister',views.WorkPlaceJobDescriptionAPI.as_view() , name="workPlaceJobDescriptionRegisterPage"),
    path('workPlaceJobDescriptionGet',views.WorkPlaceJobDescriptionGetAPI.as_view() , name="workPlaceJobDescriptionGetPage"),
    path('workPlacejobDescriptionGetOne',views.WorkPlaceJobDescriptionGetOneAPI.as_view() , name="workPlacejobDescriptionGetOnePage"),
    path('workPlacejobDescriptionDelete',views.WorkPlaceJobDescriptionDeleteAPI.as_view() , name="workPlacejobDescriptionDeletePage"),  
    path('WorkPlaceJobDescriptionGetbyDescp',views.WorkPlaceJobDescriptionGetbyDescpAPI.as_view() , name="WorkPlaceJobDescriptionGetbyDescpPage"),  
        
    path('languageJobDescriptionRegister',views.LanguageJobDescriptionAPI.as_view() , name="languageJobDescriptionRegisterPage"),
    path('languageJobDescriptionGet',views.LanguageJobDescriptionGetAPI.as_view() , name="languageJobDescriptionGetPage"),
    path('languagejobDescriptionGetOne',views.LanguageJobDescriptionGetOneAPI.as_view() , name="languagejobDescriptionGetOnePage"),
    path('languagejobDescriptionDelete',views.LanguageJobDescriptionDeleteAPI.as_view() , name="languagejobDescriptionDeletePage"),    
    path('LanguageJobDescriptionGetbyDescp',views.LanguageJobDescriptionGetbyDescpAPI.as_view() , name="LanguageJobDescriptionGetbyDescpPage"),
        
    path('joiningperiodJobDescriptionRegister',views.JoiningPeriodJobDescriptionAPI.as_view() , name="joiningperiodJobDescriptionRegisterPage"),
    path('joiningperiodJobDescriptionGet',views.JoiningPeriodJobDscriptionGetAPI.as_view() , name="joiningperiodJobDescriptionGetPage"),
    path('joiningperiodjobDescriptionGetOne',views.JoiningPeriodJobDescriptionGetOneAPI.as_view() , name="joiningperiodjobDescriptionGetOnePage"),
    path('joiningperiodjobDescriptionDelete',views.JoiningPeriodJobDescriptionDeleteAPI.as_view() , name="joiningperiodjobDescriptionDeletePage"), 
    path('JoiningPeriodJobDescriptionGetbyDescp',views.JoiningPeriodJobDescriptionGetbyDescpAPI.as_view() , name="JoiningPeriodJobDescriptionGetbyDescpPage"),   
    path('autoJobDescription',views.autoJobDescriptionAPI.as_view() , name="autoJobDescriptionPage"),   
    path('autoCompareCandidateJobDescrip',views.autoCompareCandidateJobDescripAPI.as_view() , name="autoCompareCandidateJobDescripPage"),   
    path('autoCompareCandidateJobDescripList',views.autoCompareCandidateJobDescripListAPI.as_view() , name="autoCompareCandidateJobDescripListPage"),   
    path('autoCompareCandidateJobDescripAI',views.autoCompareCandidateJobDescripAIAPI.as_view() , name="autoCompareCandidateJobDescripAIPage"),   
    
    path('RecruiterBulkResumeUpload',views.RecruiterBulkResumeUploadAPI.as_view() , name="RecruiterBulkResumeUploadPage"),   
    path('RecruiterResumeJobDescriptionCompare',views.RecruiterResumeJobDescriptionCompareAPI.as_view() , name="RecruiterResumeJobDescriptionComparePage"),   

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
