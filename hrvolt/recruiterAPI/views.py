from django.shortcuts import render
from .models import *
from django.core.exceptions import SuspiciousFileOperation
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
from candidateresumeAPI.models import *
from candidatePreferenceAPI.models import *
import json
from hrvolt.emailsend import mailSend
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
import operator
from userloginAPI.views import APIKeyAuthentication
import zipfile
import json 

from .preference import aiComperision
from .extractResumeText import getResumeText

# import spacy

# nlp = spacy.load("en_core_web_sm")



###################################################################################################################################################

# Create your views here.
class JobDescriptionAPI(APIView):

    '''
        job Description API(INSERT)
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
                    if user.user_is_loggedin:
                        
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
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
   
    
               
class JobDescriptionUpdateAPI(APIView):

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
                        if user.user_is_loggedin:
                    
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
                                "Message": "You are not logged in",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                            
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Level data is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
         
class JobDescriptionDeleteAPI(APIView):
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
            if user.user_is_loggedin:
                
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
          
class JobDescriptionGetAPI(APIView):
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
                "Data": JobDescriptionDetails,
            }
        return Response(res, status=status.HTTP_201_CREATED)      

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]  
    
class JobDescriptionGetOneAPI(APIView):
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
            
            if user.user_is_loggedin:
                
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class JobDescriptionGetUserAPI(APIView):
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
            
            if user.user_is_loggedin:
                
                if JobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_action = getData["job_description_action"]).exists():

                    JobDescriptionDetail = JobDescriptionModel.objects.filter(user_id = getData["user_id"],job_description_action = getData["job_description_action"]).values().order_by('-job_description_registration_date')


                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Description Detail",
                            "Data": {
                                "JobDescriptionDetail":JobDescriptionDetail,
                                "Total_job_posts": len(JobDescriptionDetail)
                            },

                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Description data is not found",
                            "Data": {
                                "Total_job_posts": 0},
                            }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class JobDescriptionGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)        

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
     
###################################################################################################################################################
# Education

class EducationJobDescriptionAPI(APIView):
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
            
            if user.user_is_loggedin:
                
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class EducationJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class EducationJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
         
class EducationJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class EducationJobDescriptionDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]        

###################################################################################################################################################

# Education Field

class EducationFieldJobDescriptionAPI(APIView):
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
            
            if user.user_is_loggedin:
                
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class EducationFieldJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class EducationFieldJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class EducationFieldJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class EducationFieldJobDescriptionDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
###################################################################################################################################################
# Soft skills

class SoftSkillsJobDescriptionAPI(APIView):
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
            
            if user.user_is_loggedin:
                
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class SoftSkillsJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class SoftSkillsJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
              
class SoftSkillsJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class SoftSkillsJobDescriptionDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
           
###################################################################################################################################################

class TechnicalSkillsJobDescriptionAPI(APIView):
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
            
            if user.user_is_loggedin:
                
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class TechnicalSkillsJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class TechnicalSkillsJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class TechnicalSkillsJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class TechnicalSkillsJobDescriptionDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class CustomJobDescriptionResponsibilityAPI(APIView):
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
            
            if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Level is not exits",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class CustomJobDescriptionResponsibilityGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionResponsibilityGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionResponsibilityGetfromUserJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionResponsibilityGetfromJobPositionJobLevelAPI(APIView):
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
                
                    if user.user_is_loggedin:
                        
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionResponsibilityGetfromJobPositionAPI(APIView):
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
                
                    if user.user_is_loggedin:
                        
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionResponsibilityDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]        

###################################################################################################################################################
        
class CustomJobDescriptionRequirementAPI(APIView):
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
            
            if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Level is not exits",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionRequirementGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionRequirementGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionRequirementGetfromUserJobDescriptionAPI(APIView):
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
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionRequirementGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionRequirementGetfromJobPositionAPI(APIView):
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
            
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionRequirementDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class CustomJobDescriptionBenefitAPI(APIView):
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
            
            if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Level is not exits",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class CustomJobDescriptionBenefitGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionBenefitGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionBenefitGetfromUserJobDescriptionAPI(APIView):
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
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionBenefitGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionBenefitGetfromJobPositionAPI(APIView):
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
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CustomJobDescriptionBenefitDeleteAPI(APIView):
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

            if user.user_is_loggedin:
             
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class JobDescriptionResponsibilityAPI(APIView):
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
            
            if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetfromUserJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetfromJobPositionJobLevelAPI(APIView):
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
                
                    if user.user_is_loggedin:
                        
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityGetfromJobPositionAPI(APIView):
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
                
                    if user.user_is_loggedin:
                        
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionResponsibilityDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################
class BothJobDescriptionResponsibilityGetfromUserJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                    
                    if CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).exists():
                        customJobDescriptionResponsibilityDetail = CustomJobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).values()
                    
                        if JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).exists():
                            JobDescriptionResponsibilityDetail = JobDescriptionResponsibilityModel.objects.filter(user_id = getData["user_id"],job_description_id=getData['job_description_id']).values()
                            res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Both Job Description Responsibility Detail",
                                    "Data": {
                                        "JobDescriptionResponsibilityDetail":JobDescriptionResponsibilityDetail,
                                        "CustomJobDescriptionResponsibilityDetails":customJobDescriptionResponsibilityDetail},
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Description Responsibility data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Custom Job Description Responsibility data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class BothJobDescriptionResponsibilityGetfromJobPositionJobLevelAPI(APIView):
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
                
                    if user.user_is_loggedin:
                        
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
                                            "CustomJobDescriptionResponsibilityDetails":customJobDescriptionResponsibilityDetail},
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)

                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": " Custom Job Description Responsibility data is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                            
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Description Responsibility data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class BothJobDescriptionResponsibilityGetfromJobPositionAPI(APIView):
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
                
                    if user.user_is_loggedin:
                        
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
                                            "CustomJobDescriptionResponsibilityDetails":customJobDescriptionResponsibilityDetail},
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Custom Job Description Responsibility data is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Description Responsibility data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class JobDescriptionRequirementAPI(APIView):
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
            
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionRequirementGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]       

class JobDescriptionRequirementGetfromUserJobDescriptionAPI(APIView):
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
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]        

class JobDescriptionRequirementGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionRequirementGetfromJobPositionAPI(APIView):
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
            
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionRequirementDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################
       
class BothJobDescriptionRequirementGetfromUserJobDescriptionAPI(APIView):
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
                if user.user_is_loggedin:
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
                                        "customJobDescriptionRequirementDetail":customJobDescriptionRequirementDetail}
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Description Requirement data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " custom Job Description Requirement data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class BothJobDescriptionRequirementGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
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
                                            "customJobDescriptionRequirementDetail": customJobDescriptionRequirementDetail}
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": " Job Description Requirement data is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Custom Job Description Requirement data is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class BothJobDescriptionRequirementGetfromJobPositionAPI(APIView):
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
            
                if user.user_is_loggedin:
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
                                        "customJobDescriptionRequirementDetail":customJobDescriptionRequirementDetail}
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " Job Description Requirement data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": " custom Job Description Requirement data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]           

###################################################################################################################################################

class JobDescriptionBenefitAPI(APIView):
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
            
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
       
class JobDescriptionBenefitGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetfromUserJobDescriptionAPI(APIView):
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
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
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
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionBenefitGetfromJobPositionAPI(APIView):
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
                if user.user_is_loggedin:
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionBenefitDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class BothJobDescriptionBenefitGetfromUserJobDescriptionAPI(APIView):
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

                if user.user_is_loggedin:
   
                    if JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():
                       
                        if CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).exists():

                            customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                            JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(user_id = getData["user_id"],job_description_id = getData["job_description_id"]).values()
                            res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Both Job Description Benefit Detail",
                                    "Data": {
                                        "JobDescriptionBenefitDetail":JobDescriptionBenefitDetail,
                                        "customJobDescriptionBenefitDetail":customJobDescriptionBenefitDetail}
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Custom Job Description Benefit data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": " Job Description Benefit data is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job description is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class BothJobDescriptionBenefitGetfromJobPositionJobLevelAPI(APIView):
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
                    if user.user_is_loggedin:
                        if CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                            customJobDescriptionBenefittDetail = CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                            if JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).exists():
                                JobDescriptionBenefittDetail = JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"],job_level_id=getData["job_level_id"]).values()
                                res = {
                                        "Status": "success",
                                        "Code": 201,
                                        "Message": "Both Job Description Benefit Detail",
                                        "Data": {
                                            "customJobDescriptionBenefittDetail":customJobDescriptionBenefittDetail,
                                            "JobDescriptionBenefittDetail":JobDescriptionBenefittDetail}
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Job Description Benefitt data is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Custom Job Description Benefitt data is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User is not loggedin",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class BothJobDescriptionBenefitGetfromJobPositionAPI(APIView):
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
                if user.user_is_loggedin:
                    if CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                        customJobDescriptionBenefitDetail = CustomJobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                        if JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                            JobDescriptionBenefitDetail = JobDescriptionBenefitsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Both Job Description Benefit Detail",
                                "Data": {
                                    "customJobDescriptionBenefitDetail":customJobDescriptionBenefitDetail,
                                    "JobDescriptionBenefitDetail":JobDescriptionBenefitDetail}
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Custom Job Description Benefit data is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job position is not exits",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class CompanyDetailRegisterAPI(APIView):
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
                    #           "Code": 201,
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "sector is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    
class CompanyDetailsUpdateAPI(APIView):
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

                        if user.user_is_loggedin: 
                            
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

                            if getData['location_id'] != "":
                                LastUpdateData.location_id= getData['location_id']
                                
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
                                "Code": 401,
                                "Message": "You are not logged in",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "company Details is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "company Type is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Sector Details is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]



class CompanyDetailsGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        

class CompanyDetailsGetOneByUserAPI(APIView):
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
            if user.user_is_loggedin:
                UserCompanyData = UserCompanyModel.objects.get(user_id=getData['user_id'])
                CompanyData = CompanyModel.objects.get(company_info_id=UserCompanyData.company_info_id)

                if CompanyData.location_id == None:

                    loc_id =  ""
                    loc_name = ""

                else:

                    loc_id =  CompanyData.location_id
                    loc_name = CompanyData.location.location_name



                output = {
                            "company_info_id": CompanyData.company_info_id,
                            "company_name": CompanyData.company_name,
                            "company_description": CompanyData.company_description,
                            "company_established_year": CompanyData.company_established_year,
                            "contact_number": CompanyData.contact_number,
                            "company_email": CompanyData.company_email,
                            "company_googlelink": CompanyData.company_googlelink,
                            "company_linkdinlink": CompanyData.company_linkdinlink,
                            "company_team_member": CompanyData.company_team_member,
                            "company_twitter_link": CompanyData.company_twitter_link,
                            "company_facebook_link": CompanyData.company_facebook_link,
                            "sector_id": CompanyData.sector_id,
                            "sector_name": CompanyData.sector.sector_name,
                            "location_id": loc_id,
                            "location_name": loc_name,
                            "company_type_id": CompanyData.company_type_id,
                            "company_type_name": CompanyData.company_type.company_type_name,
                            "company_action": CompanyData.company_action,
                            "company_registration_date": CompanyData.company_registration_date,
                        }

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Company Type Detail",
                        "Data": output
                    }
                return Response(res, status=status.HTTP_201_CREATED)
               
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class CompanyDetailsDeleteAPI(APIView):
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

                if user.user_is_loggedin:

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
                        "Message": "You are not logged in",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "company details is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]    
###################################################################################################################################################
                  

class CompanyLocationDetailRegisterAPI(APIView):

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
                                
                                if user.user_is_loggedin: 
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
                                        "Message": "You are not logged in",
                                        "Data":[],}
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Location is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        user = NewUser.objects.get(id=getData["user_id"])
                        if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                            
                            if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                                
                                if user.user_is_loggedin: 
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
                                        "Message": "You are not logged in",
                                        "Data":[],}
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Location is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    user = NewUser.objects.get(id=getData["user_id"])
                    if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                        
                        if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                            
                            if user.user_is_loggedin: 
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
                                    "Message": "You are not logged in",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Location is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Company is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company location is already register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CompanyLocationDetailsUpdateAPI(APIView):
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
                                    
                                    if user.user_is_loggedin: 
                                        
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
                                            "Message": "You are not logged in",
                                            "Data":[],}
                                        return Response(res, status=status.HTTP_201_CREATED)
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 401,
                                        "Message": "Location is not found",
                                        "Data":[],}
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Company is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            user = NewUser.objects.get(id=getData["user_id"])
                            if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                                
                                if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                                    
                                    if user.user_is_loggedin: 
                                        
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
                                            "Message": "You are not logged in",
                                            "Data":[],}
                                        return Response(res, status=status.HTTP_201_CREATED)
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 401,
                                        "Message": "Location is not found",
                                        "Data":[],}
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Company is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        user = NewUser.objects.get(id=getData["user_id"])
                        if CompanyModel.objects.filter(company_info_id=getData["company_info_id"]).exists():
                            
                            if LocationModel.objects.filter(location_id=getData["location_id"]).exists():
                                
                                if user.user_is_loggedin: 
                                    
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
                                        "Message": "You are not logged in",
                                        "Data":[],}
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Location is not found",
                                    "Data":[],}
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company location details is already register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Company location data is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CompanyLocationDetailsCompanyGetAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CompanyLocationDetailsGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CompanyLocationDetailsDeleteAPI(APIView):
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

                if user.user_is_loggedin:

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
                        "Message": "You are not logged in",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "company location details is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class JobDescriptionCompanyLocationDetailRegisterAPI(APIView):
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
                        
                        if user.user_is_loggedin: 
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
                                "Message": "You are not logged in",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Company location is not found",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Work place is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Descrition is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]        

class JobDescriptionCompanyLocationDetailsUpdateAPI(APIView):
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
                        if user.user_is_loggedin: 
                            
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
                                "Message": "You are not logged in",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "company Location is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Work Place is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description Details is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]



class JobDescriptionCompanyLocationDetailsGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionCompanyLocationDetailsDeleteAPI(APIView):
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

                if user.user_is_loggedin:

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
                        "Message": "You are not logged in",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "company location details is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]   

###################################################################################################################################################


class JobDescriptionEmploymentTypeDetailRegisterAPI(APIView):
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
                        
                    if user.user_is_loggedin: 
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
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Employment type is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Descrition is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionEmploymentTypeDetailsUpdateAPI(APIView):
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
                        if user.user_is_loggedin: 
                            
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
                                "Message": "You are not logged in",
                                "Data":[],}
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description Employment Type is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Employment Type is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description Details is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionEmploymentTypeGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)


    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class JobDescriptionEmploymentTypeDetailsGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JobDescriptionEmploymentTypeDetailsDeleteAPI(APIView):
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

                if user.user_is_loggedin:

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
                        "Message": "You are not logged in",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Job Description Employment Type is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################

class UserCompanyRegisterAPI(APIView):
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
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


        
class UserCompanyUpdateAPI(APIView):
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
                    if user.user_is_loggedin: 
                        
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
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
            
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User Company is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]                 

class UserCompanyGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class UserCompanyGetOneUserAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class UserCompanyDeleteAPI(APIView):
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

                if user.user_is_loggedin:

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
                        "Message": "You are not logged in",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User Company is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]   
    
###############################################################################################################################################

class AllJobDescriptionGetAPI(APIView):
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin:
                
                JobDescriptionDetail0 = JobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                JobDescriptionDetail1 = EducationJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                educationField = EducationFieldJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                JobDescriptionDetail2 = SoftSkillJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                JobDescriptionDetail3 = TechnicalSkillJobDescriptionModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                JobDescriptionDetail4 = CustomJobDescriptionResponsibilityModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                JobDescriptionDetail5 = CustomJobDescriptionRequirementsModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                JobDescriptionDetail6 = CustomJobDescriptionBenefitsModel.objects.filter( job_description_id = getData["job_description_id"]).values()

                JobDescriptionDetail7 = JobDescriptionResponsibilityModel.objects.filter( job_description_id = getData["job_description_id"]).values()

                job_responsibility_dict = []

                job_description_details = JobDescriptionResponsibilityModel.objects.filter(job_description__job_description_id=getData["job_description_id"])

                for detail in job_description_details:
                    job_responsibility_dict.append({
                        "job_responsibility_id": detail.job_responsibility.job_responsibility_id,
                        "job_responsibility_description": detail.job_responsibility.job_responsibility_description
                    })

                JobDescriptionDetail9 = JobDescriptionBenefitsModel.objects.filter( job_description_id = getData["job_description_id"]).values()


                job_benefit_dict = []

                job_description_benefit_details = JobDescriptionBenefitsModel.objects.filter(job_description__job_description_id=getData["job_description_id"])

                for detail in job_description_benefit_details:
                    job_benefit_dict.append({
                        "job_benefit_id": detail.job_benefit.job_benefit_id,
                        "job_benefit_description": detail.job_benefit.job_benefit_description
                    })


                JobDescriptionDetail11 = JobDescriptionEmploymentTypeModel.objects.filter( job_description_id = getData["job_description_id"]).values()

                job_empType_dict = []

                job_description_emp_type_details = JobDescriptionEmploymentTypeModel.objects.filter(job_description__job_description_id=getData["job_description_id"])

                for detail in job_description_emp_type_details:
                    job_empType_dict.append({
                        "employment_type_id": detail.employment_type.employment_type_id,
                        "employment_type_name": detail.employment_type.employment_type_name
                    })



                JobDescriptionDetail8 = JobDescriptionRequirementModel.objects.filter( job_description_id = getData["job_description_id"]).values()

                
                JobDescriptionDetail10 = JobDescriptionCompanyLocationModel.objects.filter( job_description_id = getData["job_description_id"]).values()
                
                


                NationalityDetail = NationalityJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                GenderDetail = GenderJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                WorkPlaceDetail = WorkPlaceJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                LanguageDetail = LanguageJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                JoiningPeriodDetail = JoiningPeriodJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Description Detail",
                        "Data":{
                            "jobDescription": JobDescriptionDetail0,#JobDescriptionModel
                            "jobEducation": JobDescriptionDetail1,#EducationJobDescriptionModel
                            "jobEducationField": educationField,
                            "jobSoftSkills": JobDescriptionDetail2,#SoftSkillJobDescriptionModel
                            "jobTechnicalSkills": JobDescriptionDetail3,#TechnicalSkillJobDescriptionModel
                            "jobCustomResponsibilities": JobDescriptionDetail4,#CustomJobDescriptionResponsibilityModel
                            "jobCustomReq": JobDescriptionDetail5,#CustomJobDescriptionRequirementsModel
                            "jobCustomBenefits": JobDescriptionDetail6,#CustomJobDescriptionBenefitsModel
                            "jobResponsibilities": job_responsibility_dict,#JobDescriptionResponsibilityModel
                            "jobRequirements": JobDescriptionDetail8,#JobDescriptionRequirementModel
                            "jobBenefits": job_benefit_dict,#JobDescriptionBenefitsModel
                            "jobLocations": JobDescriptionDetail10,#JobDescriptionCompanyLocationModel
                            "jobEmploymentType": job_empType_dict,#JobDescriptionEmploymentTypeModel
                            "Nationality":NationalityDetail,#NationalityJobDescriptionModel
                            "Gender":GenderDetail,#GenderJobDescriptionModel
                            "WorkPlace":WorkPlaceDetail,#WorkPlaceJobDescriptionModel
                            "language":LanguageDetail,#LanguageJobDescriptionModel
                            "JoiningPeriod":JoiningPeriodDetail,#JoiningPeriodJobDescriptionModel
                            },
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                # else:
                #     res = {
                # "Status": "error",
                # "Code": 401,
                # "Message": "Job Description data is not found",
                # "Data":[],}
                #     return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
        
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

        
###################################################################################################################################################
# Nationality Job Description

class NationalityJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class NationalityJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class NationalityJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class NationalityJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class NationalityJobDescriptionDeleteAPI(APIView):
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
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
###################################################################################################################################################
# gender Job Description

class GenderJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                        
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
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class GenderJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class GenderJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class GenderJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class GenderJobDescriptionDeleteAPI(APIView):
    '''
        Gender Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "gender_job_description_id": "BroaderAI_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################


class WorkPlaceJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class WorkPlaceJobDescriptionGetAPI(APIView):
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
                "Message": "work place Job Description Details",
                "Data": WorkPlaceJobDescriptionDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class WorkPlaceJobDescriptionDeleteAPI(APIView):
    '''
        Work Place Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "work_place_job_description_id": "BroaderAI_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]        

###################################################################################################################################################


class LanguageJobDescriptionAPI(APIView):
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
                
                if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class LanguageJobDescriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]   

class LanguageJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class LanguageJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class LanguageJobDescriptionDeleteAPI(APIView):
    '''
        Language Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "language_job_description_id": "BroaderAI_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

###################################################################################################################################################


class JoiningPeriodJobDescriptionAPI(APIView):
    '''
        joining period Job Description API(Insert)
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
                
                if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not loggedin",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "This record is all ready is register",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class JoiningPeriodJobDscriptionGetAPI(APIView):
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JoiningPeriodJobDescriptionGetbyDescpAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class JoiningPeriodJobDescriptionGetOneAPI(APIView):
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
            if user.user_is_loggedin:
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
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class JoiningPeriodJobDescriptionDeleteAPI(APIView):
    '''
        Nationalitys Job Description API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "joining_period_job_description_id": "BroaderAI_job_description_7cm5bv4gmkoz2nl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin:
                    
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
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exists",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        

