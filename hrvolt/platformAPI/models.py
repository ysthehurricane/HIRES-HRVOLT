from django.db import models
import datetime
from userloginAPI.models import NewUser, UserContractModel
from databaseAPI.models import *


class contractLoggedInModel(models.Model):
    
    class Meta:
        db_table = "contract_login_tb"

    contract_login_id = models.CharField(max_length= 60, primary_key=True) #id of resume
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE) #user id
    hr_contract = models.ForeignKey(UserContractModel,on_delete=models.CASCADE,default=None) #contract id
    user_unique_api_key = models.CharField(max_length= 50, blank=True, null=True, default=None)
    is_loggedin = models.BooleanField(default=False)
    contract_login_registration_date = models.DateTimeField(default=datetime.datetime.now())

