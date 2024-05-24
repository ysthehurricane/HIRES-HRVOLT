from django.db import models
import datetime
from databaseAPI.models import *
# Create your models here.

class MainEducationWeightageModel(models.Model):
    class Meta:
        db_table = "main_education_weightage_tb"
    main_education_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    main_education_total_weightage =  models.CharField(max_length=60,blank=True,null=True,default=None)
    main_education_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class EducationCategoriesWeightageModel(models.Model):
    class Meta:
        db_table = "main_education_categories_weightage_tb"
    education_categories_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    main_education_weightage = models.ForeignKey(MainEducationWeightageModel, on_delete=models.CASCADE, default=None)
    education = models.ForeignKey(EducationModel, on_delete=models.CASCADE, default=None)
    education_categories_weightage =  models.CharField(max_length=60,blank=True,null=True,default=None)
    education_categories_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class MainExperienceWeightageModel(models.Model):
    class Meta:
        db_table = "main_experience_weightage_tb"
    main_experience_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    per_internship_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Total_internship_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    per_month_experience_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Total_experience_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Non_relevant_experience_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    main_experience_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class TechnicalSkillWeightageModel(models.Model):
    class Meta:
        db_table = "main_technical_skill_weightage_tb"
    main_technical_skill_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    per_technical_skill_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Total_technical_skill_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    per_haveto_technical_skill_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    per_optional_technical_skill_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    main_technical_skill_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class SoftSkillWeightageModel(models.Model):
    class Meta:
        db_table = "main_soft_skill_weightage_tb"
    main_soft_skill_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    per_soft_skill_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Total_soft_skill_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    main_soft_skill_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CurricularActivitiesWeightageModel(models.Model):
    class Meta:
        db_table = "main_curricular_activity_weightage_tb"
    main_curricular_activity_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    per_curricular_activity_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Total_curricular_activity_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    main_curricular_activity_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class AnyDropWeightageModel(models.Model):
    class Meta:
        db_table = "main_any_drop_weightage_tb"
    main_any_drop_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    any_drop_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    main_any_drop_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())

class ProjectWeightageModel(models.Model):
    class Meta:
        db_table = "main_project_weightage_tb"
    main_project_weightage_id = models.CharField(max_length= 60, primary_key=True, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    per_project_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    Total_project_weightage = models.CharField(max_length=60,blank=True,null=True,default=None)
    main_project_weightage_registration_date = models.DateTimeField(default=datetime.datetime.now())