class autoJobDescriptionAPI(APIView):
    '''
        Job Description API(post)
        Request : post
        Data =  {
                    "user_id": "BroaderAI_firsetest3_0yyhogjnlh",
                    "job_level_id": "BroaderAI_job_description_7cm5bv4gmkoz2nl",
                    "job_position_id":
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():

                    if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():

                        emplType = list(EmploymentTypeModel.objects.all().values())
                        print(emplType,'0000')
                        jobPeriod = list(JoiningPeriodModel.objects.all().values())
                        workPlace = list(WorkPlaceModel.objects.all().values())
                        education = list(EducationModel.objects.all().values())
                        educationField = list(EducationFieldModel.objects.all().values())
                        softSkill = list(SoftSkillsModel.objects.all().values())
                        benefits = list(JobBenefitModel.objects.all().values())
                        # responsibility = list(JobResponsibilityModel.objects.all().values())
                        nationality = list(NationalityModel.objects.all().values())

                        gender = ['male','female']
                        language = list(LanguageModel.objects.all().values())
                        
                        random_gender = random.randint(1, len(gender))
                        selected_genders = random.sample(gender, random_gender)

                        number_of_vacancy = random.randint(1,5)

                        salary_max = random.randint(10000,60000)
                        salary_min = random.randint(5000, salary_max - 1)

                        random_emp_type = random.randint(1,3)
                        selected_emp_types = random.sample(emplType, random_emp_type)

                        random_work_place = random.randint(1,3)
                        selected_work_places = random.sample(workPlace, random_work_place)

                        random_language = random.randint(1, len(language))
                        selected_languages = random.sample(language, random_language)

                        random_joinPeriod = random.randint(1, 3)
                        selected_joinPeriods = random.sample(jobPeriod, random_joinPeriod)

                        random_education = random.randint(1, 4)
                        selected_educations = random.sample(education, random_education)

                        random_eduField = random.randint(1, 4)
                        selected_eduFields = random.sample(educationField, random_eduField)

                        random_nation = random.randint(1,3)
                        selected_nations = random.sample(nationality, random_nation)

                        random_softskill = random.randint(1,5)
                        selected_softskills = random.sample(softSkill,random_softskill)
                        random_benefits = random.randint(1,5)
                        selected_benefits = random.sample(benefits,random_benefits)
                        
                        htotech =[]

                        tech = []

                        haveToTechSkill = HaveToTechnicalSkillsModel.objects.filter(job_level_id=getData["job_level_id"], job_position_id = getData["job_position_id"]).values()

                        for i in haveToTechSkill:
                            # tech[i["have_to_technical_skills_id"]] = i["have_to_technical_skills_name"]

                            tech.append({
                                "technical_skill_id":  i["main_unique_technical_skills_id"],
                                "technical_skill_name": i["have_to_technical_skills_name"]
                            })

                            # htotech.append(i["have_to_technical_skills_name"])

                            htotech.append({
                                "have_to_technical_skills_name": i["have_to_technical_skills_name"],
                                "main_unique_technical_skills_id": i["main_unique_technical_skills_id"],
                                "technical_skills_id":i["technical_skills_id"]
                            })
            
                        random_htotech = random.randint(1,5)
                        selected_htotechs = random.sample(htotech,random_htotech)
                        optTech = []
                        
                        optTechSkill = OptionalTechnicalSkillsModel.objects.filter(job_level_id=getData["job_level_id"], job_position_id = getData["job_position_id"]).values()

                        for i in optTechSkill:

                            tech.append({
                                "technical_skill_id":  i["main_unique_technical_skills_id"],
                                "technical_skill_name": i["optional_technical_skills_name"]
                            })

                            # tech[i["optional_technical_skills_id"]] = i["optional_technical_skills_name"]
                            # optTech.append(i["optional_technical_skills_name"])

                            optTech.append({
                                "optional_technical_skills_name": i["optional_technical_skills_name"],
                                "main_unique_technical_skills_id": i["main_unique_technical_skills_id"],
                                "technical_skills_id":i["technical_skills_id"]
                            })

                        random_optTech = random.randint(1,5)
                        selected_optTechs = random.sample(optTech,random_optTech)

                        resplist = []
                        responsibility = JobResponsibilityModel.objects.filter(job_position_id = getData["job_position_id"]).values()
                        for resp in responsibility:
                            resplist.append({
                                "job_responsibility_id": resp["job_responsibility_id"],
                                "job_responsibility_description":resp['job_responsibility_description']
                            })

                        random_responsibility = random.randint(1,10)
                        selected_responsibility = random.sample(resplist,random_responsibility)

                        userCompany = CompanyModel.objects.all().values()
                        for comp in userCompany:
                            comp = comp

                        random_tech = random.randint(1,8)
                        selected_Techs = random.sample(tech, random_tech)

                        unique_ids = set()

                        # Filter out duplicates and keep only unique entries
                        unique_tech = [entry for entry in selected_Techs if (entry['technical_skill_id'] not in unique_ids) or unique_ids.add(entry['technical_skill_id'])]


                        # techmain = TechnicalSkillsMainModel.objects.filter(job_level_id=getData["job_level_id"], job_position_id = getData["job_position_id"]).values()
                            

                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job Description Details",
                                "Data":{
                                     "job_level_name":JobLevelModel.objects.get(job_level_id = getData["job_level_id"]).job_level_name,
                                    "job_position_name": JobPositionModel.objects.get(job_position_id = getData["job_position_id"]).job_position_name,
                                    "job_level_id": getData["job_level_id"],
                                    "job_position_id": getData["job_position_id"],
                                    "number_of_vacancy":number_of_vacancy,
                                    "Technical_skills": unique_tech,
                                    "company_name": comp,
                                    "Nationality":selected_nations,
                                    "gender":selected_genders,
                                    "min_salary": round(salary_min, -3),
                                    "max_salary":round(salary_max, -3),
                                    "Education":selected_educations,
                                    "Education_Field":selected_eduFields,
                                    "Soft_Skills":selected_softskills,
                                    "employment_type":selected_emp_types,
                                    "Joining_Period":selected_joinPeriods,
                                    "Languages":selected_languages,
                                    "Work_Place":selected_work_places,
                                    "have_to_tech_skill":selected_htotechs,
                                    "optional_tech_skill":selected_optTechs,
                                    "Benefits":selected_benefits,
                                    "responsibility":selected_responsibility
                                }
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Position data is not found",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Level data is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
        

class autoCompareCandidateJobDescripAPI(APIView):
    '''
        Job Description API(post)
        Request : post
        Data =  {
                    "user_id": "BroaderAI_grishapatel95_gdxr0jx8iv",
                    "job_description_id": "BroaderAI_job_description_3ghrhh6rd7gbjym",
                    "recruiter_user_id": "BroaderAI_patelyash2504_rc0z5kgyrf"
                }
    '''
    def post(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["recruiter_user_id"]).exists():
            user = NewUser.objects.get(id=getData["recruiter_user_id"])

            if user.user_is_loggedin:

                #EDUCATION
                if CandidateBasicEducationDetails.objects.filter(user_id = getData["user_id"]).exists():
                    basicEdu = CandidateBasicEducationDetails.objects.get(user_id = getData["user_id"])
                    EduCandidateList = [basicEdu.candidate_last_education_id]

                    jDEdu = EducationJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    EdujobDesList =  [type['education_id'] for type in jDEdu]
                    if EduCandidateList in EdujobDesList:
                        edu_score = 1
                    else:
                        EdujobDesList = []
                        edu_score = 0
                else:
                    EdujobDesList = []
                    edu_score = 0


                #Employment Type
                if CandidateEmploymentTypePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    emp = CandidateEmploymentTypePreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                    EmpTypeList = [type['employment_type_id'] for type in emp]

                    JdEmp = JobDescriptionEmploymentTypeModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    EmpTypejobDesDataList = [type['employment_type_id'] for type in JdEmp]
                    for et in EmpTypeList:
                        if et in EmpTypejobDesDataList:
                            emp_score = 1
                        else:
                            EmpTypejobDesDataList = []
                            emp_score = 0
                else:
                    EmpTypejobDesDataList = []
                    emp_score = 0

                #work place
                if CandidateWorkplacePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():       
                    wp = CandidateWorkplacePreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                    workPlaceList = [type['work_place_id'] for type in wp]
                    

                    Jdwp = WorkPlaceJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    workPlacejobDesDataList = [type['work_place_id'] for type in Jdwp]
                   
                    for et in workPlaceList:
                        if et in workPlacejobDesDataList:
                            wp_score = 1
                        else:
                            workPlacejobDesDataList = []
                            wp_score = 0
                else:
                    workPlacejobDesDataList = []
                    wp_score = 0

                #joining time
                if CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    join = CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                    joinTimeCandList = [type['joining_period_id'] for type in join]
                   

                    jDjoin = JoiningPeriodJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    joinTimejobDesDataList = [jt['joining_period_id'] for jt in jDjoin]
                

                    if any(jt in joinTimejobDesDataList for jt in joinTimeCandList):
                        JT_score = 1
                    else:
                        joinTimejobDesDataList = []
                        JT_score = 0
                else:
                    joinTimejobDesDataList = []
                    JT_score = 0

                #Language
                if CandidateLanguageModel.objects.filter(user_id = getData["user_id"]).exists():
                    lang = CandidateLanguageModel.objects.filter(user_id = getData["user_id"]).values()
                    langCandList = [type['candidate_language_id'] for type in lang]
                  

                    jDlang = LanguageJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    
                    langjobDesDataList = [lang['language_id'] for lang in jDlang]

                    

                    if any(lang in langjobDesDataList for lang in langCandList):
                        common_lang_elements = set(langCandList) & set(langjobDesDataList)
                        lang_score = (len(common_lang_elements) / len(langjobDesDataList)) * 100
                    else:
                        langjobDesDataList = []
                        lang_score = 0
                else:
                    langjobDesDataList = []
                    lang_score = 0

                #Edu field
                if CandidateBasicEducationDetails.objects.filter(user_id = getData["user_id"]).exists():
                    basicEduField = CandidateBasicEducationDetails.objects.get(user_id = getData["user_id"])
                    EduFieldCandidateList = [basicEduField.candidate_last_education_field_id]

                    jDEduField = EducationFieldJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    EduFieldjobDesList =  [type['education_field_id'] for type in jDEduField]
                    if EduFieldCandidateList in EduFieldjobDesList:
                        eduField_score = 1
                    else:
                        EduFieldjobDesList = []
                        eduField_score = 0
                else:
                    EduFieldjobDesList = []
                    eduField_score = 0

                #Gender
                if NewUser.objects.filter(id = getData["user_id"]).exists():  
                    gender = NewUser.objects.get(id = getData["user_id"])
                    genderCandidateList = gender.user_gender

                    jDgender = GenderJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    genderjobDesList = [type['gender'] for type in jDgender]

                    if genderCandidateList in genderjobDesList:
                        gender_score = 1
                    else:
                        genderjobDesList = []
                        gender_score = 0
                else:
                    genderjobDesList = []
                    gender_score = 0

                recruiterDetails = []

                #Soft Skill
                if CandidateSoftskillsModel.objects.filter(user_id = getData["user_id"]).exists():
                    softskill = CandidateSoftskillsModel.objects.filter(user_id = getData["user_id"]).values()
                    softSkillCandidateList = [softtype['candidate_soft_skill_id'] for softtype in softskill]

                    jDsoftSkill = SoftSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                    softSkilljobDesList = [softtype['soft_skills_id'] for softtype in jDsoftSkill]
                    softSkillNamejobDesList = [softtype['soft_skills_name'] for softtype in jDsoftSkill]
                    recruiterDetails.append({"Soft_skills":softSkillNamejobDesList})

                    if any(ss in softSkilljobDesList for ss in softSkillCandidateList):
                        common_soft_elements = set(softSkillCandidateList) & set(softSkilljobDesList)
                        softSkill_score = (len(common_soft_elements) / len(softSkilljobDesList)) * 100
                        # softSkill_score = 1
                    else:
                        softSkilljobDesList = []
                        softSkill_score = 0
                else:
                    softSkilljobDesList = []
                    softSkill_score = 0

                #Technical Skill
                if CandidateTechnicalskillsModel.objects.filter(user_id = getData["user_id"]).exists():
                    techskill = CandidateTechnicalskillsModel.objects.filter(user_id = getData["user_id"]).values()

                    techSkillCandidateList = [techtype['candidate_technical_skill_id'] for techtype in techskill]

                    jDtechSkill = TechnicalSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()

                    techSkilljobDesList = [techtype['technical_skills_id'] for techtype in jDtechSkill]

                    techSkillNamejobDesList = [techtype['technical_skills_name'] for techtype in jDtechSkill]
                   
                    recruiterDetails.append({"Technical_skills":techSkillNamejobDesList})

                    
                    if any(th in techSkilljobDesList for th in techSkillCandidateList):
                        # techSkill_score = 1
                        common_tech_elements = set(techSkillCandidateList) & set(techSkilljobDesList)
                        techSkill_score = (len(common_tech_elements) / len(techSkilljobDesList)) * 100
                    else:
                        techSkilljobDesList = []
                        techSkill_score = 0
                else:
                    techSkilljobDesList = []
                    techSkill_score = 0

                #job level
                    
                jobLevel = CandidatePreferenceModel.objects.get(user_id = getData["user_id"])
                jobLevelCand = [jobLevel.job_level_id]

                jDjobLevel = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                jobleveljobDesList = [type['job_level_id'] for type in jDjobLevel]
                joblevelNamejobDesList = [type['job_level_name'] for type in jDjobLevel]

                recruiterDetails.append(joblevelNamejobDesList)

                if jobLevelCand in jobleveljobDesList:
                    joblevel_score = 1
                else:
                    joblevel_score = 0

                #job Pos
                
                jobPosition = CandidatePreferenceModel.objects.get(user_id = getData["user_id"])
                jobPositionCand = [jobPosition.job_position_id]

                jDjobPosition = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                jobPositionjobDesList = [type['job_position_id'] for type in jDjobPosition]
                jobPositionNamejobDesList = [type['job_position_name'] for type in jDjobPosition]
                recruiterDetails.append(jobPositionNamejobDesList)

                if jobPositionCand in jobPositionjobDesList:
                    jobPosition_score = 1
                else:
                    jobPosition_score = 0

                #Nationality Comparison
                    
                nation = NewUser.objects.get(id = getData["user_id"])
                nationCandidateList = nation.user_country

                jDnation = NationalityJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                nationjobDesList = [type['nationality_id'] for type in jDnation]

                if nationCandidateList in nationjobDesList:
                    nation_score = 1
                else:
                    nation_score = 0

                #job description
            
                #responsibility
                jDRespons = JobDescriptionResponsibilityModel.objects.filter(job_description_id = getData["job_description_id"]).values()
              
                for res in jDRespons:
                    ResjobDesList = res['job_responsibility_id']
                    responsibity = JobResponsibilityModel.objects.get(job_responsibility_id = res['job_responsibility_id']).job_responsibility_description
                
                    recruiterDetails.append(responsibity)

                #job title
                jDjobtitle = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                jobtitleNamejobDesList = [type['job_tilte'] for type in jDjobtitle]
                recruiterDetails.append(jobtitleNamejobDesList)

                jobDescription_string = json.dumps(recruiterDetails, indent=4)
                cleaned_jobDescription_string = jobDescription_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")

                #Candidate Resume

                candidateDetails = []

                basicInfo = NewUser.objects.get(id = getData['user_id'])
                summary = basicInfo.user_summary
                candidateDetails.append(summary)

                mainEdu = CandidateMainEducationDetails.objects.filter(user_id = getData["user_id"]).values()
                for edu in mainEdu:
                    eduDetail = edu['candidate_degree_name'] + ' in ' + edu['candidate_univeresity_name']
                    eduSummary =edu['candidate_summary']
                    candidateDetails.append(eduDetail)
                    candidateDetails.append(eduSummary)

                #main experience
                    
                mainExp = CandidateMainExperienceModel.objects.filter(user_id = getData["user_id"]).values()
                mainExpTechSkill = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                exps_list =[]
                exp_tech_skill =[]
                exp_tech_skill_id = []

                for exp in mainExp:
                    job_position = JobPositionModel.objects.get(job_position_id = exp['candidate_job_position_id']).job_position_name
                    job_level = JobLevelModel.objects.get(job_level_id = exp['candidate_job_level_id']).job_level_name
                    ExpDescrip = job_level + ' - ' + job_position + ' - ' + exp['candidate_job_description']
                    # candidateDetails.append(ExpDescrip)
                    for tech_skill in mainExpTechSkill:
                        if tech_skill['candidate_main_experience_id'] == exp['candidate_resume_main_experience_id']:
                            tech_skill_name = tech_skill['candidate_technical_skill_name']
                            tech_skill_id = tech_skill['candidate_technical_skill_id']
                            exp_tech_skill.append(tech_skill_name)
                            exp_tech_skill_id.append(tech_skill_id)
                        
                    exp_details = {
                                'exp_description': ExpDescrip,
                                'exp_technical_skills': exp_tech_skill,
                            }
                    exps_list.append(exp_details)
                    
                candidateDetails.append(exps_list)
                

                #candidate Preference
                    
                candJL = CandidatePreferenceModel.objects.get(user_id = getData["user_id"])
                job_level = candJL.job_level.job_level_name
                job_position = candJL.job_position.job_position_name
                candidateDetails.append(job_level)
                candidateDetails.append(job_position)


                ## Technical skill

                tech = []
                candTechSkill = CandidateTechnicalskillsModel.objects.filter(user_id = getData["user_id"]).values()
                for tch in candTechSkill:
                    tech.append(tch['candidate_technical_skill_name'])
            
                candidateDetails.append({"Technical_skill":tech})

                ## Soft skill

                soft = []
                candsoftSkill = CandidateSoftskillsModel.objects.filter(user_id = getData["user_id"]).values()
                for ss in candsoftSkill:
                    soft.append(ss['candidate_soft_skill_name'])
                candidateDetails.append({"Soft_Skill":soft})

                ## Project
                    
                technical_skills_list =[]
                tech_skill_list_id = []
                project_details = {}
                projects_list=[]
                proj = CandidateProjectModel.objects.filter(user_id = getData["user_id"]).values()
                projTech = CandidateProjectTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for pj in proj:
                    projDetail = pj['candidate_project_name'] + ' - ' + pj['candidate_project_description']
                    for tech_skill in projTech:
                        if tech_skill['candidate_project_id'] == pj['candidate_resume_project_id']:
                            tech_skill_name = tech_skill['candidate_technical_skill_name']
                            tech_skill_id = tech_skill['candidate_technical_skill_id']
                            technical_skills_list.append(tech_skill_name)
                            tech_skill_list_id.append(tech_skill_id)
                        
                    project_details = {
                                'description': projDetail,
                                'technical_skills': technical_skills_list,
                            }
                    projects_list.append(project_details)
                candidateDetails.append(projects_list)
                

                common_proj_technical_skills = list(set(techSkilljobDesList) & set(tech_skill_list_id))
              
                total_proj_tech_skill = len(common_proj_technical_skills)
                
                rec_tech_skill = len(techSkilljobDesList)
                
                if rec_tech_skill > 0:
                    proj_score = round((total_proj_tech_skill * 100) / rec_tech_skill,2)
                    
                else:
                    proj_score = 0
                    
                
                ##hackathon
                
                hktech = []
                hktech_id = []
                hackathon_list =[]
                hackathon = CandidatehackathonModel.objects.filter(user_id = getData["user_id"]).values()
                hackTech = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for ht in hackathon:
                    hackathon_name = ht['candidate_hackathon_name'] + ' - ' + ht['candidate_hackathon_description']
                    for hk in hackTech:
                        if hk['candidate_hackathon_id'] == ht['candidate_resume_hackathon_id']:
                            tech_skill_name = hk['candidate_technical_skill_name']
                            tech_skill_id = hk['candidate_technical_skill_id']
                            hktech.append(tech_skill_name)
                            hktech_id.append(tech_skill_id)
                           
                    hackathon_details = {
                                'hackathon_name': hackathon_name,
                                'technical_skills': hktech
                            }
                    hackathon_list.append(hackathon_details)
                candidateDetails.append(hackathon_list)
                    
                common_hack_technical_skills = list(set(techSkilljobDesList) & set(hktech_id))
                total_hack_tech_skill = len(common_hack_technical_skills)
                rec_tech_skill = len(techSkilljobDesList)
                if rec_tech_skill > 0:
                    hack_score = round((total_hack_tech_skill * 100) / rec_tech_skill,2)
                else:
                    hack_score = 0

                ###contribution

                contech = []
                contech_id = []
                contribution_list =[]
                contribution = CandidateContributionModel.objects.filter(user_id = getData["user_id"]).values()
                contriTech = CandidateContributionTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for contri in contribution:
                    contribution_name = contri['candidate_contribution_topic']
                    for contrib in contriTech: 
                        if contrib['candidate_contribution_id'] == contri['candidate_resume_contribution_id']:
                            tech_skill_name = contrib['candidate_technical_skill_name']
                            contech.append(tech_skill_name)
                            contech_id.append(contrib['candidate_technical_skill_id'])
                          
                    contribution_details = {
                                'contribution_name': contribution_name,
                                'technical_skills': contech
                            }
                    contribution_list.append(contribution_details)
                candidateDetails.append(contribution_list)
                common_contri_technical_skills = list(set(techSkilljobDesList) & set(contech_id))
                rec_tech_skill = len(techSkilljobDesList)
                total_contri_tech_skill = len(common_contri_technical_skills)
                if rec_tech_skill > 0:
                    contri_score = round((total_contri_tech_skill * 100) / rec_tech_skill,2)
                else:
                    contri_score = 0

                ##workshop

                wrkshoptech = []
                wrkshoptech_id = []
                wrkshop_list =[]
                workshop = CandidateWorkshopModel.objects.filter(user_id = getData["user_id"]).values()
                workshopTech = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for ws in workshop:
                    workshop_name = ws['candidate_workshop_name'] + ' - ' + ws['candidate_workshop_topic'] + ' - '+ ws['candidate_workshop_description']
                    for wsTech in workshopTech: 
                        if wsTech['candidate_workshop_id'] == ws['candidate_resume_workshop_id']:
                            tech_skill_name = wsTech['candidate_technical_skill_name']
                            wrkshoptech.append(tech_skill_name)
                            wrkshoptech_id.append(wsTech['candidate_technical_skill_id'])
                           
                    workshop_details = {
                                'workshop_name': workshop_name,
                                'technical_skills': wrkshoptech
                            }
                    wrkshop_list.append(workshop_details)
                candidateDetails.append(wrkshop_list)
                common_workshop_technical_skills = list(set(techSkilljobDesList) & set(wrkshoptech_id))
                total_workshop_tech_skill = len(common_workshop_technical_skills)
                rec_tech_skill = len(techSkilljobDesList)

                if rec_tech_skill > 0:
                    workshop_score = round((total_workshop_tech_skill * 100) / rec_tech_skill,2)
                else:
                    workshop_score = 0

                seminar = CandidateSeminarModel.objects.filter(user_id = getData["user_id"]).values()
                for sem in seminar:
                    seminarDetail = sem['candidate_seminar_name'] + ' - ' + sem['candidate_seminar_description']
                    candidateDetails.append(seminarDetail)
                    

                ##competition
                    
                comptech = []
                comptech_id = []
                comp_list =[]
                competition = CandidateCompetitionModel.objects.filter(user_id = getData["user_id"]).values()
                competitionTech = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for comp in competition:
                    competition_name = comp['candidate_competition_name'] + ' - ' + comp['candidate_competition_description']
                    for cpTech in competitionTech: 
                        if cpTech['candidate_competition_id'] == comp['candidate_resume_competition_id']:
                            tech_skill_name = cpTech['candidate_technical_skill_name']
                            comptech.append(tech_skill_name)
                            comptech_id.append(cpTech['candidate_technical_skill_id'])
                            
                    competition_details = {
                                'competition_name': competition_name,
                                'technical_skills': comptech
                            }
                    comp_list.append(competition_details)
                candidateDetails.append(comp_list)
                common_competition_technical_skills = list(set(techSkilljobDesList) & set(comptech_id))
                total_competition_tech_skill = len(common_competition_technical_skills)
                rec_tech_skill = len(techSkilljobDesList)
                if rec_tech_skill > 0:
                    competition_score = round((total_competition_tech_skill * 100) / rec_tech_skill,2)
                else:
                    competition_score = 0

                ##certificate
                    
                certtech = []
                certtech_id = []
                certi_list =[]
                certificate = CandidateCertificateModel.objects.filter(user_id = getData["user_id"]).values()
                certificateTech = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for comp in certificate:
                    certificate_name = comp['candidate_certificate_name'] + ' - ' + comp['candidate_certificate_description']
                    for cfTech in certificateTech: 
                        if cfTech['candidate_certificate_id'] == comp['candidate_resume_certificate_id']:
                            tech_skill_name = cfTech['candidate_technical_skill_name']
                            certtech.append(tech_skill_name)
                            certtech_id.append(cfTech['candidate_technical_skill_id'])
                            
                    certificate_details = {
                                'certificate_name': certificate_name,
                                'technical_skills': certtech
                            }
                    certi_list.append(certificate_details)
                candidateDetails.append(certi_list)
                common_certificate_technical_skills = list(set(techSkilljobDesList) & set(certtech_id))
                total_certificate_tech_skill = len(common_certificate_technical_skills)
                rec_tech_skill = len(techSkilljobDesList)
                if rec_tech_skill > 0:
                    certificate_score = round((total_certificate_tech_skill * 100) / rec_tech_skill,2)
                else:
                    certificate_score = 0
                
                candidate_details_string = json.dumps(candidateDetails, indent=4)
                cleaned_candidate_details_string = candidate_details_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")

                aiCompPercentageScore = float(aiComperision(cleaned_jobDescription_string,cleaned_candidate_details_string))

                main_count = 0
                if edu_score == 1:
                    main_count +=1
                if eduField_score == 1:
                    main_count +=1
                if emp_score == 1:
                    main_count +=1
                if wp_score == 1:
                    main_count +=1
                if JT_score == 1:
                    main_count +=1
                if softSkill_score == 1:
                    main_count +=1
                if techSkill_score == 1:
                    main_count +=1
                if joblevel_score == 1:
                    main_count +=1
                if jobPosition_score == 1:
                    main_count +=1
                if nation_score == 1:
                    main_count +=1

                manual_per = (main_count * 100) / 10
                total_per = (manual_per * 40) / 100
                final_per = ((aiCompPercentageScore * 60) / 100) + total_per


                match_dict = {}
                not_match_dict = {}

                output = {
                        "Education":edu_score,
                        "Education Field":eduField_score,
                        "Employment Type":emp_score,
                        "Work Place":wp_score,
                        "Joining Period":JT_score,
                        "Language":lang_score,
                        "Gender":gender_score,
                        "Soft Skills":softSkill_score,
                        "Technical Skills":techSkill_score,
                        "Job Level":joblevel_score,
                        "Job Position":jobPosition_score,
                        "Nationality":nation_score,
                        "Project":proj_score,
                        "Hackathon":hack_score,
                        "Contribution":contri_score,
                        "Workshop":workshop_score,
                        "Competition":competition_score,
                        "Certificate":certificate_score,  
                    }

                for key, value in output.items():
                    if key in [
                        "Education", "Education Field", "Employment Type", "Work Place",
                        "Joining Period", "Language", "Gender", "Soft Skills", "Technical Skills",
                        "Nationality", "Project",
                        "Hackathon", "Contribution", "Workshop",
                        "Competition", "Certificate"
                    ]:
                        if value == 0:
                            not_match_dict[key] = output[key]
                        else:
                            if value == 1:
                                match_dict[key] = round(output[key] * 100, 2)
                            else:
                                match_dict[key] = output[key]



                user = NewUser.objects.get(id = getData["user_id"])
                jobDesc = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])

                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Joining Period Job Description Details",
                    "Data":{
                            "user_id":getData["user_id"],
                            "user_name": user.first_name + " " + user.last_name, 
                            "job_description_id": getData["job_description_id"],
                            "job_pos": jobDesc.job_level_name + " " + jobDesc.job_position_name,
                            "recruiter_user_id":getData["recruiter_user_id"],
                            "not_match_dict": not_match_dict,
                            "match_dict":match_dict,
                            "candidateDetails":cleaned_candidate_details_string,
                            "recruiterDetails":cleaned_jobDescription_string,
                            "AI_Comparision_Percentage":aiCompPercentageScore,
                            "Preference_Percentage":manual_per,
                            "Final_Percentage": round(float(final_per), 2)
                    }
                }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)



class autoCompareCandidateJobDescripListAPI(APIView):

    '''
        Job Description API(post)
        Request : post
        Data =  {
                    "job_description_id": "BroaderAI_job_description_3ghrhh6rd7gbjym",
                    "recruiter_user_id": "BroaderAI_patelyash2504_rc0z5kgyrf"
                }
    '''

    def post(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["recruiter_user_id"]).exists():

            user = NewUser.objects.get(id=getData["recruiter_user_id"])

            if user.user_is_loggedin:

                if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

                    jobDescriptionData = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])

                    if CandidatePreferenceModel.objects.filter(job_position_id = jobDescriptionData.job_position_id, job_level_id = jobDescriptionData.job_level_id).exists():

                        candidates = CandidatePreferenceModel.objects.filter(job_position_id = jobDescriptionData.job_position_id, job_level_id = jobDescriptionData.job_level_id).values()


                        userDetails = []

                        if len(candidates) > 0:

                            for candidate in candidates:

                                #EDUCATION
                                if CandidateBasicEducationDetails.objects.filter(user_id = candidate["user_id"]).exists():
                                    basicEdu = CandidateBasicEducationDetails.objects.get(user_id = candidate["user_id"])
                                    EduCandidateList = [basicEdu.candidate_last_education_id]

                                    jDEdu = EducationJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    EdujobDesList =  [type['education_id'] for type in jDEdu]
                                    if EduCandidateList in EdujobDesList:
                                        edu_score = 1
                                    else:
                                        edu_score = 0
                                else:
                                    edu_score = 0


                                #Employment Type
                                if CandidateEmploymentTypePreferenceModel.objects.filter(user_id = candidate["user_id"]).exists():
                                    emp = CandidateEmploymentTypePreferenceModel.objects.filter(user_id = candidate["user_id"]).values()
                                    EmpTypeList = [type['employment_type_id'] for type in emp]

                                    JdEmp = JobDescriptionEmploymentTypeModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    EmpTypejobDesDataList = [type['employment_type_id'] for type in JdEmp]
                                    for et in EmpTypeList:
                                        if et in EmpTypejobDesDataList:
                                            emp_score = 1
                                        else:
                                            emp_score = 0
                                else:
                                    emp_score = 0

                                #work place
                                if CandidateWorkplacePreferenceModel.objects.filter(user_id = candidate["user_id"]).exists():       
                                    wp = CandidateWorkplacePreferenceModel.objects.filter(user_id = candidate["user_id"]).values()
                                    workPlaceList = [type['work_place_id'] for type in wp]
                                    

                                    Jdwp = WorkPlaceJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    workPlacejobDesDataList = [type['work_place_id'] for type in Jdwp]
                                
                                    for et in workPlaceList:
                                        if et in workPlacejobDesDataList:
                                            wp_score = 1
                                        else:
                                            wp_score = 0
                                else:
                                    wp_score = 0

                                #joining time
                                if CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = candidate["user_id"]).exists():
                                    join = CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = candidate["user_id"]).values()
                                    joinTimeCandList = [type['joining_period_id'] for type in join]
                                

                                    jDjoin = JoiningPeriodJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    joinTimejobDesDataList = [jt['joining_period_id'] for jt in jDjoin]
                                

                                    if any(jt in joinTimejobDesDataList for jt in joinTimeCandList):
                                        JT_score = 1
                                    else:
                                        JT_score = 0
                                else:
                                    JT_score = 0

                                #Language
                                if CandidateLanguageModel.objects.filter(user_id = candidate["user_id"]).exists():
                                    lang = CandidateLanguageModel.objects.filter(user_id = candidate["user_id"]).values()
                                    langCandList = [type['candidate_language_id'] for type in lang]
                                

                                    jDlang = LanguageJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    langjobDesDataList = [lang['language_id'] for lang in jDlang]
                                

                                    if any(lang in langjobDesDataList for lang in langCandList):
                                        lang_score = 1
                                    else:
                                        lang_score = 0
                                else:
                                    lang_score = 0

                                #Edu field
                                if CandidateBasicEducationDetails.objects.filter(user_id = candidate["user_id"]).exists():
                                    basicEduField = CandidateBasicEducationDetails.objects.get(user_id = candidate["user_id"])
                                    EduFieldCandidateList = [basicEduField.candidate_last_education_field_id]

                                    jDEduField = EducationFieldJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    EduFieldjobDesList =  [type['education_field_id'] for type in jDEduField]
                                    if EduFieldCandidateList in EduFieldjobDesList:
                                        eduField_score = 1
                                    else:
                                        eduField_score = 0
                                else:
                                    eduField_score = 0

                                #Gender
                                if NewUser.objects.filter(id = candidate["user_id"]).exists():  
                                    gender = NewUser.objects.get(id = candidate["user_id"])
                                    genderCandidateList = gender.user_gender

                                    jDgender = GenderJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    genderjobDesList = [type['gender'] for type in jDgender]

                                    if genderCandidateList in genderjobDesList:
                                        gender_score = 1
                                    else:
                                        gender_score = 0
                                else:
                                    gender_score = 0

                                recruiterDetails = []

                                #Soft Skill
                                if CandidateSoftskillsModel.objects.filter(user_id = candidate["user_id"]).exists():
                                    softskill = CandidateSoftskillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                    softSkillCandidateList = [type['candidate_soft_skill_id'] for type in softskill]

                                    jDsoftSkill = SoftSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                    softSkilljobDesList = [type['soft_skills_id'] for type in jDsoftSkill]
                                    softSkillNamejobDesList = [type['soft_skills_name'] for type in jDsoftSkill]
                                    recruiterDetails.append({"Soft_skills":softSkillNamejobDesList})

                                    if any(ss in softSkilljobDesList for ss in softSkillCandidateList):
                                        softSkill_score = 1
                                    else:
                                        softSkill_score = 0
                                else:
                                    softSkill_score = 0

                                techSkilljobDesList = []

                                #Technical Skill
                                if CandidateTechnicalskillsModel.objects.filter(user_id = candidate["user_id"]).exists():
                                    techskill = CandidateTechnicalskillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                    techSkillCandidateList = [type['candidate_technical_skill_id'] for type in techskill]

                                    jDtechSkill = TechnicalSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()

                                    techSkilljobDesList = [type['technical_skills_id'] for type in jDtechSkill]

                                    techSkillNamejobDesList = [type['technical_skills_name'] for type in jDtechSkill]
                                
                                    recruiterDetails.append({"Technical_skills":techSkillNamejobDesList})
                                    
                                    if any(th in techSkilljobDesList for th in techSkillCandidateList):
                                        techSkill_score = 1
                                    else:
                                        techSkill_score = 0
                                else:
                                    techSkill_score = 0

                                #job level
                                    
                                jobLevel = CandidatePreferenceModel.objects.get(user_id = candidate["user_id"])
                                jobLevelCand = [jobLevel.job_level_id]

                                jDjobLevel = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                jobleveljobDesList = [type['job_level_id'] for type in jDjobLevel]
                                joblevelNamejobDesList = [type['job_level_name'] for type in jDjobLevel]

                                recruiterDetails.append(joblevelNamejobDesList)

                                if jobLevelCand in jobleveljobDesList:
                                    joblevel_score = 1
                                else:
                                    joblevel_score = 0

                                #job Pos
                                
                                jobPosition = CandidatePreferenceModel.objects.get(user_id = candidate["user_id"])
                                jobPositionCand = [jobPosition.job_position_id]

                                jDjobPosition = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                jobPositionjobDesList = [type['job_position_id'] for type in jDjobPosition]
                                jobPositionNamejobDesList = [type['job_position_name'] for type in jDjobPosition]
                                recruiterDetails.append(jobPositionNamejobDesList)

                                if jobPositionCand in jobPositionjobDesList:
                                    jobPosition_score = 1
                                else:
                                    jobPosition_score = 0

                                #Nationality Comparison
                                    
                                nation = NewUser.objects.get(id = candidate["user_id"])
                                nationCandidateList = nation.user_country

                                jDnation = NationalityJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                nationjobDesList = [type['nationality_id'] for type in jDnation]

                                if nationCandidateList in nationjobDesList:
                                    nation_score = 1
                                else:
                                    nation_score = 0

                                #job description
                            
                                #responsibility
                                jDRespons = JobDescriptionResponsibilityModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                            
                                for res in jDRespons:
                                    ResjobDesList = res['job_responsibility_id']
                                    responsibity = JobResponsibilityModel.objects.get(job_responsibility_id = res['job_responsibility_id']).job_responsibility_description
                                
                                    recruiterDetails.append(responsibity)

                                #job title
                                jDjobtitle = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                                jobtitleNamejobDesList = [type['job_tilte'] for type in jDjobtitle]
                                recruiterDetails.append(jobtitleNamejobDesList)

                                jobDescription_string = json.dumps(recruiterDetails, indent=4)
                                cleaned_jobDescription_string = jobDescription_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")

                                #Candidate Resume

                                candidateDetails = []

                                basicInfo = NewUser.objects.get(id = candidate['user_id'])
                                summary = basicInfo.user_summary
                                candidateDetails.append(summary)

                                mainEdu = CandidateMainEducationDetails.objects.filter(user_id = candidate["user_id"]).values()
                                for edu in mainEdu:
                                    eduDetail = edu['candidate_degree_name'] + ' in ' + edu['candidate_univeresity_name']
                                    eduSummary =edu['candidate_summary']
                                    candidateDetails.append(eduDetail)
                                    candidateDetails.append(eduSummary)

                                #main experience
                                    
                                mainExp = CandidateMainExperienceModel.objects.filter(user_id = candidate["user_id"]).values()
                                mainExpTechSkill = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                exps_list =[]
                                exp_tech_skill =[]
                                exp_tech_skill_id = []

                                for exp in mainExp:
                                    job_position = JobPositionModel.objects.get(job_position_id = exp['candidate_job_position_id']).job_position_name
                                    job_level = JobLevelModel.objects.get(job_level_id = exp['candidate_job_level_id']).job_level_name
                                    ExpDescrip = job_level + ' - ' + job_position + ' - ' + exp['candidate_job_description']
                                    # candidateDetails.append(ExpDescrip)
                                    for tech_skill in mainExpTechSkill:
                                        if tech_skill['candidate_main_experience_id'] == exp['candidate_resume_main_experience_id']:
                                            tech_skill_name = tech_skill['candidate_technical_skill_name']
                                            tech_skill_id = tech_skill['candidate_technical_skill_id']
                                            exp_tech_skill.append(tech_skill_name)
                                            exp_tech_skill_id.append(tech_skill_id)
                                        
                                    exp_details = {
                                                'exp_description': ExpDescrip,
                                                'exp_technical_skills': exp_tech_skill,
                                            }
                                    exps_list.append(exp_details)
                                    
                                candidateDetails.append(exps_list)
                                

                                #candidate Preference
                                    
                                candJL = CandidatePreferenceModel.objects.get(user_id = candidate["user_id"])
                                job_level = candJL.job_level.job_level_name
                                job_position = candJL.job_position.job_position_name
                                candidateDetails.append(job_level)
                                candidateDetails.append(job_position)


                                ## Technical skill

                                tech = []
                                candTechSkill = CandidateTechnicalskillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for tch in candTechSkill:
                                    tech.append(tch['candidate_technical_skill_name'])
                            
                                candidateDetails.append({"Technical_skill":tech})

                                ## Soft skill

                                soft = []
                                candsoftSkill = CandidateSoftskillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for ss in candsoftSkill:
                                    soft.append(ss['candidate_soft_skill_name'])
                                candidateDetails.append({"Soft_Skill":soft})

                                ## Project
                                    
                                technical_skills_list =[]
                                tech_skill_list_id = []
                                project_details = {}
                                projects_list=[]
                                proj = CandidateProjectModel.objects.filter(user_id = candidate["user_id"]).values()
                                projTech = CandidateProjectTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for pj in proj:
                                    projDetail = pj['candidate_project_name'] + ' - ' + pj['candidate_project_description']
                                    for tech_skill in projTech:
                                        if tech_skill['candidate_project_id'] == pj['candidate_resume_project_id']:
                                            tech_skill_name = tech_skill['candidate_technical_skill_name']
                                            tech_skill_id = tech_skill['candidate_technical_skill_id']
                                            technical_skills_list.append(tech_skill_name)
                                            tech_skill_list_id.append(tech_skill_id)
                                        
                                    project_details = {
                                                'description': projDetail,
                                                'technical_skills': technical_skills_list,
                                            }
                                    projects_list.append(project_details)
                                candidateDetails.append(projects_list)

                                
                                if techSkilljobDesList:
                                    common_proj_technical_skills = list(set(techSkilljobDesList) & set(tech_skill_list_id))
                                
                                    total_proj_tech_skill = len(common_proj_technical_skills)
                                    
                                    rec_tech_skill = len(techSkilljobDesList)
                                else:

                                    common_proj_technical_skills = []
                                
                                    total_proj_tech_skill = len(common_proj_technical_skills)
                                    
                                    rec_tech_skill = 0

                                
                                if rec_tech_skill > 0:
                                    proj_score = round((total_proj_tech_skill * 100) / rec_tech_skill,2)
                                    
                                else:
                                    proj_score = 0
                                    
                                
                                ##hackathon
                                
                                hktech = []
                                hktech_id = []
                                hackathon_list =[]
                                hackathon = CandidatehackathonModel.objects.filter(user_id = candidate["user_id"]).values()
                                hackTech = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for ht in hackathon:
                                    hackathon_name = ht['candidate_hackathon_name'] + ' - ' + ht['candidate_hackathon_description']
                                    for hk in hackTech:
                                        if hk['candidate_hackathon_id'] == ht['candidate_resume_hackathon_id']:
                                            tech_skill_name = hk['candidate_technical_skill_name']
                                            tech_skill_id = hk['candidate_technical_skill_id']
                                            hktech.append(tech_skill_name)
                                            hktech_id.append(tech_skill_id)
                                        
                                    hackathon_details = {
                                                'hackathon_name': hackathon_name,
                                                'technical_skills': hktech
                                            }
                                    hackathon_list.append(hackathon_details)
                                candidateDetails.append(hackathon_list)
                                    
                                common_hack_technical_skills = list(set(techSkilljobDesList) & set(hktech_id))
                                total_hack_tech_skill = len(common_hack_technical_skills)
                                rec_tech_skill = len(techSkilljobDesList)
                                if rec_tech_skill > 0:
                                    hack_score = round((total_hack_tech_skill * 100) / rec_tech_skill,2)
                                else:
                                    hack_score = 0

                                ###contribution

                                contech = []
                                contech_id = []
                                contribution_list =[]
                                contribution = CandidateContributionModel.objects.filter(user_id = candidate["user_id"]).values()
                                contriTech = CandidateContributionTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()


                                for contri in contribution:
                                    contribution_name = contri['candidate_contribution_topic']
                                    for contrib in contriTech: 

                                        if contrib['candidate_contribution_id'] == contri['candidate_resume_contribution_id']:
                                            tech_skill_name = contrib['candidate_technical_skill_name']
                                            contech.append(tech_skill_name)
                                            contech_id.append(contrib['candidate_technical_skill_id'])
                                        
                                    contribution_details = {
                                                'contribution_name': contribution_name,
                                                'technical_skills': contech
                                            }
                                    contribution_list.append(contribution_details)

                                candidateDetails.append(contribution_list)
                                common_contri_technical_skills = list(set(techSkilljobDesList) & set(contech_id))
                                rec_tech_skill = len(techSkilljobDesList)
                                total_contri_tech_skill = len(common_contri_technical_skills)
                                if rec_tech_skill > 0:
                                    contri_score = round((total_contri_tech_skill * 100) / rec_tech_skill,2)
                                else:
                                    contri_score = 0

                                ##workshop

                                wrkshoptech = []
                                wrkshoptech_id = []
                                wrkshop_list =[]
                                workshop = CandidateWorkshopModel.objects.filter(user_id = candidate["user_id"]).values()
                                workshopTech = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for ws in workshop:
                                    workshop_name = ws['candidate_workshop_name'] + ' - ' + ws['candidate_workshop_topic'] + ' - '+ ws['candidate_workshop_description']
                                    for wsTech in workshopTech: 
                                        if wsTech['candidate_workshop_id'] == ws['candidate_resume_workshop_id']:
                                            tech_skill_name = wsTech['candidate_technical_skill_name']
                                            wrkshoptech.append(tech_skill_name)
                                            wrkshoptech_id.append(wsTech['candidate_technical_skill_id'])
                                        
                                    workshop_details = {
                                                'workshop_name': workshop_name,
                                                'technical_skills': wrkshoptech
                                            }
                                    wrkshop_list.append(workshop_details)
                                candidateDetails.append(wrkshop_list)
                                common_workshop_technical_skills = list(set(techSkilljobDesList) & set(wrkshoptech_id))
                                total_workshop_tech_skill = len(common_workshop_technical_skills)
                                rec_tech_skill = len(techSkilljobDesList)

                                if rec_tech_skill > 0:
                                    workshop_score = round((total_workshop_tech_skill * 100) / rec_tech_skill,2)
                                else:
                                    workshop_score = 0

                                seminar = CandidateSeminarModel.objects.filter(user_id = candidate["user_id"]).values()
                                for sem in seminar:
                                    seminarDetail = sem['candidate_seminar_name'] + ' - ' + sem['candidate_seminar_description']
                                    candidateDetails.append(seminarDetail)
                                    

                                ##competition
                                    
                                comptech = []
                                comptech_id = []
                                comp_list =[]
                                competition = CandidateCompetitionModel.objects.filter(user_id = candidate["user_id"]).values()
                                competitionTech = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for comp in competition:
                                    competition_name = comp['candidate_competition_name'] + ' - ' + comp['candidate_competition_description']
                                    for cpTech in competitionTech: 
                                        if cpTech['candidate_competition_id'] == comp['candidate_resume_competition_id']:
                                            tech_skill_name = cpTech['candidate_technical_skill_name']
                                            comptech.append(tech_skill_name)
                                            comptech_id.append(cpTech['candidate_technical_skill_id'])
                                            
                                    competition_details = {
                                                'competition_name': competition_name,
                                                'technical_skills': comptech
                                            }
                                    comp_list.append(competition_details)
                                candidateDetails.append(comp_list)
                                common_competition_technical_skills = list(set(techSkilljobDesList) & set(comptech_id))
                                total_competition_tech_skill = len(common_competition_technical_skills)
                                rec_tech_skill = len(techSkilljobDesList)
                                if rec_tech_skill > 0:
                                    competition_score = round((total_competition_tech_skill * 100) / rec_tech_skill,2)
                                else:
                                    competition_score = 0

                                ##certificate
                                    
                                certtech = []
                                certtech_id = []
                                certi_list =[]
                                certificate = CandidateCertificateModel.objects.filter(user_id = candidate["user_id"]).values()
                                certificateTech = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id = candidate["user_id"]).values()
                                for comp in certificate:
                                    certificate_name = comp['candidate_certificate_name'] + ' - ' + comp['candidate_certificate_description']
                                    for cfTech in certificateTech: 
                                        if cfTech['candidate_certificate_id'] == comp['candidate_resume_certificate_id']:
                                            tech_skill_name = cfTech['candidate_technical_skill_name']
                                            certtech.append(tech_skill_name)
                                            certtech_id.append(cfTech['candidate_technical_skill_id'])
                                            
                                    certificate_details = {
                                                'certificate_name': certificate_name,
                                                'technical_skills': certtech
                                            }
                                    certi_list.append(certificate_details)
                                candidateDetails.append(certi_list)
                                common_certificate_technical_skills = list(set(techSkilljobDesList) & set(certtech_id))
                                total_certificate_tech_skill = len(common_certificate_technical_skills)
                                rec_tech_skill = len(techSkilljobDesList)
                                if rec_tech_skill > 0:
                                    certificate_score = round((total_certificate_tech_skill * 100) / rec_tech_skill,2)
                                else:
                                    certificate_score = 0
                                
                                candidate_details_string = json.dumps(candidateDetails, indent=4)
                                cleaned_candidate_details_string = candidate_details_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")

                                aiCompPercentageScore = float(aiComperision(cleaned_jobDescription_string,cleaned_candidate_details_string))

                                # aiCompPercentageScore = 0

                                main_count = 0
                                if edu_score == 1:
                                    main_count +=1
                                if eduField_score == 1:
                                    main_count +=1
                                if emp_score == 1:
                                    main_count +=1
                                if wp_score == 1:
                                    main_count +=1
                                if JT_score == 1:
                                    main_count +=1
                                if softSkill_score == 1:
                                    main_count +=1
                                if techSkill_score == 1:
                                    main_count +=1
                                if joblevel_score == 1:
                                    main_count +=1
                                if jobPosition_score == 1:
                                    main_count +=1
                                if nation_score == 1:
                                    main_count +=1

                                manual_per = (main_count * 100) / 10
                                total_per = (manual_per * 40) / 100
                                final_per = ((aiCompPercentageScore * 60) / 100) + total_per
                                

                                userBasicInfo = NewUser.objects.get(id=candidate["user_id"])

                                userTechSkills = CandidateTechnicalskillsModel.objects.filter(user_id=candidate["user_id"]).values()

                                techskill = ' ,'.join([ useTech["candidate_technical_skill_name"].upper() for useTech in userTechSkills])[:-1]

                                if CandidateUserResumeUpload.objects.filter(user_id=candidate["user_id"]).exists():

                                    userResume = CandidateUserResumeUpload.objects.get(user_id=candidate["user_id"])
                                    userResume = str(userResume.candidate_resumeUpload)
                                
                                else:

                                    userResume = ""




                                # userResume = CandidateUserResumeUpload.objects.get(user_id=candidate["user_id"])

                                # print("resume: ", userResume.candidate_resumeUpload)

                                # resumepath = os.path.join(settings.BASE_PATH, str(userResume.candidate_resumeUpload))
                                # print(resumepath) 


                                res = {
                                    "user_id": candidate["user_id"],
                                    "user_name": userBasicInfo.first_name + " " + userBasicInfo.last_name,
                                    "user_position": JobPositionModel.objects.get(job_position_id = jobDescriptionData.job_position_id).job_position_name,
                                    "user_level": JobLevelModel.objects.get(job_level_id = jobDescriptionData.job_level_id).job_level_name,
                                    "user_tech": techskill,
                                    "job_description_id": getData["job_description_id"],
                                    "recruiter_user_id":getData["recruiter_user_id"],
                                    
                                    "AI_Comparision_Percentage":aiCompPercentageScore,
                                    "Preference_Percentage":manual_per,
                                    "Final_Percentage": round(float(final_per), 2),
                                    "user_resume": settings.BASE_URL + userResume
                                    
                                }
                        

                                userDetails.append(res)

                            
                            sorted_userDetails = sorted(userDetails, key=lambda x: x['Final_Percentage'], reverse=True)

                            output = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Candidate list",
                                    "Data": sorted_userDetails
                                }

                            return Response(output, status=status.HTTP_201_CREATED)

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "No Candidates",
                            "Data": userDetails
                        }

                        return Response(res, status=status.HTTP_201_CREATED)

                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "No Candidates",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
        
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Post is not found",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)



class autoCompareCandidateJobDescripAIAPI(APIView):
    '''
        Job Description comparision ai API(post)
        Request : post
        Data =  {
                    "user_id": "BroaderAI_grishapatel95_gdxr0jx8iv",
                    "job_description_id": "BroaderAI_job_description_3ghrhh6rd7gbjym",
                    "recruiter_user_id": "BroaderAI_patelyash2504_rc0z5kgyrf"
                }
    '''
    def post(self, request, format=None):
        
        getData = request.data

        if NewUser.objects.filter(id = getData["recruiter_user_id"]).exists():
            user = NewUser.objects.get(id=getData["recruiter_user_id"])
            if user.user_is_loggedin:

                # Recruiter Job Description Details
                recruiterDetails = []

                #Soft Skill
                jDsoftSkill = SoftSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                softSkillNamejobDesList = [type['soft_skills_name'] for type in jDsoftSkill]
                recruiterDetails.append({"Soft_skills":softSkillNamejobDesList})


                #Technical Skill
                jDtechSkill = TechnicalSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                techSkilljobDesList = [type['technical_skills_id'] for type in jDtechSkill]
                techSkillNamejobDesList = [type['technical_skills_name'] for type in jDtechSkill]
              
                recruiterDetails.append({"Technical_skills":techSkillNamejobDesList})
                    

                #job level
                jDjobLevel = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                joblevelNamejobDesList = [type['job_level_name'] for type in jDjobLevel]

                recruiterDetails.append(joblevelNamejobDesList)

                #job Pos
                jDjobPosition = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                jobPositionNamejobDesList = [type['job_position_name'] for type in jDjobPosition]
                recruiterDetails.append(jobPositionNamejobDesList)

                #responsibility
                jDRespons = JobDescriptionResponsibilityModel.objects.filter(job_description_id = getData["job_description_id"]).values()
               
                for res in jDRespons:
                    responsibity = JobResponsibilityModel.objects.get(job_responsibility_id = res['job_responsibility_id']).job_responsibility_description
                    recruiterDetails.append(responsibity)

                #job title
                jDjobtitle = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                jobtitleNamejobDesList = [type['job_tilte'] for type in jDjobtitle]
                recruiterDetails.append(jobtitleNamejobDesList)

                jobDescription_string = json.dumps(recruiterDetails, indent=4)
                cleaned_jobDescription_string = jobDescription_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")


                #Candidate Resume

                candidateDetails = []

                basicInfo = NewUser.objects.get(id = getData['user_id'])
                summary = basicInfo.user_summary
                candidateDetails.append(summary)

                #main education
                mainEdu = CandidateMainEducationDetails.objects.filter(user_id = getData["user_id"]).values()
                for edu in mainEdu:
                    eduDetail = edu['candidate_degree_name'] + ' in ' + edu['candidate_univeresity_name']
                    eduSummary =edu['candidate_summary']
                    candidateDetails.append(eduDetail)
                    candidateDetails.append(eduSummary)

                #main experience
                    
                mainExp = CandidateMainExperienceModel.objects.filter(user_id = getData["user_id"]).values()
                mainExpTechSkill = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                exps_list =[]
                exp_tech_skill =[]
                exp_tech_skill_id = []
                for exp in mainExp:
                    job_position = JobPositionModel.objects.get(job_position_id = exp['candidate_job_position_id']).job_position_name
                    job_level = JobLevelModel.objects.get(job_level_id = exp['candidate_job_level_id']).job_level_name
                    ExpDescrip = job_level + ' - ' + job_position + ' - ' + exp['candidate_job_description']
                    # candidateDetails.append(ExpDescrip)
                    for tech_skill in mainExpTechSkill:
                        if tech_skill['candidate_main_experience_id'] == exp['candidate_resume_main_experience_id']:
                            tech_skill_name = tech_skill['candidate_technical_skill_name']
                            tech_skill_id = tech_skill['candidate_technical_skill_id']
                            exp_tech_skill.append(tech_skill_name)
                            exp_tech_skill_id.append(tech_skill_id)
                        
                    exp_details = {
                                'exp_description': ExpDescrip,
                                'exp_technical_skills': exp_tech_skill,
                            }
                    exps_list.append(exp_details)
                 
                candidateDetails.append(exps_list)
                

                #candidate Preference
                    
                candJL = CandidatePreferenceModel.objects.get(user_id = getData["user_id"])
                job_level = candJL.job_level.job_level_name
                job_position = candJL.job_position.job_position_name
                candidateDetails.append(job_level)
                candidateDetails.append(job_position)


                ## Technical skill

                tech = []
                candTechSkill = CandidateTechnicalskillsModel.objects.filter(user_id = getData["user_id"]).values()
                for tch in candTechSkill:
                    tech.append(tch['candidate_technical_skill_name'])
            
                candidateDetails.append({"Technical_skill":tech})

                ## Soft skill

                soft = []
                candsoftSkill = CandidateSoftskillsModel.objects.filter(user_id = getData["user_id"]).values()
                for ss in candsoftSkill:
                    soft.append(ss['candidate_soft_skill_name'])
                candidateDetails.append({"Soft_Skill":soft})

                ## Project
                    
                technical_skills_list =[]
                tech_skill_list_id = []
                project_details = {}
                projects_list=[]
                proj = CandidateProjectModel.objects.filter(user_id = getData["user_id"]).values()
                projTech = CandidateProjectTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for pj in proj:
                    projDetail = pj['candidate_project_name'] + ' - ' + pj['candidate_project_description']
                    for tech_skill in projTech:
                        if tech_skill['candidate_project_id'] == pj['candidate_resume_project_id']:
                            tech_skill_name = tech_skill['candidate_technical_skill_name']
                            tech_skill_id = tech_skill['candidate_technical_skill_id']
                            technical_skills_list.append(tech_skill_name)
                            tech_skill_list_id.append(tech_skill_id)
                        
                    project_details = {
                                'description': projDetail,
                                'technical_skills': technical_skills_list,
                            }
                    projects_list.append(project_details)
                candidateDetails.append(projects_list)

                
                ##hackathon
                
                hktech = []
                hktech_id = []
                hackathon_list =[]
                hackathon = CandidatehackathonModel.objects.filter(user_id = getData["user_id"]).values()
                hackTech = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for ht in hackathon:
                    hackathon_name = ht['candidate_hackathon_name'] + ' - ' + ht['candidate_hackathon_description']
                    for hk in hackTech:
                        if hk['candidate_hackathon_id'] == ht['candidate_resume_hackathon_id']:
                            tech_skill_name = hk['candidate_technical_skill_name']
                            tech_skill_id = hk['candidate_technical_skill_id']
                            hktech.append(tech_skill_name)
                            hktech_id.append(tech_skill_id)
                            
                    hackathon_details = {
                                'hackathon_name': hackathon_name,
                                'technical_skills': hktech
                            }
                    hackathon_list.append(hackathon_details)
                candidateDetails.append(hackathon_list)

                ###contribution

                contech = []
                contech_id = []
                contribution_list =[]
                contribution = CandidateContributionModel.objects.filter(user_id = getData["user_id"]).values()
                contriTech = CandidateContributionTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for contri in contribution:
                    contribution_name = contri['candidate_contribution_topic']
                    for contrib in contriTech: 
                        if contrib['candidate_contribution_id'] == contri['candidate_resume_contribution_id']:
                            tech_skill_name = contrib['candidate_technical_skill_name']
                            contech.append(tech_skill_name)
                            contech_id.append(contrib['candidate_technical_skill_id'])
                           
                    contribution_details = {
                                'contribution_name': contribution_name,
                                'technical_skills': contech
                            }
                    contribution_list.append(contribution_details)
                candidateDetails.append(contribution_list)

                ##workshop

                wrkshoptech = []
                wrkshoptech_id = []
                wrkshop_list =[]
                workshop = CandidateWorkshopModel.objects.filter(user_id = getData["user_id"]).values()
                workshopTech = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for ws in workshop:
                    workshop_name = ws['candidate_workshop_name'] + ' - ' + ws['candidate_workshop_topic'] + ' - '+ ws['candidate_workshop_description']
                    for wsTech in workshopTech: 
                        if wsTech['candidate_workshop_id'] == ws['candidate_resume_workshop_id']:
                            tech_skill_name = wsTech['candidate_technical_skill_name']
                            wrkshoptech.append(tech_skill_name)
                            wrkshoptech_id.append(wsTech['candidate_technical_skill_id'])
                          
                    workshop_details = {
                                'workshop_name': workshop_name,
                                'technical_skills': wrkshoptech
                            }
                    wrkshop_list.append(workshop_details)
                candidateDetails.append(wrkshop_list)

                ##seminar

                seminar = CandidateSeminarModel.objects.filter(user_id = getData["user_id"]).values()
                for sem in seminar:
                    seminarDetail = sem['candidate_seminar_name'] + ' - ' + sem['candidate_seminar_description']
                    candidateDetails.append(seminarDetail)
                  

                ##competition
                    
                comptech = []
                comptech_id = []
                comp_list =[]
                competition = CandidateCompetitionModel.objects.filter(user_id = getData["user_id"]).values()
                competitionTech = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for comp in competition:
                    competition_name = comp['candidate_competition_name'] + ' - ' + comp['candidate_competition_description']
                    for cpTech in competitionTech: 
                        if cpTech['candidate_competition_id'] == comp['candidate_resume_competition_id']:
                            tech_skill_name = cpTech['candidate_technical_skill_name']
                            comptech.append(tech_skill_name)
                            comptech_id.append(cpTech['candidate_technical_skill_id'])
                          
                    competition_details = {
                                'competition_name': competition_name,
                                'technical_skills': comptech
                            }
                    comp_list.append(competition_details)
                candidateDetails.append(comp_list)

                ##certificate
                    
                certtech = []
                certtech_id = []
                certi_list =[]
                certificate = CandidateCertificateModel.objects.filter(user_id = getData["user_id"]).values()
                certificateTech = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id = getData["user_id"]).values()
                for comp in certificate:
                    certificate_name = comp['candidate_certificate_name'] + ' - ' + comp['candidate_certificate_description']
                    for cfTech in certificateTech: 
                        if cfTech['candidate_certificate_id'] == comp['candidate_resume_certificate_id']:
                            tech_skill_name = cfTech['candidate_technical_skill_name']
                            certtech.append(tech_skill_name)
                            certtech_id.append(cfTech['candidate_technical_skill_id'])
                        
                    certificate_details = {
                                'certificate_name': certificate_name,
                                'technical_skills': certtech
                            }
                    certi_list.append(certificate_details)
                candidateDetails.append(certi_list)
                
                candidate_details_string = json.dumps(candidateDetails, indent=4)
                cleaned_candidate_details_string = candidate_details_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")

                aiCompPercentageScore = float(aiComperision(cleaned_jobDescription_string,cleaned_candidate_details_string))

                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Comparision Details",
                    "Data":{
                            "user_id":getData["user_id"],
                            "job_description_id": getData["job_description_id"],
                            "recruiter_user_id":getData["recruiter_user_id"],
                            "candidateDetails":cleaned_candidate_details_string,
                            "recruiterDetails":cleaned_jobDescription_string,
                            "AI_Comparision_Percentage":aiCompPercentageScore
                    }
                }
                return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)


class RecruiterBulkResumeUploadAPI(APIView):
    '''
        Job Description comparision ai API(post)
        Request : post
        Data =  {
                    "recruiter_user_id": "BroaderAI_patelyash2504_rc0z5kgyrf"
                }
    '''
    def post(self, request, format=None):

        if not request.FILES:

            return Response({"Error": "File is required"}, status=status.HTTP_201_CREATED)

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            #bulk resume upload
            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))

            uniqueID = "BroaderAI_recruiter_bulk_resume_" + randomstr
            getData["recruiter_bulk_resume_upload_id"] = uniqueID
            
            serializer = RecruiterBulkResumeUploadSerializer(data=getData)
        
            if serializer.is_valid():

                #store zip folder in path in media folder
                if RecruiterBulkResumeUploadModel.objects.filter(user_id = getData["user_id"]).exists():

                    userUpload = RecruiterBulkResumeUploadModel.objects.get(user_id = getData["user_id"])
                    filepath = userUpload.recruiter_bulk_resume_upload.name
                    filepath = filepath.split("/media/")[1]

                    print("my path: ", filepath)
                    print("all my hhh: ", os.path.join(settings.MEDIA_ROOT,  filepath))

                    # filepath = filepath.split("/")[0] +"\\" +  filepath.split("/")[1] 
                    userUpload.delete()
                    os.remove(os.path.join(settings.MEDIA_ROOT,  filepath))
                    
                
                serializer.save()

                resp = serializer.data

                #store zip folder path in model
                userRes = RecruiterBulkResumeUploadModel(
                    recruiter_bulk_resume_upload_id =  resp["recruiter_bulk_resume_upload_id"],
                    user_id  = resp["user_id"],
                    recruiter_bulk_resume_upload = resp["recruiter_bulk_resume_upload"],
                    )

                userRes.save() #save model

                #to unzip the zip folder
                if userRes.pk:

                    try:

                        file_path = ""

                        #get zip folder from model
                        data = RecruiterBulkResumeUploadModel.objects.get(recruiter_bulk_resume_upload_id=resp["recruiter_bulk_resume_upload_id"], user_id=resp["user_id"])

                        original_path = str(data.recruiter_bulk_resume_upload) #zip folder path

                        # fullpath = os.getcwd() + original_path.replace("/", "\\") #full zip folder path from e:

                        fullpath = "/home/hrvolt" + original_path #full zip folder path from e:

                        target_directory = os.path.join(settings.MEDIA_ROOT, 'extracted_resumes') #make directory in media folder

                        os.makedirs(target_directory, exist_ok=True)

                        with zipfile.ZipFile(fullpath, 'r') as zip_ref: #unzip folder

                            for file_name in zip_ref.namelist():
                            
                                file_info = zip_ref.getinfo(file_name) #getting file name
                            
                                if file_info.is_dir():
                                    continue

                                
                                file_path = os.path.join(target_directory, file_name) #full path for all unzip files

                                print("allpath: ", file_path)

                                if file_path.lower().endswith('.pdf'): #validation only lower and .pdf is allowed

                                    zip_ref.extract(file_name, target_directory)

                                    print("rty tyuui")

                                    #store extracted file in new model
                                    randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                                    uniqueID = "BroaderAI_recruiter_extracted_file_" + randomstr
                                    
                                    try:
                                        resumeText = getResumeText(file_path) #resume parsing for extracting text

                                    except Exception as e:
                                        
                                        print("error", e)
                                        resumeText = ''

                                    # recZipfile = RecruiterExtractedZipFileModel(
                                    #     recruiter_resume_extracted_file_id=uniqueID,
                                    #     recruiter_bulk_resume_upload_id=data.recruiter_bulk_resume_upload_id,
                                    #     user_id=data.user_id,
                                    #     resume_file_path='\media' + file_path.split('\media')[1], 
                                    #     resume_extracted_text=resumeText
                                        
                                    # )

                                    recZipfile = RecruiterExtractedZipFileModel(
                                        recruiter_resume_extracted_file_id=uniqueID,
                                        recruiter_bulk_resume_upload_id=data.recruiter_bulk_resume_upload_id,
                                        user_id=data.user_id,
                                        resume_file_path='/media' + file_path.split('/media')[1], 
                                        resume_extracted_text=resumeText
                                        
                                    )

                                    recZipfile.save()

                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Resume Zip is successfully uploaded",
                            
                            "Data": {

                                "recruiter_bulk_resume_upload_id" : resp["recruiter_bulk_resume_upload_id"],
                                "user_id" :  resp["user_id"],
                                "recruiter_bulk_resume_upload_link" : settings.BASE_URL + resp["recruiter_bulk_resume_upload"],
                                "recruiter_bulk_resume_upload" : resp["recruiter_bulk_resume_upload"],
                                "recruiter_resume_extracted_file_id":uniqueID,
                                "resume_file_path" :file_path

                            }
                        }

                        return Response(res, status=status.HTTP_201_CREATED)
 
                    except Exception as e:
                        print("Error : ", e)
                        pass

                
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
                "Message": "User is not found",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)

class RecruiterResumeJobDescriptionCompareAPI(APIView):
    '''
        Job Description comparision ai API(post)
        Request : post
        Data =  {
                    "user_id": "BroaderAI_patelyash2504_rc0z5kgyrf",
                    "job_description_id:,
                    "recruiter_bulk_resume_upload_id":
                }
    '''
    def post(self, request, format=None): 
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin:

                if JobDescriptionModel.objects.filter(user_id = getData["user_id"], job_description_id = getData["job_description_id"]).exists():

                    if RecruiterBulkResumeUploadModel.objects.filter(user_id = getData["user_id"], recruiter_bulk_resume_upload_id = getData["recruiter_bulk_resume_upload_id"]).exists():

                        # Recruiter Job Description Details
                        recruiterDetails = []

                        #Soft Skill
                        jDsoftSkill = SoftSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                        softSkillNamejobDesList = [type['soft_skills_name'] for type in jDsoftSkill]
                        recruiterDetails.append({"Soft_skills":softSkillNamejobDesList})


                        #Technical Skill
                        jDtechSkill = TechnicalSkillJobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                        techSkilljobDesList = [type['technical_skills_id'] for type in jDtechSkill]
                        techSkillNamejobDesList = [type['technical_skills_name'] for type in jDtechSkill]
                        recruiterDetails.append({"Technical_skills":techSkillNamejobDesList})
                            

                        #job level
                        jDjobLevel = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                        joblevelNamejobDesList = [type['job_level_name'] for type in jDjobLevel]

                        recruiterDetails.append(joblevelNamejobDesList)

                        #job Pos
                        jDjobPosition = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                        jobPositionNamejobDesList = [type['job_position_name'] for type in jDjobPosition]
                        recruiterDetails.append(jobPositionNamejobDesList)

                        #responsibility
                        jDRespons = JobDescriptionResponsibilityModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                       
                        for res in jDRespons:
                            responsibity = JobResponsibilityModel.objects.get(job_responsibility_id = res['job_responsibility_id']).job_responsibility_description
                        
                            recruiterDetails.append(responsibity)

                        #job title
                        jDjobtitle = JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).values()
                        jobtitleNamejobDesList = [type['job_tilte'] for type in jDjobtitle]
                        recruiterDetails.append(jobtitleNamejobDesList)

                        jobDescription_string = json.dumps(recruiterDetails, indent=4)
                        cleaned_jobDescription_string = jobDescription_string.replace("\\", "").replace("\"", "").replace("\n", "").replace("\\n", "").replace("    ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "")


                        #bulk resume data
                        extracted_text = {}
                        resume_list = []
                        resumeText = RecruiterExtractedZipFileModel.objects.filter(user_id = getData["user_id"],recruiter_bulk_resume_upload_id = getData["recruiter_bulk_resume_upload_id"]).values()
                        for resume in resumeText:

                            # doc = nlp(resume['resume_extracted_text'])

                            # names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

                            # if len(names) != 0:
                            #     person = names[0] 
                            # else:
                            #     person = ""


                            person = ""

                            extracted_text= {
                                "resume_file_path" : settings.BASE_URL + resume['resume_file_path'],
                                "text": resume['resume_extracted_text'],
                                "candidate_name": person,
                                "aiCompPercentageScore" : float(aiComperision(cleaned_jobDescription_string,resume['resume_extracted_text']))
                                
                                }

                            resume_list.append(extracted_text)

                        sorted_resumes = sorted(resume_list, key=operator.itemgetter('aiCompPercentageScore'), reverse=True)


                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Comparision Details",
                            "Data":{
                                    "user_id":getData["user_id"],
                                    "job_description_id": getData["job_description_id"],
                                    "recruiterDetails":cleaned_jobDescription_string,
                                    "aiCompPercentageScore":sorted_resumes
                            }
                        }

                        return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Recruiter has not upload any Resume Zip. Please Upload Resume Zip!",
                            "Data":[],}
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Recruiter has not specific job Description. Please post job Description!",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
                    "Data":[],}
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not exits",
                "Data":[],}
            return Response(res, status=status.HTTP_201_CREATED)
