from rest_framework import serializers
from .models import *
import re
import string
import random
from datetime import datetime
from userloginAPI.models import NewUser
from databaseAPI.models import *

class CandidatePreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = CandidatePreferenceModel
        fields = ["user_id", "job_position_id", "job_level_id"]
    
    def validate(self, data):
        return data

class CandidateEmploymentTypePreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    employment_type_id = serializers.PrimaryKeyRelatedField(queryset=EmploymentTypeModel.objects.all(), source='employment_type')
    
    class Meta:
        model = CandidateEmploymentTypePreferenceModel
        fields = ["user_id", "employment_type_id","employment_type_name"]
    
    def validate(self, data):
        return data

class CandidatePreferenceLocationSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    location_id = serializers.PrimaryKeyRelatedField(queryset=LocationModel.objects.all(), source='location')
    
    class Meta:
        model = CandidatePreferenceLocationModel
        fields = ["user_id", "location_id","location_name"]
    
    def validate(self, data):
        return data

class CandidateCompanyPreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    company_type_id = serializers.PrimaryKeyRelatedField(queryset=CompanyTypeModel.objects.all(), source='company_type')
    
    class Meta:
        model = CandidateCompanyPreferenceModel
        fields = ["user_id", "company_type_id","company_type_name"]
    
    def validate(self, data):
        return data

class CandidateCompanySectorPreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    sector_id = serializers.PrimaryKeyRelatedField(queryset=SectorModel.objects.all(), source='sector')
    
    class Meta:
        model = CandidateCompanySectorPreferenceModel
        fields = ["user_id", "sector_id","sector_name"]
    
    def validate(self, data):
        return data

class CandidateWorkplacePreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    work_place_id = serializers.PrimaryKeyRelatedField(queryset=WorkPlaceModel.objects.all(), source='work_place')
    
    class Meta:
        model = CandidateWorkplacePreferenceModel
        fields = ["user_id", "work_place_id","work_place_name"]
    
    def validate(self, data):
        return data

class CandidateJoiningPeriodPreferenceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    joining_period_id = serializers.PrimaryKeyRelatedField(queryset=JoiningPeriodModel.objects.all(), source='joining_period')
    
    class Meta:
        model = CandidateJoiningPeriodPreferenceModel
        fields = ["user_id", "joining_period_id","joining_period_name"]
    
    def validate(self, data):
        return data

