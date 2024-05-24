from rest_framework import serializers
from .models import *
import re
import string
import random
from datetime import datetime
from databaseAPI.models import *

class MainEducationWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = MainEducationWeightageModel
        fields = ["job_level_id","main_education_total_weightage"]
    
    def validate(self, data):
        return data
    
class EducationCategoriesWeightageserializer(serializers.ModelSerializer):

    main_education_weightage_id = serializers.PrimaryKeyRelatedField(queryset=MainEducationWeightageModel.objects.all(), source='main_education_weightage')
    education_id = serializers.PrimaryKeyRelatedField(queryset=EducationModel.objects.all(), source='education')
    class Meta:
        model = EducationCategoriesWeightageModel
        fields = ["main_education_weightage_id","education_id","education_categories_weightage"]
    
    def validate(self, data):
        return data
    
class MainExperienceWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    
    class Meta:
        model = MainExperienceWeightageModel
        fields = ["job_level_id","per_internship_weightage","Total_internship_weightage","per_month_experience_weightage", "Total_experience_weightage"]
    
    def validate(self, data):
        return data
    
class TechnicalSkillWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    
    class Meta:
        model = TechnicalSkillWeightageModel
        fields = ["job_level_id","per_technical_skill_weightage","Total_technical_skill_weightage","per_haveto_technical_skill_weightage", "per_optional_technical_skill_weightage"]
    
    def validate(self, data):
        return data
    
class SoftSkillWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    
    class Meta:
        model = SoftSkillWeightageModel
        fields = ["job_level_id","per_soft_skill_weightage","Total_soft_skill_weightage"]
    
    def validate(self, data):
        return data
    
class CurricularActivitiesWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    
    class Meta:
        model = CurricularActivitiesWeightageModel
        fields = ["job_level_id","per_curricular_activity_weightage","Total_curricular_activity_weightage"]
    
    def validate(self, data):
        return data
    
class AnyDropWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    
    class Meta:
        model = AnyDropWeightageModel
        fields = ["job_level_id","any_drop_weightage"]
    
    def validate(self, data):
        return data
    
class ProjectWeightageserializer(serializers.ModelSerializer):

    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    
    class Meta:
        model = ProjectWeightageModel
        fields = ["job_level_id","per_project_weightage","Total_project_weightage"]
    
    def validate(self, data):
        return data
    
