# from django.db import models
# import datetime
# from databaseAPI.models import *
# from userloginAPI.models import *
# from candidateresumeAPI.models import *
# from candidateReportAnalysisAPI.models import *

# ######## Basic Education ################### 

# class CandidateBasicEducationHistoryDetails(models.Model):

#     class Meta:
#         db_table = "candidate_resume_basic_education_hist_tb"

    
#     candidate_resume_basic_education_hist_id = models.CharField(max_length= 100, primary_key=True)
#     user = models.ForeignKey(NewUser, on_delete=models.CASCADE,default=None) #user id
#     candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
#     candidate_last_education = models.ForeignKey(EducationModel,on_delete=models.CASCADE,default="select")
#     candidate_last_education_field = models.ForeignKey(EducationFieldModel,on_delete=models.CASCADE,default="select")
#     candidate_total_years_education_hist = models.CharField(max_length= 10, blank=True, null=True, default= None) #except drop year
#     candidate_education_year_drop_hist = models.BooleanField(default=False) #drop in education
#     candidate_resume_education_register_hist_at = models.DateTimeField(default=datetime.datetime.now())

# ######## Main Education ################### 
    
# class CandidateMainEducationHistoryDetails(models.Model):

#     class Meta:
#         db_table = "candidate_resume_main_education_hist_tb"

#     candidate_resume_main_education_hist_id = models.CharField(max_length= 100, primary_key=True)
#     user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None) #user id
#     candidate_report_analysis = models.ForeignKey(CandidateReportAnalysisModel, on_delete=models.CASCADE, default=None)
#     candidate_degree_name_hist = models.TextField(blank=True, null=True, default=None)
#     candidate_univeresity_name_hist = models.TextField(blank=True, null=True, default=None)
#     candidate_result_class_hist = models.CharField(max_length = 40, blank=True, null= True, default=None)
#     candidate_start_year_hist = models.CharField(max_length= 10,blank=True, null=True, default= None)
#     candidate_end_year_hist = models.CharField(max_length= 10,blank=True, null=True, default= None)
#     candidate_summary_hist = models.TextField(blank=True, null=False, default=None)
#     candidate_resume_main_education_hist_register_at = models.DateTimeField(default=datetime.datetime.now())
