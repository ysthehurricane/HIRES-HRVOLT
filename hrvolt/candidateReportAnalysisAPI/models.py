from django.db import models
import datetime
from databaseAPI.models import *
from userloginAPI.models import *
from candidateresumeAPI.models import *

class CandidateReportAnalysisModel(models.Model):

    class Meta:
        db_table = "candidate_report_tb"

    candidate_report_analysis_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    education = models.ForeignKey(EducationModel, on_delete=models.CASCADE, default=None, null=False)
    education_field = models.ForeignKey(EducationFieldModel, on_delete=models.CASCADE, default=None)
    candidate_education_score = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_education_relevancy = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_technical_skills = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_haveto_skills = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_optional_skills = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_technical_skill_weightage = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_relevant_projects = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_projects = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_project_relevant_score = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_month_experience = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_relevant_field_experience = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_number_of_internship = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_relevant_experience_score = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_softskill = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_total_softskill_score = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_number_of_curriculum_activities = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_number_of_curriculum_activity_score = models.CharField(max_length=100,blank=True, null=True, default=None)
    is_candidate_any_drop_year = models.CharField(max_length=100,blank=True, null=True, default=None)
    candidate_drop_year_penalty_score = models.CharField(max_length=100,blank=True, null=True, default=None)
    
    candidate_report_analysis_registration_date = models.DateTimeField(default=datetime.datetime.now())

######## Basic Education ################### 

