from rest_framework import serializers
from .models import *
from userloginAPI.models import NewUser
from databaseAPI.models import *


# from django.utils.translation import gettext_lazy as _

import re

import string
import random
from datetime import datetime

class CandidateUserResumeUploadSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateUserResumeUpload
        fields = ['candidate_resumeUpload_id','user_id', 'candidate_resumeUpload', 'candidate_uploaded_at']

    def validate(self, data):

        resume_file = data["candidate_resumeUpload"]

        if not resume_file:
            raise serializers.ValidationError({"errorMsg": 'File is required'})
        
        if not resume_file.name.lower().endswith('.pdf') and not resume_file.name.lower().endswith('.doc') and not resume_file.name.lower().endswith('.docx'):
            
            raise serializers.ValidationError({"errorMsg": "unsupported file extension. Only PDF and DOC files are allowed."})

        return data

class GetUserResumeSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateUserResumeUpload
        fields = ['candidate_resumeUpload_id','user_id']

    def validate(self, data):
        
        return data

class CandidateUserCoverLetterUploadSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateUserCoverLetterUpload
        fields = ['coverletter_id','user_id', 'candidate_coverletter', 'candidate_uploaded_at']

    def validate(self, data):

        resume_file = data["candidate_coverletter"]

        if not resume_file:
            raise serializers.ValidationError({"errorMsg": 'File is required'})
        
        if not resume_file.name.lower().endswith('.pdf') and not resume_file.name.lower().endswith('.doc') and not resume_file.name.lower().endswith('.docx'):
            raise serializers.ValidationError({"errorMsg": "unsupported file extension. Only PDF and DOC files are allowed."})

        return data


class CandidateBasicEducationDetailsSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_last_education_id = serializers.PrimaryKeyRelatedField(queryset=EducationModel.objects.all(), source='candidate_last_education')
    candidate_last_education_field_id = serializers.PrimaryKeyRelatedField(queryset=EducationFieldModel.objects.all(), source='candidate_last_education_field')


    class Meta:
        model = CandidateBasicEducationDetails
        fields = ["user_id", "candidate_last_education_id", "candidate_last_education_field_id", "candidate_total_years_education", "candidate_education_year_drop","candidate_total_years_education_arabic"]

    def validate(self, data):

        candidate_total_years_education = data["candidate_total_years_education"]

        if candidate_total_years_education == None or candidate_total_years_education == "":
            raise serializers.ValidationError({'errorMsg':'Years of education is required'})

        if not str(candidate_total_years_education).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})

        return data    


class CandidateMainEducationDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    class Meta:
        model = CandidateMainEducationDetails
        fields = ["user_id", "candidate_degree_name", "candidate_univeresity_name", "candidate_result_class", "candidate_start_year", "candidate_end_year", "candidate_summary","candidate_degree_name_arabic","candidate_univeresity_name_arabic","candidate_result_class_arabic","candidate_start_year_arabic","candidate_end_year_arabic","candidate_summary_arabic"]
    def validate(self, data):
        candidate_degree_name = data["candidate_degree_name"]
        candidate_univeresity_name = data["candidate_univeresity_name"]
        candidate_result_class = data["candidate_result_class"]
        candidate_start_year = data["candidate_start_year"]
        candidate_end_year = data["candidate_end_year"]
        if candidate_degree_name == None or candidate_degree_name == "":
            raise serializers.ValidationError({'errorMsg':'Degree Name is required'})
        if candidate_univeresity_name == None or candidate_univeresity_name == "":
            raise serializers.ValidationError({'errorMsg':'University Name is required'})
        if candidate_result_class == None or candidate_result_class == "":
            raise serializers.ValidationError({'errorMsg':'Result class is required'})
        if candidate_start_year == None or candidate_start_year == "":
            raise serializers.ValidationError({'errorMsg':'Starting Year is required'})
        if candidate_end_year == None or candidate_end_year == "":
            raise serializers.ValidationError({'errorMsg':'Ending Year is required'})
        data["candidate_degree_name"] = data["candidate_degree_name"].lower()
        data["candidate_univeresity_name"] = data["candidate_univeresity_name"].lower()
        data["candidate_result_class"] = data["candidate_result_class"].lower()
        data["candidate_start_year"] = data["candidate_start_year"].lower()
        data["candidate_end_year"] = data["candidate_end_year"].lower()
        return data
    
class CandidateBasicExperienceSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateBasicExperienceModel
        fields = ["user_id", "candidate_total_years_of_experience", "candidate_total_years_of_experience_applied_for", "candidate_total_internship", "candidate_works_companies", "candidate_field_transition", "candidate_works_startup", "candidate_works_MNC","candidate_total_years_of_experience_arabic","candidate_total_years_of_experience_applied_for_arabic","candidate_total_internship_arabic","candidate_works_companies_arabic"]

    def validate(self, data):

        candidate_total_years_of_experience = data["candidate_total_years_of_experience"]
        candidate_total_years_of_experience_applied_for = data["candidate_total_years_of_experience_applied_for"]
        candidate_total_internship = data["candidate_total_internship"]
        candidate_works_companies = data["candidate_works_companies"]
        candidate_field_transition = data["candidate_field_transition"]
        candidate_works_startup = data["candidate_works_startup"]
        candidate_works_MNC = data["candidate_works_MNC"]

        if candidate_total_years_of_experience == None or candidate_total_years_of_experience == "":
            raise serializers.ValidationError({'errorMsg':'Degree Name is required'})

        if not str(candidate_total_years_of_experience).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})

        if candidate_total_years_of_experience_applied_for == None or candidate_total_years_of_experience_applied_for == "":
            raise serializers.ValidationError({'errorMsg':'University Name is required'})

        if not str(candidate_total_years_of_experience_applied_for).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})

        if candidate_total_internship == None or candidate_total_internship == "":
            raise serializers.ValidationError({'errorMsg':'Result class is required'})
        
        if not str(candidate_total_internship).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})

        if candidate_works_companies == None or candidate_works_companies == "":
            raise serializers.ValidationError({'errorMsg':'number of work companies is required'})
        
        if not str(candidate_works_companies).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})
        
        if candidate_field_transition == None or candidate_field_transition == "":
            data["candidate_field_transition"] = False

        if candidate_works_startup == None or candidate_works_startup == "":
            data["candidate_works_startup"] = False

        if candidate_works_MNC == None or candidate_works_MNC == "":
            data["candidate_works_MNC"] = False
            
            # raise serializers.ValidationError({'errorMsg':'selection is required'})

        
        # if candidate_works_startup == None or candidate_works_startup == "":
        #     raise serializers.ValidationError({'errorMsg':'selection is required'})

        # if candidate_works_MNC == None or candidate_works_MNC == "":
        #     raise serializers.ValidationError({'errorMsg':'selection is required'})
        
        return data

class CandidateMainExperienceSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_work_place_id = serializers.PrimaryKeyRelatedField(queryset=WorkPlaceModel.objects.all(), source='candidate_work_place')
    candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

    class Meta:
        model = CandidateMainExperienceModel
        fields = ["user_id", "candidate_job_position_id", "candidate_work_place_id", "candidate_company_name", "candidate_job_level_id", "candidate_company_location", "candidate_job_start_year", "candidate_job_end_year", "candidate_job_description","candidate_company_name_arabic","candidate_company_location_arabic","candidate_job_start_year_arabic","candidate_job_end_year_arabic","candidate_job_description_arabic"]

    def validate(self, data):

        candidate_job_position = data["candidate_job_position"]
        candidate_work_place = data["candidate_work_place"]
        candidate_company_name = data["candidate_company_name"]
        candidate_job_level = data["candidate_job_level"]
        candidate_company_location = data["candidate_company_location"]
        candidate_job_start_year = data["candidate_job_start_year"]
        candidate_job_end_year = data["candidate_job_end_year"]
        candidate_job_description = data["candidate_job_description"]

        if candidate_job_position == "select" or candidate_job_position == "":
            raise serializers.ValidationError({'errorMsg':'Job Position is required'})

        if candidate_work_place == "select" or candidate_work_place == "":
            raise serializers.ValidationError({'errorMsg':'selection is required'})

        if candidate_company_name == None or candidate_company_name == "":
            raise serializers.ValidationError({'errorMsg':'Company Name is required'})

        if candidate_job_level == "select" or candidate_job_level == "":
            raise serializers.ValidationError({'errorMsg':'selection is required'})

        if candidate_company_location == "select" or candidate_company_location == "":
            raise serializers.ValidationError({'errorMsg':'selection is required'})
        
        if not str(candidate_job_start_year).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})

        if not str(candidate_job_end_year).isdigit():
            raise serializers.ValidationError({'errorMsg':'Only number is required'})

        data["candidate_job_description"] = data["candidate_job_description"].lower()
        return data

