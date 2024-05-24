from django.shortcuts import render
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import string
import random
import os
from userloginAPI.models import NewUser 
import json
from hrvolt.emailsend import mailSend
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from recruiterAPI.serializers import *
from userloginAPI.views import APIKeyAuthentication

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainSerializer

###################################################################################################################################################

# Create your views here.

# views.py

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


def generate_token(useremail):
    
    user = get_user_model().objects.get(email=useremail)
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return access_token


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            useremail = serializer.validated_data['useremail']

            token = generate_token(useremail)
            res = {"Status": "success",
                    "Code": 201,
                    "Message": [], 
                    "Data":{'access': token},
            }
            return Response(res, status=status.HTTP_201_CREATED)

        res = {
            "Status": "error",
            "Code": 400,
            "Message":list(serializer.errors.values())[0][0],
            "Data":[],
        }
        return Response(res, status=status.HTTP_201_CREATED)
    

class UserLoggedInValidateAPI(APIView):

    '''
        user logged in API(INSERT)
        Request : POST
        Data =  {
                    "email":"BroaderAI_firsetest3_0yyhogjnlh",
                    "user_unique_api_key":"11"
                }
    '''
    

    def post(self, request ,format=None):

        getData = request.data
        
        if NewUser.objects.filter(email=getData["email"]).exists():

            user = NewUser.objects.get(email=getData["email"])

            if UserContractModel.objects.filter(user_id=user.id, user_unique_api_key=getData["user_unique_api_key"]).exists():

                user_unique_api_key = UserContractModel.objects.get(user_id=user.id, user_unique_api_key=getData["user_unique_api_key"])


                if not contractLoggedInModel.objects.filter(user_id=user.id, user_unique_api_key=getData["user_unique_api_key"]).exists():

                    randomstr = ''.join(random.choices(string.ascii_lowercase +string.digits, k=15))

                    uniqueID = "BroaderAI_contract_user_logged_" + randomstr

                    contract_logged_in = contractLoggedInModel(contract_login_id =uniqueID, user_id=user.id,hr_contract_id=user_unique_api_key.hr_contract_id,is_loggedin=True, user_unique_api_key=getData["user_unique_api_key"])

                    contract_logged_in.save()


                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User Logged in Details", 
                            "Data":{
                                "user_id": user.id,
                                "email":getData["email"],
                                "user_unique_api_key":getData["user_unique_api_key"],
                                "is_loggedin": True

                            }
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
                
                else:

                    if not contractLoggedInModel.objects.filter(user_id=user.id, user_unique_api_key=getData["user_unique_api_key"], is_loggedin=False).exists():
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Already Loggedin. please logout from other device.",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        contract_logged_true = contractLoggedInModel.objects.get(user_id=user.id, user_unique_api_key=getData["user_unique_api_key"])

                        contract_logged_true.is_loggedin=True
                        contract_logged_true.save()

                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User Logged in successfully", 
                            "Data":{
                                "user_id": user.id,
                                "email":getData["email"],
                                "user_unique_api_key":getData["user_unique_api_key"],
                                "is_loggedin": True
                            }
                        }

                        return Response(res, status=status.HTTP_201_CREATED)

                
            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "API Key is invalid",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
