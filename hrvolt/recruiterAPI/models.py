from django.db import models
import datetime
from userloginAPI.models import NewUser
from databaseAPI.models import *

# Create your models here.
class JobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_job_desc_tb"
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_tilte = models.CharField(max_length=100,blank=True, null=True,default=None)
    job_description_id = models.CharField(max_length=100, primary_key= True, default=None) # id of job description
    salary_min = models.CharField(max_length=100,blank=False,null=False,default=None)
    salary_max = models.CharField(max_length=100,blank=False,null=False,default=None)
    number_of_vacancy =  models.CharField(max_length=200,blank=False,null=False,default=None)
    job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())
        
class EducationJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_education_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    education_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    education = models.ForeignKey(EducationModel,on_delete=models.CASCADE,default=None)
    education_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    education_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    education_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())


class EducationFieldJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_education_field_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    education_field_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    education_field  = models.ForeignKey(EducationFieldModel,on_delete=models.CASCADE,default=None)
    education_field_name= models.CharField(max_length=100,blank=False,null=False,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    education_field_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    education_field_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())
    
class SoftSkillJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_soft_skill_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    soft_skills_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    soft_skills = models.ForeignKey(SoftSkillsModel,on_delete=models.CASCADE,default=None)
    soft_skills_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    soft_skills_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    soft_skills_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())

class TechnicalSkillJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_technical_skill_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    technical_skills_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    technical_skills = models.ForeignKey(TechnicalSkillsUniqueModel,on_delete=models.CASCADE,default=None)
    technical_skills_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    technical_skills_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    technical_skills_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())
    
class CustomJobDescriptionResponsibilityModel(models.Model):
    class Meta:
        db_table = "recruiter_custom_job_desc_responsibility_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    custom_job_description_responsibility_id = models.CharField(max_length=100, primary_key= True, default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    responsibilities_description = models.CharField(max_length=100,blank=True,null=True,default=None)
    custom_job_description_responsibility_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    custom_job_description_responsibility_registration_date = models.DateTimeField(default=datetime.datetime.now())    
       
class CustomJobDescriptionRequirementsModel(models.Model):
    class Meta:
        db_table = "recruiter_custom_job_desc_requirement_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    custom_job_description_requirement_id = models.CharField(max_length=100, primary_key= True, default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    requirement_description = models.CharField(max_length=100,blank=True,null=True,default=None)
    custom_job_description_requirement_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    custom_job_description_requirement_registration_date = models.DateTimeField(default=datetime.datetime.now())  

class CustomJobDescriptionBenefitsModel(models.Model):
    class Meta:
        db_table = "recruiter_custom_job_desc_benefit_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    custom_job_description_benefit_id = models.CharField(max_length=100, primary_key= True, default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    benefit_description = models.CharField(max_length=100,blank=True,null=True,default=None)
    custom_job_description_benefit_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    custom_job_description_benefit_registration_date = models.DateTimeField(default=datetime.datetime.now())  
  
class JobDescriptionResponsibilityModel(models.Model):
    class Meta:
        db_table = "recruiter_job_desc_responsibility_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    job_description_responsibility_id = models.CharField(max_length=100, primary_key= True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    job_responsibility = models.ForeignKey(JobResponsibilityModel,on_delete=models.CASCADE,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_description_responsibility_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_description_responsibility_registration_date = models.DateTimeField(default=datetime.datetime.now())   
      
class JobDescriptionRequirementModel(models.Model):
    
    class Meta:
        db_table = "recruiter_job_desc_requirement_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    job_description_requirement_id = models.CharField(max_length=100, primary_key= True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    job_requirement = models.ForeignKey(JobRequirementModel,on_delete=models.CASCADE,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_description_requirement_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_description_requirement_registration_date = models.DateTimeField(default=datetime.datetime.now()) 

class JobDescriptionBenefitsModel(models.Model):    
    class Meta:
        db_table = "recruiter_job_desc_benefit_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    job_description_benefit_id = models.CharField(max_length=100, primary_key= True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    job_benefit = models.ForeignKey(JobBenefitModel,on_delete=models.CASCADE,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_description_benefit_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_description_benefit_registration_date = models.DateTimeField(default=datetime.datetime.now())        
    
#############################################################################################################################

class CompanyModel(models.Model):
    
    class Meta:
        db_table = "recruiter_company_information_tb"
        
    company_info_id = models.CharField(max_length=100,primary_key=True,default=None)
    company_name= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_description= models.CharField(max_length=200,blank=False,null=False,default=None)
    company_established_year= models.CharField(max_length=100,blank=False,null=False,default=None)
    location = models.ForeignKey(LocationModel,on_delete=models.CASCADE,default=None, blank=True, null=True)
    contact_number= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_email= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_googlelink= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_linkdinlink= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_team_member= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_twitter_link= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_facebook_link= models.CharField(max_length=100,blank=False,null=False,default=None)
    sector = models.ForeignKey(SectorModel, on_delete=models.CASCADE, default=None)
    company_type = models.ForeignKey(CompanyTypeModel, on_delete=models.CASCADE, default=None)
    company_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    company_registration_date = models.DateTimeField(default=datetime.datetime.now()) 