# class CandidateMainExperienceTechnicalSkillsSerializer(serializers.ModelSerializer):

#     user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
#     candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
#     candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsModel.objects.all(), source='candidate_technical_skill')
#     candidate_main_experience_id = serializers.PrimaryKeyRelatedField(queryset=CandidateMainExperienceModel.objects.all(), source='candidate_main_experience')
#     candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

#     class Meta:
#         model = CandidateMainExperienceTechnicalSkillsModel
#         fields = ["user_id", "candidate_main_experience_id", "candidate_technical_skill_id","candidate_job_position_id", "candidate_job_level_id","candidate_technical_skill_name"]

#     def validate(self, data):

#         return data

class CandidateMainExperienceTechnicalSkillsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_main_experience_id = serializers.PrimaryKeyRelatedField(queryset=CandidateMainExperienceModel.objects.all(), source='candidate_main_experience')
    candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')
    class Meta:
        model = CandidateMainExperienceTechnicalSkillsModel
        fields = ["user_id", "candidate_main_experience_id", "candidate_technical_skill_id","candidate_job_position_id", "candidate_job_level_id","candidate_technical_skill_name","candidate_technical_skill_name_arabic"]
    def validate(self, data):
        return data

class CandidateTechnicalskillserializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')

    class Meta:
        model = CandidateTechnicalskillsModel
        fields = ["user_id", "candidate_technical_skill_id", "candidate_technical_skill_name","candidate_technical_skill_level","candidate_technical_skill_name_arabic","candidate_technical_skill_level_arabic"]

    def validate(self, data):

        return data

class CandidateSoftskillserializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_soft_skill_id = serializers.PrimaryKeyRelatedField(queryset=SoftSkillsModel.objects.all(), source='candidate_soft_skill')

    class Meta:
        model = CandidateSoftskillsModel
        fields = ["user_id", "candidate_soft_skill_id", "candidate_soft_skill_name","candidate_soft_skill_level","candidate_soft_skill_name_arabic","candidate_soft_skill_level_arabic"]

    def validate(self, data):

        return data

class CandidateLanguageserializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_language_id = serializers.PrimaryKeyRelatedField(queryset=LanguageModel.objects.all(), source='candidate_language')

    class Meta:
        model = CandidateLanguageModel
        fields = ["user_id", "candidate_language_id", "candidate_language_name","candidate_language_level","candidate_language_name_arabic","candidate_language_level_arabic"]

    def validate(self, data):

        return data
        
class CandidateProjectSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:

        model = CandidateProjectModel
        fields = ['user_id', 'candidate_project_name', 'candidate_project_start_date', 'candidate_project_end_date', 'candidate_project_url', 'candidate_project_description',"candidate_project_name_arabic","candidate_project_start_date_arabic","candidate_project_end_date_arabic","candidate_project_description_arabic"]

    def validate(self, data):
        
        candidate_project_name = data["candidate_project_name"]
        if candidate_project_name == None or candidate_project_name == "":
            raise serializers.ValidationError({'errorMsg':'Company project Name is required'})
        data["candidate_project_name"] = data["candidate_project_name"].capitalize()
        data["candidate_project_description"] = data["candidate_project_description"].lower()
        return data

