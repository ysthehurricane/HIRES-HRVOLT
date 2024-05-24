from rest_framework import serializers
from .models import *
import re
import string
import random
from datetime import datetime

class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectorModel
        fields = ["sector_name","sector_action","sector_name_arabic"]
    
    def validate(self, data):
        sector_name=data["sector_name"]
    
        if sector_name == None or sector_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Sector name is required'})
        data["sector_name"] = data["sector_name"].lower()
        return data

class JobPositionSerializer(serializers.ModelSerializer):

    sector_id = serializers.PrimaryKeyRelatedField(queryset=SectorModel.objects.all(), source='sector')

    class Meta:
        model = JobPositionModel
        fields = ["job_position_name","sector_id","job_position_action","job_position_name_arabic"]

    def validate(self, data):
        job_position_name=data["job_position_name"]

        if job_position_name == None or job_position_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Job Position name is required'})
        data["job_position_name"] = data["job_position_name"].lower()
        return data

class JobLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobLevelModel
        fields = ["job_level_name","job_level_action","job_level_name_arabic"]
    
    def validate(self, data):
        job_level_name=data["job_level_name"]
    
        if job_level_name == None or job_level_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Job level name is required'})
        data["job_level_name"] = data["job_level_name"].lower()
        return data

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationModel
        fields = ["location_name","location_action","location_name_arabic"]
    
    def validate(self, data):
        location_name=data["location_name"]
    
        if location_name == None or location_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Location name is required'})
        data["location_name"] = data["location_name"].lower()
        return data

class CompanyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyTypeModel
        fields = ["company_type_name", "company_type_action","company_type_name_arabic"]
    
    def validate(self, data):
        company_type_name=data["company_type_name"]
    
        if company_type_name == None or company_type_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Company Type name is required'})
        data["company_type_name"] = data["company_type_name"].lower()
        return data

class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlaceModel
        fields = ["work_place_name","work_place_action","work_place_name_arabic"]
    
    def validate(self, data):
        work_place_name=data["work_place_name"]
    
        if work_place_name == None or work_place_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Work Place name is required'})
        data["work_place_name"] = data["work_place_name"].lower()
        return data

class EmploymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmploymentTypeModel
        fields = ["employment_type_name", "employment_type_action","employment_type_name_arabic"]
    
    def validate(self, data):
        employment_type_name=data["employment_type_name"]
    
        if employment_type_name == None or employment_type_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Employment Type name is required'})
        data["employment_type_name"] = data["employment_type_name"].lower()
        return data

class JoiningPeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = JoiningPeriodModel
        fields = ["joining_period_name","joining_period_action","joining_period_name_arabic"]
    
    def validate(self, data):
        joining_period_name=data["joining_period_name"]
    
        if joining_period_name == None or joining_period_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Joining Period name is required'})
        data["joining_period_name"] = data["joining_period_name"].lower()
        return data


class UniqueTechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkillsUniqueModel
        fields = [ "unique_technical_skills_name", "unique_technical_skills_category", "unique_technical_skills_action","unique_technical_skills_name_arabic","unique_technical_skills_category_arabic"]
    def validate(self, data):
        unique_technical_skills_name=data["unique_technical_skills_name"]
        if unique_technical_skills_name == None or unique_technical_skills_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Technical Skills name is required'})
        data["unique_technical_skills_name"] = data["unique_technical_skills_name"].lower()
        data["unique_technical_skills_category"] = data["unique_technical_skills_category"].lower()
        return data

class MainTechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
    technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all())
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = TechnicalSkillsMainModel
        fields = [ "job_position_id", "job_level_id", "technical_skills_id", "technical_skills_name", "technical_skills_category", "technical_skills_action","technical_skills_name_arabic","technical_skills_category_arabic"]
    def validate(self, data):
        return data

class TechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = TechnicalSkillsModel
        fields = [ "job_position_id", "job_level_id", "technical_skills_name", "technical_skills_name_arabic","technical_skills_category_arabic", "technical_skills_category", "technical_skills_action"]

    def validate(self, data):
        technical_skills_name=data["technical_skills_name"]
    
        if technical_skills_name == None or technical_skills_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Technical Skills name is required'})
        data["technical_skills_name"] = data["technical_skills_name"].lower()
        data["technical_skills_category"] = data["technical_skills_category"].lower()
        return data
        
# class HaveToTechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
#     technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsModel.objects.all(), source='technical_skills')
#     job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
#     job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

#     class Meta:
#         model = HaveToTechnicalSkillsModel
#         fields = ["technical_skills_id", "job_position_id", "job_level_id", "have_to_technical_skills_name", "have_to_technical_skills_category"]

#     def validate(self, data):
        
#         return data

# class OptionalTechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
#     technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsModel.objects.all(), source='technical_skills')
#     job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
#     job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

#     class Meta:
#         model = OptionalTechnicalSkillsModel
#         fields = ["technical_skills_id", "job_position_id", "job_level_id", "optional_technical_skills_name", "optional_technical_skills_category"]

#     def validate(self, data):
        
        # return data

class HaveToTechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
    technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsMainModel.objects.all(), source='technical_skills')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    main_unique_technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='main_unique_technical_skills')
    class Meta:
        model = HaveToTechnicalSkillsModel

        fields = ["technical_skills_id", "main_unique_technical_skills_id", "job_position_id", "job_level_id", "have_to_technical_skills_name","have_to_technical_skills_name_arabic","have_to_technical_skills_category","have_to_technical_skills_category_arabic","have_to_technical_skills_action"]

    def validate(self, data):

        print('iioioio', data)
        return data
        
class OptionalTechnicalSkillsDetailsSerializer(serializers.ModelSerializer):
    technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsMainModel.objects.all(), source='technical_skills')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    main_unique_technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='main_unique_technical_skills')
    class Meta:
        model = OptionalTechnicalSkillsModel
        fields = ["technical_skills_id","main_unique_technical_skills_id", "job_position_id", "job_level_id", "optional_technical_skills_name", "optional_technical_skills_name_arabic","optional_technical_skills_category","optional_technical_skills_category_arabic","optional_technical_skills_action"]
    def validate(self, data):
        return data

class SoftSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoftSkillsModel
        fields = ["soft_skills_name","soft_skills_action","soft_skills_name_arabic"]
    
    def validate(self, data):
        soft_skills_name=data["soft_skills_name"]
    
        if soft_skills_name == None or soft_skills_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Soft Skills name is required'})
        data["soft_skills_name"] = data["soft_skills_name"].lower()
        return data

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageModel
        fields = ["language_name","language_action","language_name_arabic"]
    
    def validate(self, data):
        language_name=data["language_name"]
    
        if language_name == None or language_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Language name is required'})
        data["language_name"] = data["language_name"].lower()
        return data

class JobRequirementSerializer(serializers.ModelSerializer):
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = JobRequirementModel
        fields = [ "job_position_id", "job_level_id", "job_requirement_description", "job_requirement_action","job_requirement_description_arabic"]

    def validate(self, data):
        job_requirement_description=data["job_requirement_description"]
    
        if job_requirement_description == None or job_requirement_description == "":
            raise serializers.ValidationError({'errorMsg' : 'Job Requirement name is required'})
        data["job_requirement_description"] = data["job_requirement_description"].lower()

        return data

class JobBenefitSerializer(serializers.ModelSerializer):
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = JobBenefitModel
        fields = [ "job_position_id", "job_level_id", "job_benefit_description", "job_benefit_action","job_benefit_description_arabic"]

    def validate(self, data):
        job_benefit_description=data["job_benefit_description"]
    
        if job_benefit_description == None or job_benefit_description == "":
            raise serializers.ValidationError({'errorMsg' : 'Job Benefit name is required'})
        data["job_benefit_description"] = data["job_benefit_description"].lower()
        
        return data

class JobResponsibilitySerializer(serializers.ModelSerializer):
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = JobResponsibilityModel
        fields = [ "job_position_id", "job_level_id", "job_responsibility_description", "job_responsibility_action","job_responsibility_description_arabic"]

    def validate(self, data):
        job_responsibility_description=data["job_responsibility_description"]
    
        if job_responsibility_description == None or job_responsibility_description == "":
            raise serializers.ValidationError({'errorMsg' : 'Job Responibility name is required'})
        data["job_responsibility_description"] = data["job_responsibility_description"].lower()
        
        return data

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationModel
        fields = ["education_name", "education_years","education_action","education_years_arabic","education_name_arabic"]
    def validate(self, data):
        education_name=data["education_name"]
        education_years=data["education_years"]
        if education_name == None or education_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Education name is required'})
        if education_years == None or education_years == "":
            raise serializers.ValidationError({'errorMsg' : 'Education years is required'})
        data["education_name"] = data["education_name"].lower()
        return data

class EducationFieldSerializer(serializers.ModelSerializer):
    sector_id = serializers.PrimaryKeyRelatedField(queryset=SectorModel.objects.all(), source='sector')
    class Meta:
        model = EducationFieldModel
        fields = ["education_field_name", "sector_id","education_field_action","education_field_name_arabic"]
    def validate(self, data):
        education_field_name=data["education_field_name"]
        if education_field_name == None or education_field_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Education name is required'})
        data["education_field_name"] = data["education_field_name"].lower()
        return data

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalityModel
        fields = ["nationality_name","nationality_action","nationality_name_arabic"]
    def validate(self, data):
        nationality_name=data["nationality_name"]
        if nationality_name == None or nationality_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Nationality name is required'})
        data["nationality_name"] = data["nationality_name"].lower()
        return data

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityModel
        fields = ["university_name","university_action","university_name_arabic"]
    def validate(self, data):
        university_name=data["university_name"]
        if university_name == None or university_name == "":
            raise serializers.ValidationError({'errorMsg' : 'University name is required'})
        data["university_name"] = data["university_name"].lower()
        return data
        
class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegreeModel
        fields = ["degree_name","degree_action","degree_name_arabic"]
    def validate(self, data):
        degree_name=data["degree_name"]
        if degree_name == None or degree_name == "":
            raise serializers.ValidationError({'errorMsg' : 'degree name is required'})
        data["degree_name"] = data["degree_name"].lower()
        return data