class CompanyLocationModel(models.Model):
    
    class Meta:
        db_table = "recruiter_company_location_tb"
        
    company_location_id = models.CharField(max_length=100,primary_key=True,default=None)
    company_info = models.ForeignKey(CompanyModel,on_delete=models.CASCADE,default=None)
    location = models.ForeignKey(LocationModel,on_delete=models.CASCADE,default=None)
    is_headquarter= models.CharField(max_length=100,blank=False,null=False,default=None)
    company_address =models.TextField(blank=False, null=False, default=None)
    company_location_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    company_location_registration_date = models.DateTimeField(default=datetime.datetime.now()) 
    
class JobDescriptionCompanyLocationModel(models.Model):
    class Meta:
        db_table = "recruiter_Job_description_company_location_tb"
    Job_description_company_location_id = models.CharField(max_length=100,primary_key=True,default=None)
    company_location = models.ForeignKey(CompanyLocationModel,on_delete=models.CASCADE,default=None)
    work_place = models.ForeignKey(WorkPlaceModel,on_delete=models.CASCADE,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    Job_description_company_location_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    Job_description_company_location_registration_date = models.DateTimeField(default=datetime.datetime.now()) 
    
class JobDescriptionEmploymentTypeModel(models.Model):
    class Meta:
        db_table = "recruiter_Job_description_employment_type_tb"
    Job_description_employment_type_id = models.CharField(max_length=100,primary_key=True,default=None)
    employment_type= models.ForeignKey(EmploymentTypeModel,on_delete=models.CASCADE,default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    Job_description_employment_type_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    Job_description_employment_type_registration_date = models.DateTimeField(default=datetime.datetime.now()) 
    
class UserCompanyModel(models.Model):
    
    class Meta:
        db_table = "recruiter_user_company_tb"
        
    user_company_id = models.CharField(max_length=100,primary_key=True,default=None)
    company_info = models.ForeignKey(CompanyModel,on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    user_company_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    user_company_registration_date = models.DateTimeField(default=datetime.datetime.now()) 
    
#############################################################################################################################

class NationalityJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_nationality_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    nationality_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    nationality = models.ForeignKey(NationalityModel,on_delete=models.CASCADE,default=None)
    nationality_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    nationality_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    nationality_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())

class GenderJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_gender_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    gender_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    gender= models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    gender_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    gender_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())

class WorkPlaceJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_work_place_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    work_place_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    work_place = models.ForeignKey(WorkPlaceModel,on_delete=models.CASCADE,default=None)
    work_place_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    work_place_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    work_place_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())

class LanguageJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_language_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    language_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    language = models.ForeignKey(LanguageModel,on_delete=models.CASCADE,default=None)
    language_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    language_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    language_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JoiningPeriodJobDescriptionModel(models.Model):
    class Meta:
        db_table = "recruiter_joiningperiod_job_desc_tb"
        
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    joining_period_job_description_id = models.CharField(max_length=100, primary_key= True, default=None)
    joining_period = models.ForeignKey(JoiningPeriodModel,on_delete=models.CASCADE,default=None)
    joining_period_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    joining_period_job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    joining_period_job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())

class RecruiterBulkResumeUploadModel(models.Model):
    
    class Meta:
        db_table = "recruiter_bulk_resume_upload_tb"

    recruiter_bulk_resume_upload_id = models.CharField(max_length= 60, primary_key=True) 
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE) #user id
    recruiter_bulk_resume_upload = models.FileField(upload_to='recruiter_resumesUpload/',default=None, blank=True)
    recruiter_bulk_resume_upload_registration_date = models.DateTimeField(default=datetime.datetime.now())

class RecruiterExtractedZipFileModel(models.Model):
    
    class Meta:
        db_table = "recruiter_resume_extracted_file_tb"

    recruiter_resume_extracted_file_id = models.CharField(max_length= 60, primary_key=True) 
    recruiter_bulk_resume_upload = models.ForeignKey(RecruiterBulkResumeUploadModel,on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE) #user id
    resume_file_path = models.TextField(blank=True, null=True, default=None)
    resume_extracted_text = models.TextField(blank=True, null=True, default=None)
    recruiter_resume_extracted_file_registration_date = models.DateTimeField(default=datetime.datetime.now())