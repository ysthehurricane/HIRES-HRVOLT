from rest_framework import serializers
from .models import *
import re
import os
link_regex_pattern = r'^https?://[^\s]+$'


class JobDescriptionSerializer(serializers.ModelSerializer):
    
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = JobDescriptionModel
        fields = [ "job_position_id", "job_level_id", "salary_min", "salary_max","number_of_vacancy","user_id","job_level_name","job_position_name","job_tilte", "job_description_action"]

    def validate(self, data):
        salary_min=data["salary_min"]
        salary_max=data["salary_max"]
        job_tilte = data["job_tilte"]
        number_of_vacancy = data["number_of_vacancy"]
        
        if not str(salary_min).isdigit():
            raise serializers.ValidationError({'errorMsg': 'Enter only digits'})

        if not str(salary_max).isdigit():
            raise serializers.ValidationError({'errorMsg': 'Enter only digits'})

        if job_tilte == None or job_tilte =="":
            raise serializers.ValidationError({'errorMsg' : 'job_tilte is required'})
        
        if number_of_vacancy == None or number_of_vacancy == "" or  not str(number_of_vacancy).isdigit():
            raise serializers.ValidationError({'errorMsg' : 'Number of vacancy is required'})
        
        
        return data
    
class EducationJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    education_id = serializers.PrimaryKeyRelatedField(queryset=EducationModel.objects.all(), source='education')
    class Meta:
        model = EducationJobDescriptionModel
        fields = ["user_id", "job_description_id","education_id","education_name"]
    def validate(self, data):
        return data


class EducationFieldJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    education_field_id = serializers.PrimaryKeyRelatedField(queryset=EducationFieldModel.objects.all(), source='education_field')
    class Meta:
        model = EducationFieldJobDescriptionModel
        fields = ["user_id", "job_description_id","education_field_id","education_field_name"]
    def validate(self, data):
        return data

class SoftSkillsJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    soft_skills_id = serializers.PrimaryKeyRelatedField(queryset=SoftSkillsModel.objects.all(), source='soft_skills')

    class Meta:
        model = SoftSkillJobDescriptionModel
        fields = ["user_id", "job_description_id", "soft_skills_id", "soft_skills_name"]
    def validate(self, data):
        return data

class TechnicalSkillsJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    technical_skills_id = serializers.PrimaryKeyRelatedField(queryset=TechnicalSkillsUniqueModel.objects.all(), source='technical_skills')

    class Meta:
        model = TechnicalSkillJobDescriptionModel
        fields = ["user_id", "job_description_id", "technical_skills_id", "technical_skills_name"]
    def validate(self, data):
        return data

class CustomJobDescriptionResponsibilitySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

    class Meta:
        model = CustomJobDescriptionResponsibilityModel
        fields = ["user_id", "job_description_id", "job_position_id", "job_position_name","responsibilities_description","job_level_id","job_level_name"]
        
        
    def validate(self, data):
        responsibilities_description = data['responsibilities_description']
        if responsibilities_description == None or responsibilities_description == "" :
            raise serializers.ValidationError({'errorMsg' : 'Responsibilities Description is required'})
        
        data['responsibilities_description'] = data['responsibilities_description'].lower()

        return data
    
class CustomJobDescriptionRequirementSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

    class Meta:
        model = CustomJobDescriptionRequirementsModel
        fields = ["user_id", "job_description_id", "job_position_id", "job_position_name","requirement_description","job_level_id","job_level_name"]
        
        
    def validate(self, data):
        requirement_description = data['requirement_description']
        if requirement_description == None or requirement_description == "" :
            raise serializers.ValidationError({'errorMsg' : 'Requirement Description is required'})
        
        data['requirement_description'] = data['requirement_description'].lower()

        return data

class CustomJobDescriptionBenefitSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

    class Meta:
        model = CustomJobDescriptionBenefitsModel
        fields = ["user_id", "job_description_id", "job_position_id", "job_position_name","benefit_description","job_level_id","job_level_name"]
        
        
    def validate(self, data):
        benefit_description = data['benefit_description']
        if benefit_description == None or benefit_description == "" :
            raise serializers.ValidationError({'errorMsg' : 'Benefit Description is required'})
        
        data['benefit_description'] = data['benefit_description'].lower()

        return data

class JobDescriptionResponsibilitySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    job_responsibility_id = serializers.PrimaryKeyRelatedField(queryset=JobResponsibilityModel.objects.all(), source='job_responsibility')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

    class Meta:
        model = JobDescriptionResponsibilityModel
        fields = ["user_id", "job_description_id", "job_responsibility_id","job_position_id","job_level_id","job_position_name","job_level_name"]
        
        
    def validate(self, data):
        return data
    
class JobDescriptionRequirementSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    job_requirement_id = serializers.PrimaryKeyRelatedField(queryset=JobRequirementModel.objects.all(), source='job_requirement')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

    class Meta:
        model =  JobDescriptionRequirementModel
        fields = ["user_id", "job_description_id", "job_requirement_id","job_position_id","job_level_id","job_position_name","job_level_name"]
        
        
    def validate(self, data):
        return data

class JobDescriptionBenefitSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    job_benefit_id = serializers.PrimaryKeyRelatedField(queryset=JobBenefitModel.objects.all(), source='job_benefit')
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')

    class Meta:
        model = JobDescriptionBenefitsModel
        fields = ["user_id", "job_description_id", "job_benefit_id","job_position_id","job_level_id","job_position_name","job_level_name"]
        
        
    def validate(self, data):
        return data  

class CompanySerializer(serializers.ModelSerializer):
    sector_id = serializers.PrimaryKeyRelatedField(queryset=SectorModel.objects.all(), source='sector')
    company_type_id = serializers.PrimaryKeyRelatedField(queryset=CompanyTypeModel.objects.all(), source='company_type')
    class Meta:
        model = CompanyModel
        fields = ['company_name','company_description','company_established_year','contact_number','company_email',
                  'company_googlelink','company_linkdinlink','company_type_id','company_team_member',
                  'company_twitter_link','company_facebook_link','sector_id']
    def validate(self, data):
        company_name= data['company_name']
        
        if company_name == None or company_name =="":
            raise serializers.ValidationError({'errorMsg' : 'company_name is required'})
       
        data['company_name']= data['company_name'].lower()

        return data    

class CompanyLocationSerializer(serializers.ModelSerializer):
    company_info_id = serializers.PrimaryKeyRelatedField(queryset=CompanyModel.objects.all(), source='company_info')
    location_id = serializers.PrimaryKeyRelatedField(queryset=LocationModel.objects.all(), source='location')

    class Meta:
        model = CompanyLocationModel
        fields = ["is_headquarter","location_id","company_info_id","company_address"]
            
    def validate(self, data):
        company_address= data['company_address']
        
        if company_address == None or company_address =="":
            raise serializers.ValidationError({'errorMsg' : 'company_address is required'})
        
        data['company_address'] = data['company_address'].lower()
        
        return data    
    
class JobDescritionEmploymentTypeSerializer(serializers.ModelSerializer):
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    employment_type_id = serializers.PrimaryKeyRelatedField(queryset=EmploymentTypeModel.objects.all(), source='employment_type')

    class Meta:
        model = JobDescriptionEmploymentTypeModel
        fields = ["job_description_id","employment_type_id", "Job_description_employment_type_action"]
            
    def validate(self, data):
        return data    
    
class JobDescritionCompanyLocationSerializer(serializers.ModelSerializer):
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    company_location_id = serializers.PrimaryKeyRelatedField(queryset=CompanyLocationModel.objects.all(), source='company_location')
    work_place_id = serializers.PrimaryKeyRelatedField(queryset=WorkPlaceModel.objects.all(), source='work_place')

    class Meta:
        model = JobDescriptionCompanyLocationModel
        fields = ["job_description_id", "company_location_id", "work_place_id"]

    def validate(self, data):
        return data

class UserCompanySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    company_info_id = serializers.PrimaryKeyRelatedField(queryset=CompanyModel.objects.all(), source='company_info')

    class Meta:
        model = UserCompanyModel
        fields = ["user_id","company_info_id"]
            
    def validate(self, data):
        return data    

class NationalityJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    nationality_id = serializers.PrimaryKeyRelatedField(queryset=NationalityModel.objects.all(), source='nationality')

    class Meta:
        model = NationalityJobDescriptionModel
        fields = ["user_id", "job_description_id", "nationality_id", "nationality_name"]
    def validate(self, data):
        return data


class GenderJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')

    class Meta:
        model = GenderJobDescriptionModel
        fields = ["user_id", "job_description_id", "gender"]
        
    def validate(self, data):
        gender = data["gender"]
        
        if gender == None or gender =="":
            raise serializers.ValidationError({'errorMsg' : 'gender is required'})
        
        return data



class WorkPlaceJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    work_place_id = serializers.PrimaryKeyRelatedField(queryset=WorkPlaceModel.objects.all(), source='work_place')

    class Meta:
        model = WorkPlaceJobDescriptionModel
        fields = ["user_id", "job_description_id", "work_place_id", "work_place_name"]
    def validate(self, data):
        return data


class LanguageJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    language_id = serializers.PrimaryKeyRelatedField(queryset=LanguageModel.objects.all(), source='language')

    class Meta:
        model = LanguageJobDescriptionModel
        fields = ["user_id", "job_description_id", "language_id", "language_name"]
    def validate(self, data):
        return data

class JoiningPeriodJobDescriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')
    job_description_id = serializers.PrimaryKeyRelatedField(queryset=JobDescriptionModel.objects.all(), source='job_description')
    joining_period_id = serializers.PrimaryKeyRelatedField(queryset=JoiningPeriodModel.objects.all(), source='joining_period')

    class Meta:
        model = JoiningPeriodJobDescriptionModel
        fields = ["user_id", "job_description_id", "joining_period_id", "joining_period_name"]
    def validate(self, data):
        return data
    
class RecruiterBulkResumeUploadSerializer(serializers.ModelSerializer):
    
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = RecruiterBulkResumeUploadModel
        fields = ['recruiter_bulk_resume_upload_id', 'user_id', 'recruiter_bulk_resume_upload', 'recruiter_bulk_resume_upload_registration_date']

    def validate(self, data):
        resume_file = data["recruiter_bulk_resume_upload"]

        if not resume_file:
            raise serializers.ValidationError({"errorMsg": 'File is required'})
        
        if not resume_file.name.lower().endswith('.zip'):
            raise serializers.ValidationError({"errorMsg": "Unsupported file extension. Only ZIP files are allowed."})
        
        if resume_file.size > 10 * 1024 * 1024:  # Convert MB to bytes
            raise serializers.ValidationError({"errorMsg": "File size exceeds the limit. Maximum allowed size is 10 MB."})

        return data
    
class RecruiterExtractedZipFileSerializer(serializers.ModelSerializer):
    recruiter_bulk_resume_upload_id = serializers.PrimaryKeyRelatedField(queryset=RecruiterBulkResumeUploadModel.objects.all(), source='recruiter_bulk_resume_upload')
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user')

    class Meta:
        model = RecruiterExtractedZipFileModel
        fields = [ 'recruiter_bulk_resume_upload_id','user_id', 'resume_file_path', 'recruiter_resume_extracted_file_registration_date']

    def validate(self, data):
        # resume_file_path = data.get("resume_file_path", None)

        # if not resume_file_path:
        #     raise serializers.ValidationError({"errorMsg": 'File is required'})
        
        # if not resume_file_path.name.lower().endswith('.pdf'):
        #     raise serializers.ValidationError({"errorMsg": "Unsupported file extension. Only Pdf files are allowed."})

        return data