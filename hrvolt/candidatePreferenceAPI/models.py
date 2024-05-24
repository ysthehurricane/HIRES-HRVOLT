from django.db import models
import datetime
from databaseAPI.models import *
from userloginAPI.models import *

class CandidatePreferenceModel(models.Model):

    class Meta:
        db_table = "candidate_preference_tb"

    candidate_preference_id = models.CharField(max_length= 60, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None)
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None)
    candidate_preference_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CandidateEmploymentTypePreferenceModel(models.Model):

    class Meta:
        db_table = "candidate_employment_type_preference_tb"

    candidate_employment_type_preference_id = models.CharField(max_length= 100, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    employment_type = models.ForeignKey(EmploymentTypeModel, on_delete=models.CASCADE, default=None)
    employment_type_name = models.TextField(blank=True, null=True, default=None) #permanent, full time
    candidate_employment_type_preference_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CandidatePreferenceLocationModel(models.Model):

    class Meta:
        db_table = "candidate_preference_location_tb"

    candidate_preference_location_id = models.CharField(max_length= 60, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    location = models.ForeignKey(LocationModel, on_delete=models.CASCADE, default=None)
    location_name = models.TextField(blank=True, null=True, default=None) #surat, vadodara, mumbai
    candidate_preference_location_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CandidateCompanyPreferenceModel(models.Model):

    class Meta:
        db_table = "candidate_company_preference_tb"

    candidate_company_preference_id = models.CharField(max_length= 60, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    company_type = models.ForeignKey(CompanyTypeModel, on_delete=models.CASCADE, default=None)
    company_type_name = models.TextField(blank=True, null=True, default=None) #MNC, startup, Indian MNC
    candidate_company_preference_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CandidateCompanySectorPreferenceModel(models.Model):

    class Meta:
        db_table = "candidate_company_sector_preference_tb"

    candidate_company_sector_preference_id = models.CharField(max_length= 100, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    sector = models.ForeignKey(SectorModel, on_delete=models.CASCADE, default=None)
    sector_name = models.TextField(blank=True, null=True, default=None) # IT, Health, etc
    candidate_company_sector_preference_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CandidateWorkplacePreferenceModel(models.Model):

    class Meta:
        db_table = "candidate_workplace_preference_tb"

    candidate_workplace_preference_id = models.CharField(max_length= 100, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    work_place = models.ForeignKey(WorkPlaceModel, on_delete=models.CASCADE, default=None)
    work_place_name = models.TextField(blank=True, null=True, default=None) #MNC, startup, Indian MNC
    candidate_workplace_preference_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CandidateJoiningPeriodPreferenceModel(models.Model):

    class Meta:
        db_table = "candidate_joining_period_preference_tb"

    candidate_joining_period_preference_id = models.CharField(max_length= 100, primary_key=True, default=None)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, default=None)
    joining_period = models.ForeignKey(JoiningPeriodModel, on_delete=models.CASCADE, default=None)
    joining_period_name = models.TextField(blank=True, null=True, default=None) #MNC, startup, Indian MNC
    candidate_joining_period_preference_registration_date = models.DateTimeField(default=datetime.datetime.now())