# class CandidateProjectTechnicalSkillsSerializer(serializers.ModelSerializer):

#     user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
#     candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
#     candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsModel.objects.all(), source='candidate_technical_skill')
#     candidate_project_id = serializers.PrimaryKeyRelatedField(queryset=CandidateProjectModel.objects.all(), source='candidate_project')
#     candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

#     class Meta:
#         model = CandidateProjectTechnicalSkillsModel
#         fields = ["user_id", "candidate_project_id", "candidate_technical_skill_id","candidate_technical_skill_name","candidate_job_position_id","candidate_job_level_id"]

#     def validate(self, data):

#         return data   

class CandidateProjectTechnicalSkillsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_project_id = serializers.PrimaryKeyRelatedField(queryset=CandidateProjectModel.objects.all(), source='candidate_project')
    class Meta:
        model = CandidateProjectTechnicalSkillsModel
        fields = ["user_id", "candidate_project_id", "candidate_technical_skill_id","candidate_technical_skill_name","candidate_technical_skill_name_arabic"]
    def validate(self, data):
        return data

class CandidatehackathonSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidatehackathonModel
        fields = ['user_id', 'candidate_hackathon_name', 'candidate_hackathon_mode','candidate_hackathon_organisation_name','candidate_hackathon_certificateID', 'candidate_hackathon_type', 'candidate_hackathon_field', 'candidate_hackathon_certificate_issue_date','candidate_hackathon_certificateURL','candidate_hackathon_description','candidate_hackathon_name_arabic','candidate_hackathon_mode_arabic','candidate_hackathon_organisation_name_arabic','candidate_hackathon_certificateID_arabic','candidate_hackathon_type_arabic','candidate_hackathon_field_arabic','candidate_hackathon_certificate_issue_date_arabic','candidate_hackathon_description_arabic']

    def validate(self, data):

        candidate_hackathon_name = data["candidate_hackathon_name"]
        if candidate_hackathon_name == None or candidate_hackathon_name == "":
            raise serializers.ValidationError({'errorMsg':'hackathon Name is required'})

        data["candidate_hackathon_name"] = data["candidate_hackathon_name"].capitalize()
        data["candidate_hackathon_description"] = data["candidate_hackathon_description"].lower()

        return data 

class CandidateHackathonTechnicalSkillsSerializer(serializers.ModelSerializer):


    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    # candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_hackathon_id = serializers.PrimaryKeyRelatedField(queryset=CandidatehackathonModel.objects.all(), source='candidate_hackathon')
    # candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

    class Meta:
        model = CandidateHackathonTechnicalSkillsModel
        fields = ["user_id", "candidate_hackathon_id", "candidate_technical_skill_id","candidate_technical_skill_name",'candidate_technical_skill_name_arabic']

    def validate(self, data):

        return data       
    
class CandidateContributionSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateContributionModel
        fields = ['user_id', 'candidate_contribution_topic', 'candidate_contribution_keyword','candidate_contribution_organisation_name','candidate_contribution_certificateID', 'candidate_contribution_certificateURL', 'candidate_contribution_publish_date','candidate_contribution_certificate_issue_date','candidate_contribution_summary','candidate_contribution_topic_arabic','candidate_contribution_keyword_arabic','candidate_contribution_organisation_name_arabic','candidate_contribution_certificateID_arabic','candidate_contribution_publish_date_arabic','candidate_contribution_certificate_issue_date_arabic','candidate_contribution_summary_arabic']

    def validate(self, data):

        candidate_contribution_topic = data["candidate_contribution_topic"]
        if candidate_contribution_topic == None or candidate_contribution_topic == "":
            raise serializers.ValidationError({'errorMsg':'contribution Name is required'})

        data["candidate_contribution_topic"] = data["candidate_contribution_topic"].capitalize()
        data["candidate_contribution_summary"] = data["candidate_contribution_summary"].lower()

        return data 
    
