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
from candidatePreferenceAPI.models import *
from candidateresumeAPI.models import *
from databaseAPI.models import *

#######################################

############# Education ###############

#######################################

class MainEducationWeightageRegisterAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "main_education_total_weightage" : 2.5
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_education_weightage_" + randomstr
        
        serializer = MainEducationWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_education_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate weightage Details is Added",
                "Data": {   
                    "main_education_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainEducationWeightageUpdateAPI(APIView):
    '''
        MainEducationWeightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id": "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "main_education_total_weightage" : 2.5
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = MainEducationWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = MainEducationWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.main_education_total_weightage = getData["main_education_total_weightage"]
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainEducationWeightageGetAPI(APIView):
    '''
        MainEducationWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        mainEducationWeightageDetails = MainEducationWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": mainEducationWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MainEducationWeightageDeleteAPI(APIView):
    '''
        MainEducationWeightage API(delete)
        Request : delete
        Data =  {
                    "main_education_weightage_id":"BroaderAI_main_education_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if MainEducationWeightageModel.objects.filter(main_education_weightage_id = getData["main_education_weightage_id"]).exists():
            MainEducationWeightageDetail = MainEducationWeightageModel.objects.get(main_education_weightage_id = getData["main_education_weightage_id"])
            MainEducationWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Education Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main Education Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

################################################
        
############# Education Category ################
        
################################################
        
class EducationCategoriesWeightageRegisterAPI(APIView):
    '''
    {
    method: POST
    Data = {
        "main_education_weightage_id" : BroaderAI_main_education_weightage_x1bnnpn6po9rpwq",
        "education_id" : "BroaderAI_education_28ptahzd1qf6s6t",
        "education_categories_weightage" : 2.5
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if not EducationCategoriesWeightageModel.objects.filter(main_education_weightage_id = getData['main_education_weightage_id'],education_id=getData["education_id"]).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

            uniqueID = "BroaderAI_education_category_weightage_" + randomstr
            
            serializer = EducationCategoriesWeightageserializer(data=getData)
            
            if serializer.is_valid():
                
                serializer.save(education_categories_weightage_id = uniqueID)
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education Weightage is Added",
                    "Data": {   
                        "education_categories_weightage_id" : uniqueID
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
                "Message": "Education is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
  
class EducationCategoriesWeightageUpdateAPI(APIView):
    '''
        EducationCategoriesWeightage API(Insert)
        Request : patch
        Data = {
                    "education_categories_weightage_id" : "BroaderAI_education_category_weightage_4df1jiob6p6q2kz",
                    "main_education_weightage_id" : "BroaderAI_main_education_weightage_x1bnnpn6po9rpwq",
                    "education_id" : "BroaderAI_education_28ptahzd1qf6s6t",
                    "education_categories_weightage" : 2.5
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if EducationCategoriesWeightageModel.objects.filter(education_categories_weightage_id = getData['education_categories_weightage_id']).exists():

            serializer = EducationCategoriesWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = EducationCategoriesWeightageModel.objects.get(education_categories_weightage_id = getData["education_categories_weightage_id"])
                updateData.education_categories_weightage_id = getData["education_categories_weightage_id"]
                updateData.main_education_weightage_id = getData["main_education_weightage_id"]
                updateData.education_id = getData["education_id"]
                updateData.education_categories_weightage = getData["education_categories_weightage"]
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Education is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class EducationCategoriesWeightageGetAPI(APIView):
    '''
        EducationCategoriesWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        educationCategoriesWeightageDetails = EducationCategoriesWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": educationCategoriesWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class EducationCategoriesWeightageDeleteAPI(APIView):
    '''
        EducationCategoriesWeightage API(delete)
        Request : delete
        Data =  {
                    "education_categories_weightage_id":"BroaderAI_education_category_weightage_yell3e6w6ewiom7"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if EducationCategoriesWeightageModel.objects.filter(education_categories_weightage_id = getData["education_categories_weightage_id"]).exists():
            educationCategoriesWeightageDetail = EducationCategoriesWeightageModel.objects.get(education_categories_weightage_id = getData["education_categories_weightage_id"])
            educationCategoriesWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education Category Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education Category Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        



##################################################

############# Experience ########################       

###################################################
        
class MainExperienceWeightageRegisterAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "per_internship_weightage" : 2.5,
    "Total_internship_weightage" :,
    "per_month_experience_weightage" :,
    "Total_experience_weightage":
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_experience_weightage_" + randomstr
        
        serializer = MainExperienceWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_experience_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate experience weightage Details is Added",
                "Data": {   
                    "main_experience_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainExperienceWeightageUpdateAPI(APIView):
    '''
        MainexperienceWeightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "per_internship_weightage" : 2.5,
                    "Total_internship_weightage" :,
                    "per_month_experience_weightage" :,
                    "Total_experience_weightage":
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = MainExperienceWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = MainExperienceWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.per_internship_weightage = getData["per_internship_weightage"]
                updateData.Total_internship_weightage = getData["Total_internship_weightage"]
                updateData.per_month_experience_weightage = getData["per_month_experience_weightage"]
                updateData.Total_experience_weightage = getData["Total_experience_weightage"]
                
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainExperienceWeightageGetAPI(APIView):
    '''
        MainexperienceWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        mainexperienceWeightageDetails = MainExperienceWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": mainexperienceWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MainExperienceWeightageDeleteAPI(APIView):
    '''
        MainexperienceWeightage API(delete)
        Request : delete
        Data =  {
                    "main_experience_weightage_id":"BroaderAI_main_experience_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if MainExperienceWeightageModel.objects.filter(main_experience_weightage_id = getData["main_experience_weightage_id"]).exists():
            MainexperienceWeightageDetail = MainExperienceWeightageModel.objects.get(main_experience_weightage_id = getData["main_experience_weightage_id"])
            MainexperienceWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main experience Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main experience Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

##################################################

############# Technical Skills ###################
        
###################################################
        
class TechnicalSkillWeightageAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "per_technical_skill_weightage" : 2.5,
    "Total_technical_skill_weightage" :,
    "per_haveto_technical_skill_weightage" :,
    "per_optional_technical_skill_weightage":,

    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_technical_skill_weightage_" + randomstr
        
        serializer = TechnicalSkillWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_technical_skill_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate technical Skill weightage Details is Added",
                "Data": {   
                    "main_technical_skill_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MaintechnicalSkillWeightageUpdateAPI(APIView):
    '''
        MaintechnicalSkillWeightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "per_technical_skill_weightage" : 2.5,
                    "Total_technical_skill_weightage" :,
                    "per_haveto_technical_skill_weightage" :,
                    "per_optional_technical_skill_weightage":,
                    
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = TechnicalSkillWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = TechnicalSkillWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.per_technical_skill_weightage = getData["per_technical_skill_weightage"]
                updateData.Total_technical_skill_weightage = getData["Total_technical_skill_weightage"]
                updateData.per_haveto_technical_skill_weightage = getData["per_haveto_technical_skill_weightage"]
                updateData.per_optional_technical_skill_weightage = getData["per_optional_technical_skill_weightage"]
               
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MaintechnicalSkillWeightageGetAPI(APIView):
    '''
        MaintechnicalSkillWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        maintechnicalSkillWeightageDetails = TechnicalSkillWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": maintechnicalSkillWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MaintechnicalSkillWeightageDeleteAPI(APIView):
    '''
        Main technicalSkill Weightage API(delete)
        Request : delete
        Data =  {
                    "main_technical_skill_weightage_id":"BroaderAI_main_technicalSkill_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if TechnicalSkillWeightageModel.objects.filter(main_technical_skill_weightage_id = getData["main_technical_skill_weightage_id"]).exists():
            MaintechnicalSkillWeightageDetail = TechnicalSkillWeightageModel.objects.get(main_technical_skill_weightage_id = getData["main_technical_skill_weightage_id"])
            MaintechnicalSkillWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main technicalSkill Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main technicalSkill Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

##################################################
        
############# Soft Skills ########################
        
###################################################    

class SoftSkillWeightageAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "per_soft_skill_weightage" : 2.5,
    "Total_soft_skill_weightage" :,
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_soft_skill_weightage_" + randomstr
        
        serializer = SoftSkillWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_soft_skill_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate soft Skill weightage Details is Added",
                "Data": {   
                    "main_soft_skill_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainSoftSkillWeightageUpdateAPI(APIView):
    '''
        MainSoftSkillWeightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "per_soft_skill_weightage" : 2.5,
                    "Total_soft_skill_weightage" :,
                    
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = SoftSkillWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = SoftSkillWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.per_soft_skill_weightage = getData["per_soft_skill_weightage"]
                updateData.Total_soft_skill_weightage = getData["Total_soft_skill_weightage"]
                
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainSoftSkillWeightageGetAPI(APIView):
    '''
        MainSoftSkillWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        mainSoftSkillWeightageDetails = SoftSkillWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": mainSoftSkillWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MainSoftSkillWeightageDeleteAPI(APIView):
    '''
        Main SoftSkill Weightage API(delete)
        Request : delete
        Data =  {
                    "main_soft_skill_weightage_id":"BroaderAI_main_SoftSkill_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if SoftSkillWeightageModel.objects.filter(main_soft_skill_weightage_id = getData["main_soft_skill_weightage_id"]).exists():
            mainSoftSkillWeightageDetail = SoftSkillWeightageModel.objects.get(main_soft_skill_weightage_id = getData["main_soft_skill_weightage_id"])
            mainSoftSkillWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main SoftSkill Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main SoftSkill Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]



##################################################
        
############# curricular Activities ################
        
###################################################
        

class CurricularActivitiesWeightageAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "per_curricular_activity_weightage" : 2.5,
    "Total_curricular_activity_weightage" :,
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_curricular_activity_weightage_" + randomstr
        
        serializer = CurricularActivitiesWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_curricular_activity_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate curricular activity weightage Details is Added",
                "Data": {   
                    "main_curricular_activity_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainCurricularActivitiesWeightageUpdateAPI(APIView):
    '''
        MainCurricularActivitiesWeightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "per_curricular_activity_weightage" : 2.5,
                    "Total_curricular_activity_weightage" :,
                    
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = CurricularActivitiesWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = CurricularActivitiesWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.per_curricular_activity_weightage = getData["per_curricular_activity_weightage"]
                updateData.Total_curricular_activity_weightage = getData["Total_curricular_activity_weightage"]
                
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainCurricularActivitiesWeightageGetAPI(APIView):
    '''
        MainCurricularActivitiesWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        mainCurricularActivitiesWeightageDetails = CurricularActivitiesWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": mainCurricularActivitiesWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MainCurricularActivitiesWeightageDeleteAPI(APIView):
    '''
        Main CurricularActivities Weightage API(delete)
        Request : delete
        Data =  {
                    "main_curricular_activity_weightage_id":"BroaderAI_main_CurricularActivities_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if CurricularActivitiesWeightageModel.objects.filter(main_curricular_activity_weightage_id = getData["main_curricular_activity_weightage_id"]).exists():
            mainCurricularActivitiesWeightageDetail = CurricularActivitiesWeightageModel.objects.get(main_curricular_activity_weightage_id = getData["main_curricular_activity_weightage_id"])
            mainCurricularActivitiesWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Curricular Activities Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main Curricular Activities Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

##################################################
        
############# Any drop ################
        
###################################################
        

class AnyDropWeightageAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "any_drop_weightage" : 2.5,
    
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_any_drop_weightage_" + randomstr
        
        serializer = AnyDropWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_any_drop_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Any Drop weightage Details is Added",
                "Data": {   
                    "main_any_drop_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainAnyDropWeightageUpdateAPI(APIView):
    '''
        Main Any Drop Weightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "any_drop_weightage" : 2.5
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = AnyDropWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = AnyDropWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.any_drop_weightage = getData["any_drop_weightage"]
               
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainAnyDropWeightageGetAPI(APIView):
    '''
        MainAnyDropWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        mainAnyDropWeightageDetails = AnyDropWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": mainAnyDropWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MainAnyDropWeightageDeleteAPI(APIView):
    '''
        Main any drop Weightage API(delete)
        Request : delete
        Data =  {
                    "main_any_drop_weightage_id":"BroaderAI_main_any_drop_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if AnyDropWeightageModel.objects.filter(main_any_drop_weightage_id = getData["main_any_drop_weightage_id"]).exists():
            mainAnyDropWeightageDetail = AnyDropWeightageModel.objects.get(main_any_drop_weightage_id = getData["main_any_drop_weightage_id"])
            mainAnyDropWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Any drop Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main Any drop Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

##################################################
        
############# Projects ################
        
###################################################
        

class ProjectWeightageAPI(APIView):
    '''
    {
    method: POST
    {
    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
    "per_project_weightage" : 2.5,
    "Total_project_weightage" :,
    }
    }
    '''
    def post(self, request ,format=None):
        getData = request.data

        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))

        uniqueID = "BroaderAI_main_project_weightage_" + randomstr
        
        serializer = ProjectWeightageserializer(data=getData)
        
        if serializer.is_valid():
            
            serializer.save(main_project_weightage_id= uniqueID)
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate project weightage Details is Added",
                "Data": {   
                    "main_project_weightage_id" : uniqueID
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
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainProjectWeightageUpdateAPI(APIView):
    '''
        MainProjectWeightage API(Insert)
        Request : patch
        Data = {
                    "job_level_id" : "BroaderAI_job_level_t2n0z8nqjvvv48s",
                    "per_project_weightage" : 2.5,
                    "Total_project_weightage" :,
                    
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

            serializer = ProjectWeightageserializer(data=getData)

            if serializer.is_valid():
                updateData = ProjectWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                updateData.job_level_id = getData["job_level_id"]
                updateData.per_project_weightage = getData["per_project_weightage"]
                updateData.Total_project_weightage = getData["Total_project_weightage"]
                
                updateData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Weightage is Updated",
                    "Data": getData
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
                "Message": "Job Level is not exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
        
class MainProjectWeightageGetAPI(APIView):
    '''
        MainProjectWeightage API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        mainProjectWeightageDetails = ProjectWeightageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Weightage Details",
                "Data": mainProjectWeightageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class MainProjectWeightageDeleteAPI(APIView):
    '''
        Main Project Weightage API(delete)
        Request : delete
        Data =  {
                    "main_project_weightage_id":"BroaderAI_main_Project_weightage_x1bnnpn6po9rpwq"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if ProjectWeightageModel.objects.filter(main_project_weightage_id = getData["main_project_weightage_id"]).exists():
            mainProjectWeightageDetail = ProjectWeightageModel.objects.get(main_project_weightage_id = getData["main_project_weightage_id"])
            mainProjectWeightageDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main project Weightage is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main project Weightage data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
