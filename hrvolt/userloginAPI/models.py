from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class NewUser(AbstractUser):

    id = models.CharField(max_length= 60, primary_key=True)
    user_birthdate = models.DateField(null=True, blank=True)
    user_mobileno = models.CharField(max_length=20, null=True, blank=True)
    user_gender = models.JSONField( null=True, blank=True)
    user_summary = models.TextField(null=True, blank=True)
    user_address = models.TextField(null=True, blank=True)
    user_jobtitle = models.JSONField(null=True, blank=True)
    user_country = models.JSONField(null=True, blank=True)
    user_pincode = models.CharField(max_length=20, null=True, blank=True)
    user_facebook = models.TextField(null=True, blank=True)
    user_linkedin = models.TextField(null=True, blank=True)
    user_github = models.TextField(null=True, blank=True)
    user_medium = models.TextField(null=True, blank=True)
    user_other1 = models.TextField(null=True, blank=True)
    user_other2 = models.TextField(null=True, blank=True)
    user_stackoverflow = models.TextField(null=True, blank=True)
    user_is_recruiter = models.BooleanField(default=False)
    user_is_verified = models.BooleanField(default=False)
    user_is_loggedin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name + " " + self.last_name


class UserEmailVerification(models.Model):
    
    class Meta:
        db_table = "candidate_email_verification"

    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    OTP_verify = models.CharField(max_length = 10, blank=False, null=False)
    expire_time = models.DateTimeField(default= datetime.datetime.now())

class UserContractModel(models.Model):
    
    class Meta:
        db_table = "hr_contract_tb"

    hr_contract_id = models.CharField(max_length=100, primary_key= True, default=None)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    contract_start_date = models.CharField(max_length= 50, blank=True, null=True, default=None)
    contract_end_date = models.CharField(max_length= 50, blank=True, null=True, default=None)
    number_of_loggedin_allow = models.CharField(max_length= 50, blank=True, null=True, default=None)
    user_unique_api_key = models.CharField(max_length= 50, blank=True, null=True, default=None)
    isvalid = models.CharField(max_length= 5, blank=True, null=True, default=True)
    hr_contract_registration_date = models.DateTimeField(default= datetime.datetime.now())

class UserLoggedModel(models.Model):
    
    class Meta:
        db_table = "hr_logged_tb"

    hr_logged_id = models.CharField(max_length=100, primary_key= True, default=None)
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,default=None)
    hr_contract = models.ForeignKey(UserContractModel,on_delete=models.CASCADE,default=None)
    user_device_ip = models.CharField(max_length= 100, blank=True, null=True, default=None)
    hr_logged_registration_date = models.DateTimeField(default= datetime.datetime.now())