class CandidateBasicEducationHistoryDetails(models.Model):

    class Meta:
        db_table = "candidate_resume_basic_education_hist_tb"

    
    candidate_resume_basic_education_hist_id = models.CharField(max_length= 100, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE,default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_last_education = models.ForeignKey(EducationModel,on_delete=models.CASCADE,default="select")
    candidate_last_education_field = models.ForeignKey(EducationFieldModel,on_delete=models.CASCADE,default="select")
    candidate_total_years_education_hist = models.CharField(max_length= 10, blank=True, null=True, default= None) #except drop year
    candidate_education_year_drop_hist = models.BooleanField(default=False) #drop in education
    candidate_resume_education_register_hist_at = models.DateTimeField(default=datetime.datetime.now())

######## Main Education ################### 
    
class CandidateMainEducationHistoryDetails(models.Model):

    class Meta:
        db_table = "candidate_resume_main_education_hist_tb"

    candidate_resume_main_education_hist_id = models.CharField(max_length= 100, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_degree_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_univeresity_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_result_class_hist = models.CharField(max_length = 40, blank=True, null= True, default=None)
    candidate_start_year_hist = models.CharField(max_length= 10,blank=True, null=True, default= None)
    candidate_end_year_hist = models.CharField(max_length= 10,blank=True, null=True, default= None)
    candidate_summary_hist = models.TextField(blank=True, null=False, default=None)
    candidate_resume_main_education_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

######## Technical Skills ################### 

class candidateReportHavetoTechSkillModel(models.Model):
    class Meta:
        db_table = "candidate_report_haveto_technical_skill_tb"
    candidate_report_haveto_tech_skill_id = models.CharField(max_length= 120, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    technical_skills = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None) #django, python developer
    have_to_technical_skills_name = models.TextField(blank=True, null=True, default=None) 
    candidate_report_haveto_tech_skill_registration_date = models.DateTimeField(default=datetime.datetime.now())

class candidateReportOptionalTechSkillModel(models.Model):
    class Meta:
        db_table = "candidate_report_optional_technical_skill_tb"
    candidate_report_optional_tech_skill_id = models.CharField(max_length= 120, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    technical_skills = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None) #django, python developer
    optional_technical_skills_name = models.TextField(blank=True, null=True, default=None) 
    candidate_report_optional_tech_skill_registration_date = models.DateTimeField(default=datetime.datetime.now())

class candidateReportTechSkillHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_report_technical_skill_history_tb"
    candidate_report_technical_skill_history_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    technical_skills_name = models.TextField(blank=True, null=True, default=None)
    candidate_technical_skill_status = models.CharField(max_length=100,blank=True, null=True, default=None) #have_to, optional
    candidate_report_tech_skill_hist_registration_date = models.DateTimeField(default=datetime.datetime.now())


#############################################
    

###### Projects #############################
    

class candidateReportAnalysisProjectRelevantSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_report_project_relevant_tech_skills_tb"
    candidate_report_project_relevant_skills_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_resume_project_technical_skill = models.ForeignKey(CandidateProjectTechnicalSkillsModel, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_resume_project = models.ForeignKey(CandidateProjectModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None) #django, python developer
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_report_project_relevant_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

class candidateReportAnalysisProjectNonRelevantSkillsModel(models.Model):
    class Meta:
        db_table = "candidate_report_proj_non_relevant_tech_skills_tb"
    candidate_report_project_non_relevant_skills_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_resume_project_technical_skill = models.ForeignKey(CandidateProjectTechnicalSkillsModel, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_resume_project = models.ForeignKey(CandidateProjectModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None) #django, python developer
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default=None)
    candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None) # senior,junior
    candidate_report_project_non_relevant_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

class candidateReportAnalysisProjectRelevancyModel(models.Model):
    class Meta:
        db_table = "candidate_report_project_relevant_tb"
    candidate_report_project_relevancy_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_resume_project = models.ForeignKey(CandidateProjectModel, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_project_relevant = models.CharField(max_length=100,blank=True, null=True, default=None) #yes, no
    candidate_report_project_relevancy_registration_date = models.DateTimeField(default=datetime.datetime.now())


class candidateReportAnalysisProjectHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_report_analysis_project_history_tb"
    candidate_report_project_hist_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_project_name = models.TextField(blank=True, null=True, default=None)
    candidate_project_start_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_end_date  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_url = models.TextField(blank=True, null=True, default=None)
    candidate_project_description = models.TextField(blank=True, null=True, default=None)
    candidate_project_relevant = models.CharField(max_length=100,blank=True, null=True, default=None) #yes, no
    candidate_report_project_hist_registration_date = models.DateTimeField(default=datetime.datetime.now())

class candidateReportAnalysisProjectTechnicalSkillHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_report_project_technical_skill_history_tb"
    candidate_report_project_tech_skill_hist_id = models.CharField(max_length= 80, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_report_project_history = models.ForeignKey(candidateReportAnalysisProjectHistoryModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill_name = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_project_technical_skill_relevant = models.CharField(max_length=100,blank=True, null=True, default=None) #yes, no
    candidate_report_project_tech_skill_hist_registration_date = models.DateTimeField(default=datetime.datetime.now())


##############################################
    
###### Basic Experience #############################
    

class CandidateBasicExperienceHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_basic_experience_hist_tb"

    candidate_resume_basic_experience_hist_id = models.CharField(max_length= 100, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE,default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_total_years_of_experience_hist = models.CharField(max_length= 10, blank=True, null=True, default= None)
    candidate_total_years_of_experience_applied_for_hist = models.CharField(max_length= 10, blank=True, null=True, default= None) 
    candidate_total_internship_hist = models.CharField(max_length= 10, blank=True, null=True, default= None) 
    candidate_works_companies_hist = models.CharField(max_length= 10, blank=True, null=True, default= None)
    candidate_field_transition_hist = models.BooleanField(default=False) 
    candidate_works_startup_hist = models.BooleanField(default=False) 
    candidate_works_MNC_hist = models.BooleanField(default=False) 
    candidate_resume_basic_experience_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

##############################################
    
###### Main Experience #############################
    

class CandidateMainExperienceHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_main_experience_hist_tb"

    candidate_resume_main_experience_hist_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE, default="select")
    candidate_work_place = models.ForeignKey(WorkPlaceModel,on_delete=models.CASCADE,default="select") # offline, online, remote, hybrid
    candidate_company_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_job_level =  models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default="select") # senior,junior
    candidate_company_location_hist = models.TextField(blank=True, null=True,default="select")
    candidate_job_start_year_hist = models.CharField(max_length= 10, blank=True, null=True, default= "select")
    candidate_job_end_year_hist = models.CharField(max_length= 10, blank=True, null=True, default= "select")
    candidate_job_description_hist = models.TextField(blank=True, null=False, default=None)
    candidate_resume_main_experience_hist_register_at = models.DateTimeField(default=datetime.datetime.now())


###################################################
    
######## Soft skills ##############################
    
class CandidateSoftskillsHistoryModel(models.Model):
    
    class Meta:
        db_table = "candidate_resume_soft_skills_hist_tb"
    
    candidate_resume_soft_skills_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_soft_skill_name_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_soft_skill_level_hist = models.CharField(max_length=100,blank=True,null=True,default=None)# beginner, advance #intermmediate
    candidate_resume_soft_skills_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

###################################################
    
######## hackathon ##############################
    

class CandidatehackathonHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_hackathon_hist_tb"

    candidate_resume_hackathon_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_hackathon_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_mode_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_organisation_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_certificateID_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_type_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_field_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_participate_certificate_hist = models.FileField(upload_to='candidate_hackathons/',default=None, blank=True)
    candidate_hackathon_certificate_issue_date_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_hackathon_certificateURL_hist = models.TextField(blank=True, null=True, default=None)
    candidate_hackathon_description_hist = models.TextField(blank=True, null=True, default=None)
    
    candidate_resume_hackathon_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateHackathonTechnicalSkillsHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_resume_hackathon_technical_skill_hist_tb"

    candidate_resume_hackathon_tech_skill_hist_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_hackathon = models.ForeignKey(CandidatehackathonModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_resume_hackathon_technical_skill_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

###################################################
    
######## contribution ##############################
    
class CandidateContributionHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_contribution_hist_tb"

    candidate_resume_contribution_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_contribution_topic_hist = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_keyword_hist = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_organisation_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_certificateID_hist = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_certificateURL_hist = models.TextField(blank=True, null=True, default=None)
    candidate_contribution_participate_certificate_hist = models.FileField(upload_to='candidate_contributions/',default=None, blank=True)
    candidate_contribution_publish_date_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_contribution_certificate_issue_date_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_contribution_summary_hist = models.TextField(blank=True, null=True, default=None)
    candidate_resume_contribution_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateContributionTechnicalSkillsHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_resume_contribution_tech_skill_hist_tb"

    candidate_resume_contribution_technical_skill_hist_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_contribution = models.ForeignKey(CandidateContributionModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_resume_contribution_technical_skill_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

###################################################
    
######## workshop ##############################
    
class CandidateWorkshopHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_workshop_hist_tb"

    candidate_resume_workshop_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_workshop_organisation_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_type_hist = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_topic_hist = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_certificateID_hist = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_certificateURL_hist = models.TextField(blank=True, null=True, default=None)
    candidate_workshop_participate_certificate_hist = models.FileField(upload_to='candidate_workshops/',default=None, blank=True)
    candidate_workshop_duration_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_workshop_certificate_issue_date_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_workshop_description_hist = models.TextField(blank=True, null=True, default=None)
    candidate_resume_workshop_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateWorkshopTechnicalSkillsHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_resume_workshop_technical_skill_hist_tb"

    candidate_resume_workshop_technical_skill_hist_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_workshop = models.ForeignKey(CandidateWorkshopModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_resume_workshop_tech_skill_hist_register_at = models.DateTimeField(default=datetime.datetime.now())


###################################################
    
######## seminar ##############################
    
class CandidateSeminarHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_seminar_hist_tb"

    candidate_resume_seminar_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_seminar_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_host_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_type_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_organisation_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_mode_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_topic_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_certificateID_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_certificateURL_hist = models.TextField(blank=True, null=True, default=None)
    candidate_seminar_participate_certificate_hist = models.FileField(upload_to='candidate_seminars/',default=None, blank=True)
    candidate_seminar_certificate_issue_date_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_seminar_description_hist = models.TextField(blank=True, null=True, default=None)
    candidate_resume_seminar_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

###################################################
    
######## competition ##############################

class CandidateCompetitionHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_competition_hist_tb"

    candidate_resume_competition_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_competition_organisation_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_competition_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_competition_type_hist = models.TextField(blank=True, null=True, default=None)
    candidate_competition_mode_hist = models.TextField(blank=True, null=True, default=None)
    candidate_competition_certificateID_hist = models.TextField(blank=True, null=True, default=None)
    candidate_competition_certificateURL_hist = models.TextField(blank=True, null=True, default=None)
    candidate_competition_participate_certificate_hist = models.FileField(upload_to='candidate_competitions/',default=None, blank=True)
    candidate_competition_certificate_issue_date_hist  = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_competition_description_hist = models.TextField(blank=True, null=True, default=None)
    candidate_resume_competition_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateCompetitionTechnicalSkillsHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_resume_competition_technical_skill_hist_tb"

    candidate_resume_competition_tech_skill_hist_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_competition = models.ForeignKey(CandidateCompetitionModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_resume_competition_tech_skill_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

###################################################
    
######## competition ##############################
    

class CandidateCertificateHistoryModel(models.Model):

    class Meta:
        db_table = "candidate_resume_certificate_hist_tb"

    candidate_resume_certificate_hist_id = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_certificate_organisation_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_name_hist = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_certificateID_hist = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_certificateURL_hist = models.TextField(blank=True, null=True, default=None)
    candidate_certificate_participate_certificate_hist = models.FileField(upload_to='candidate_certificates/',default=None, blank=True)
    candidate_certificate_issue_date_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_certificate_expire_date_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_certificate_description_hist = models.TextField(blank=True, null=True, default=None)
    candidate_resume_certificate_hist_register_at = models.DateTimeField(default=datetime.datetime.now())

class CandidateCertificateTechnicalSkillsHistoryModel(models.Model):
    class Meta:
        db_table = "candidate_resume_certificate_technical_skill_hist_tb"

    candidate_resume_certificate_tech_skill_hist_id = models.CharField(max_length= 60, primary_key=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
    candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
    candidate_certificate = models.ForeignKey(CandidateCertificateModel, on_delete=models.CASCADE, default=None)
    candidate_technical_skill = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE, default= None)
    candidate_technical_skill_name_hist = models.CharField(max_length= 100, blank=True, null=True, default=None)
    candidate_resume_certificate_tech_skill_hist_register_at = models.DateTimeField(default=datetime.datetime.now())