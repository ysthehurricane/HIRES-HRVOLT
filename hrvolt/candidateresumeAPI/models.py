from django.db import models
import datetime
from userloginAPI.models import NewUser
from databaseAPI.models import *


class CandidateUserResumeUpload(models.Model):
    
    class Meta:
        db_table = "candidate_resume_Upload_tb"

    candidate_resumeUpload_id = models.CharField(max_length= 60, primary_key=True) #id of resume
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE) #user id
    candidate_resumeUpload = models.FileField(upload_to='resumes/')
    candidate_uploaded_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateUserCoverLetterUpload(models.Model): 

    class Meta:
        db_table = "candidate_resume_coverletter_tb"

    coverletter_id = models.CharField(max_length= 60, primary_key=True) #id of resume
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE) #user id
    candidate_coverletter = models.FileField(upload_to='coverletter/')
    candidate_uploaded_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateBasicEducationDetails(models.Model):

    class Meta:
        db_table = "candidate_resume_basic_education_tb"

    
    candidate_resume_basic_education_id = models.CharField(max_length= 100, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE,default=None) #user id
    candidate_last_education = models.ForeignKey(EducationModel,on_delete=models.CASCADE,default="select")
    candidate_last_education_field = models.ForeignKey(EducationFieldModel,on_delete=models.CASCADE,default="select")
    candidate_total_years_education = models.CharField(max_length= 10, blank=True, null=True, default= None) #except drop year
    candidate_total_years_education_arabic = models.CharField(max_length= 10, blank=True, null=True, default= None) #except drop year
    candidate_education_year_drop = models.BooleanField(default=False) #drop in education
    candidate_resume_education_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateMainEducationDetails(models.Model):

    class Meta:
        db_table = "candidate_resume_main_education_tb"

    candidate_resume_main_education_id = models.CharField(max_length= 100, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_degree_name = models.TextField(blank=True, null=True, default=None)
    candidate_univeresity_name = models.TextField(blank=True, null=True, default=None)
    candidate_result_class = models.CharField(max_length = 40, blank=True, null= True, default=None)
    candidate_start_year = models.CharField(max_length= 10,blank=True, null=True, default= None)
    candidate_end_year = models.CharField(max_length= 10,blank=True, null=True, default= None)
    candidate_summary = models.TextField(blank=True, null=False, default=None)
    candidate_degree_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_univeresity_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_result_class_arabic = models.CharField(max_length = 40, blank=True, null= True, default=None)
    candidate_start_year_arabic = models.CharField(max_length= 10,blank=True, null=True, default= None)
    candidate_end_year_arabic = models.CharField(max_length= 10,blank=True, null=True, default= None)
    candidate_summary_arabic = models.TextField(blank=True, null=False, default=None)
    candidate_resume_main_education_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateBasicExperienceModel(models.Model):

    class Meta:
        db_table = "candidate_resume_basic_experience_tb"

    candidate_resume_basic_experience_id = models.CharField(max_length= 100, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE,default=None) #user id
    candidate_total_years_of_experience = models.CharField(max_length= 10, blank=True, null=True, default= None)
    candidate_total_years_of_experience_applied_for = models.CharField(max_length= 10, blank=True, null=True, default= None) 
    candidate_total_internship = models.CharField(max_length= 10, blank=True, null=True, default= None) 
    candidate_works_companies = models.CharField(max_length= 10, blank=True, null=True, default= None)
    candidate_total_years_of_experience_arabic = models.CharField(max_length= 10, blank=True, null=True, default= None)
    candidate_total_years_of_experience_applied_for_arabic = models.CharField(max_length= 10, blank=True, null=True, default= None) 
    candidate_total_internship_arabic = models.CharField(max_length= 10, blank=True, null=True, default= None) 
    candidate_works_companies_arabic = models.CharField(max_length= 10, blank=True, null=True, default= None)
    candidate_field_transition = models.BooleanField(default=False) 
    candidate_works_startup = models.BooleanField(default=False) 
    candidate_works_MNC = models.BooleanField(default=False) 
    candidate_resume_basic_experience_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateMainExperienceModel(models.Model):

    class Meta:
        db_table = "candidate_resume_main_experience_tb"

    candidate_resume_main_experience_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default="select")
    candidate_work_place = models.ForeignKey(WorkPlaceModel,on_delete=models.CASCADE,default="select") # offline, online, remote, hybrid
    candidate_company_name = models.TextField(blank=True, null=True, default=None)
    candidate_company_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default="select") # senior,junior
    candidate_company_location = models.TextField(blank=True, null=True,default="select")
    candidate_company_location_arabic = models.TextField(blank=True, null=True,default="select")
    candidate_job_start_year = models.CharField(max_length= 10, blank=True, null=True, default= "select")
    candidate_job_end_year = models.CharField(max_length= 10, blank=True, null=True, default= "select")
    candidate_job_start_year_arabic = models.CharField(max_length= 10, blank=True, null=True, default= "select")
    candidate_job_end_year_arabic = models.CharField(max_length= 10, blank=True, null=True, default= "select")
    candidate_job_description = models.TextField(blank=True, null=False, default=None)
    candidate_job_description_arabic = models.TextField(blank=True, null=False, default=None)
    candidate_resume_main_experience_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateMainExperienceTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_main_experience_technical_skill_tb"

    candidate_resume_main_experience_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_main_experience = models.ForeignKey(CandidateMainExperienceModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_resume_main_experience_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateTechnicalskillsModel(models.Model):
    
    class Meta:
        db_table = "candidate_resume_technical_skills_tb"
    
    candidate_resume_technical_skills_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_level = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_level_arabic = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_resume_technical_skills_register_at = models.DateTimeField(default=datetime.datetime.now())


class CandidateSoftskillsModel(models.Model):
    
    class Meta:
        db_table = "candidate_resume_soft_skills_tb"
    
    candidate_resume_soft_skills_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_soft_skill = models.ForeignKey(SoftSkillsModel, on_delete=models.CASCADE, default= None)
    candidate_soft_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_soft_skill_level = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_soft_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_soft_skill_level_arabic = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_resume_soft_skills_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateLanguageModel(models.Model):
    
    class Meta:
        db_table = "candidate_resume_language_tb"
    
    candidate_resume_language_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_language = models.ForeignKey(LanguageModel, on_delete=models.CASCADE, default= None)
    candidate_language_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_language_level = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_language_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_language_level_arabic = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_resume_language_register_at = models.DateTimeField(default=datetime.datetime.now())
    
class CandidateProjectModel(models.Model):

    class Meta:
        db_table = "candidate_resume_project_tb"

    candidate_resume_project_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_project_name = models.TextField(blank=True, null=True, default=None)
    candidate_project_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_project_start_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_start_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_end_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_end_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_url = models.TextField(blank=True, null=True, default=None)
    candidate_resumeUpload = models.FileField(upload_to='candidate_projects/',default=None, blank=True)
    candidate_project_description = models.TextField(blank=True, null=True, default=None)
    candidate_project_description_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_resume_project_register_at = models.DateTimeField(default=datetime.datetime.now())

# class CandidateProjectTechnicalSkillsModel(models.Model):
#     class Meta:
#         db_table = "candidate_resume_projects_technical_skill_tb"

#     candidate_resume_project_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
#     user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
#     candidate_project = models.ForeignKey(CandidateProjectModel, on_delete=models.CASCADE, default=None)
#     candidate_technical_skill = models.ForeignKey(TechnicalSkillsModel, on_delete=models.CASCADE, default= None)
#     candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
#     candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
#     candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
#     candidate_resume_project_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateProjectTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_projects_technical_skill_tb"
    candidate_resume_project_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_project = models.ForeignKey(CandidateProjectModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_resume_project_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidatehackathonModel(models.Model):

    class Meta:
        db_table = "candidate_resume_hackathon_tb"

    candidate_resume_hackathon_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_hackathon_name = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_mode = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_mode_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_organisation_name = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_organisation_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_certificateID = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_certificateID_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_type = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_type_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_field = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_field_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_participate_certificate = models.FileField(upload_to='candidate_hackathons/',default=None, blank=True)
    candidate_hackathon_certificate_issue_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_hackathon_certificate_issue_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_hackathon_certificateURL = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_description = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_description_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_resume_hackathon_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateHackathonTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_hackathon_technical_skill_tb"

    candidate_resume_hackathon_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_hackathon = models.ForeignKey(CandidatehackathonModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    # candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    # candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_resume_hackathon_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateContributionModel(models.Model):

    class Meta:
        db_table = "candidate_resume_contribution_tb"

    candidate_resume_contribution_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_contribution_topic = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_topic_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_keyword = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_keyword_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_organisation_name = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_organisation_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_certificateID = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_certificateID_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_certificateURL = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_participate_certificate = models.FileField(upload_to='candidate_contributions/',default=None, blank=True)
    candidate_contribution_publish_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_contribution_publish_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_contribution_certificate_issue_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_contribution_certificate_issue_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_contribution_summary = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_summary_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_resume_contribution_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateContributionTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_contribution_technical_skill_tb"

    candidate_resume_contribution_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_contribution = models.ForeignKey(CandidateContributionModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    # candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    # candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_resume_contribution_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateWorkshopModel(models.Model):

    class Meta:
        db_table = "candidate_resume_workshop_tb"

    candidate_resume_workshop_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_workshop_organisation_name = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_organisation_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_name = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_type = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_type_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_topic = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_topic_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_certificateID = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_certificateID_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_certificateURL = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_participate_certificate = models.FileField(upload_to='candidate_workshops/',default=None, blank=True)
    candidate_workshop_duration  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_workshop_duration_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_workshop_certificate_issue_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_workshop_certificate_issue_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_workshop_description = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_description_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_resume_workshop_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateWorkshopTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_workshop_technical_skill_tb"

    candidate_resume_workshop_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_workshop = models.ForeignKey(CandidateWorkshopModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    # candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    # candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_resume_workshop_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateSeminarModel(models.Model):

    class Meta:
        db_table = "candidate_resume_seminar_tb"

    candidate_resume_seminar_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_seminar_name = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_name_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_seminar_host = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_host_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_seminar_type = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_type_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_seminar_organisation_name = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_organisation_name_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_seminar_mode = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_mode_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_topic = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_topic_arabic = models.TextField(blank=True, null=True, default=None)
    
    candidate_seminar_certificateID = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_certificateID_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_seminar_certificateURL = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_participate_certificate = models.FileField(upload_to='candidate_seminars/',default=None, blank=True)
    candidate_seminar_certificate_issue_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_seminar_certificate_issue_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    
    candidate_seminar_description = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_description_arabic = models.TextField(blank=True, null=True, default=None)
    
    candidate_resume_seminar_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateCompetitionModel(models.Model):

    class Meta:
        db_table = "candidate_resume_competition_tb"

    candidate_resume_competition_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_competition_organisation_name = models.TextField(blank=True, null=True, default=None)
    candidate_competition_organisation_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_competition_name = models.TextField(blank=True, null=True, default=None)
    candidate_competition_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_competition_type = models.TextField(blank=True, null=True, default=None)
    candidate_competition_type_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_competition_mode = models.TextField(blank=True, null=True, default=None)
    candidate_competition_mode_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_competition_certificateID = models.TextField(blank=True, null=True, default=None)
    candidate_competition_certificateID_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_competition_certificateURL = models.TextField(blank=True, null=True, default=None)
    candidate_competition_participate_certificate = models.FileField(upload_to='candidate_competitions/',default=None, blank=True)
    candidate_competition_certificate_issue_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_competition_certificate_issue_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_competition_description = models.TextField(blank=True, null=True, default=None)
    candidate_competition_description_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_resume_competition_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateCompetitionTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_competition_technical_skill_tb"

    candidate_resume_competition_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_competition = models.ForeignKey(CandidateCompetitionModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)
    # candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    # candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_resume_competition_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateCertificateModel(models.Model):

    class Meta:
        db_table = "candidate_resume_certificate_tb"

    candidate_resume_certificate_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_certificate_organisation_name = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_organisation_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_name = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_name_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_certificateID = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_certificateID_arabic = models.TextField(blank=True, null=True, default=None)

    candidate_certificate_certificateURL = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_participate_certificate = models.FileField(upload_to='candidate_certificates/',default=None, blank=True)
    candidate_certificate_issue_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_certificate_issue_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_certificate_expire_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_certificate_expire_date_arabic  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_certificate_description = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_description_arabic = models.TextField(blank=True, null=True, default=None)
    candidate_resume_certificate_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateCertificateTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_resume_certificate_technical_skill_tb"

    candidate_resume_certificate_technical_skill_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_certificate = models.ForeignKey(CandidateCertificateModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_technical_skill_name_arabic = models.CharField(max_length= 100, blank=True, null=True, default=None)

    # candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    # candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_resume_certificate_technical_skill_register_at = models.DateTimeField(default=datetime.datetime.now())