class UserLoggedOutUpdateAPI(APIView):

    '''
        user logged in API(INSERT)
        Request : patch
        Data =  {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "user_unique_api_key":"11"
                }
    '''
    

    def patch(self, request ,format=None):

        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            # user = NewUser.objects.get(id=getData["user_id"])

            if UserContractModel.objects.filter(user_unique_api_key=getData["user_unique_api_key"]).exists():
                user_unique_api_key = UserContractModel.objects.get(user_unique_api_key=getData["user_unique_api_key"])

                if contractLoggedInModel.objects.filter(user_id=getData["user_id"], user_unique_api_key=getData["user_unique_api_key"]).exists():

                    
                    contractLoggedInModel.objects.filter(user_id=getData["user_id"], hr_contract_id = user_unique_api_key.hr_contract_id, user_unique_api_key=getData["user_unique_api_key"]).update(is_loggedin=False)


                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User Logged Out Details", 
                            "Data":{
                                "user_id": getData["user_id"],
                                "user_unique_api_key":getData["user_unique_api_key"],
                                "is_loggedin": False

                            }
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
                
                else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            
            else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "API Key is invalid",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobDescriptionPlatformAPI(APIView):

    '''
        job Description Platform API(INSERT)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf",
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "number_of_vacancy":"11",
                    "salary_max":"21000",
                    "salary_min":"15000",
                    "job_tilte": "Python Developer"
                    "job_description_action": "active"     # active/deactive/archive/draft
                }
    '''
    

    def post(self, request ,format=None):

        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                JobPosition = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    JobLevel = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                    
                        
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))

                    uniqueID = "BroaderAI_job_description_" + randomstr
                    getData["job_description_id"] = uniqueID
                    
                    getData['job_position_name']=JobPosition.job_position_name
                    getData['job_level_name']=JobLevel.job_level_name
                    
                    serializer = JobDescriptionSerializer(data=getData)
                    if serializer.is_valid():
                        serializer.save(job_description_id=getData["job_description_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Description is Added",
                            "Data": {   
                                "job_description_id" : getData['job_description_id']
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)


        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
 
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionUpdatePlatformAPI(APIView):

    '''
        job Description API(UPDATE)
        Request : PATCH
        Data =  {
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf",
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "number_of_vacancy":"11",
                    "salary_max":"21000",
                    "salary_min":"15000",
                    "job_tilte": "Python Developer",
                    "job_description_action": "active" # active/deactive/archive/draft
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
            
                if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists(): 
                    JobPosition = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                    if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                        JobLevel = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                        
                        serializer = JobDescriptionSerializer(data=getData)
                        
                        getData['job_position_name']=JobPosition.job_position_name
                        getData['job_level_name']=JobLevel.job_level_name
                        
                        if serializer.is_valid():
                            LastUpdateData = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])
                            LastUpdateData.user_id = getData['user_id']
                            LastUpdateData.job_position_id = getData["job_position_id"]
                            LastUpdateData.job_level_id = getData["job_level_id"]
                            LastUpdateData.number_of_vacancy = getData["number_of_vacancy"]
                            LastUpdateData.salary_max = getData["salary_max"]
                            LastUpdateData.salary_min = getData["salary_min"]
                            LastUpdateData.job_tilte = getData["job_tilte"]
                            LastUpdateData.job_description_action = getData["job_description_action"]
                            LastUpdateData.job_position_name = JobPosition.job_position_name
                            LastUpdateData.job_level_name = JobLevel.job_level_name
                            LastUpdateData.save()
                            
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job Description is Updated",
                                "Data": {
                                    "job_description_id": getData["job_description_id"],
                                    "vacancy": getData["number_of_vacancy"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Level data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionDeletePlatformAPI(APIView):
    '''
        job Description API(delete)
        Request : delete
        Data =  {
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
                
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"],user_id=getData["user_id"]).exists():
                
                JobDescriptionDetail = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"],user_id=getData["user_id"])
                JobDescriptionDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description is successfully Deleted",
                        "Data":[],
                        
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
    
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionGetPlatformAPI(APIView):
    '''
        Job Description API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        JobDescriptionDetails = JobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Description Details",
                "Data": JobDescriptionDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)        

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Job Description API(View)
        Request : POST
        Data =  {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "job_description_action": "active",  # active/deactive/archive/draft
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

                
            if JobDescriptionModel.objects.filter( user_id=getData["user_id"], job_description_id = getData["job_description_id"],job_description_action = getData["job_description_action"]).exists():
                
                JobDescriptionDetail = JobDescriptionModel.objects.filter(user_id=getData["user_id"] , job_description_id = getData["job_description_id"],job_description_action = getData["job_description_action"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Detail",
                        "Data": JobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionGetUserPlatformAPI(APIView):
    '''
        Get One Job Description User API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_action": "active", # active/deactive/archive/draft
                }
    '''
    def post(self, request, format=None):

        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                            
            if JobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_action = getData["job_description_action"]).exists():
                JobDescriptionDetail = JobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_action = getData["job_description_action"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Detail",
                        "Data": JobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get One Job Description Job Level Job Position API(View)
        Request : POST
        Data =  {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_description_action": "active", # active/deactive/archive/draft
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if JobDescriptionModel.objects.filter(user_id=getData["user_id"],job_level_id = getData["job_level_id"],job_position_id = getData["job_position_id"],job_description_action = getData["job_description_action"]).exists():
                        
                        JobDescriptionDetail = JobDescriptionModel.objects.filter(user_id=getData["user_id"],job_level_id = getData["job_level_id"],job_position_id = getData["job_position_id"],job_description_action = getData["job_description_action"]).values()
                        
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job Description Detail",
                                "Data": JobDescriptionDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)        
 
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

 
###################################################################################################################################################
# Education

class EducationJobDescriptionPlatformAPI(APIView):
    '''
        Education Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "education_id": "BroaderAI_education_cn2uuw5455blakl",
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

                
            if EducationModel.objects.filter(education_id = getData["education_id"]).exists():
                        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                
                uniqueID = "BroaderAI_education_job_description_" + randomstr

                getData["education_job_description_id"] = uniqueID
                
                educationData= EducationModel.objects.get(education_id = getData["education_id"])
                getData['education_name']  = educationData.education_name
                                    
                serializer = EducationJobDescriptionSerializer(data=getData)
                
                if serializer.is_valid():
                    serializer.save(education_job_description_id=getData["education_job_description_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Job Description is Added",
                        "Data": {
                            "education_job_description_id": getData["education_job_description_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Education is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class EducationJobDescriptionGetPlatformAPI(APIView):
    '''
        Education Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        EducationJobDescriptionGetDetails = EducationJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Education Job Description Details",
                "Data": EducationJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class EducationJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":,
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if EducationJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                educationJobDescriptionDetail = EducationJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Job Description Detail",
                        "Data": educationJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Education Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
  
class EducationJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if EducationJobDescriptionModel.objects.filter(user_id = getData["user_id"]).exists():
                educationJobDescriptionDetail = EducationJobDescriptionModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Job Description Detail",
                        "Data": educationJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Education Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class EducationJobDescriptionDeletePlatformAPI(APIView):
    '''
        Education Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "education_job_description_id": "BroaderAI_education_job_description_keothlt8opo8715"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

                    
            if EducationJobDescriptionModel.objects.filter(education_job_description_id = getData["education_job_description_id"], user_id = getData["user_id"]).exists():
                educationJobDescriptionModelDetail = EducationJobDescriptionModel.objects.get(education_job_description_id = getData["education_job_description_id"], user_id = getData["user_id"])
                educationJobDescriptionModelDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Education Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]        

###################################################################################################################################################

# Education Field

class EducationFieldJobDescriptionPlatformAPI(APIView):
    '''
        Education Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "education_field_id": "BroaderAI_education_cn2uuw5455blakl",
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
                
            if EducationFieldModel.objects.filter(education_field_id = getData["education_field_id"]).exists():
                        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                
                uniqueID = "BroaderAI_education_field_job_description_" + randomstr

                getData["education_field_job_description_id"] = uniqueID
                
                educationData= EducationFieldModel.objects.get(education_field_id = getData["education_field_id"])
                getData['education_field_name']  = educationData.education_field_name
                                    
                serializer = EducationFieldJobDescriptionSerializer(data=getData)
                
                if serializer.is_valid():
                    serializer.save(education_field_job_description_id=getData["education_field_job_description_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Field Job Description is Added",
                        "Data": {
                            "education_field_job_description_id": getData["education_field_job_description_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Education Field is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 
    
class EducationFieldJobDescriptionGetPlatformAPI(APIView):
    '''
        Education Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        EducationFieldJobDescriptionGetDetails = EducationFieldJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Education Field Job Description Details",
                "Data": EducationFieldJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class EducationFieldJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if EducationFieldJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id=getData["job_description_id"]).exists():
                educationFieldJobDescriptionDetail = EducationFieldJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id=getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Field Job Description Detail",
                        "Data": educationFieldJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Education Field Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class EducationFieldJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if EducationFieldJobDescriptionModel.objects.filter(user_id = getData["user_id"]).exists():
                educationFieldJobDescriptionDetail = EducationFieldJobDescriptionModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Field Job Description Detail",
                        "Data": educationFieldJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Education Field Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class EducationFieldJobDescriptionDeletePlatformAPI(APIView):
    '''
        Education Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "education_field_job_description_id": "BroaderAI_education_job_description_keothlt8opo8715"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

                    
            if EducationFieldJobDescriptionModel.objects.filter(education_field_job_description_id = getData["education_field_job_description_id"], user_id = getData["user_id"]).exists():
                EducationFieldJobDescriptionModelDetail = EducationFieldJobDescriptionModel.objects.get(education_field_job_description_id = getData["education_field_job_description_id"], user_id = getData["user_id"])
                EducationFieldJobDescriptionModelDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Field Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Education Field Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

###################################################################################################################################################
# Soft skills

class SoftSkillsJobDescriptionPlatformAPI(APIView):
    '''
        Soft Skill Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "soft_skills_id": "BroaderAI_Soft_Skills_wlqb09w3i8oem0k"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
    
            if SoftSkillsModel.objects.filter(soft_skills_id = getData["soft_skills_id"]).exists():
                        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                    
                uniqueID = "BroaderAI_soft_skill_job_description_" + randomstr

                getData["soft_skills_job_description_id"] = uniqueID
                
                softskillData = SoftSkillsModel.objects.get(soft_skills_id=getData["soft_skills_id"])
                getData['soft_skills_name'] = softskillData.soft_skills_name

                serializer = SoftSkillsJobDescriptionSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(soft_skills_job_description_id=getData["soft_skills_job_description_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Soft Skills Job Description is Added",
                        "Data": {
                            "soft_skills_job_description_id": getData["soft_skills_job_description_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Soft Skills is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 
 
class SoftSkillsJobDescriptionGetPlatformAPI(APIView):
    '''
        Soft Skill Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        SoftSkillJobDescriptionGetDetails = SoftSkillJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Soft Skill Job Description Details",
                "Data": SoftSkillJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class SoftSkillsJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if SoftSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id=getData["job_description_id"]).exists():
                softskillJobDescriptionDetail = SoftSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id=getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Soft Skills Job Description Detail",
                        "Data": softskillJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Soft skills Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
 
class SoftSkillsJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if SoftSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"]).exists():
                softskillJobDescriptionDetail = SoftSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Soft Skills Job Description Detail",
                        "Data": softskillJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Soft skills Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class SoftSkillsJobDescriptionDeletePlatformAPI(APIView):
    '''
        Soft Skills Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "soft_skills_job_description_id": "BroaderAI_soft_skill_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
    
            if SoftSkillJobDescriptionModel.objects.filter(soft_skills_job_description_id = getData["soft_skills_job_description_id"], user_id = getData["user_id"]).exists():
                softskillJobDescriptionDetail = SoftSkillJobDescriptionModel.objects.get(soft_skills_job_description_id = getData["soft_skills_job_description_id"], user_id = getData["user_id"])
                softskillJobDescriptionDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Soft Skill Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Soft Skill Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

###################################################################################################################################################

class TechnicalSkillsJobDescriptionPlatformAPI(APIView):
    '''
        Technical Skills Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "technical_skills_id": "BroaderAI_Technical_Skills_ivqwek1yhrd9yz6"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData["technical_skills_id"]).exists():
                        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                    
                uniqueID = "BroaderAI_technical_skill_job_description_" + randomstr

                getData["technical_skills_job_description_id"] = uniqueID
                
                TechnicalSkillsData = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id=getData["technical_skills_id"])
                getData['technical_skills_name'] = TechnicalSkillsData.unique_technical_skills_name

                serializer = TechnicalSkillsJobDescriptionSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(technical_skills_job_description_id=getData["technical_skills_job_description_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Technical Skills Job Description is Added",
                        "Data": {
                            "technical_skills_job_description_id": getData["technical_skills_job_description_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Technical Skills is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 
    
class TechnicalSkillsJobDescriptionGetPlatformAPI(APIView):
    '''
        Technical Skill Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        TechnicalSkillJobDescriptionGetDetails = TechnicalSkillJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Technical Skill Job Description Details",
                "Data": TechnicalSkillJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class TechnicalSkillsJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if TechnicalSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id=getData["job_description_id"]).exists():
                technicalskillsJobDescriptionDetail = TechnicalSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_id=getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Technical Skills Job Description Detail",
                        "Data": technicalskillsJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Technical skills Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class TechnicalSkillsJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if TechnicalSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"]).exists():
                technicalskillsJobDescriptionDetail = TechnicalSkillJobDescriptionModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Technical Skills Job Description Detail",
                        "Data": technicalskillsJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Technical skills Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class TechnicalSkillsJobDescriptionDeletePlatformAPI(APIView):
    '''
        Technical Skills Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "technical_skills_job_description_id": "BroaderAI_technical_skill_job_description_07gqwa1bhv0hkrb",
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if TechnicalSkillJobDescriptionModel.objects.filter(technical_skills_job_description_id = getData["technical_skills_job_description_id"], user_id = getData["user_id"]).exists():
                technicalskillJobDescriptionDetail = TechnicalSkillJobDescriptionModel.objects.get(technical_skills_job_description_id = getData["technical_skills_job_description_id"], user_id = getData["user_id"])
                technicalskillJobDescriptionDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Technical Skill Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Technical Skill Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

###################################################################################################################################################

class CustomJobDescriptionResponsibilityPlatformAPI(APIView):
    '''
        Custom  Job Description Responsibility API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "responsibilities_description":"ABC",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data 

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                
                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                
                    if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                            
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                            
                        uniqueID = "BroaderAI_custom_job_description_responsibility" + randomstr

                        getData["custom_job_description_responsibility_id"] = uniqueID
                        
                        JobPositionData = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                        getData['job_position_name'] = JobPositionData.job_position_name
                        
                        JobLevelData = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                        getData['job_level_name']=JobLevelData.job_level_name
                        
                        
                        serializer = CustomJobDescriptionResponsibilitySerializer(data=getData)

                        if serializer.is_valid():
                            serializer.save(custom_job_description_responsibility_id=getData["custom_job_description_responsibility_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Responsibility is Added",
                                "Data": {
                                    "custom_job_description_responsibility_id": getData["custom_job_description_responsibility_id"],
                                    "user_id":getData['user_id'],
                                    "job_description_id":getData["job_description_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Position is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Level is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job description is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 
   
class CustomJobDescriptionResponsibilityGetPlatformAPI(APIView):
    '''
        Custom  Job Description Responsibility API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        CustomJobDescriptionResponsibilityGetDetails = CustomJobDescriptionResponsibilityModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Custom  Job Description Responsibility Details",
                "Data": CustomJobDescriptionResponsibilityGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionResponsibilityGetOnePlatformAPI(APIView):
    '''
        Get Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"]).exists():
                customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Custom Job Description Responsibility Detail",
                        "Data": customJobDescriptionResponsibilityDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Custom Job Description Responsibility data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionResponsibilityGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get Custom Job Description Responsibility from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])
                    
                if CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).exists():
                    customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Custom Job Description Responsibility Detail",
                            "Data": customJobDescriptionResponsibilityDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Custom Job Description Responsibility data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get Custom Job Description Responsibility from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    user = NewUser.objects.get(id=getData["user_id"])
                        
                    if CustomJobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).exists():
                        customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Responsibility Detail",
                                "Data": customJobDescriptionResponsibilityDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionResponsibilityGetfromJobPositionPlatformAPI(APIView):
    '''
        Get Custom Job Description Responsibility  from Job Position API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                    user = NewUser.objects.get(id=getData["user_id"])
                
                    if CustomJobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).exists():
                        customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Responsibility Detail",
                                "Data": customJobDescriptionResponsibilityDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionResponsibilityDeletePlatformAPI(APIView):
    '''
        Custom  Job Description Responsibility API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "custom_job_description_responsibility_id": "BroaderAI_custom_job_description_responsibilityhy3bsc9qzy519c7"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if CustomJobDescriptionResponsibilityModel.objects.filter(custom_job_description_responsibility_id = getData["custom_job_description_responsibility_id"], user_id = getData["user_id"]).exists():
                customJobDescriptionResponsibilityDetails = CustomJobDescriptionResponsibilityModel.objects.get(custom_job_description_responsibility_id = getData["custom_job_description_responsibility_id"], user_id = getData["user_id"])
                customJobDescriptionResponsibilityDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Custom  Job Description Responsibility is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Custom  Job Description Responsibility data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
 
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

###################################################################################################################################################
        
class CustomJobDescriptionRequirementPlatformAPI(APIView):
    '''
        Custom  Job Description Requirement API(Insert)
        Request : POST
        Data ={
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf",
                    "requirement_description":"ABC"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                
                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                
                    if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                            
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                            
                        uniqueID = "BroaderAI_custom_job_description_requirement" + randomstr

                        getData["custom_job_description_requirement_id"] = uniqueID
                        
                        JobPositionData = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                        getData['job_position_name'] = JobPositionData.job_position_name
                        
                        JobLevelData = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                        getData['job_level_name']=JobLevelData.job_level_name
                        
                        
                        serializer = CustomJobDescriptionRequirementSerializer(data=getData)

                        if serializer.is_valid():
                            serializer.save(custom_job_description_requirement_id=getData["custom_job_description_requirement_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Requirement is Added",
                                "Data": {
                                    "custom_job_description_requirement_id": getData["custom_job_description_requirement_id"],
                                    "user_id":getData['user_id'],
                                    "job_description_id":getData["job_description_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Position is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Level is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job description is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionRequirementGetPlatformAPI(APIView):
    '''
        Custom  Job Description Requirement API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        CustomJobDescriptionRequirementGetDetails = CustomJobDescriptionRequirementsModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Custom  Job Description Requirement Details",
                "Data": CustomJobDescriptionRequirementGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionRequirementGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CustomJobDescriptionRequirementsModel.objects.filter(user_id = getData["user_id"]).exists():
                customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Custom Job Description Requirement Detail",
                        "Data": customJobDescriptionRequirementDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Custom Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionRequirementGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get Custom Job Description Requirement from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

                if CustomJobDescriptionRequirementsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                    customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Custom Job Description Requirement Detail",
                            "Data": customJobDescriptionRequirementDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Custom Job Description Requirement data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
               
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionRequirementGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get Custom Job Description Requirement from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    
                    if CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                        customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Requirement Detail",
                                "Data": customJobDescriptionRequirementDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Requirement data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionRequirementGetfromJobPositionPlatformAPI(APIView):
    '''
        Get Custom Job Description Requirement from Job Position API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():

                if CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Custom Job Description Requirement Detail",
                            "Data": customJobDescriptionRequirementDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Custom Job Description Requirement data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionRequirementDeletePlatformAPI(APIView):
    '''
        Custom  Job Description Requirement API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "custom_job_description_requirement_id": "BroaderAI_custom_job_description_requirementuaku7rr6ar7cft2"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if CustomJobDescriptionRequirementsModel.objects.filter(custom_job_description_requirement_id = getData["custom_job_description_requirement_id"], user_id = getData["user_id"]).exists():
                customJobDescriptionRequirementDetails = CustomJobDescriptionRequirementsModel.objects.get(custom_job_description_requirement_id = getData["custom_job_description_requirement_id"], user_id = getData["user_id"])
                customJobDescriptionRequirementDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Custom  Job Description Requirement is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Custom  Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

###################################################################################################################################################

class CustomJobDescriptionBenefitPlatformAPI(APIView):
    '''
        Custom  Job Description Benefit API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf",
                    "benefit_description":"ABC"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                
                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                
                    if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                            
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                            
                        uniqueID = "BroaderAI_custom_job_description_benefit" + randomstr

                        getData["custom_job_description_benefit_id"] = uniqueID
                        
                        JobPositionData = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                        getData['job_position_name'] = JobPositionData.job_position_name
                        
                        JobLevelData = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                        getData['job_level_name']=JobLevelData.job_level_name
                        
                        
                        serializer = CustomJobDescriptionBenefitSerializer(data=getData)

                        if serializer.is_valid():
                            serializer.save(custom_job_description_benefit_id=getData["custom_job_description_benefit_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Benefit is Added",
                                "Data": {
                                    "custom_job_description_benefit_id": getData["custom_job_description_benefit_id"],
                                    "user_id":getData['user_id'],
                                    "job_description_id":getData["job_description_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Position is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Level is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job description is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionBenefitGetPlatformAPI(APIView):
    '''
        Custom  Job Description Benefit API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        CustomJobDescriptionBenefitGetDetails = CustomJobDescriptionBenefitsModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Custom  Job Description Benefit Details",
                "Data": CustomJobDescriptionBenefitGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionBenefitGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"]).exists():
                customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Custom Job Description Benefit Detail",
                        "Data": customJobDescriptionBenefitDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Custom Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionBenefitGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get Custom Job Description Benefit from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

                if CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                    customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Custom Job Description Benefit Detail",
                            "Data": customJobDescriptionBenefitDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Custom Job Description Benefit data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionBenefitGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get Custom Job Description Benefit from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                        customJobDescriptionBenefittDetail = CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Custom Job Description Benefit Detail",
                                "Data": customJobDescriptionBenefittDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Benefitt data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
    
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionBenefitGetfromJobPositionPlatformAPI(APIView):
    '''
        Get Custom Job Description Benefit from JobPosition API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                    
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():

                if CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Custom Job Description Benefit Detail",
                            "Data": customJobDescriptionBenefitDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Custom Job Description Benefit data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

class CustomJobDescriptionBenefitDeletePlatformAPI(APIView):
    '''
        Custom  Job Description Requirement API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "custom_job_description_benefit_id": "BroaderAI_custom_job_description_requirementuaku7rr6ar7cft2"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
              
            if CustomJobDescriptionBenefitsModel.objects.filter(custom_job_description_benefit_id = getData["custom_job_description_benefit_id"], user_id = getData["user_id"]).exists():
                customJobDescriptionBenefitsDetails = CustomJobDescriptionBenefitsModel.objects.get(custom_job_description_benefit_id = getData["custom_job_description_benefit_id"], user_id = getData["user_id"])
                customJobDescriptionBenefitsDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Custom  Job Description Benefits is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Custom  Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated] 

###################################################################################################################################################

class JobDescriptionResponsibilityPlatformAPI(APIView):
    '''
        Job Description Responsibility API(Insert)
        
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d",
                    "job_responsibility_id": "BroaderAI_Job_Responsibility_ovoayt6k2fconk0"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                JobDescriptionData = JobDescriptionModel.objects.filter(user_id=getData["user_id"], job_description_id=getData["job_description_id"]).first()
                if JobResponsibilityModel.objects.filter(job_responsibility_id = getData["job_responsibility_id"]).exists():
                
                            
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                                        
                    uniqueID = "BroaderAI_job_description_responsibility" + randomstr

                    JobLevelData=JobLevelModel.objects.get(job_level_id=JobDescriptionData.job_level_id)
                    JobPositionData=JobPositionModel.objects.get(job_position_id=JobDescriptionData.job_position_id)
                    
                    getData["job_description_responsibility_id"] = uniqueID
                    getData["job_position_id"]=JobPositionData.job_position_id
                    getData["job_level_id"]=JobLevelData.job_level_id
                    getData['job_level_name']=JobLevelData.job_level_name
                    getData['job_position_name'] = JobPositionData.job_position_name
                    print(getData,"yahd")
                    serializer = JobDescriptionResponsibilitySerializer(data=getData)

                    if serializer.is_valid():
                        serializer.save(job_description_responsibility_id=getData["job_description_responsibility_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Description Responsibility is Added",
                            "Data": {
                                "job_description_responsibility_id": getData["job_description_responsibility_id"],
                                "user_id":getData['user_id'],
                                "job_description_id":getData["job_description_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Responsibility is not exits",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job description is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetOnePlatformAPI(APIView):
    '''
        Get Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"]).exists():
                JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": " Job Description Responsibility Detail",
                        "Data": JobDescriptionResponsibilityDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Job Description Responsibility data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get  Job Description Responsibility from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                    
                if JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).exists():
                    JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": " Job Description Responsibility Detail",
                            "Data": JobDescriptionResponsibilityDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Responsibility data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get  Job Description Responsibility from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "job_level_id": "BroaderAI_job_level_mc5ulyfn8ihxicy",
                    "job_position_id": "BroaderAI_job_position_3u7kqvrgn2f0uya"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    user = NewUser.objects.get(id=getData["user_id"])
                        
                    if JobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).exists():
                        JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": " Job Description Responsibility Detail",
                                "Data": JobDescriptionResponsibilityDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetfromJobPositionPlatformAPI(APIView):
    '''
        Get Job Description Responsibility  from Job Position API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                user = NewUser.objects.get(id=getData["user_id"])
                    
                if JobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).exists():
                    JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": " Job Description Responsibility Detail",
                            "Data": JobDescriptionResponsibilityDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Responsibility data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
    
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityDeletePlatformAPI(APIView):
    '''
         Job Description Responsibility API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_responsibility_id": "BroaderAI_job_description_responsibilitybpfoa3anlgns45z"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if JobDescriptionResponsibilityModel.objects.filter(job_description_responsibility_id = getData["job_description_responsibility_id"], user_id = getData["user_id"]).exists():
                JobDescriptionResponsibilityDetails = JobDescriptionResponsibilityModel.objects.get(job_description_responsibility_id = getData["job_description_responsibility_id"], user_id = getData["user_id"])
                JobDescriptionResponsibilityDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": " Job Description Responsibility is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Job Description Responsibility data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class BothJobDescriptionResponsibilityGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get Both Job Description Responsibility from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                    
                if CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).exists():
                    customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).values()
                
                    if JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).exists():
                        JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Both Job Description Responsibility Detail",
                                "Data": JobDescriptionResponsibilityDetail,
                                "Data1":customJobDescriptionResponsibilityDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class BothJobDescriptionResponsibilityGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get Both  Job Description Responsibility from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "job_level_id": "BroaderAI_job_level_mc5ulyfn8ihxicy",
                    "job_position_id": "BroaderAI_job_position_3u7kqvrgn2f0uya"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    user = NewUser.objects.get(id=getData["user_id"])
                        
                    if JobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).exists():
                        JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).values()
                        if CustomJobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).exists():
                            customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(job_level_id = getData["job_level_id"],job_position_id=getData['job_position_id']).values()
                            res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": " Both Job Description Responsibility Detail",
                                    "Data": {
                                        "JobDescriptionResponsibilityDetail":JobDescriptionResponsibilityDetail,
                                        "Data1":customJobDescriptionResponsibilityDetail},
                                }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Custom Job Description Responsibility data is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class BothJobDescriptionResponsibilityGetfromJobPositionPlatformAPI(APIView):
    '''
        Get Both Job Description Responsibility  from Job Position API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                    user = NewUser.objects.get(id=getData["user_id"])
                        
                    if JobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).exists():
                        JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).values()
                        
                        if CustomJobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).exists():
                            customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(job_position_id=getData['job_position_id']).values()
                            res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": " Both Job Description Responsibility Detail",
                                    "Data": {
                                        "JobDescriptionResponsibilityDetail":JobDescriptionResponsibilityDetail,
                                        "Data1":customJobDescriptionResponsibilityDetail},
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Custom Job Description Responsibility data is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Responsibility data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
 
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class JobDescriptionRequirementPlatformAPI(APIView):
    '''
        Job Description Requirement API(Insert)
        Request : POST
        Data ={
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d",
                    "job_requirement_id": "BroaderAI_Job_Requirement_efsixzmz99cu9hu"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                JobDescriptionData = JobDescriptionModel.objects.filter(user_id=getData["user_id"], job_description_id=getData["job_description_id"]).first()

                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                    
                uniqueID = "BroaderAI_job_description_requirement" + randomstr

                getData["job_description_requirement_id"] = uniqueID
                
                JobLevelData=JobLevelModel.objects.get(job_level_id=JobDescriptionData.job_level_id)
                JobPositionData=JobPositionModel.objects.get(job_position_id=JobDescriptionData.job_position_id)
                getData['job_position_id'] = JobPositionData.job_position_id
                getData['job_level_id']=JobLevelData.job_level_id
                getData['job_level_name']=JobLevelData.job_level_name
                getData['job_position_name'] = JobPositionData.job_position_name
                
                serializer = JobDescriptionRequirementSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(job_description_requirement_id=getData["job_description_requirement_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Requirement is Added",
                        "Data": {
                            "job_description_requirement_id": getData["job_description_requirement_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job description is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionRequirementGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionRequirementModel.objects.filter(user_id = getData["user_id"]).exists():
                JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": " Job Description Requirement Detail",
                        "Data": JobDescriptionRequirementDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
    
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionRequirementGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get  Job Description Requirement from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

                if JobDescriptionRequirementModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                    JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": " Job Description Requirement Detail",
                            "Data": JobDescriptionRequirementDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Requirement data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]       

class JobDescriptionRequirementGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get  Job Description Requirement from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                        JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": " Job Description Requirement Detail",
                                "Data": JobDescriptionRequirementDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Requirement data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionRequirementGetfromJobPositionPlatformAPI(APIView):
    '''
        Get  Job Description Requirement from Job Position API(View)
        Request : POST
        Data =  {
                    
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                }
                
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():

                if JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": " Job Description Requirement Detail",
                            "Data": JobDescriptionRequirementDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Requirement data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionRequirementDeletePlatformAPI(APIView):
    '''
        Custom  Job Description Requirement API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_requirement_id": "BroaderAI_job_description_requirementuaku7rr6ar7cft2"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if JobDescriptionRequirementModel.objects.filter(job_description_requirement_id = getData["job_description_requirement_id"], user_id = getData["user_id"]).exists():
                JobDescriptionRequirementDetails = JobDescriptionRequirementModel.objects.get(job_description_requirement_id = getData["job_description_requirement_id"], user_id = getData["user_id"])
                JobDescriptionRequirementDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "  Job Description Requirement is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "  Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]       

###################################################################################################################################################

###################################################################################################################################################
       
class BothJobDescriptionRequirementGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get both  Job Description Requirement from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

                if CustomJobDescriptionRequirementsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                    customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                    if JobDescriptionRequirementModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                        JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": " Job Description Requirement Detail",
                                "Data": {
                                    "JobDescriptionRequirementDetail":JobDescriptionRequirementDetail,
                                    "Data1":customJobDescriptionRequirementDetail
                                }
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Requirement data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " custom Job Description Requirement data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class BothJobDescriptionRequirementGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get  Job Description Requirement from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                        customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                        
                        if JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                            JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                            res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": " Job Description Requirement Detail",
                                    "Data": {
                                        "JobDescriptionRequirementDetail":JobDescriptionRequirementDetail,
                                        "Data1": customJobDescriptionRequirementDetail
                                    }
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Description Requirement data is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Custom Job Description Requirement data is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class BothJobDescriptionRequirementGetfromJobPositionPlatformAPI(APIView):
    '''
        Get  Job Description Requirement from Job Position API(View)
        Request : POST
        Data =  {
                    
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                }
                
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():

                if CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    customJobDescriptionRequirementDetail = CustomJobDescriptionRequirementsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    if JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                        JobDescriptionRequirementDetail = JobDescriptionRequirementModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": " Job Description Requirement Detail",
                                "Data": {
                                    "JobDescriptionRequirementDetail":JobDescriptionRequirementDetail,
                                    "Data1":customJobDescriptionRequirementDetail
                                }
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Requirement data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " custom Job Description Requirement data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class JobDescriptionBenefitPlatformAPI(APIView):
    '''
        Job Description Benefit API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d",
                    "job_benefit_id":"BroaderAI_Job_Benefit_6y7bh0g84x03fs1"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                JobDescriptionData = JobDescriptionModel.objects.filter(user_id=getData["user_id"], job_description_id=getData["job_description_id"]).first()
                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                    
                uniqueID = "BroaderAI_job_description_benefit" + randomstr

                getData["job_description_benefit_id"] = uniqueID
                
                JobLevelData=JobLevelModel.objects.get(job_level_id=JobDescriptionData.job_level_id)
                JobPositionData=JobPositionModel.objects.get(job_position_id=JobDescriptionData.job_position_id)
                getData['job_position_id'] = JobPositionData.job_position_id
                getData['job_level_id']=JobLevelData.job_level_id
                getData['job_level_name']=JobLevelData.job_level_name
                getData['job_position_name'] = JobPositionData.job_position_name
                serializer = JobDescriptionBenefitSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(job_description_benefit_id=getData["job_description_benefit_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": " Job Description Benefit is Added",
                        "Data": {
                            "job_description_benefit_id": getData["job_description_benefit_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job description is not exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"]).exists():
                JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": " Job Description Benefit Detail",
                        "Data": JobDescriptionBenefitDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": " Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get Job Description Benefit from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
  
                if JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                    JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": " Job Description Benefit Detail",
                            "Data": JobDescriptionBenefitDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Benefit data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get  Job Description Benefit from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                        JobDescriptionBenefittDetail = JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": " Job Description Benefit Detail",
                                "Data": JobDescriptionBenefittDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Benefitt data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetfromJobPositionPlatformAPI(APIView):
    '''
        Get  Job Description Benefit from JobPosition API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                    
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
 
                if JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": " Job Description Benefit Detail",
                            "Data": JobDescriptionBenefitDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Benefit data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionBenefitDeletePlatformAPI(APIView):
    '''
        Job Description Requirement API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_benefit_id": "BroaderAI_job_description_requirementuaku7rr6ar7cft2"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])  
                    
            if JobDescriptionBenefitsModel.objects.filter(job_description_benefit_id = getData["job_description_benefit_id"], user_id = getData["user_id"]).exists():
                JobDescriptionRequirementDetails = JobDescriptionBenefitsModel.objects.get(job_description_benefit_id = getData["job_description_benefit_id"], user_id = getData["user_id"])
                JobDescriptionRequirementDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Requirement is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description Requirement data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class BothJobDescriptionBenefitGetfromUserJobDescriptionPlatformAPI(APIView):
    '''
        Get Both Job Description Benefit from User Job Description API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_znt8sxin1rg1g1d"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

                if JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                    
                    if CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                        customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                        JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Both Job Description Benefit Detail",
                                "Data": JobDescriptionBenefitDetail,
                                "Data1":customJobDescriptionBenefitDetail
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Benefit data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Job Description Benefit data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class BothJobDescriptionBenefitGetfromJobPositionJobLevelPlatformAPI(APIView):
    '''
        Get Both Job Description Benefit from Job Position Job Level API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "BroaderAI_job_level_gcs56oghq4ae0gf"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                        customJobDescriptionBenefittDetail = CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                        if JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                            JobDescriptionBenefittDetail = JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                            res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Both Job Description Benefit Detail",
                                    "Data": customJobDescriptionBenefittDetail,
                                    "Data1":JobDescriptionBenefittDetail
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Job Description Benefitt data is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Benefitt data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                   
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class BothJobDescriptionBenefitGetfromJobPositionPlatformAPI(APIView):
    '''
        Get Both Job Description Benefit from JobPosition API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_position_id": "BroaderAI_job_position_6d9xkfg8wr0nvml"
                    
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():

                if CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    if JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                        JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Both Job Description Benefit Detail",
                            "Data": {
                                "CustomJobDescriptionBenefitDetail":customJobDescriptionBenefitDetail,
                                "Data 1":JobDescriptionBenefitDetail}
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Custom Job Description Benefit data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job position is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
     
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class CompanyDetailRegisterPlatformAPI(APIView):
    '''
        Company Information Register API(Insert)
        Request : Post
        Data =   {
        "user_id":"BroaderAI_yashpp5545_o0ge7pbkax",
        "company_name":"Broader AI",
        "company_description":"Toward Automation",
        "company_established_year":"2022",
        "contact_number":"9913480866",
        "company_email":"yashpp5545@gmail.com",
        "company_googlelink":"https://www.broaderai.com/Services",
        "company_linkdinlink":"https://www.broaderai.com/Services",
        "company_team_member":"25",
        "company_twitter_link":"https://www.broaderai.com/Services",
        "company_facebook_link":"https://www.broaderai.com/Services",
        "company_type_id":"BroaderAI_Company_Type_ocb1ivxxd4qbgk7",
        "sector_id":"BroaderAI_sector_u0agy56cf7ihxjj",
        "company_action" :active
    }
        '''
    def post(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():
                if CompanyTypeModel.objects.filter(company_type_id=getData["company_type_id"]).exists():
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                    uniqueID = "BroaderAI_company_details_" + randomstr
                    getData["company_info_id"] = uniqueID
                    companyDetail = CompanyModel(
                        company_info_id = uniqueID,
                        company_name= getData["company_name"],
                        company_description= getData["company_description"],
                        company_established_year= getData["company_established_year"],
                        contact_number= getData["contact_number"],
                        company_email= getData["company_email"],
                        company_googlelink= getData["company_googlelink"],
                        company_linkdinlink= getData["company_linkdinlink"],
                        company_team_member= getData["company_team_member"],
                        company_twitter_link= getData["company_twitter_link"],
                        company_facebook_link= getData["company_facebook_link"],
                        sector_id = getData["sector_id"],
                        company_type_id = getData["company_type_id"], 
                        company_action = getData["company_action"]
                    )
                    companyDetail.save()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "company Details is Added",
                            "Data": {   
                                "company_info_id" : uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                    # serializer = CompanySerializer(data=getData)
                    # if serializer.is_valid():
                    #     serializer.save(company_info_id=getData["company_info_id"])
                    #     res = {
                    #           "Status": "success",
                    #         "Code": 201,
                    #         "Message": "company Details is Added",
                    #         "Data": {   "company_info_id" : getData['company_info_id'],
                    #                     "user_id": getData["user_id"]
                    #         }
                    #     }
                    #     return Response(res, status=status.HTTP_201_CREATED)
                    # else:
                    # res = {
                    #     "Status": "error",
                    #     "Code": 400,
                    #     "Message":list(serializer.errors.values())[0][0],
                    #     "Data":[],
                    # }
                    #     return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company type is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "sector is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyDetailsUpdatePlatformAPI(APIView):
    '''
        Company Information Update API(Update)
        Request : Patch
        Data =   {
                "company_info_id": "BroaderAI_company_details_biwv6fds3o4zgfg",
                "user_id":"BroaderAI_yashpp5545_o0ge7pbkax",
                "company_name":"Broader AI",
                "company_description":"Toward Automation",
                "company_established_year":"2022",
                "contact_number":"9913480866",
                "company_email":"yashpp5545@gmail.com",
                "company_googlelink":"https://www.broaderai.com/Services",
                "company_linkdinlink":"https://www.broaderai.com/Services",
                "company_team_member":"25",
                "company_twitter_link":"https://www.broaderai.com/Services",
                "company_facebook_link":"https://www.broaderai.com/Services",
                "company_type_id":"BroaderAI_Company_Type_ocb1ivxxd4qbgk7",
                "sector_id":"BroaderAI_sector_u0agy56cf7ihxjj",
                "company_action":active
    }
        '''
    def patch(self, request ,formate=None):
        
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            
            if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():
                
                if CompanyTypeModel.objects.filter(company_type_id=getData["company_type_id"]).exists():
                    
                    user = NewUser.objects.get(id=getData["user_id"])
                    if CompanyModel.objects.filter(company_info_id=getData['company_info_id']).exists():
                    
                            
                        serializer = CompanySerializer(data=getData)
                        if serializer.is_valid():

                            LastUpdateData=CompanyModel.objects.get(company_info_id=getData['company_info_id'])
                            LastUpdateData.company_name= getData['company_name']
                            LastUpdateData.company_description= getData['company_description']
                            LastUpdateData.company_established_year= getData['company_established_year']
                            LastUpdateData.contact_number= getData['contact_number']
                            LastUpdateData.company_email= getData['company_email']
                            LastUpdateData.company_googlelink= getData['company_googlelink']
                            LastUpdateData.company_linkdinlink= getData['company_linkdinlink']
                            LastUpdateData.company_team_member= getData['company_team_member']
                            LastUpdateData.company_twitter_link= getData['company_twitter_link']
                            LastUpdateData.company_facebook_link= getData['company_facebook_link']
                            LastUpdateData.sector_id = getData["sector_id"]
                            LastUpdateData.company_type_id=getData["company_type_id"]
                            LastUpdateData.company_action = getData["company_action"]
                            LastUpdateData.save()

                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "company Details is Updated",
                                "Data": {   "company_info_id" : getData['company_info_id'],
                                            "user_id": getData["user_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "company Details is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "company Type is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Sector Details is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyDetailsGetOnePlatformAPI(APIView):
    '''
        Company Information Get one API(View)
        Request : Post
        Data =    {
                        "company_info_id": "BroaderAI_company_details_u9sve9l5imktqe4",
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CompanyModel.objects.filter(company_info_id=getData['company_info_id']).exists():
                CompanyData = CompanyModel.objects.filter(company_info_id=getData['company_info_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Company Type Detail",
                        "Data": CompanyData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
    
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyDetailsGetUserPlatformAPI(APIView):
    '''
        Company Information Get one API(View)
        Request : Post
        Data =    {
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CompanyModel.objects.filter(company_info_id=getData['company_info_id']).exists():
                CompanyData = CompanyModel.objects.filter(company_info_id=getData['company_info_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Company Type Detail",
                        "Data": CompanyData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyDetailsDeletePlatformAPI(APIView):
    '''
        Company Information Delete API(delete)
        Request : delete
        Data =   {
                    "company_info_id": "BroaderAI_company_details_u9sve9l5imktqe4",
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                }
    '''
    def delete(self, request, format=None):

        getData = request.data # data comes from post request
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if CompanyModel.objects.filter(company_info_id = getData["company_info_id"]).exists():
                
                user = NewUser.objects.get(id = getData["user_id"])

                companydetasils= CompanyModel.objects.get(company_info_id = getData["company_info_id"]) 

                companydetasils.delete()

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Successfully deleted",
                        "Data": {
                                    "user_id": getData["user_id"]
                                }
                    }

                return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "company details is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]



########################################################################################
        

class CompanyLocationDetailRegisterPlatformAPI(APIView):
    '''
        Company Location Information Register API(Insert)
        Request : Post
        Data =   {
        "user_id":"BroaderAI_yashpp5545_o0ge7pbkax",
        "company_info_id": "BroaderAI_company_details_biwv6fds3o4zgfg",
        "location_id" :"BroaderAI_location_t1m8ev30guawu9q",
        "is_headquarter":"Yes",
        "company_address":"426 soham archde"
}
    '''
    def post(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if not CompanyLocationModel.objects.filter(company_address=getData['company_address'],company_info_id = getData["company_info_id"], location_id = getData["location_id"] ).exists():
                
                if getData["is_headquarter"] =="Yes":
                    if CompanyLocationModel.objects.filter(company_info_id = getData["company_info_id"], is_headquarter = "Yes" ).exists():
                        CompanyLocationModel.objects.filter(company_info_id=getData["company_info_id"], is_headquarter="Yes").update(is_headquarter="No")

                        user = NewUser.objects.get(id=getData["user_id"])
                        if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                            
                            if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                              
                                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                                    string.digits, k=15))

                                uniqueID = "BroaderAI_company_location_details_" + randomstr
                                getData["company_location_id"] = uniqueID
                                
                                serializer = CompanyLocationSerializer(data=getData)
                                
                                if serializer.is_valid():
                                    
                                    serializer.save(company_location_id=getData["company_location_id"])
                                    res = {
                                        "Status": "success",
                                        "Code": 201,
                                        "Message": "company Location Details is Added",
                                        "Data": {   "company_location_id" : getData['company_location_id'],
                                                    "user_id": getData["user_id"]
                                        }
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                                
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 400,
                                        "Message":list(serializer.errors.values())[0][0],
                                        "Data":[],
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                   
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Location is not found",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        user = NewUser.objects.get(id=getData["user_id"])
                        if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                            
                            if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
 
                                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                                    string.digits, k=15))

                                uniqueID = "BroaderAI_company_location_details_" + randomstr
                                getData["company_location_id"] = uniqueID
                                
                                serializer = CompanyLocationSerializer(data=getData)
                                
                                if serializer.is_valid():
                                    
                                    serializer.save(company_location_id=getData["company_location_id"])
                                    res = {
                                        "Status": "success",
                                        "Code": 201,
                                        "Message": "company Location Details is Added",
                                        "Data": {   "company_location_id" : getData['company_location_id'],
                                                    "user_id": getData["user_id"]
                                        }
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                                
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 400,
                                        "Message":list(serializer.errors.values())[0][0],
                                        "Data":[],
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                            
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Location is not found",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    user = NewUser.objects.get(id=getData["user_id"])
                    if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                        
                        if LocationModel.objects.filter(location_id=getData["location_id"]).exists():

                            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                                string.digits, k=15))

                            uniqueID = "BroaderAI_company_location_details_" + randomstr
                            getData["company_location_id"] = uniqueID
                            
                            serializer = CompanyLocationSerializer(data=getData)
                            
                            if serializer.is_valid():
                                
                                serializer.save(company_location_id=getData["company_location_id"])
                                res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "company Location Details is Added",
                                    "Data": {   "company_location_id" : getData['company_location_id'],
                                                "user_id": getData["user_id"]
                                    }
                                }
                                return Response(res, status=status.HTTP_201_CREATED)
                            
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 400,
                                    "Message":list(serializer.errors.values())[0][0],
                                    "Data":[],
                                }
                                return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Location is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Company is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company location is already register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyLocationDetailsUpdatePlatformAPI(APIView):
    '''
        Company Location Information Update API(Update)
        Request : Patch
        Data =   {
            "company_location_id": "BroaderAI_company_location_details_gwv2knponpv6cso",
            "user_id":"BroaderAI_yashpp5545_o0ge7pbkax",
            "company_info_id": "BroaderAI_company_details_biwv6fds3o4zgfg",
            "location_id" :"BroaderAI_location_t1m8ev30guawu9q",
            "is_headquarter":"Yes",
            "company_address":"426 soham archde"
            }
    '''
    def patch(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CompanyLocationModel.objects.filter(company_location_id=getData["company_location_id"]).exists():
                if not CompanyLocationModel.objects.filter(is_headquarter=getData['is_headquarter'],company_address=getData['company_address'],company_info_id = getData["company_info_id"], location_id = getData["location_id"] ).exists():
                    
                    if getData["is_headquarter"] =="Yes":
                        
                        if CompanyLocationModel.objects.filter(company_info_id = getData["company_info_id"], is_headquarter = "Yes" ).exists():

                            CompanyLocationModel.objects.filter(company_info_id=getData["company_info_id"], is_headquarter="Yes").update(is_headquarter="No")

                            user = NewUser.objects.get(id=getData["user_id"])
                            if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                                
                                if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
   
                                    serializer = CompanyLocationSerializer(data=getData)
                                    if serializer.is_valid():
                                        print('Yash')
                                        LastUpdateData=CompanyLocationModel.objects.get(company_location_id=getData['company_location_id'])
                                        LastUpdateData.company_info_id=getData['company_info_id']
                                        LastUpdateData.location_id = getData['location_id']
                                        LastUpdateData.is_headquarter=getData['is_headquarter']
                                        LastUpdateData.company_address=getData['company_address']
                                        LastUpdateData.save()
                                        
                                        res = {
                                            "Status": "success",
                                            "Code": 201,
                                            "Message": "company Location Details is Updated",
                                            "Data": {   "company_location_id" : getData['company_location_id'],
                                                        "user_id": getData["user_id"]
                                            }
                                        }
                                        return Response(res, status=status.HTTP_201_CREATED)
                                    
                                    else:
                                        res = {
                                            "Status": "error",
                                            "Code": 400,
                                            "Message":list(serializer.errors.values())[0][0],
                                            "Data":[],
                                        }
                                        return Response(res, status=status.HTTP_201_CREATED)
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 401,
                                        "Message": "Location is not found",
                                        "Data":[],
                                        }
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Company is not found",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            user = NewUser.objects.get(id=getData["user_id"])
                            if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                                
                                if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                                   
                                    serializer = CompanyLocationSerializer(data=getData)
                                    if serializer.is_valid():
                    
                                        LastUpdateData=CompanyLocationModel.objects.get(company_location_id=getData['company_location_id'])
                                        LastUpdateData.company_info_id=getData['company_info_id']
                                        LastUpdateData.location_id = getData['location_id']
                                        LastUpdateData.is_headquarter=getData['is_headquarter']
                                        LastUpdateData.company_address=getData['company_address']
                                        LastUpdateData.save()
                                        
                                        res = {
                                            "Status": "success",
                                            "Code": 201,
                                            "Message": "company Location Details is Updated",
                                            "Data": {   "company_location_id" : getData['company_location_id'],
                                                        "user_id": getData["user_id"]
                                            }
                                        }
                                        return Response(res, status=status.HTTP_201_CREATED)
                                    
                                    else:
                                        res = {
                                            "Status": "error",
                                            "Code": 400,
                                            "Message":list(serializer.errors.values())[0][0],
                                            "Data":[],
                                        }
                                        return Response(res, status=status.HTTP_201_CREATED)
                                    
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 401,
                                        "Message": "Location is not found",
                                        "Data":[],
                                        }
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Company is not found",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        user = NewUser.objects.get(id=getData["user_id"])
                        if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                            
                            if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                             
                                serializer = CompanyLocationSerializer(data=getData)
                                if serializer.is_valid():
                                    LastUpdateData=CompanyLocationModel.objects.get(company_location_id=getData['company_location_id'])
                                    LastUpdateData.company_info_id=getData['company_info_id']
                                    LastUpdateData.location_id = getData['location_id']
                                    LastUpdateData.is_headquarter=getData['is_headquarter']
                                    LastUpdateData.company_address=getData['company_address']
                                    LastUpdateData.save()
                                    
                                    res = {
                                        "Status": "success",
                                        "Code": 201,
                                        "Message": "company Location Details is Updated",
                                        "Data": {   "company_location_id" : getData['company_location_id'],
                                                    "user_id": getData["user_id"]
                                        }
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                                
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 400,
                                        "Message":list(serializer.errors.values())[0][0],
                                        "Data":[],
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                                
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Location is not found",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company location details is already register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company location data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyLocationDetailsCompanyGetPlatformAPI(APIView):
    '''
        Company location Information Get API(View)
        Request : Post
        Data =    {
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                        "company_info_id": "BroaderAI_company_details_biwv6fds3o4zgfg",
                    }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CompanyLocationModel.objects.filter(company_info_id=getData['company_info_id']).exists():
                CompanyLocationData = CompanyLocationModel.objects.filter(company_info_id=getData['company_info_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Company Location Detail",
                        "Data": CompanyLocationData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company location data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyLocationDetailsGetOnePlatformAPI(APIView):
    '''
        Company Information Get one API(View)
        Request : Post
        Data =    {
                        "company_location_id": "BroaderAI_company_location_details_1uc27stzhs5d297",
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if CompanyLocationModel.objects.filter(company_location_id=getData['company_location_id']).exists():
                CompanyLocationData = CompanyLocationModel.objects.filter(company_location_id=getData['company_location_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Company Location Detail",
                        "Data": CompanyLocationData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company location data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class CompanyLocationDetailsDeletePlatformAPI(APIView):
    '''
        Company Information Delete API(delete)
        Request : delete
        Data =   {
                    "company_location_id": "BroaderAI_company_location_details_1uc27stzhs5d297",
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                }
    '''
    def delete(self, request, format=None):

        getData = request.data # data comes from post request
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if CompanyLocationModel.objects.filter(company_location_id = getData["company_location_id"]).exists():
                
                user = NewUser.objects.get(id = getData["user_id"])

                companylocationdetails= CompanyLocationModel.objects.get(company_location_id = getData["company_location_id"]) 

                companylocationdetails.delete()

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Successfully deleted",
                        "Data": {
                                    "user_id": getData["user_id"]
                                }
                    }

                return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "company location details is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
    
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class JobDescriptionCompanyLocationDetailRegisterPlatformAPI(APIView):
    '''
        Job Description Company Location Detail Register API(Insert)
        Request : Post
        Data =   {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "company_location_id": "BroaderAI_company_location_details_gwv2knponpv6cso",
                    "work_place_id": "BroaderAI_Work_Place_4ga8en8ovachx4j"
                    "job_description_id": "BroaderAI_job_description_wscn158p2f13rmv",
                    "Job_description_company_location_action": "active"
                    }
    '''
    def post(self, request ,formate=None):
        
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id=getData["job_description_id"]).exists():
                
                if WorkPlaceModel.objects.filter(work_place_id=getData["work_place_id"]).exists():
                    if CompanyLocationModel.objects.filter(company_location_id=getData["company_location_id"]).exists():

                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

                        uniqueID = "BroaderAI_job_description_company_location_details_" + randomstr
                        getData["Job_description_company_location_id"] = uniqueID
                        
                        serializer = JobDescritionCompanyLocationSerializer(data=getData)
                        
                        if serializer.is_valid():
                            
                            serializer.save(Job_description_company_location_id=getData["Job_description_company_location_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job Description Company Location Detail Added",
                                "Data": {   "Job_description_company_location_id" : getData['Job_description_company_location_id'],
                                            "user_id": getData["user_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company location is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Work place is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Descrition is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionCompanyLocationDetailsUpdatePlatformAPI(APIView):
    '''
        Job Description Company Information Register API(Update)
        Request : Patch
        Data =   {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "Job_description_company_location_id": "BroaderAI_job_description_company_location_details_tbacaq19qm93lpf",
                    "company_location_id": "BroaderAI_company_location_details_gwv2knponpv6cso",
                    "work_place_id": "BroaderAI_Work_Place_4ga8en8ovachx4j",
                    "job_description_id": "BroaderAI_job_description_wscn158p2f13rmv",
                    "Job_description_company_location_action": "active"
                }
        '''
    def patch(self, request ,formate=None):
        
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if JobDescriptionModel.objects.filter(job_description_id=getData["job_description_id"]).exists():

                if WorkPlaceModel.objects.filter(work_place_id=getData["work_place_id"]).exists():
                    
                    if CompanyLocationModel.objects.filter(company_location_id=getData["company_location_id"]).exists():

                        user = NewUser.objects.get(id=getData["user_id"]) 
                            
                        serializer = JobDescritionCompanyLocationSerializer(data=getData)
                        if serializer.is_valid():
                            
                            LastUpdateData=JobDescriptionCompanyLocationModel.objects.get(Job_description_company_location_id=getData['Job_description_company_location_id'])
                            LastUpdateData.company_location_id= getData['company_location_id']
                            LastUpdateData.work_place_id= getData['work_place_id']
                            LastUpdateData.job_description_id= getData['job_description_id']
                            LastUpdateData.Job_description_company_location_action = getData['Job_description_company_location_action']
                            LastUpdateData.save()
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job Description company Details is Updated",
                                "Data": {   "Job_description_company_location_id" : getData['Job_description_company_location_id'],
                                            "user_id": getData["user_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "company Location is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Work Place is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description Details is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
   
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionCompanyLocationDetailsGetOnePlatformAPI(APIView):
    '''
        Job Description Company Information Get one API(View)
        Request : Post
        Data =    {
                         "Job_description_company_location_id": "BroaderAI_job_description_company_location_details_7ybkya33cnhsl3l",
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionCompanyLocationModel.objects.filter(Job_description_company_location_id=getData['Job_description_company_location_id']).exists():
                JobDescriptionCompanyLocationData = JobDescriptionCompanyLocationModel.objects.filter(Job_description_company_location_id=getData['Job_description_company_location_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Company Location Detail",
                        "Data": JobDescriptionCompanyLocationData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description Company location data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionCompanyLocationDetailsDeletePlatformAPI(APIView):
    '''
        Job Description Company Information Delete API(delete)
        Request : delete
        Data =   {
                         "Job_description_company_location_id": "BroaderAI_job_description_company_location_details_7ybkya33cnhsl3l",
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    }
    '''
    def delete(self, request, format=None):

        getData = request.data # data comes from post request
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobDescriptionCompanyLocationModel.objects.filter(Job_description_company_location_id = getData["Job_description_company_location_id"]).exists():
                
                user = NewUser.objects.get(id = getData["user_id"])

                JobDescriptioncompanylocationdetails= JobDescriptionCompanyLocationModel.objects.get(Job_description_company_location_id = getData["Job_description_company_location_id"]) 

                JobDescriptioncompanylocationdetails.delete()

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Successfully deleted",
                        "Data": {
                                    "user_id": getData["user_id"]
                                }
                    }

                return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "company location details is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
    
    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################


class JobDescriptionEmploymentTypeDetailRegisterPlatformAPI(APIView):
    '''
        Job Description Employment Type Detail Register API(Insert)
        Request : Post
        Data =   {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "job_description_id": "BroaderAI_job_description_wscn158p2f13rmv",
                     "employment_type_id": "BroaderAI_Employment_Type_kp2wxi0hvukglfr",
                     "Job_description_employment_type_action":active
                    }
    '''
    def post(self, request ,formate=None):
        
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if JobDescriptionModel.objects.filter(job_description_id=getData["job_description_id"]).exists():
                
                if EmploymentTypeModel.objects.filter(employment_type_id=getData["employment_type_id"]).exists():

                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))

                    uniqueID = "BroaderAI_job_description_employment_type_details_" + randomstr
                    getData["Job_description_employment_type_id"] = uniqueID
                    
                    serializer = JobDescritionEmploymentTypeSerializer(data=getData)
                    
                    if serializer.is_valid():
                        
                        serializer.save(Job_description_employment_type_id=getData["Job_description_employment_type_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Description Employment type Detail Added",
                            "Data": {   "Job_description_employment_type_id" : getData['Job_description_employment_type_id'],
                                        "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                  
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Employment type is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Descrition is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionEmploymentTypeDetailsUpdatePlatformAPI(APIView):
    '''
        Job Description Employment Type Details API(Update)
        Request : Patch
        Data =   {
            "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
            "Job_description_employment_type_id": "BroaderAI_job_description_employment_type_details_jkhs9qukija4ogu",
            "employment_type_id": "BroaderAI_Employment_Type_kp2wxi0hvukglfr",
            "job_description_id": "BroaderAI_job_description_wscn158p2f13rmv"
        }
        '''
    def patch(self, request ,formate=None):
        
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if JobDescriptionModel.objects.filter(job_description_id=getData["job_description_id"]).exists():
                
                if EmploymentTypeModel.objects.filter(employment_type_id=getData["employment_type_id"]).exists():
                    
                    if JobDescriptionEmploymentTypeModel.objects.filter(Job_description_employment_type_id=getData["Job_description_employment_type_id"]).exists():

                        user = NewUser.objects.get(id=getData["user_id"])

                            
                        serializer = JobDescritionEmploymentTypeSerializer(data=getData)
                        if serializer.is_valid():

                            LastUpdateData=JobDescriptionEmploymentTypeModel.objects.get(Job_description_employment_type_id=getData['Job_description_employment_type_id'])
                            LastUpdateData.employment_type_id= getData['employment_type_id']
                            LastUpdateData.job_description_id= getData['job_description_id']
                            LastUpdateData.save()
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job descrition Emloyment type is Updated",
                                "Data": {   "Job_description_employment_type_id" : getData['Job_description_employment_type_id'],
                                            "user_id": getData["user_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message":list(serializer.errors.values())[0][0],
                                "Data":[],
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description Employment Type is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Employment Type is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description Details is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]  

class JobDescriptionEmploymentTypeGetbyDescpPlatformAPI(APIView):
    '''
        Job Description Employment type Information Get API(View)
        Request : Post
        Data =   {
                    "job_description_id": 'BroaderAI_job_description_3ghrhh6rd7gbjym',
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionEmploymentTypeModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                JobDescriptionEmploymentTypeData = JobDescriptionEmploymentTypeModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Employment type  Detail",
                        "Data": JobDescriptionEmploymentTypeData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description Employment Type data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)


    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
  
class JobDescriptionEmploymentTypeDetailsGetOnePlatformAPI(APIView):
    '''
        Job Description  Employment type Get one API(View)
        Request : Post
        Data =    {
                        "Job_description_employment_type_id": "BroaderAI_job_description_employment_type_details_dd25h35tch5twrs"
                        "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    }
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JobDescriptionEmploymentTypeModel.objects.filter(Job_description_employment_type_id=getData['Job_description_employment_type_id']).exists():
                JobDescriptionEmploymentTypeData = JobDescriptionEmploymentTypeModel.objects.filter(Job_description_employment_type_id=getData['Job_description_employment_type_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Employment type Detail",
                        "Data": JobDescriptionEmploymentTypeData
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description Employment Type is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JobDescriptionEmploymentTypeDetailsDeletePlatformAPI(APIView):
    '''
        Job Description Employment Type Delete API(delete)
        Request : delete
        Data =   {
                    "Job_description_employment_type_id": "BroaderAI_job_description_employment_type_details_jkhs9qukija4ogu",
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                }
    '''
    def delete(self, request, format=None):

        getData = request.data # data comes from post request
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if JobDescriptionEmploymentTypeModel.objects.filter(Job_description_employment_type_id = getData["Job_description_employment_type_id"]).exists():
                
                user = NewUser.objects.get(id = getData["user_id"])

                JobDescriptionEmploymentTypeData= JobDescriptionEmploymentTypeModel.objects.get(Job_description_employment_type_id = getData["Job_description_employment_type_id"]) 

                JobDescriptionEmploymentTypeData.delete()

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Successfully deleted",
                        "Data": {
                                    "user_id": getData["user_id"]
                                }
                    }

                return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description Employment Type is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################

class UserCompanyRegisterPlatformAPI(APIView):
    '''
        User Company Register API(Insert)
        Request : Post
        Data =   {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "company_info_id": "BroaderAI_company_details_u9sve9l5imktqe4",
                    }
    '''
    def post(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_user_company_details_" + randomstr
                getData["user_company_id"] = uniqueID
                serializer = UserCompanySerializer(data=getData)
                if serializer.is_valid():
                    serializer.save(user_company_id=getData["user_company_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "User Company Detail Added",
                        "Data": {   "user_company_id" : getData['user_company_id'],
                                    "user_id": getData["user_id"],
                                    "company_info_id": getData["company_info_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]        

class UserCompanyUpdatePlatformAPI(APIView):
    '''
        User Company Update API(Update)
        Request : Patch
        Data =   {
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "user_company_id": "BroaderAI_user_company_details_ntodlfvd7ffjmbw"
                    "company_info_id": "BroaderAI_company_details_biwv6fds3o4zgfg"

                    }
        '''
    def patch(self, request ,formate=None):
        
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if UserCompanyModel.objects.filter(user_company_id=getData["user_company_id"]).exists():
                if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                    
                    user = NewUser.objects.get(id=getData["user_id"])
                        
                    serializer = UserCompanySerializer(data=getData)
                    if serializer.is_valid():

                        LastUpdateData=UserCompanyModel.objects.get(user_company_id=getData['user_company_id'])
                        LastUpdateData.company_info_id= getData['company_info_id']
                        LastUpdateData.user_id= getData['user_id']
                        LastUpdateData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job descrition Emloyment type is Updated",
                            "Data": {   "user_company_id" : getData['user_company_id'],
                                        "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User Company is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class UserCompanyGetOnePlatformAPI(APIView):
    '''
        User Company Get one API(View)
        Request : Post
        Data =    {
                        
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "company_info_id": "BroaderAI_company_details_u9sve9l5imktqe4",
                }
            
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if UserCompanyModel.objects.filter(company_info_id=getData['company_info_id']).exists():
                usercompanydata = UserCompanyModel.objects.filter(company_info_id=getData['company_info_id']).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "User Company  Detail",
                        "Data": usercompanydata
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User Company is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class UserCompanyGetOneUserPlatformAPI(APIView):
    '''
        User Company Get one API(View)
        Request : Post
        Data =    {
                        
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax"
                    
                }
            
    '''
    def post(self, request, format=None):

        getData = request.data 
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if UserCompanyModel.objects.filter(user_id=getData['user_id']).exists():
                usercompanydata = UserCompanyModel.objects.filter(user_id=getData['user_id']).values()

                companyDetails = CompanyModel.objects.filter(company_info_id=usercompanydata[0]["company_info_id"]).values()

                company_type_details = CompanyTypeModel.objects.get(company_type_id= companyDetails[0]["company_type_id"])
                sector_details = SectorModel.objects.get(sector_id= companyDetails[0]["sector_id"])

                companyDetails[0]["sector_name"] = sector_details.sector_name
                companyDetails[0]["company_type_name"] = company_type_details.company_type_name

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "User Company  Detail",
                        "Data": {
                            "User_company_data": usercompanydata,
                            "Company_details": companyDetails[0],
                            "company_main_details": {
                                "company_info_id":  companyDetails[0]["company_info_id"],
                                "company_name": companyDetails[0]["company_name"],
                                "company_type_id": companyDetails[0]["company_type_id"],
                                "company_type_name": company_type_details.company_type_name,
                                "sector_id": companyDetails[0]["sector_id"],
                                "sector_name": sector_details.sector_name,
                            }
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User Company is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class UserCompanyDeletePlatformAPI(APIView):
    '''
        User Company Delete API(delete)
        Request : delete
        Data =   {
                        
                    "user_id": "BroaderAI_yashpp5545_o0ge7pbkax",
                    "user_company_id": "BroaderAI_user_company_details_ntodlfvd7ffjmbw",
                }
    '''
    def delete(self, request, format=None):

        getData = request.data # data comes from post request
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            
            if UserCompanyModel.objects.filter(user_company_id = getData["user_company_id"],user_id = getData["user_id"]).exists():
                
                user = NewUser.objects.get(id = getData["user_id"])

                
                UserCompanyData= UserCompanyModel.objects.get(user_company_id = getData["user_company_id"],user_id = getData["user_id"]) 

                UserCompanyData.delete()

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Successfully deleted",
                        "Data": {
                                    "user_id": getData["user_id"]
                                }
                    }

                return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User Company is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

    
###############################################################################################################################################

class AllJobDescriptionGetPlatformAPI(APIView):
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                
            # if JobDescriptionModel.objects.filter( user_id=getData["user_id"], job_description_id = getData["job_description_id"],job_description_action = getData["job_description_action"]).exists():
            JobDescriptionDetail0 = JobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail1 = EducationJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail2 = SoftSkillJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail3 = TechnicalSkillJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail4 = CustomJobDescriptionResponsibilityModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail5 = CustomJobDescriptionRequirementsModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail6 = CustomJobDescriptionBenefitsModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail7 = JobDescriptionResponsibilityModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail8 = JobDescriptionRequirementModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail9 = JobDescriptionBenefitsModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail10 = JobDescriptionCompanyLocationModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            JobDescriptionDetail11 = JobDescriptionEmploymentTypeModel.objects.filter( job_description_id = getData["job_description_id"]).values()
            NationalityDetail = NationalityJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
            GenderDetail = GenderJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
            WorkPlaceDetail = WorkPlaceJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
            LanguageDetail = LanguageJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
            JoiningPeriodDetail = JoiningPeriodJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()

            # print(JobDescriptionDetail0,JobDescriptionDetail1,JobDescriptionDetail2,JobDescriptionDetail3,JobDescriptionDetail4,JobDescriptionDetail5,JobDescriptionDetail6,JobDescriptionDetail7,JobDescriptionDetail8,JobDescriptionDetail9,JobDescriptionDetail10,JobDescriptionDetail11)
            
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Description Detail",
                    "Data": {
                        "JobDescription_Data":JobDescriptionDetail0,#JobDescriptionModel
                        "EducationJobDescription_Data": JobDescriptionDetail1,#EducationJobDescriptionModel
                        "SoftSkillJobDescription_Data": JobDescriptionDetail2,#SoftSkillJobDescriptionModel
                        "TechnicalSkillJobDescription_Data": JobDescriptionDetail3,#TechnicalSkillJobDescriptionModel
                        "CustomJobDescriptionResponsibility_Data": JobDescriptionDetail4,#CustomJobDescriptionResponsibilityModel
                        "CustomJobDescriptionRequirements_Data": JobDescriptionDetail5,#CustomJobDescriptionRequirementsModel
                        "CustomJobDescriptionBenefits_Data": JobDescriptionDetail6,#CustomJobDescriptionBenefitsModel
                        "JobDescriptionResponsibility_Data": JobDescriptionDetail7,#JobDescriptionResponsibilityModel
                        "JobDescriptionRequirement_Data": JobDescriptionDetail8,#JobDescriptionRequirementModel
                        "JobDescriptionBenefits_Data": JobDescriptionDetail9,#JobDescriptionBenefitsModel
                        "JobDescriptionCompanyLocation_Data": JobDescriptionDetail10,#JobDescriptionCompanyLocationModel
                        "JobDescriptionEmploymentType_Data": JobDescriptionDetail11,#JobDescriptionEmploymentTypeModel
                        "Nationality_Data":NationalityDetail,#NationalityJobDescriptionModel
                        "Gender_Data":GenderDetail,#GenderJobDescriptionModel
                        "WorkPlace_Data":WorkPlaceDetail,#WorkPlaceJobDescriptionModel
                        "language_Data":LanguageDetail,#LanguageJobDescriptionModel
                        "JoiningPeriod_Data":JoiningPeriodDetail,#JoiningPeriodJobDescriptionModel
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
            # else:
            #     res = {
            # "Status": "error",
            # "Code": 401,
            # "Message": "Job Description data is not found",
            # "Data":[],
            # }
            #     return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

        
###################################################################################################################################################
# Nationality Job Description

class NationalityJobDescriptionPlatformAPI(APIView):
    '''
        Nationality Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "nationality_id": "BroaderAI_nationality_wlqb09w3i8oem0k"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if not NationalityJobDescriptionModel.objects.filter(user_id=getData['user_id'],job_description_id=getData['job_description_id'],nationality_id = getData["nationality_id"]).exists():
                    
                if NationalityModel.objects.filter(nationality_id = getData["nationality_id"]).exists():
                        
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                                        
                    uniqueID = "BroaderAI_nationality_job_description_" + randomstr

                    getData["nationality_job_description_id"] = uniqueID
                    
                    NationalityData = NationalityModel.objects.get(nationality_id=getData["nationality_id"])
                    getData['nationality_name'] = NationalityData.nationality_name

                    serializer = NationalityJobDescriptionSerializer(data=getData)

                    if serializer.is_valid():
                        serializer.save(nationality_job_description_id=getData["nationality_job_description_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Nationalitys Job Description is Added",
                            "Data": {
                                "nationality_job_description_id": getData["nationality_job_description_id"],
                                "user_id":getData['user_id'],
                                "job_description_id":getData["job_description_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Nationalitys is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
             
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class NationalityJobDescriptionGetPlatformAPI(APIView):
    '''
        Nationality Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        NationalityJobDescriptionGetDetails = NationalityJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Nationality Job Description Details",
                "Data": NationalityJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]  

class NationalityJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if NationalityJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                NationalityJobDescriptionDetail = NationalityJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Nationalitys Job Description Detail",
                        "Data": NationalityJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Nationalitys Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class NationalityJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "nationality_job_description_id": "BroaderAI_nationality_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if NationalityJobDescriptionModel.objects.filter(nationality_job_description_id = getData["nationality_job_description_id"]).exists():
                NationalityJobDescriptionDetail = NationalityJobDescriptionModel.objects.filter(nationality_job_description_id = getData["nationality_job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Nationalitys Job Description Detail",
                        "Data": NationalityJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Nationalitys Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class NationalityJobDescriptionDeletePlatformAPI(APIView):
    '''
        Nationalitys Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "nationality_job_description_id": "BroaderAI_soft_skill_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if NationalityJobDescriptionModel.objects.filter(nationality_job_description_id = getData["nationality_job_description_id"]).exists():
                NationalityJobDescriptionDetail = NationalityJobDescriptionModel.objects.get(nationality_job_description_id = getData["nationality_job_description_id"])
                NationalityJobDescriptionDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Nationality Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Nationality Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

        
###################################################################################################################################################
# gender Job Description

class GenderJobDescriptionPlatformAPI(APIView):
    '''
        Gender Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "gender": "Male"    
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if not GenderJobDescriptionModel.objects.filter(user_id=getData['user_id'],job_description_id=getData['job_description_id'],gender = getData["gender"]).exists():

                        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                    
                uniqueID = "BroaderAI_gender_job_description_" + randomstr

                getData["gender_job_description_id"] = uniqueID
                
                # NationalityData = NationalityModel.objects.get(gender_id=getData["gender_id"])
                # getData['gender_name'] = NationalityData.gender_name

                serializer = GenderJobDescriptionSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(gender_job_description_id=getData["gender_job_description_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Gender Job Description is Added",
                        "Data": {
                            "gender_job_description_id": getData["gender_job_description_id"],
                            "user_id":getData['user_id'],
                            "job_description_id":getData["job_description_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message":list(serializer.errors.values())[0][0],
                        "Data":[],
                    }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class GenderJobDescriptionGetPlatformAPI(APIView):
    '''
        Gender Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        GenderJobDescriptionGetDetails = GenderJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Gender Job Description Details",
                "Data": GenderJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class GenderJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if GenderJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                GenderJobDescriptionDetail = GenderJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Gender Job Description Detail",
                        "Data": GenderJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Gender Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class GenderJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "gender_job_description_id": "BroaderAI_gender_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if GenderJobDescriptionModel.objects.filter(gender_job_description_id = getData["gender_job_description_id"]).exists():
                GenderJobDescriptionDetail = GenderJobDescriptionModel.objects.filter(gender_job_description_id = getData["gender_job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Gender Job Description Detail",
                        "Data": GenderJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Gender Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class GenderJobDescriptionDeletePlatformAPI(APIView):
    '''
        Gender Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "gender_job_description_id": "BroaderAI_soft_skill_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if GenderJobDescriptionModel.objects.filter(gender_job_description_id = getData["gender_job_description_id"]).exists():
                GenderJobDescriptionDetail = GenderJobDescriptionModel.objects.get(gender_job_description_id = getData["gender_job_description_id"])
                GenderJobDescriptionDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Gender Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Gender Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################


class WorkPlaceJobDescriptionPlatformAPI(APIView):
    '''
        Work Place Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "work_place_id": "BroaderAI_work_place_wlqb09w3i8oem0k"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if not WorkPlaceJobDescriptionModel.objects.filter(user_id=getData['user_id'],job_description_id=getData['job_description_id'],work_place_id = getData["work_place_id"]).exists():

                    
                if WorkPlaceModel.objects.filter(work_place_id = getData["work_place_id"]).exists():
                        
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                                        
                    uniqueID = "BroaderAI_work_place_job_description_" + randomstr

                    getData["work_place_job_description_id"] = uniqueID
                    
                    WorkPlaceData = WorkPlaceModel.objects.get(work_place_id=getData["work_place_id"])
                    getData['work_place_name'] = WorkPlaceData.work_place_name

                    serializer = WorkPlaceJobDescriptionSerializer(data=getData)

                    if serializer.is_valid():
                        serializer.save(work_place_job_description_id=getData["work_place_job_description_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Work Place Job Description is Added",
                            "Data": {
                                "work_place_job_description_id": getData["work_place_job_description_id"],
                                "user_id":getData['user_id'],
                                "job_description_id":getData["job_description_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Work Place is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionGetPlatformAPI(APIView):
    '''
        Work Place Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        WorkPlaceJobDescriptionDetails = WorkPlaceJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Nationality Job Description Details",
                "Data": WorkPlaceJobDescriptionDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if WorkPlaceJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                WorkPlaceJobDescriptionDetails = WorkPlaceJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Work Place Job Description Detail",
                        "Data": WorkPlaceJobDescriptionDetails
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Work Place Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "work_place_job_description_id": "BroaderAI_work_place_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if WorkPlaceJobDescriptionModel.objects.filter(work_place_job_description_id = getData["work_place_job_description_id"]).exists():
                WorkPlaceJobDescriptionDetails = WorkPlaceJobDescriptionModel.objects.filter(work_place_job_description_id = getData["work_place_job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Work Place Job Description Detail",
                        "Data": WorkPlaceJobDescriptionDetails
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Work Place Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionDeletePlatformAPI(APIView):
    '''
        Work Place Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "work_place_job_description_id": "BroaderAI_soft_skill_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if WorkPlaceJobDescriptionModel.objects.filter(work_place_job_description_id = getData["work_place_job_description_id"]).exists():
                WorkPlaceJobDescriptionDetails = WorkPlaceJobDescriptionModel.objects.get(work_place_job_description_id = getData["work_place_job_description_id"])
                WorkPlaceJobDescriptionDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "WorkPlaceJobDescriptionDetails Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Work Place Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################


class LanguageJobDescriptionPlatformAPI(APIView):
    '''
        Language Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "language_id": "BroaderAI_language_wlqb09w3i8oem0k"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if not LanguageJobDescriptionModel.objects.filter(user_id=getData['user_id'], job_description_id=getData['job_description_id'],language_id = getData["language_id"]).exists():

                    
                if LanguageModel.objects.filter(language_id = getData["language_id"]).exists():
                        
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                                        
                    uniqueID = "BroaderAI_language_job_description_" + randomstr

                    getData["language_job_description_id"] = uniqueID
                    
                    NationalityData = LanguageModel.objects.get(language_id=getData["language_id"])
                    getData['language_name'] = NationalityData.language_name

                    serializer = LanguageJobDescriptionSerializer(data=getData)

                    if serializer.is_valid():
                        serializer.save(language_job_description_id=getData["language_job_description_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Language Job Description is Added",
                            "Data": {
                                "language_job_description_id": getData["language_job_description_id"],
                                "user_id":getData['user_id'],
                                "job_description_id":getData["job_description_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Language is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class LanguageJobDescriptionGetPlatformAPI(APIView):
    '''
        Language Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        LanguageJobDescriptionGetDetails = LanguageJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Language Job Description Details",
                "Data": LanguageJobDescriptionGetDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class LanguageJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if LanguageJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                LanguageJobDescriptionGetDetails = LanguageJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Language Job Description Detail",
                        "Data": LanguageJobDescriptionGetDetails
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Language Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class LanguageJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "language_job_description_id": "BroaderAI_language_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if LanguageJobDescriptionModel.objects.filter(language_job_description_id = getData["language_job_description_id"]).exists():
                LanguageJobDescriptionGetDetails = LanguageJobDescriptionModel.objects.filter(language_job_description_id = getData["language_job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Language Job Description Detail",
                        "Data": LanguageJobDescriptionGetDetails
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Language Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
          
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class LanguageJobDescriptionDeletePlatformAPI(APIView):
    '''
        Language Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "language_job_description_id": "BroaderAI_soft_skill_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                    
            if LanguageJobDescriptionModel.objects.filter(language_job_description_id = getData["language_job_description_id"]).exists():
                LanguageJobDescriptionGetDetails = LanguageJobDescriptionModel.objects.get(language_job_description_id = getData["language_job_description_id"])
                LanguageJobDescriptionGetDetails.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Language Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Language Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

###################################################################################################################################################


class JoiningPeriodJobDescriptionPlatformAPI(APIView):
    '''
        Nationality Job Description API(Insert)
        Request : POST
        Data = {
                    "user_id":"BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id":"BroaderAI_job_description_6s8ceoxeahnp168",
                    "joining_period_id": "BroaderAI_joining_period_wlqb09w3i8oem0k"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if not JoiningPeriodJobDescriptionModel.objects.filter(user_id=getData['user_id'],job_description_id=getData['job_description_id'],joining_period_id = getData["joining_period_id"]).exists():
                    
                if JoiningPeriodModel.objects.filter(joining_period_id = getData["joining_period_id"]).exists():
                        
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                                        
                    uniqueID = "BroaderAI_joining_period_job_description_" + randomstr

                    getData["joining_period_job_description_id"] = uniqueID
                    
                    JoiningPeriodData = JoiningPeriodModel.objects.get(joining_period_id=getData["joining_period_id"])
                    getData['joining_period_name'] = JoiningPeriodData.joining_period_name

                    serializer = JoiningPeriodJobDescriptionSerializer(data=getData)

                    if serializer.is_valid():
                        serializer.save(joining_period_job_description_id=getData["joining_period_job_description_id"])
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Joining Period Job Description is Added",
                            "Data": {
                                "joining_period_job_description_id": getData["joining_period_job_description_id"],
                                "user_id":getData['user_id'],
                                "job_description_id":getData["job_description_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message":list(serializer.errors.values())[0][0],
                            "Data":[],
                        }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": " Joining Period is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JoiningPeriodJobDscriptionGetPlatformAPI(APIView):
    '''
        Joining Period Job Description Get API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        JoiningPeriodJobDescriptionDetails = JoiningPeriodJobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Joining Period Job Description Details",
                "Data": JoiningPeriodJobDescriptionDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JoiningPeriodJobDescriptionGetbyDescpPlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_description_id": "BroaderAI_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JoiningPeriodJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                JoiningPeriodJobDescriptionDetail = JoiningPeriodJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Joining Period Job Description Detail",
                        "Data": JoiningPeriodJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Joining Period Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
 

class JoiningPeriodJobDescriptionGetOnePlatformAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "joining_period_job_description_id": "BroaderAI_joining_period_job_description_8x4vfh6s12n2hez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if JoiningPeriodJobDescriptionModel.objects.filter(joining_period_job_description_id = getData["joining_period_job_description_id"]).exists():
                JoiningPeriodJobDescriptionDetail = JoiningPeriodJobDescriptionModel.objects.filter(joining_period_job_description_id = getData["joining_period_job_description_id"]).values()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Joining Period Job Description Detail",
                        "Data": JoiningPeriodJobDescriptionDetail
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Joining Period Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
    
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]

class JoiningPeriodJobDescriptionDeletePlatformAPI(APIView):
    '''
        Nationalitys Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "joining_period_job_description_id": "BroaderAI_soft_skill_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
                  
            if JoiningPeriodJobDescriptionModel.objects.filter(joining_period_job_description_id = getData["joining_period_job_description_id"]).exists():
                JoiningPeriodJobDescriptionDetail = JoiningPeriodJobDescriptionModel.objects.get(joining_period_job_description_id = getData["joining_period_job_description_id"])
                JoiningPeriodJobDescriptionDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Joining Period Job Description is successfully Deleted",
                        "Data": {   "user_id" : getData['user_id']
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Joining Period Job Description data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    # authentication_classes=[APIKeyAuthentication]
    # permission_classes=[IsAuthenticated]
          