class CandidateContributionTechnicalSkillsSerializer(serializers.ModelSerializer):


    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    # candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_contribution_id = serializers.PrimaryKeyRelatedField(queryset=CandidateContributionModel.objects.all(), source='candidate_contribution')
    # candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

    class Meta:
        model = CandidateContributionTechnicalSkillsModel
        fields = ["user_id", "candidate_contribution_id", "candidate_technical_skill_id","candidate_technical_skill_name",'candidate_technical_skill_name_arabic']

    def validate(self, data):

        return data       

class CandidateWorkshopSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateWorkshopModel
        fields = ['user_id', 'candidate_workshop_organisation_name', 'candidate_workshop_name','candidate_workshop_type','candidate_workshop_topic', 'candidate_workshop_certificateID','candidate_workshop_certificateURL', 'candidate_workshop_duration','candidate_workshop_certificate_issue_date','candidate_workshop_description','candidate_workshop_organisation_name_arabic','candidate_workshop_name_arabic','candidate_workshop_type_arabic','candidate_workshop_topic_arabic','candidate_workshop_certificateID_arabic','candidate_workshop_duration_arabic','candidate_workshop_certificate_issue_date_arabic','candidate_workshop_description_arabic']

    def validate(self, data):

        candidate_workshop_name = data["candidate_workshop_name"]
        candidate_workshop_topic = data["candidate_workshop_topic"]
        candidate_workshop_organisation_name = data["candidate_workshop_organisation_name"]

        if candidate_workshop_name == None or candidate_workshop_name == "":
            raise serializers.ValidationError({'errorMsg':'Workshop Name is required'})
        if candidate_workshop_topic == None or candidate_workshop_topic == "":
            raise serializers.ValidationError({'errorMsg':'Workshop topic is required'})
        if candidate_workshop_organisation_name == None or candidate_workshop_organisation_name == "":
            raise serializers.ValidationError({'errorMsg':'Workshop organisation Name is required'})

        data["candidate_workshop_name"] = data["candidate_workshop_name"].capitalize()
        data["candidate_workshop_topic"] = data["candidate_workshop_topic"].capitalize()
        data["candidate_workshop_organisation_name"] = data["candidate_workshop_organisation_name"].capitalize()
        data["candidate_workshop_description"] = data["candidate_workshop_description"].lower()

        return data 
    
class CandidateWorkshopTechnicalSkillsSerializer(serializers.ModelSerializer):


    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    # candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_workshop_id = serializers.PrimaryKeyRelatedField(queryset=CandidateWorkshopModel.objects.all(), source='candidate_workshop')
    # candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

    class Meta:
        model = CandidateWorkshopTechnicalSkillsModel
        fields = ["user_id", "candidate_workshop_id", "candidate_technical_skill_id","candidate_technical_skill_name","candidate_technical_skill_name_arabic"]

    def validate(self, data):

        return data
    
class CandidateSeminarSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateSeminarModel
        fields = ['user_id', 'candidate_seminar_name', 'candidate_seminar_host','candidate_seminar_type','candidate_seminar_organisation_name', 'candidate_seminar_mode', 'candidate_seminar_topic','candidate_seminar_certificateID', 'candidate_seminar_certificateURL','candidate_seminar_certificate_issue_date','candidate_seminar_description','candidate_seminar_name_arabic','candidate_seminar_host_arabic','candidate_seminar_type_arabic','candidate_seminar_organisation_name_arabic','candidate_seminar_mode_arabic','candidate_seminar_topic_arabic','candidate_seminar_certificateID_arabic','candidate_seminar_certificate_issue_date_arabic','candidate_seminar_description_arabic']

    def validate(self, data):

        # candidate_seminar_description = data["candidate_seminar_description"]
        candidate_seminar_organisation_name = data["candidate_seminar_organisation_name"]
        candidate_seminar_name = data["candidate_seminar_name"]

        # if candidate_seminar_description == None or candidate_seminar_description == "":
        #     raise serializers.ValidationError({'errorMsg':'Workshop Name is required'})
        if candidate_seminar_organisation_name == None or candidate_seminar_organisation_name == "":
            raise serializers.ValidationError({'errorMsg':'Workshop topic is required'})
        if candidate_seminar_name == None or candidate_seminar_name == "":
            raise serializers.ValidationError({'errorMsg':'Workshop organisation Name is required'})

        data["candidate_seminar_host"] = data["candidate_seminar_host"].capitalize()
        data["candidate_seminar_organisation_name"] = data["candidate_seminar_organisation_name"].capitalize()
        data["candidate_seminar_name"] = data["candidate_seminar_name"].capitalize()
        data["candidate_seminar_description"] = data["candidate_seminar_description"].lower()

        return data
    
class CandidateCompetitionSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateCompetitionModel
        fields = ['user_id', 'candidate_competition_organisation_name', 'candidate_competition_name','candidate_competition_type','candidate_competition_mode', 'candidate_competition_certificateID', 'candidate_competition_certificateURL','candidate_competition_certificate_issue_date','candidate_competition_description','candidate_competition_organisation_name_arabic','candidate_competition_name_arabic','candidate_competition_type_arabic','candidate_competition_mode_arabic','candidate_competition_certificateID_arabic','candidate_competition_certificate_issue_date_arabic','candidate_competition_description_arabic']

    def validate(self, data):

        candidate_competition_name = data["candidate_competition_name"]
        if candidate_competition_name == None or candidate_competition_name == "":
            raise serializers.ValidationError({'errorMsg':'Competition Name is required'})

        data["candidate_competition_name"] = data["candidate_competition_name"].lower()
        data["candidate_competition_description"] = data["candidate_competition_description"].lower()

        return data 
    
class CandidateCompetitionTechnicalSkillsSerializer(serializers.ModelSerializer):


    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    # candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_competition_id = serializers.PrimaryKeyRelatedField(queryset=CandidateCompetitionModel.objects.all(), source='candidate_competition')
    # candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

    class Meta:
        model = CandidateCompetitionTechnicalSkillsModel
        fields = ["user_id", "candidate_competition_id", "candidate_technical_skill_id","candidate_technical_skill_name","candidate_technical_skill_name_arabic"]

    def validate(self, data):

        return data 

class CandidateCertificateSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = CandidateCertificateModel
        fields = ['user_id', 'candidate_certificate_organisation_name', 'candidate_certificate_name', 'candidate_certificate_certificateID', 'candidate_certificate_certificateURL','candidate_certificate_issue_date','candidate_certificate_expire_date','candidate_certificate_description','candidate_certificate_organisation_name_arabic','candidate_certificate_name_arabic','candidate_certificate_certificateID_arabic','candidate_certificate_issue_date_arabic','candidate_certificate_expire_date_arabic','candidate_certificate_description_arabic']

    def validate(self, data):

        candidate_certificate_name = data["candidate_certificate_name"]
        if candidate_certificate_name == None or candidate_certificate_name == "":
            raise serializers.ValidationError({'errorMsg':'Certificate Name is required'})

        data["candidate_certificate_name"] = data["candidate_certificate_name"].lower()
        data["candidate_certificate_description"] = data["candidate_certificate_description"].lower()

        return data 
    
class CandidateCertificateTechnicalSkillsSerializer(serializers.ModelSerializer):


    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    # candidate_job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='candidate_job_position')
    candidate_technical_skill_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='candidate_technical_skill')
    candidate_certificate_id = serializers.PrimaryKeyRelatedField(queryset=CandidateCertificateModel.objects.all(), source='candidate_certificate')
    # candidate_job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='candidate_job_level')

    class Meta:
        model = CandidateCertificateTechnicalSkillsModel
        fields = ["user_id", "candidate_certificate_id", "candidate_technical_skill_id","candidate_technical_skill_name","candidate_technical_skill_name_arabic"]

    def validate(self, data):

        return data      
