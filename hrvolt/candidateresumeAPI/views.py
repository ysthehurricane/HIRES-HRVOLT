from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
                                                                   
import string
import random
import os
import json
import re
from datetime import datetime, timedelta

import requests 

from .models import *
from databaseAPI.models import *
from userloginAPI.models import *

from .serializers import *
from hrvolt.emailsend import mailSend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

# import logging

# from langdetect import detect

# from Translator import translator 

# logging.basicConfig(filename='candidateResumeAPI.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# from .resumeParse import *


# import py3langid as langid

# def detect_language(text):
#     lang, _ = langid.classify(text)
#     return lang

# def is_english(text):
#     pattern = re.compile(r'^[a-zA-Z0-9 !@#$%^&*(),.?":{}|<>_+=\[\]-]+$')
    
#     return bool(pattern.match(text))



class userResumeUploadAPI(APIView):

    '''
        Use Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : resumeUpload
        Value : Files upload....

        }
    
    '''

    def post(self, request, format=None):

        try:

            if not request.FILES:

                return Response({"Error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)

            getData = request.data

            if NewUser.objects.filter(id = getData["user_id"]).exists():

                user = NewUser.objects.get(id = getData["user_id"])

                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_userresumefile" + randomstr
                getData["candidate_resumeUpload_id"] = uniqueID
                
                serializer = CandidateUserResumeUploadSerializer(data=getData)
            
                if serializer.is_valid():

                    if CandidateUserResumeUpload.objects.filter(user_id = getData["user_id"]).exists():

                        userUpload = CandidateUserResumeUpload.objects.get(user_id = getData["user_id"])
                        filepath = userUpload.candidate_resumeUpload.name
                        filepath = filepath.split("/media/")[1]
                        filepath = filepath.split("/")[0] +"\\" +  filepath.split("/")[1] 
                        userUpload.delete()
                        os.remove(os.path.join(settings.MEDIA_ROOT,  filepath))
                    
                    serializer.save()

                    resp = serializer.data

                    userRes = CandidateUserResumeUpload(
                        candidate_resumeUpload_id =  resp["candidate_resumeUpload_id"],
                        user_id  = resp["user_id"],
                        candidate_resumeUpload = resp["candidate_resumeUpload"],
                        )

                    userRes.save()

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Resume is successfully uploaded",
                        "Data": {
                            "candidate_resumeUpload_id" : resp["candidate_resumeUpload_id"],
                            "user_id" :  resp["user_id"],
                            "candidate_resumeUpload_link" : settings.BASE_URL + resp["candidate_resumeUpload"],
                            "candidate_resumeUpload" : resp["candidate_resumeUpload"]

                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
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

        except Exception as e:
            # logging.error('Error: ',e)
            pass



class getUserResumeAPI(APIView):
    '''
    Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

    '''
    def post(self, request, format=None):

        try:

            getData = request.data # data comes from post request

            if NewUser.objects.filter(id = getData["user_id"]).exists():
                
                if CandidateUserResumeUpload.objects.filter(user_id = getData["user_id"]).exists():
                    
                    user = NewUser.objects.get(id = getData["user_id"])

                    if user.user_is_loggedin and user.user_is_verified:

                        resumeDetails = CandidateUserResumeUpload.objects.get(user_id = getData["user_id"]) 

                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "User Resume Details", 
                                "Data":{
                                    "user_id": getData["user_id"],
                                    "candidate_resumeUpload_id":resumeDetails.candidate_resumeUpload_id,
                                    "candidate_resumeUpload" : settings.BASE_URL + str(resumeDetails.candidate_resumeUpload)
                                }
                            }

                        return Response(res, status=status.HTTP_201_CREATED)

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User resume details is not found",
                        "Data":None }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class userCoverLetterAPI(APIView):

    '''
        Use Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : coverletter
        Value : Files upload....

        }
    
    '''

    def post(self, request, format=None):

        try:

            if not request.FILES:

                return Response({"Error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)


            getData = request.data

            if NewUser.objects.filter(id = getData["user_id"]).exists(): 
    
                user = NewUser.objects.get(id = getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified: 

                    
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))


                    uniqueID = "BroaderAI_usercoverltter" + randomstr
                    getData["coverletter_id"] = uniqueID
                    
                    serializer = CandidateUserCoverLetterUploadSerializer(data=getData)
                
                    if serializer.is_valid():

                        if CandidateUserCoverLetterUpload.objects.filter(user_id = getData["user_id"]).exists():

                            userUpload = CandidateUserCoverLetterUpload.objects.get(user_id = getData["user_id"])
                            filepath = userUpload.candidate_coverletter.name
                            filepath = filepath.split("/media/")[1]
                            filepath = filepath.split("/")[0] +"\\" +  filepath.split("/")[1] 
                            userUpload.delete()
                            os.remove(os.path.join(settings.MEDIA_ROOT,  filepath))

                        serializer.save()

                        resp = serializer.data

                        userRes = CandidateUserCoverLetterUpload(
                            coverletter_id =  resp["coverletter_id"],
                            user_id  = resp["user_id"],
                            candidate_coverletter = resp["candidate_coverletter"],
                            )

                        userRes.save()

                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Cover Letter is successfully uploaded",
                            "Data": {
                                "coverletter_id" : resp["coverletter_id"],
                                "user_id" :  resp["user_id"],
                                "candidate_coverletter" : resp["candidate_coverletter"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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
            
        except Exception as e:
            # logging.error('Error: ',e)
            pass


class getUserCoverAPI(APIView):
    '''
        User Cover API
        request = post
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a
        }
    
    '''
    def post(self, request, format=None):

        try:

            getData = request.data # data comes from post request

            if NewUser.objects.filter(id = getData["user_id"]).exists():
                
                if CandidateUserCoverLetterUpload.objects.filter(user_id = getData["user_id"]).exists():
                    
                    user = NewUser.objects.get(id = getData["user_id"])

                    if user.user_is_loggedin and user.user_is_verified:

                        coverDetails = CandidateUserCoverLetterUpload.objects.get(user_id = getData["user_id"]) 

                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "User Cover Details", 
                                "Data":{
                                    "user_id": getData["user_id"],
                                    "coverletter_id":coverDetails.coverletter_id,
                                    "candidate_coverletter" : settings.BASE_URL + str(coverDetails.candidate_coverletter)
                                }
                            }

                        return Response(res, status=status.HTTP_201_CREATED)

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User cover details is not found", 
                        "Data":[] }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#   Basic Education APIs (Begin)

####################################################

class candidateBasicEducationRegisterAPI(APIView):
    '''
        Candidate Basic Education API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_last_education_id": "BroaderAI_Lasteducationxq96dwyeolkra62",
                    "candidate_last_education_field_id": "BroaderAI_educationfield2bj6k7owr6u8hfe",
                    "candidate_total_years_education": 15,
                    "candidate_education_year_drop": true
                }
    '''
    def post(self, request ,formate=None):
        
        try: 

            getData = request.data

            if NewUser.objects.filter(id=getData["user_id"]).exists():
            
                user = NewUser.objects.get(id=getData["user_id"])
            
                if user.user_is_loggedin and user.user_is_verified: 

                    if EducationModel.objects.filter(education_id = getData["candidate_last_education_id"]).exists():

                        if EducationFieldModel.objects.filter(education_field_id = getData["candidate_last_education_field_id"]).exists():

                            if not CandidateBasicEducationDetails.objects.filter(user_id=getData["user_id"]).exists():

                                randomstr = ''.join(random.choices(string.ascii_lowercase +string.digits, k=15))

                                uniqueID = "BroaderAI_Candidate_Basic_education_" + randomstr

                                getData["candidate_total_years_education_arabic"] = "0"
                                
                                # getData["candidate_resume_basic_education_id"] = uniqueID
                                
                                # if is_english(str(getData["candidate_total_years_education"])):
                                #     getData["candidate_total_years_education_arabic"] =  str(translator.translator_en_ar(getData["candidate_total_years_education"], "en", "ar")["translated_text"])

                                # else:
                                #     getData["candidate_total_years_education_arabic"] =  getData["candidate_total_years_education"]
                                #     getData["candidate_total_years_education"] =  str(translator.translator_en_ar(getData["candidate_total_years_education"], "ar", "en")["translated_text"])

                                serializer = CandidateBasicEducationDetailsSerializer(data=getData)
                                if serializer.is_valid():
                                    
                                    serializer.save(candidate_resume_basic_education_id = uniqueID)

                                    res = {
                                        "Status": "success",
                                        "Code": 201,
                                        "Message": "Candidate Basic Education is Added",
                                        "Data": {
                                            "candidate_resume_basic_education_id": uniqueID,
                                            "user_id": getData["user_id"]
                                        }
                                    }
                                    return Response(res, status=status.HTTP_201_CREATED)
                            
                                else:
                                    res = {"Status": "error",
                                            "Code": 400,
                                            "Message": list(serializer.errors.values())[0][0], 
                                            "Data":[],
                                        }
                                    return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Basic education is already exist! ",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)

                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Education Field is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Education is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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

        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class candidateBasicEducationUpdateAPI(APIView):
    '''
        Candidate Basic Education API(Update)
        Request : PATCH
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_basic_education_id": "BroaderAI_Candidate_Basic_education_ptq3sjwoyi2t9er",
                    "candidate_last_education_id": "BroaderAI_Lasteducationxq96dwyeolkra62",
                    "candidate_last_education_field_id": "BroaderAI_educationfield2bj6k7owr6u8hfe",
                    "candidate_total_years_education": 15,
                    "candidate_education_year_drop": true
                }
    '''
    def patch(self, request ,formate=None):
        
        try:

            getData = request.data

            if NewUser.objects.filter(id=getData["user_id"]).exists():
            
                user = NewUser.objects.get(id=getData["user_id"])
            
                if user.user_is_loggedin and user.user_is_verified: 

                    if EducationModel.objects.filter(education_id = getData["candidate_last_education_id"]).exists():

                        if EducationFieldModel.objects.filter(education_field_id = getData["candidate_last_education_field_id"]).exists():

                            getData["candidate_total_years_education_arabic"] = "Not Translated"


                            # if is_english(str(getData["candidate_total_years_education"])):
                            #     getData["candidate_total_years_education_arabic"] =  str(translator.translator_en_ar(getData["candidate_total_years_education"], "en", "ar")["translated_text"])

                            # else:
                            #     getData["candidate_total_years_education_arabic"] =  getData["candidate_total_years_education"]
                            #     getData["candidate_total_years_education"] =  str(translator.translator_en_ar(getData["candidate_total_years_education"], "ar", "en")["translated_text"])

                            serializer = CandidateBasicEducationDetailsSerializer(data=getData)
                            print("--------")
                            if serializer.is_valid():

                                LastUpdateData = CandidateBasicEducationDetails.objects.get(user_id = getData["user_id"])
                                LastUpdateData.candidate_last_education_id = getData["candidate_last_education_id"]
                                LastUpdateData.candidate_last_education_field_id = getData["candidate_last_education_field_id"]
                                LastUpdateData.candidate_total_years_education = getData["candidate_total_years_education"]
                                LastUpdateData.candidate_total_years_education_arabic = getData["candidate_total_years_education_arabic"]
                                LastUpdateData.candidate_education_year_drop = getData["candidate_education_year_drop"]

                                LastUpdateData.save()
                                print('[[[[[]]]]]')

                                res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Candidate Basic Education is Updated",
                                    "Data": {
                                        "user_id": getData["user_id"]
                                    }
                                }
                                return Response(res, status=status.HTTP_201_CREATED)
                            
                            else:
                                res = {"Status": "error",
                                        "Code": 400,
                                        "Message": list(serializer.errors.values())[0][0], 
                                        "Data":[],
                                    }
                                print(res["Message"])
                                return Response(res, status=status.HTTP_201_CREATED)

                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Education Field is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Education is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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
    
        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
            
class candidateBasicEducationGetAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
            Data =  {
                        "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                    }
    '''
    def post(self, request, format=None):

        try:

            getData = request.data

            if NewUser.objects.filter(id=getData["user_id"]).exists():
            
                user = NewUser.objects.get(id=getData["user_id"])
            
                if user.user_is_loggedin and user.user_is_verified:

                    
                    candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id = getData["user_id"])
                    educationdata = EducationModel.objects.get(education_id = candidateBasicEducationData.candidate_last_education_id)
                    educationfielddata = EducationFieldModel.objects.get(education_field_id = candidateBasicEducationData.candidate_last_education_field_id)

                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Basic Education Detail",
                            "Data": {
                                "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                                "user_id": candidateBasicEducationData.user_id,
                                "candidate_last_education_id": candidateBasicEducationData.candidate_last_education_id,
                                "candidate_last_education_name": educationdata.education_name,
                                "candidate_last_education_name_arabic": educationdata.education_name_arabic,
                                "candidate_last_education_years": educationdata.education_years,
                                "candidate_last_education_field_id": candidateBasicEducationData.candidate_last_education_field_id,
                                "candidate_last_education_field_name": educationfielddata.education_field_name,
                                "candidate_last_education_field_name_arabic": educationfielddata.education_field_name_arabic,
                                "candidate_total_years_education": candidateBasicEducationData.candidate_total_years_education,
                                "candidate_education_year_drop": candidateBasicEducationData.candidate_education_year_drop,
                            }
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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
    
        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class candidateBasicEducationDeleteAPI(APIView):
    '''
        Candidate Basic Education API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def delete(self, request, format=None):

        try:

            getData = request.data

            if NewUser.objects.filter(id=getData["user_id"]).exists():
            
                user = NewUser.objects.get(id=getData["user_id"])
            
                if user.user_is_loggedin and user.user_is_verified:

                    candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id = getData["user_id"])
                    candidateBasicEducationData.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Basic Education data is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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

        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#   Basic Education APIs (End)

####################################################


#####################################################

#   Main Education APIs (Begin)

####################################################

class candidateMainEducationRegisterAPI(APIView):
    '''
        Candidate Main Education(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_degree_name": "B-tech",
            "candidate_univeresity_name": "PPSU",
            "candidate_result_class": "First Class",
            "candidate_start_year": "2015",
            "candidate_end_year": " ",
            "candidate_summary": "yashhhh hhh hfg" 
        }
    '''
    
    def post(self, request ,formate=None):
        
        try:

            getData = request.data
            if NewUser.objects.filter(id=getData["user_id"]).exists():
            
                user = NewUser.objects.get(id=getData["user_id"])
            
                if user.user_is_loggedin and user.user_is_verified: 
                    
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))

                    uniqueID = "BroaderAI_Main_education_" + randomstr

                    getData["candidate_degree_name_arabic"] = "Not Translated"
                    getData["candidate_univeresity_name_arabic"] = "Not Translated"
                    getData["candidate_result_class_arabic"] = "Not Translated"
                    getData["candidate_summary_arabic"] = "Not Translated"

                    # getData["candidate_resume_main_education_id"] = uniqueID

                    # if is_english(str(getData["candidate_degree_name"])):
                    #     getData["candidate_degree_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_degree_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_degree_name_arabic"] =  getData["candidate_degree_name"]
                    #     getData["candidate_degree_name"] =  str(translator.translator_en_ar(getData["candidate_degree_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_univeresity_name"])):
                    #     getData["candidate_univeresity_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_univeresity_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_univeresity_name_arabic"] =  getData["candidate_univeresity_name"]
                    #     getData["candidate_univeresity_name"] =  str(translator.translator_en_ar(getData["candidate_univeresity_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_result_class"])):
                    #     getData["candidate_result_class_arabic"] =  str(translator.translator_en_ar(getData["candidate_result_class"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_result_class_arabic"] =  getData["candidate_result_class"]
                    #     getData["candidate_result_class"] =  str(translator.translator_en_ar(getData["candidate_result_class"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_summary"])):
                    #     getData["candidate_summary_arabic"] =  str(translator.translator_en_ar(getData["candidate_summary"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_summary_arabic"] =  getData["candidate_summary"]
                    #     getData["candidate_summary"] =  str(translator.translator_en_ar(getData["candidate_summary"], "ar", "en")["translated_text"])

            

                    serializer = CandidateMainEducationDetailSerializer(data=getData)

                    if serializer.is_valid():
                        
                        serializer.save(candidate_resume_main_education_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Main Education is Added",
                            "Data": {
                                "candidate_resume_main_education_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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
    
        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class candidateMainEducationUpdateAPI(APIView):

    '''
        Candidate Main Education(Insert)
        Request : patch
        Data = {
                "user_id": "BroaderAI_yashpp3622_eibf9nnjma",
                "candidate_resume_main_education_id":"BroaderAI_Main_education_hpfv9v0xduz42ol",
                "candidate_degree_name": "Bsc",
                "candidate_univeresity_name": "chh gfg",
                "candidate_result_class": "First Class",
                "candidate_start_year": 2015,
                "candidate_end_year": 2019,
                "candidate_summary": "yashhhh hhh hfg" 
            }
    '''
    
    def patch(self, request, format=None):
        try:

            getData = request.data

            user_id = getData["user_id"]
            candidate_resume_main_education_id = getData["candidate_resume_main_education_id"]

            if NewUser.objects.filter(id=user_id).exists():
                user = NewUser.objects.get(id=user_id)

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateMainEducationDetails.objects.filter(
                    user_id=user_id, candidate_resume_main_education_id=candidate_resume_main_education_id).exists():

                        getData["candidate_degree_name_arabic"] = "Not Translated"
                        getData["candidate_univeresity_name_arabic"] = "Not Translated"
                        getData["candidate_result_class_arabic"] = "Not Translated"
                        getData["candidate_summary_arabic"] = "Not Translated"
                        
                        # if is_english(str(getData["candidate_degree_name"])):
                        #     getData["candidate_degree_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_degree_name"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_degree_name_arabic"] =  getData["candidate_degree_name"]
                        #     getData["candidate_degree_name"] =  str(translator.translator_en_ar(getData["candidate_degree_name"], "ar", "en")["translated_text"])

                        # if is_english(str(getData["candidate_univeresity_name"])):
                        #     getData["candidate_univeresity_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_univeresity_name"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_univeresity_name_arabic"] =  getData["candidate_univeresity_name"]
                        #     getData["candidate_univeresity_name"] =  str(translator.translator_en_ar(getData["candidate_univeresity_name"], "ar", "en")["translated_text"])

                        # if is_english(str(getData["candidate_result_class"])):
                        #     getData["candidate_result_class_arabic"] =  str(translator.translator_en_ar(getData["candidate_result_class"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_result_class_arabic"] =  getData["candidate_result_class"]
                        #     getData["candidate_result_class"] =  str(translator.translator_en_ar(getData["candidate_result_class"], "ar", "en")["translated_text"])

                        # if is_english(str(getData["candidate_summary"])):
                        #     getData["candidate_summary_arabic"] =  str(translator.translator_en_ar(getData["candidate_summary"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_summary_arabic"] =  getData["candidate_summary"]
                        #     getData["candidate_summary"] =  str(translator.translator_en_ar(getData["candidate_summary"], "ar", "en")["translated_text"])

                        CandidateMainEducationDetails.objects.filter(
                            user_id=user_id, candidate_resume_main_education_id=candidate_resume_main_education_id
                        ).update(
                            candidate_degree_name = getData['candidate_degree_name'],
                            candidate_degree_name_arabic = getData['candidate_degree_name_arabic'],
                            candidate_univeresity_name = getData['candidate_univeresity_name'],
                            candidate_univeresity_name_arabic = getData['candidate_univeresity_name_arabic'],

                            candidate_result_class = getData['candidate_result_class'] ,
                            candidate_result_class_arabic = getData['candidate_result_class_arabic'] ,

                            candidate_start_year = getData['candidate_start_year'],
                            candidate_end_year = getData['candidate_end_year'] ,
                            candidate_summary = getData['candidate_summary'],
                            candidate_summary_arabic = getData['candidate_summary_arabic'] 

                        )
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Main education details are updated.",
                            "Data": {
                                "candidate_resume_main_education_id": getData["candidate_resume_main_education_id"],
                                "user_id": getData["user_id"]
                            }
                        }

                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate Main education details are not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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

        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class candidateGetMainEducationAPI(APIView):
    '''
        Candidate Main Education API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yashpp3622_eibf9nnjma"
                }
    '''
    def post(self, request, format=None):

        try:

            getData = request.data
            
            if NewUser.objects.filter(id=getData["user_id"]).exists():
                if CandidateMainEducationDetails.objects.filter(user_id=getData["user_id"]).exists():
                    user = NewUser.objects.get(id=getData["user_id"])

                    if user.user_is_loggedin and user.user_is_verified:
                        userMainEducationDetail = CandidateMainEducationDetails.objects.filter(user_id=getData["user_id"]).values()

                        if userMainEducationDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Main Education Details",
                                "Data": userMainEducationDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Candidate main education details is not found", 
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
 
        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class candidateGetOneMainEducationAPI(APIView):
    '''
        Candidate Main Education API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yashpp3622_eibf9nnjma",
                    "candidate_resume_main_education_id": "BroaderAI_Main_education_qxt2fh57ppkq9l4"
                }
    '''
    def post(self, request, format=None):

        try:
                
            getData = request.data
            
            if NewUser.objects.filter(id=getData["user_id"]).exists():

                if CandidateMainEducationDetails.objects.filter(user_id=getData["user_id"]).exists():
                    user = NewUser.objects.get(id=getData["user_id"])

                    if user.user_is_loggedin and user.user_is_verified:

                        if CandidateMainEducationDetails.objects.filter(user_id=getData["user_id"], candidate_resume_main_education_id=getData["candidate_resume_main_educaton_id"]).exists(): 

                            userMainEducationDetail = CandidateMainEducationDetails.objects.filter(user_id=getData["user_id"], candidate_resume_main_education_id=getData["candidate_resume_main_educaton_id"]).values()

                            if userMainEducationDetail:
                                # Construct the response dictionary
                                res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Candidate Main Education Details",
                                    "Data": userMainEducationDetail
                                }
                                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                            else:
                                res = {"Status": "error",
                                        "Code": 400,
                                        "Message": list(serializer.errors.values())[0][0], 
                                        "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "User and Main education not found",
                                "Data":[],
                                }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Candidate main education details is not found", 
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class candidateMainEducationDeleteAPI(APIView):
    '''
        main education API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_yashpp3622_eibf9nnjma",
                    "candidate_resume_main_education_id": "BroaderAI_Main_education_qxt2fh57ppkq9l4"
                }
    '''
    def delete(self, request, format=None):

        try:

            getData = request.data

            if NewUser.objects.filter(id = getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])
                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateMainEducationDetails.objects.filter(candidate_resume_main_education_id = getData["candidate_resume_main_education_id"]).exists():
                        mainEducationDetail = CandidateMainEducationDetails.objects.get(candidate_resume_main_education_id = getData["candidate_resume_main_education_id"])
                        mainEducationDetail.delete()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "main Education is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "main Education data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    
        except Exception as e:
            # logging.error('Error: ',e)
            pass

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
            

#####################################################

#   Main Education APIs (End)

####################################################


#####################################################

#   Basic Experience APIs (End)

####################################################

class CandidateBasicExperienceRegisterAPI(APIView):
    '''
        Candidate basic experience(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_total_years_of_experience": "3",
            "candidate_total_years_of_experience_applied_for": "2",
            "candidate_total_internship": "1",
            "candidate_works_companies": "2",
            "candidate_field_transition": "False",
            "candidate_works_startup": "True",
            "candidate_works_MNC": "False"
        }
    '''
    def post(self, request ,formate=None):

        try:

            getData = request.data
            if NewUser.objects.filter(id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])
                if user.user_is_loggedin and user.user_is_verified:
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                    uniqueID = "BroaderAI_basic_experience_" + randomstr

                    
                    if not CandidateBasicExperienceModel.objects.filter(user_id=getData["user_id"]).exists():
                        
                        serializer = CandidateBasicExperienceSerializer(data=getData)

                        if serializer.is_valid():

                            serializer.save(candidate_resume_basic_experience_id = uniqueID)
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "User basic experience is Added",
                                "Data": {
                                    "candidate_resume_basic_experience_id": uniqueID,
                                    "user_id": getData["user_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message" : "Candidate Basic Experience data is already exists !",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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

        except Exception as e:
            # logging.error('Error: ',e)
            pass               

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class CandidateBasicExperienceUpdateAPI(APIView):

    '''
        Candidate basic experience(update)
        Request : patch
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_resume_basic_experience_id": "BroaderAI_basic_experience_gsywuycgi3ydhpb",
            "candidate_total_years_of_experience": "3",
            "candidate_total_years_of_experience_applied_for": "2",
            "candidate_total_internship": "1",
            "candidate_works_companies": "2",
            "candidate_field_transition": "false",
            "candidate_works_startup": "true",
            "candidate_works_MNC": "False"
        }
    '''
    
    def patch(self, request, format=None):

        try:

            getData = request.data

            if NewUser.objects.filter(id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateBasicExperienceModel.objects.filter(
                    user_id= getData["user_id"], candidate_resume_basic_experience_id= getData["candidate_resume_basic_experience_id"]
                ).exists():
                        CandidateBasicExperienceModel.objects.filter(
                            user_id= getData["user_id"], candidate_resume_basic_experience_id= getData["candidate_resume_basic_experience_id"]
                        ).update(
                            candidate_resume_basic_experience_id = getData['candidate_resume_basic_experience_id'],
                            candidate_total_years_of_experience = getData['candidate_total_years_of_experience'],
                            candidate_total_years_of_experience_applied_for = getData['candidate_total_years_of_experience_applied_for'] ,
                            candidate_total_internship = getData['candidate_total_internship'],
                            candidate_works_companies = getData['candidate_works_companies'] ,
                            candidate_field_transition = getData['candidate_field_transition'],
                            candidate_works_startup = getData['candidate_works_startup'],
                            candidate_works_MNC = getData['candidate_works_MNC']
                        )
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate basic experience details are updated.",
                            "Data": {
                                "candidate_resume_basic_experience_id": getData["candidate_resume_basic_experience_id"],
                                "user_id": getData["user_id"]
                            }
                        }

                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate basic experience details are not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
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

        except Exception as e:
            # logging.error('Error: ',e)
            pass 
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
class CandidateBasicExperienceGetAPI(APIView):
    '''
        Candidate basic experience API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):

        try:

            getData = request.data
            
            if NewUser.objects.filter(id=getData["user_id"]).exists():
                if CandidateBasicExperienceModel.objects.filter(user_id=getData["user_id"]).exists():
                    user = NewUser.objects.get(id=getData["user_id"])

                    if user.user_is_loggedin and user.user_is_verified:
                        candidateDetail = CandidateBasicExperienceModel.objects.filter(user_id=getData["user_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate basic experience Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "You are not logged in",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Candidate basic experience details is not found", 
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not found",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass 

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateBasicExperienceGetOneAPI(APIView):
    '''
        Candidate basic experience API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_basic_experience_id": "BroaderAI_basic_experience_gsywuycgi3ydhpb"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateBasicExperienceModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateBasicExperienceModel.objects.filter( user_id=getData["user_id"], candidate_resume_basic_experience_id=getData["candidate_resume_basic_experience_id"]).exists(): 

                        candidateDetail = CandidateBasicExperienceModel.objects.filter(user_id=getData["user_id"], candidate_resume_basic_experience_id=getData["candidate_resume_basic_experience_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate basic experience Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and basic experience not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate basic experience details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateBasicExperienceDeleteAPI(APIView):
    '''
        basic experience API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_basic_experience_id": "BroaderAI_basic_experience_gsywuycgi3ydhpb"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateBasicExperienceModel.objects.filter(candidate_resume_basic_experience_id = getData["candidate_resume_basic_experience_id"]).exists():
                    candidateDetail = CandidateBasicExperienceModel.objects.get(candidate_resume_basic_experience_id = getData["candidate_resume_basic_experience_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Basic Experience is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Basic Experience data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
            

#####################################################

#  basic experience APIs (End)

####################################################


#####################################################

#   Main Experience APIs (Start)

####################################################

class CandidateMainExperienceRegisterAPI(APIView):
    '''
        Candidate main experience(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_job_position_id": "BroaderAI_job_position_lnsccajmh3xd2lx",
            "candidate_work_place_id": "BroaderAI_Work_Place_2yysiw35atttkkw",
            "candidate_company_name": "broader ai",
            "candidate_job_level_id": "BroaderAI_job_level_8ydq84moef0ad6p",
            "candidate_company_location": "surat",
            "candidate_job_start_year": "2022",
            "candidate_job_end_year": "2023",
            "candidate_job_description":"chatgpt"
        }
    '''
    def post(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_main_experience_" + randomstr
                # getData["candidate_resume_main_experience_id"] = uniqueID

                getData["candidate_company_name_arabic"] = "Not Translated"
                getData["candidate_company_location_arabic"] = "Not Translated"
                getData["candidate_job_description_arabic"] = "Not Translated"

                # if is_english(str(getData["candidate_company_name"])):
                #     getData["candidate_company_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_company_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_company_name_arabic"] =  getData["candidate_company_name"]
                #     getData["candidate_company_name"] =  str(translator.translator_en_ar(getData["candidate_company_name"], "ar", "en")["translated_text"])

                # if is_english(str(getData["candidate_company_location"])):
                #     getData["candidate_company_location_arabic"] =  str(translator.translator_en_ar(getData["candidate_company_location"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_company_location_arabic"] =  getData["candidate_company_location"]
                #     getData["candidate_company_location"] =  str(translator.translator_en_ar(getData["candidate_company_location"], "ar", "en")["translated_text"])

                # if is_english(str(getData["candidate_job_description"])):
                #     getData["candidate_job_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_job_description"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_job_description_arabic"] =  getData["candidate_job_description"]
                #     getData["candidate_job_description"] =  str(translator.translator_en_ar(getData["candidate_job_description"], "ar", "en")["translated_text"])


                serializer = CandidateMainExperienceSerializer(data=getData)
                if serializer.is_valid():
                    serializer.save(candidate_resume_main_experience_id = uniqueID)
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "User main experience is Added",
                        "Data": {
                            "candidate_resume_main_experience_id": uniqueID,
                            "user_id": getData["user_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class CandidateMainExperienceUpdateAPI(APIView):
    '''
        Candidate main experience(update)
        Request : patch
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_resume_main_experience_id": "BroaderAI_main_experience_x5b7xfxl20hqecb",
            "candidate_job_position_id": "BroaderAI_job_position_lnsccajmh3xd2lx",
            "candidate_work_place_id": "BroaderAI_Work_Place_2yysiw35atttkkw",
            "candidate_company_name": "broader ai",
            "candidate_job_level_id": "BroaderAI_job_level_uw7k9m2y7rx6rbj",
            "candidate_company_location": "surat",
            "candidate_job_start_year": "2022",
            "candidate_job_end_year": "2023",
            "candidate_job_description":"chatgpt"
        }
    '''
    def patch(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                if CandidateMainExperienceModel.objects.filter(user_id= getData["user_id"], candidate_resume_main_experience_id= getData["candidate_resume_main_experience_id"]).exists():

                    getData["candidate_company_name_arabic"] = "Not Translated"
                    getData["candidate_company_location_arabic"] = "Not Translated"
                    getData["candidate_job_description_arabic"] = "Not Translated"

                    
                    # if is_english(str(getData["candidate_company_name"])):
                    #     getData["candidate_company_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_company_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_company_name_arabic"] =  getData["candidate_company_name"]
                    #     getData["candidate_company_name"] =  str(translator.translator_en_ar(getData["candidate_company_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_company_location"])):
                    #     getData["candidate_company_location_arabic"] =  str(translator.translator_en_ar(getData["candidate_company_location"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_company_location_arabic"] =  getData["candidate_company_location"]
                    #     getData["candidate_company_location"] =  str(translator.translator_en_ar(getData["candidate_company_location"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_job_description"])):
                    #     getData["candidate_job_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_job_description"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_job_description_arabic"] =  getData["candidate_job_description"]
                    #     getData["candidate_job_description"] =  str(translator.translator_en_ar(getData["candidate_job_description"], "ar", "en")["translated_text"])


                    CandidateMainExperienceModel.objects.filter(
                        user_id= getData["user_id"], candidate_resume_main_experience_id= getData["candidate_resume_main_experience_id"]
                    ).update(
                        candidate_resume_main_experience_id = getData['candidate_resume_main_experience_id'],
                        candidate_job_position_id = getData['candidate_job_position_id'],
                        candidate_work_place_id = getData['candidate_work_place_id'] ,
                        candidate_company_name = getData['candidate_company_name'],
                        candidate_company_name_arabic = getData['candidate_company_name_arabic'],
                        candidate_job_level_id = getData['candidate_job_level_id'] ,
                        candidate_company_location = getData['candidate_company_location'],
                        candidate_company_location_arabic = getData['candidate_company_location_arabic'],
                        candidate_job_start_year = getData['candidate_job_start_year'],
                        candidate_job_end_year = getData['candidate_job_end_year'],
                        candidate_job_description = getData['candidate_job_description'],
                        candidate_job_description_arabic = getData['candidate_job_description_arabic']
                    )
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Candidate main experience details are updated.",
                        "Data": {
                            "candidate_resume_main_experience_id": getData["candidate_resume_main_experience_id"],
                            "user_id": getData["user_id"]
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Candidate main experience details are not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceGetAPI(APIView):
    '''
        Candidate main experience API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateMainExperienceModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])
                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateMainExperienceModel.objects.filter(user_id=getData["user_id"]).values()
                    # candidatetechnicalskill = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_main_experience_id=getData["candidate_resume_main_experience_id"]).values()
                    candidateExp = []
                    for exp in candidateDetail:
                        techkillExp = CandidateMainExperienceTechnicalSkillsModel.objects.filter(candidate_main_experience = exp["candidate_resume_main_experience_id"]).values()
                        tech = ""
                        techdata = dict()
                        for techskill in techkillExp:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = str(techskill["candidate_technical_skill_name"])
                        tech = tech[:-3]
                        candidateExp.append(
                            {
                                "candidate_resume_main_experience_id" : exp["candidate_resume_main_experience_id"],
                                "user_id" : exp["user_id"],
                                "candidate_job_position_id": exp["candidate_job_position_id"],
                                "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = exp["candidate_job_position_id"]).job_position_name,
                                "candidate_job_position_name_arabic": JobPositionModel.objects.get(job_position_id = exp["candidate_job_position_id"]).job_position_name_arabic,
                                "candidate_job_level_id": exp["candidate_job_level_id"],
                                "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = exp["candidate_job_level_id"]).job_level_name,
                                "candidate_job_level_name_arabic": JobLevelModel.objects.get(job_level_id = exp["candidate_job_level_id"]).job_level_name_arabic,
                                "candidate_work_place_id": exp["candidate_work_place_id"],
                                "candidate_work_place_name": WorkPlaceModel.objects.get(work_place_id = exp["candidate_work_place_id"]).work_place_name,
                                "candidate_work_place_name_arabic": WorkPlaceModel.objects.get(work_place_id = exp["candidate_work_place_id"]).work_place_name_arabic,
                                "candidate_company_name": exp["candidate_company_name"],
                                "candidate_company_name_arabic": exp["candidate_company_name_arabic"],

                                "candidate_company_location": exp["candidate_company_location"],
                                "candidate_company_location_arabic": exp["candidate_company_location_arabic"],

                                "candidate_job_start_year": exp["candidate_job_start_year"],
                                "candidate_job_end_year": exp["candidate_job_end_year"],
                                "candidate_job_description": exp["candidate_job_description"],
                                "candidate_job_description_arabic": exp["candidate_job_description_arabic"],

                                "candidate_technical_skills": tech,
                                "candidate_all_tech": techdata
                            }
                        )
                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate main experience Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate main experience details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceGetOneAPI(APIView):
    '''
        Candidate main experience API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_main_experience_id": "BroaderAI_main_experience_1ufaa9ab5n65z39"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateMainExperienceModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateMainExperienceModel.objects.filter( user_id=getData["user_id"], candidate_resume_main_experience_id=getData["candidate_resume_main_experience_id"]).exists(): 

                        candidateDetail = CandidateMainExperienceModel.objects.filter(user_id=getData["user_id"], candidate_resume_main_experience_id=getData["candidate_resume_main_experience_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate main experience Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and main experience not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate main experience details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceDeleteAPI(APIView):
    '''
        main experience API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_main_experience_id": "BroaderAI_main_experience_x5b7xfxl20hqecb"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateMainExperienceModel.objects.filter(candidate_resume_main_experience_id = getData["candidate_resume_main_experience_id"]).exists():
                    candidateDetail = CandidateMainExperienceModel.objects.get(candidate_resume_main_experience_id = getData["candidate_resume_main_experience_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Main Experience is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Main Experience data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]



#####################################################

#  main experience APIs (End)

####################################################

#####################################################

#   Main Experience technical skills APIs (Start)

####################################################

# class CandidateMainExperienceTechnicalSkillsRegisterAPI(APIView):
#     '''
#         Candidate main experience technical skill(Insert)
#         Request : post
#         Data = {
#             "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
#             "candidate_main_experience_id": "BroaderAI_main_experience_1ufaa9ab5n65z39",
#             "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y",
#             "candidate_job_position_id": "BroaderAI_job_position_lnsccajmh3xd2lx",
#             "candidate_job_level_id": "BroaderAI_job_level_8ydq84moef0ad6p"
#         }
#     '''
    
#     def post(self, request ,formate=None):
        
#         getData = request.data

#         if NewUser.objects.filter(id=getData["user_id"]).exists():
        
#             user = NewUser.objects.get(id=getData["user_id"])
        
#             if user.user_is_loggedin and user.user_is_verified: 

                
#                 randomstr = ''.join(random.choices(string.ascii_lowercase +
#                                     string.digits, k=15))

#                 uniqueID = "BroaderAI_main_experience_technical_skill" + randomstr
#                 # getData["candidate_resume_main_experience_technical_skill_id"] = uniqueID

#                 if TechnicalSkillsModel.objects.filter(technical_skills_id= getData['candidate_technical_skill_id']).exists():
#                     getData['candidate_technical_skill_name']=TechnicalSkillsModel.objects.get(technical_skills_id= getData['candidate_technical_skill_id']).technical_skills_name
                
#                     serializer = CandidateMainExperienceTechnicalSkillsSerializer(data=getData)
#                     if serializer.is_valid():
                        
#                         serializer.save(candidate_resume_main_experience_technical_skill_id = uniqueID)
#                         res = {
                            # "Status": "success",
                            # "Code": 201,
#                             "Message": "User main experience technical skill is Added",
#                             "Data": {
#                                 "candidate_resume_main_experience_technical_skill_id":uniqueID ,
#                                 "user_id": getData["user_id"]
#                             }
#                         }
#                         return Response(res, status=status.HTTP_201_CREATED)
                    
#                     else:
                            # res = {"Status": "error",
                            #     "Code": 400,
                            #     "Message": list(serializer.errors.values())[0][0], 
                            #     "Data":[],
                            # }
#                         return Response(res, status=status.HTTP_201_CREATED)

#                 else:
#                     res = {
#                   "Status": "error",
                    # "Code": 401,
                    # "Message": "Technical Skill is not valid"
                    # "Data":[],}
#                     return Response(res, status=status.HTTP_201_CREATED)
                
#             else:
#                 res = {
# "Status": "error",
                # "Code": 401,
                # "Message": "You are not logged in",
                # "Data":[],
                # }
#                 return Response(res, status=status.HTTP_201_CREATED)
        
#         else:
#             res = {
# "Status": "error",
                # "Code": 401,
                # "Message": "User is not found",
                # "Data":[],
                # }
#             return Response(res, status=status.HTTP_201_CREATED) 

#     # authentication_classes=[JWTAuthentication]
#     # permission_classes=[IsAuthenticated]


class CandidateMainExperienceTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate main experience technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_main_experience_id": "BroaderAI_main_experience_1ufaa9ab5n65z39",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y",
            "candidate_job_position_id": "BroaderAI_job_position_lnsccajmh3xd2lx",
            "candidate_job_level_id": "BroaderAI_job_level_8ydq84moef0ad6p"
        }
    '''
    def post(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_main_experience_technical_skill" + randomstr
                # getData["candidate_resume_main_experience_technical_skill_id"] = uniqueID
                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     c =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])

                    serializer = CandidateMainExperienceTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        serializer.save(candidate_resume_main_experience_technical_skill_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User main experience technical skill is Added",
                            "Data": {
                                "candidate_resume_main_experience_technical_skill_id":uniqueID ,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceTechnicalSkillsGetAPI(APIView):
    '''
        Candidate main experience technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate main experience Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate main experience details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate main experience technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_main_experience_id": "BroaderAI_main_experience_1ufaa9ab5n65z39"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateMainExperienceTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_main_experience_id=getData["candidate_main_experience_id"]).exists(): 

                        candidateDetail = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_main_experience_id=getData["candidate_main_experience_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate main experience technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and main experience technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate main experience technical skill is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceTechnicalSkillsDeleteAPI(APIView):
    '''
        main experience API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_main_experience_technical_skill_id": "BroaderAI_main_experience_technical_skill61xgjg0ykjqem8r"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateMainExperienceTechnicalSkillsModel.objects.filter(candidate_resume_main_experience_technical_skill_id = getData["candidate_resume_main_experience_technical_skill_id"]).exists():
                    candidateDetail = CandidateMainExperienceTechnicalSkillsModel.objects.get(candidate_resume_main_experience_technical_skill_id = getData["candidate_resume_main_experience_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Main Experience technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Main Experience technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceGetOneAllDetailsAPI(APIView):

    '''
        Candidate main experience API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_main_experience_id": "BroaderAI_main_experience_1ufaa9ab5n65z39"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateMainExperienceModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateMainExperienceModel.objects.filter( user_id=getData["user_id"], candidate_resume_main_experience_id=getData["candidate_resume_main_experience_id"]).exists(): 

                        candidateDetail = CandidateMainExperienceModel.objects.get(user_id=getData["user_id"], candidate_resume_main_experience_id=getData["candidate_resume_main_experience_id"])

                        candidatetechnicalskill = CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_main_experience_id=getData["candidate_resume_main_experience_id"]).values()



                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate main experience Details",
                                "Data": {
                                    "candidate_resume_main_experience_id" : getData['candidate_resume_main_experience_id'],
                                    "user_id" : getData['user_id'],
                                    "candidate_job_position_id" :  candidateDetail.candidate_job_position_id,
                                    "candidate_job_position_name" : candidateDetail.candidate_job_position.job_position_name,
                                    "candidate_job_position_name_arabic" : candidateDetail.candidate_job_position.job_position_name_arabic,
                                    "candidate_work_place_id" : candidateDetail.candidate_work_place_id,
                                    "candidate_work_place_name" : candidateDetail.candidate_work_place.work_place_name,
                                    "candidate_work_place_name_arabic" : candidateDetail.candidate_work_place.work_place_name_arabic,
                                    "candidate_company_name" : candidateDetail.candidate_company_name,
                                    "candidate_company_name_arabic" : candidateDetail.candidate_company_name_arabic,
                                    "candidate_job_level_id" : candidateDetail.candidate_job_level_id ,
                                    "candidate_job_level_name" : candidateDetail.candidate_job_level.job_level_name,
                                    "candidate_job_level_name_arabic" : candidateDetail.candidate_job_level.job_level_name_arabic,
                                    "candidate_company_location" : candidateDetail.candidate_company_location,
                                    "candidate_company_location_arabic" : candidateDetail.candidate_company_location_arabic,
                                    "candidate_job_start_year" : candidateDetail.candidate_job_start_year,
                                    "candidate_job_end_year" : candidateDetail.candidate_job_end_year,
                                    "candidate_job_description" : candidateDetail.candidate_job_description,
                                    "candidate_job_description_arabic" : candidateDetail.candidate_job_description_arabic,
                                    "candidate_technical_skills" : candidatetechnicalskill

                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and main experience not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate main experience details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateMainExperienceTechnicalSkillsAllDeleteAPI(APIView):
    '''
        main experience API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_main_experience_id": "BroaderAI_main_experience_technical_skill61xgjg0ykjqem8r"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                if CandidateMainExperienceTechnicalSkillsModel.objects.filter(candidate_main_experience_id = getData["candidate_resume_main_experience_id"]).exists():
                    candidateDetail = CandidateMainExperienceTechnicalSkillsModel.objects.filter(candidate_main_experience_id = getData["candidate_resume_main_experience_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Main Experience technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Main Experience technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  main experience technical skills APIs (End)

####################################################

#####################################################

#   technical skills APIs (Start)

####################################################

class CandidateTechnicalskillsAPI(APIView):
    '''
            candidate technical skill 
            request : Post
            data = {
                    
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y",  
                    "candidate_technical_skill_level" : "advance" 
                    }
                
    '''
    def post(self, request ,formate=None):
        
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                if not CandidateTechnicalskillsModel.objects.filter(candidate_technical_skill_id=getData["candidate_technical_skill_id"],user_id=getData["user_id"]).exists():

                    if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():

                        getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

                        uniqueID = "BroaderAI_candidate_resume_Technical_skill_" + randomstr
                        # getData["candidate_resume_technical_skills_id"] = uniqueID

                        getData["candidate_technical_skill_name_arabic"] = "Not Translated"
                        getData["candidate_technical_skill_level_arabic"] = "Not Translated"

                        # if is_english(str(getData["candidate_technical_skill_name"])):
                        #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                        #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])

                        # if is_english(str(getData["candidate_technical_skill_level"])):
                        #     getData["candidate_technical_skill_level_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_level"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_technical_skill_level_arabic"] =  getData["candidate_technical_skill_level"]
                        #     getData["candidate_technical_skill_level"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_level"], "ar", "en")["translated_text"])
                        
                        serializer = CandidateTechnicalskillserializer(data=getData)
                        
                        if serializer.is_valid():
                            
                            serializer.save(candidate_resume_technical_skills_id= uniqueID)
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Technical skills Details is Added",
                                "Data": {   
                                    "candidate_resume_technical_skills_id" : uniqueID,
                                    "user_id": getData["user_id"] 
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message": "Technical Skill already exists by this user",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateTechnicalskillsGetAPI(APIView):
    '''
        Candidate technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateTechnicalskillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])


                if user.user_is_loggedin and user.user_is_verified:
                    
                    candidateDetail = CandidateTechnicalskillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate technical skills Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate technical skills details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateTechnicalskillsDeleteAPI(APIView):
    '''
        Technical skill API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_technical_skill_id": "BroaderAI_candidate_resume_Technical_skill_0pod2iv5dkl6pqr"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                if CandidateTechnicalskillsModel.objects.filter(candidate_technical_skill_id = getData["candidate_technical_skill_id"]).exists():
                    candidateDetail = CandidateTechnicalskillsModel.objects.get(candidate_technical_skill_id = getData["candidate_technical_skill_id"], user_id = getData["user_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateTechnicalskillsAllDeleteAPI(APIView):
    '''
        Technical skill API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                candidateDetail = CandidateTechnicalskillsModel.objects.filter(user_id = getData["user_id"])
                candidateDetail.delete()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "technical skill is successfully Deleted",
                        "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  technical skills APIs (End)

####################################################

#####################################################

#   soft skills APIs (Start)

####################################################

class CandidateSoftskillsAPI(APIView):
    '''
            candidate soft skill 
            request : Post
            data = {
                    
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_soft_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y",  
                    "candidate_technical_skill_level" : "advance" 
                    }
                
    '''
    def post(self, request ,formate=None):
        
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                if not CandidateSoftskillsModel.objects.filter(candidate_soft_skill_id=getData["candidate_soft_skill_id"],user_id=getData["user_id"]).exists():

                    if SoftSkillsModel.objects.filter(soft_skills_id= getData['candidate_soft_skill_id']).exists():

                        getData['candidate_soft_skill_name']=SoftSkillsModel.objects.get(soft_skills_id= getData['candidate_soft_skill_id']).soft_skills_name

                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

                        uniqueID = "BroaderAI_candidate_resume_Soft_skill_" + randomstr
                        # getData["candidate_resume_soft_skills_id"] = uniqueID

                        getData["candidate_soft_skill_name_arabic"] = "Not Translated"
                        getData["candidate_soft_skill_level_arabic"] = "Not Translated"

                        # if is_english(str(getData["candidate_soft_skill_name"])):
                        #     getData["candidate_soft_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_soft_skill_name"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_soft_skill_name_arabic"] =  getData["candidate_soft_skill_name"]
                        #     getData["candidate_soft_skill_name"] =  str(translator.translator_en_ar(getData["candidate_soft_skill_name"], "ar", "en")["translated_text"])

                        # if is_english(str(getData["candidate_soft_skill_level"])):
                        #     getData["candidate_soft_skill_level_arabic"] =  str(translator.translator_en_ar(getData["candidate_soft_skill_level"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_soft_skill_level_arabic"] =  getData["candidate_soft_skill_level"]
                        #     getData["candidate_soft_skill_level"] =  str(translator.translator_en_ar(getData["candidate_soft_skill_level"], "ar", "en")["translated_text"])
                        
                        serializer = CandidateSoftskillserializer(data=getData)
                        
                        if serializer.is_valid():
                            
                            serializer.save(candidate_resume_soft_skills_id = uniqueID)
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate soft skills Details is Added",
                                "Data": {   
                                    "candidate_resume_soft_skills_id" : uniqueID,
                                    "user_id": getData["user_id"] 
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Soft skill already exists by this user",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSoftskillsGetAPI(APIView):
    '''
        Candidate soft skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateSoftskillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])


                if user.user_is_loggedin and user.user_is_verified:
                    
                    candidateDetail = CandidateSoftskillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate soft skills Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate soft skills details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSoftskillsDeleteAPI(APIView):
    '''
        soft skill API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_soft_skill_id": "BroaderAI_candidate_resume_Soft_skill_i3qfqfkze2x6o7n"
                }
    '''
    def delete(self, request, format=None):
    
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                if CandidateSoftskillsModel.objects.filter(candidate_soft_skill_id = getData["candidate_soft_skill_id"], user_id = getData["user_id"]).exists():
                    candidateDetail = CandidateSoftskillsModel.objects.get(candidate_soft_skill_id = getData["candidate_soft_skill_id"], user_id = getData["user_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "soft skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "soft skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  soft skills APIs (End)

####################################################

#####################################################

#   language APIs (Start)

####################################################

class CandidateLanguageRegisterAPI(APIView):
    '''
            candidate soft skill 
            request : Post
            data = {
                    
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_language_id": "BroaderAI_language_ktwsx4do785vo4y",  
                    "candidate_language_level" : "advance" 
                    }
                
    '''
    def post(self, request ,formate=None):
        
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                if not CandidateLanguageModel.objects.filter(candidate_language_id=getData["candidate_language_id"],user_id=getData["user_id"]).exists():

                    if LanguageModel.objects.filter(language_id = getData['candidate_language_id']).exists():

                        getData['candidate_language_name']=LanguageModel.objects.get(language_id= getData['candidate_language_id']).language_name

                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

                        uniqueID = "BroaderAI_candidate_resume_language_" + randomstr

                        getData["candidate_language_name_arabic"] = "Not Translated"
                        getData["candidate_language_level_arabic"] = "Not Translated"

                        # if is_english(str(getData["candidate_language_name"])):
                        #     getData["candidate_language_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_language_name"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_language_name_arabic"] =  getData["candidate_language_name"]
                        #     getData["candidate_language_name"] =  str(translator.translator_en_ar(getData["candidate_language_name"], "ar", "en")["translated_text"])

                        # if is_english(str(getData["candidate_language_level"])):
                        #     getData["candidate_language_level_arabic"] =  str(translator.translator_en_ar(getData["candidate_language_level"], "en", "ar")["translated_text"])

                        # else:
                        #     getData["candidate_language_level_arabic"] =  getData["candidate_language_level"]
                        #     getData["candidate_language_level"] =  str(translator.translator_en_ar(getData["candidate_language_level"], "ar", "en")["translated_text"])
                        
                        serializer = CandidateLanguageserializer(data=getData)
                        
                        if serializer.is_valid():
                            
                            serializer.save(candidate_resume_language_id = uniqueID)
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate language Details is Added",
                                "Data": {   
                                    "candidate_resume_language_id" : uniqueID,
                                    "user_id": getData["user_id"] 
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "language already exists by this user",
                        "Data":[],}
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateLanguageGetAPI(APIView):
    '''
        Candidate language API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateLanguageModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])


                if user.user_is_loggedin and user.user_is_verified:
                    
                    candidateDetail = CandidateLanguageModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate languages Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate languages details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateLanguageDeleteAPI(APIView):
    '''
        language API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_language_id": "BroaderAI_candidate_resume_language_i3qfqfkze2x6o7n"
                }
    '''
    def delete(self, request, format=None):
 
        getData = request.data
        
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                if CandidateLanguageModel.objects.filter(candidate_language_id = getData["candidate_language_id"], user_id = getData["user_id"]).exists():
                    candidateDetail = CandidateLanguageModel.objects.get(candidate_language_id = getData["candidate_language_id"], user_id = getData["user_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "language is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "language data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
  
#####################################################

#  language APIs (End)

####################################################

#####################################################

#   project APIs (Start)

####################################################

class CandidateProjectAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_project_name
        Value : amazon analysis
        
        Key : candidate_project_start_date
        Value : 5/10/22

        Key : candidate_project_end_date
        Value : 12/12/22

        Key : candidate_project_url
        Value : https://www.merriam-webster.com/dictionary/project

        Key : candidate_resumeUpload
        Value : Files upload....

        Key : candidate_project_description
        Value : created in power bi
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_project_" + randomstr
                

                getData["candidate_project_name_arabic"] = "Not Translated"
                getData["candidate_project_description_arabic"] = "Not Translated"

                # if is_english(str(getData["candidate_project_name"])):
                #     getData["candidate_project_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_project_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_project_name_arabic"] =  getData["candidate_project_name"]
                #     getData["candidate_project_name"] =  str(translator.translator_en_ar(getData["candidate_project_name"], "ar", "en")["translated_text"])

                # if is_english(str(getData["candidate_project_description"])):
                #     getData["candidate_project_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_project_description"], "en", "ar")["translated_text"])

                # else:
                    # getData["candidate_project_description_arabic"] =  getData["candidate_project_description"]
                    # getData["candidate_project_description"] =  str(translator.translator_en_ar(getData["candidate_project_description_arabic"], "ar", "en")["translated_text"])

                

                # if detect_language(str(getData["candidate_project_name"])) == "en":
                #     getData["candidate_project_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_project_name"], "en", "ar")["translated_text"])
             

                serializer = CandidateProjectSerializer(data=getData)
            
                if serializer.is_valid():

                    serializer.save(candidate_resume_project_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Project is successfully uploaded",
                        "Data": {
                            "candidate_resume_project_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_resume_project_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_project_name
        Value : amazon analysis
        
        Key : candidate_project_start_date
        Value : 5/10/22

        Key : candidate_project_end_date
        Value : 12/12/22

        Key : candidate_project_url
        Value : https://www.merriam-webster.com/dictionary/project

        Key : candidate_resumeUpload
        Value : Files upload....

        Key : candidate_project_description
        Value : created in power bi
        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateProjectModel.objects.filter(user_id = getData["user_id"], candidate_resume_project_id= getData["candidate_resume_project_id"]).exists():

                    getData["candidate_project_name_arabic"] = "Not Translated"
                    getData["candidate_project_description_arabic"] = "Not Translated"
                    
                    # if is_english(str(getData["candidate_project_name"])):
                    #     getData["candidate_project_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_project_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_project_name_arabic"] =  getData["candidate_project_name"]
                    #     getData["candidate_project_name"] =  str(translator.translator_en_ar(getData["candidate_project_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_project_description"])):
                    #     getData["candidate_project_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_project_description"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_project_description_arabic"] =  getData["candidate_project_description"]
                    #     getData["candidate_project_description"] =  str(translator.translator_en_ar(getData["candidate_project_description_arabic"], "ar", "en")["translated_text"])


                    serializer = CandidateProjectSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidateProjectModel.objects.get(user_id = getData["user_id"], candidate_resume_project_id= getData["candidate_resume_project_id"])

                        latestResume = request.FILES.get('candidate_resumeUpload')

                        if latestResume:

                            if userUpload.candidate_resumeUpload:
                                userUpload.candidate_resumeUpload.delete()

                            userUpload.candidate_resumeUpload = latestResume


                        userUpload.candidate_project_name = getData["candidate_project_name"]
                        userUpload.candidate_project_name_arabic = getData["candidate_project_name_arabic"]
                        userUpload.candidate_project_start_date = getData["candidate_project_start_date"]
                        userUpload.candidate_project_end_date = getData["candidate_project_end_date"]
                        userUpload.candidate_project_url = getData["candidate_project_url"]
                        userUpload.candidate_project_description = getData["candidate_project_description"]
                        userUpload.candidate_project_description_arabic = getData["candidate_project_description_arabic"]

                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Resume is successfully uploaded",
                            "Data": {
                                "candidate_resume_project_id" : getData["candidate_resume_project_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_resume_project_id
        Value : BroaderAI_resume_project_xe8qjoryb0hen6p
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateProjectModel.objects.filter(user_id = getData["user_id"], candidate_resume_project_id= getData["candidate_resume_project_id"]).exists():

                    userUpload = CandidateProjectModel.objects.get(user_id = getData["user_id"], candidate_resume_project_id= getData["candidate_resume_project_id"])

                    
                    if userUpload.candidate_resumeUpload:
                        userUpload.candidate_resumeUpload.delete()

                    userUpload.candidate_resumeUpload = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Project Media is deleted",
                        "Data": {
                            "candidate_resume_project_id" : getData["candidate_resume_project_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_resume_project_id
        Value : BroaderAI_resume_project_xe8qjoryb0hen6p


        Key : candidate_resumeUpload
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateProjectModel.objects.filter(user_id = getData["user_id"], candidate_resume_project_id= getData["candidate_resume_project_id"]).exists():

                
                    userUpload = CandidateProjectModel.objects.get(user_id = getData["user_id"], candidate_resume_project_id= getData["candidate_resume_project_id"])

                    latestResume = request.FILES.get('candidate_resumeUpload')

                    if latestResume:

                        if userUpload.candidate_resumeUpload:
                            userUpload.candidate_resumeUpload.delete()

                        userUpload.candidate_resumeUpload = latestResume

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Media is not uploaded",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)



                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_project_id" : getData["candidate_resume_project_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectGetOneAPI(APIView):
    '''
        Candidate projects  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_project_id": "BroaderAI_resume_project_3z6ht1qspmbmlmm"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateProjectModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateProjectModel.objects.filter( user_id=getData["user_id"], candidate_resume_project_id=getData["candidate_resume_project_id"]).exists(): 

                        candidateDetail = CandidateProjectModel.objects.filter(user_id=getData["user_id"], candidate_resume_project_id=getData["candidate_resume_project_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate projects Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and projects not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate projects  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectGetAPI(APIView):
    '''
        Candidate project API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateProjectModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])
                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateProjectModel.objects.filter(user_id=getData["user_id"]).values()
                    candidateProTech = []
                    for techdata_ in candidateDetail:
                        techkillProj = CandidateProjectTechnicalSkillsModel.objects.filter(candidate_project_id = techdata_["candidate_resume_project_id"]).values()
                        tech = ""
                        techdata = dict()
                        for techskill in techkillProj:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = {
                                "candidate_technical_skill_name": str(techskill["candidate_technical_skill_name"]),
                                # "candidate_job_position_id":  techskill["candidate_job_position_id"],
                                # "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = techskill["candidate_job_position_id"]).job_position_name,
                                # "candidate_job_level_id": techskill["candidate_job_level_id"],
                                # "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = techskill["candidate_job_level_id"]).job_level_name,
                            }
                        tech = tech[:-3]
                        candidateProTech.append(
                        {
                            "candidate_resume_project_id" : techdata_["candidate_resume_project_id"],
                            "user_id" : techdata_["user_id"],
                            "candidate_project_name": techdata_["candidate_project_name"],
                            "candidate_project_name_arabic":techdata_["candidate_project_name_arabic"],
                            "candidate_project_start_date": techdata_["candidate_project_start_date"],
                            "candidate_project_start_date_arabic":techdata_["candidate_project_start_date_arabic"],
                            "candidate_project_end_date": techdata_["candidate_project_end_date"],
                            "candidate_project_end_date_arabic":techdata_["candidate_project_end_date_arabic"],
                            "candidate_project_url": techdata_["candidate_project_url"],
                            "candidate_resumeUpload": techdata_["candidate_resumeUpload"],
                            "candidate_project_description" : techdata_["candidate_project_description"],
                            "candidate_project_description_arabic" : techdata_["candidate_project_description_arabic"],
                            "candidate_technical_skills": tech,
                            "candidate_all_tech": techdata
                        })
                    if candidateDetail:
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate projects Details",
                            "Data": candidateProTech
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate projects details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectDeleteAPI(APIView):
    '''
        Project API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_project_id": "BroaderAI_resume_project_3z6ht1qspmbmlmm"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateProjectModel.objects.filter(candidate_resume_project_id = getData["candidate_resume_project_id"]).exists():
                    candidateDetail = CandidateProjectModel.objects.get(candidate_resume_project_id = getData["candidate_resume_project_id"])
                    
                    if candidateDetail.candidate_resumeUpload:
                        candidateDetail.candidate_resumeUpload.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Project is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Project data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  project APIs (End)

####################################################

#####################################################

#  project technical skills  APIs (Start)

####################################################

# class CandidateProjectTechnicalSkillsRegisterAPI(APIView):
#     '''
#         Candidate project technical skill(Insert)
#         Request : post
#         Data = {
#             "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
#             "candidate_project_id": "BroaderAI_resume_project_8ykvlf9e821kyvd",
#             "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y",
#             "candidate_job_position_id": "BroaderAI_job_position_lnsccajmh3xd2lx",
#             "candidate_job_level_id": "BroaderAI_job_level_8ydq84moef0ad6p"
#         }
#     '''
    
#     def post(self, request ,formate=None):
        
#         getData = request.data

#         if NewUser.objects.filter(id=getData["user_id"]).exists():
        
#             user = NewUser.objects.get(id=getData["user_id"])
        
#             if user.user_is_loggedin and user.user_is_verified: 

                
#                 randomstr = ''.join(random.choices(string.ascii_lowercase +
#                                     string.digits, k=15))

#                 uniqueID = "BroaderAI_project_technical_skill" + randomstr
#                 # getData["candidate_resume_project_technical_skill_id"] = uniqueID

#                 if TechnicalSkillsModel.objects.filter(technical_skills_id= getData['candidate_technical_skill_id']).exists():
#                     getData['candidate_technical_skill_name']=TechnicalSkillsModel.objects.get(technical_skills_id= getData['candidate_technical_skill_id']).technical_skills_name
                
#                     serializer = CandidateProjectTechnicalSkillsSerializer(data=getData)
#                     if serializer.is_valid():
                        
#                         serializer.save(candidate_resume_project_technical_skill_id = uniqueID)
#                         res = {
                            # "Status": "success",
                            # "Code": 201,
#                             "Message": "User project technical skill is Added",
#                             "Data": {
#                                 "candidate_resume_project_technical_skill_id": uniqueID,
#                                 "user_id": getData["user_id"]
#                             }
#                         }
#                         return Response(res, status=status.HTTP_201_CREATED)
                    
#                     else:
                        # res = {"Status": "error",
                #                 "Code": 400,
                #                 "Message": list(serializer.errors.values())[0][0], 
                #                 "Data":[],
                #             }
#                         return Response(res, status=status.HTTP_201_CREATED)

#                 else:
#                     res = {
# "Status": "error",
                    # "Code": 401,
                    # "Message": "Technical Skill is not valid",
                    # "Data":[],
                    # }
#                     return Response(res, status=status.HTTP_201_CREATED)
                
#             else:
#                 res = {
# "Status": "error",
                    # "Code": 401,
                    # "Message": "You are not logged in",
                    # "Data":[],
                    # }
#                 return Response(res, status=status.HTTP_201_CREATED)
        
#         else:
#             res = {
# "Status": "error",
                    # "Code": 401,
                    # "Message": "User is not found",
                    # "Data":[],
                    # }
#             return Response(res, status=status.HTTP_201_CREATED) 

#     # authentication_classes=[JWTAuthentication]
#     # permission_classes=[IsAuthenticated]


class CandidateProjectTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate project technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
            "candidate_project_id": "BroaderAI_resume_project_8ykvlf9e821kyvd",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y"
        }
    '''

    def post(self, request ,formate=None):
        getData = request.data
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_project_technical_skill" + randomstr
                # getData["candidate_resume_project_technical_skill_id"] = uniqueID
                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])

                    serializer = CandidateProjectTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        serializer.save(candidate_resume_project_technical_skill_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User project technical skill is Added",
                            "Data": {
                                "candidate_resume_project_technical_skill_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class CandidateProjectTechnicalSkillsGetAPI(APIView):
    '''
        Candidate project technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateProjectTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateProjectTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate project Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate project details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate project technical skill API(view)
        Request : Post
        Data = {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_project_id": "BroaderAI_resume_project_8ykvlf9e821kyvd"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateProjectTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateProjectTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_project_id=getData["candidate_project_id"]).exists(): 

                        candidateDetail = CandidateProjectTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_project_id=getData["candidate_project_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate project technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and project technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate project technical skill is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectTechnicalSkillsDeleteAPI(APIView):
    '''
        Project API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_project_technical_skill_id": "BroaderAI_resume_project_8ykvlf9e821kyvd"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateProjectTechnicalSkillsModel.objects.filter(candidate_resume_project_technical_skill_id = getData["candidate_resume_project_technical_skill_id"]).exists():
                    candidateDetail = CandidateProjectTechnicalSkillsModel.objects.get(candidate_resume_project_technical_skill_id = getData["candidate_resume_project_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Project technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Project technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectGetOneAllDetailsAPI(APIView):

    '''
        Candidate project API(view)
        Request : Post
        Data =  {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_project_id": "BroaderAI_resume_project_8ykvlf9e821kyvd"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateProjectModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateProjectModel.objects.filter( user_id=getData["user_id"], candidate_resume_project_id=getData["candidate_resume_project_id"]).exists(): 

                        candidateDetail = CandidateProjectModel.objects.get(user_id=getData["user_id"], candidate_resume_project_id=getData["candidate_resume_project_id"])

                        candidatetechnicalskill = CandidateProjectTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_project_id=getData["candidate_resume_project_id"]).values()

                        # if TechnicalSkillsModel.objects.filter(technical_skills_id= getData['candidate_technical_skill_id']).exists():
                        #     techname=TechnicalSkillsModel.objects.get(technical_skills_id= getData['candidate_technical_skill_id']).technical_skills_name


                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate project Details",
                                "Data": {
                                    "candidate_resume_project_id" : getData['candidate_resume_project_id'],
                                    "user_id" : getData['user_id'],
                                    # "candidate_job_position_id" :  techname.candidate_job_position_id,
                                    # "candidate_job_position_name" : techname.candidate_job_position.job_position_name,
                                    "candidate_project_name" : candidateDetail.candidate_project_name,
                                    "candidate_project_name_arabic" : candidateDetail.candidate_project_name_arabic,
                                    # "candidate_job_level_id" : candidateDetail.candidate_job_level_id ,
                                    # "candidate_job_level_name" : candidateDetail.candidate_job_level.job_level_name,
                                    "candidate_project_start_date" : candidateDetail.candidate_project_start_date,
                                    "candidate_project_end_date" : candidateDetail.candidate_project_end_date,
                                    "candidate_project_url" : candidateDetail.candidate_project_url,
                                    "candidate_project_description" : candidateDetail.candidate_project_description,
                                    "candidate_project_description_arabic" : candidateDetail.candidate_project_description_arabic,
                                    "candidate_technical_skills" : candidatetechnicalskill

                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and project not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate project details is not found", 
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateProjectTechnicalSkillsAllDeleteAPI(APIView):
    '''
        Project API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_project_id": "BroaderAI_resume_project_8ykvlf9e821kyvd"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                if CandidateProjectTechnicalSkillsModel.objects.filter(candidate_project_id = getData["candidate_project_id"]).exists():
                    candidateDetail = CandidateProjectTechnicalSkillsModel.objects.filter(candidate_project_id = getData["candidate_project_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Project technical skills is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Project technical skills data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  project technical skills APIs (End)

####################################################

#####################################################

#  hackathon  APIs (Start)

####################################################
class CandidatehackathonAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_hackathon_name
        Value : amazon analysis
        
        Key : candidate_hackathon_mode
        Value : online

        Key : candidate_hackathon_organisation_name
        Value : PPSU

        Key: candidate_hackathon_certificateID
        Value : akodkeosmqkjo

        Key: candidate_hackathon_type
        Value : model

        Key: candidate_hackathon_field
        Value : python

        Key : candidate_hackathon_participate_certificate
        Value : Files upload....

        Key : candidate_hackathon_certificateURL
        Value : https://www.merriam-webster.com/dictionary/hackathon

        Key : candidate_hackathon_certificate_issue_date
        Value : 12/12/22

        Key : candidate_hackathon_description
        Value : created in power bi
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data


        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_hackathon_" + randomstr

                getData["candidate_hackathon_name_arabic"] = "Not Translated"
                getData["candidate_hackathon_mode_arabic"] = "Not Translated"
                getData["candidate_hackathon_organisation_name_arabic"] = "Not Translated"
                getData["candidate_hackathon_certificateID_arabic"] = "Not Translated"
                getData["candidate_hackathon_type_arabic"] = "Not Translated"
                getData["candidate_hackathon_field_arabic"] = "Not Translated"
                getData["candidate_hackathon_description_arabic"] = "Not Translated"

                # if is_english(str(getData["candidate_hackathon_name"])):
                #     getData["candidate_hackathon_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_hackathon_name_arabic"] =  getData["candidate_hackathon_name"]
                #     getData["candidate_hackathon_name"] =  str(translator.translator_en_ar(getData["candidate_hackathon_name"], "ar", "en")["translated_text"])

                # if str(getData["candidate_hackathon_mode"]) != "":

                #     if is_english(str(getData["candidate_hackathon_mode"])):
                #         getData["candidate_hackathon_mode_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_mode"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_hackathon_mode_arabic"] =  getData["candidate_hackathon_mode"]
                #         getData["candidate_hackathon_mode"] =  str(translator.translator_en_ar(getData["candidate_hackathon_mode"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_hackathon_mode_arabic"] = ""


                # if is_english(str(getData["candidate_hackathon_organisation_name"])):
                #     getData["candidate_hackathon_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_organisation_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_hackathon_organisation_name_arabic"] =  getData["candidate_hackathon_organisation_name"]
                #     getData["candidate_hackathon_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_hackathon_organisation_name"], "ar", "en")["translated_text"])

                # if str(getData["candidate_hackathon_certificateID"]) != "":

                #     if is_english(str(getData["candidate_hackathon_certificateID"])):
                #         getData["candidate_hackathon_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_certificateID"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_hackathon_certificateID_arabic"] =  getData["candidate_hackathon_certificateID"]
                #         getData["candidate_hackathon_certificateID"] =  str(translator.translator_en_ar(getData["candidate_hackathon_certificateID"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_hackathon_certificateID_arabic"] = ""


                
                # if str(getData["candidate_hackathon_type"]) != "":
                #     if is_english(str(getData["candidate_hackathon_type"])):
                #         getData["candidate_hackathon_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_type"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_hackathon_type_arabic"] =  getData["candidate_hackathon_type"]
                #         getData["candidate_hackathon_type"] =  str(translator.translator_en_ar(getData["candidate_hackathon_type"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_hackathon_type_arabic"] = ""


                # if str(getData["candidate_hackathon_field"]) != "":

                #     if is_english(str(getData["candidate_hackathon_field"])):
                #         getData["candidate_hackathon_field_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_field"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_hackathon_field_arabic"] =  getData["candidate_hackathon_field"]
                #         getData["candidate_hackathon_field"] =  str(translator.translator_en_ar(getData["candidate_hackathon_field"], "ar", "en")["translated_text"])                
                # else:

                #     getData["candidate_hackathon_field_arabic"] = ""



                # if str(getData["candidate_hackathon_description"]) != "":

                #     if is_english(str(getData["candidate_hackathon_description"])):
                #         getData["candidate_hackathon_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_description"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_hackathon_description_arabic"] =  getData["candidate_hackathon_description"]
                #         getData["candidate_hackathon_description"] =  str(translator.translator_en_ar(getData["candidate_hackathon_description"], "ar", "en")["translated_text"])
                
                # else:

                #     getData["candidate_hackathon_description_arabic"] = ""



                serializer = CandidatehackathonSerializer(data=getData)
            
                if serializer.is_valid():

                    if getData["candidate_hackathon_participate_certificate"] != "":
                        serializer.validated_data['candidate_hackathon_participate_certificate'] = getData["candidate_hackathon_participate_certificate"]


                    serializer.save(candidate_resume_hackathon_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "hackathon certificate is successfully uploaded",
                        "Data": {
                            "candidate_resume_hackathon_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatehackathonUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_hackathon_name
        Value : amazon analysis
        
        Key : candidate_hackathon_mode
        Value : online

        Key : candidate_hackathon_organisation_name
        Value : PPSU

        Key: candidate_hackathon_certificateID
        Value : akodkeosmqkjo

        Key: candidate_hackathon_type
        Value : model

        Key: candidate_hackathon_field
        Value : python

        Key : candidate_hackathon_participate_certificate
        Value : Files upload....

        Key : candidate_hackathon_certificateURL
        Value : https://www.merriam-webster.com/dictionary/hackathon

        Key : candidate_hackathon_certificate_issue_date
        Value : 12/12/22

        Key : candidate_hackathon_description
        Value : created in power bi

        Key : candidate_resume_hackathon_id
        Value : BroaderAI_resume_hackathon_srzwa0r2seekq7v
        
        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidatehackathonModel.objects.filter(user_id = getData["user_id"], candidate_resume_hackathon_id= getData["candidate_resume_hackathon_id"]).exists():

                    getData["candidate_hackathon_name_arabic"] = "Not Translated"
                    getData["candidate_hackathon_mode_arabic"] = "Not Translated"
                    getData["candidate_hackathon_organisation_name_arabic"] = "Not Translated"
                    getData["candidate_hackathon_certificateID_arabic"] = "Not Translated"
                    getData["candidate_hackathon_type_arabic"] = "Not Translated"
                    getData["candidate_hackathon_field_arabic"] = "Not Translated"
                    getData["candidate_hackathon_description_arabic"] = "Not Translated"


                    # if is_english(str(getData["candidate_hackathon_name"])):
                    #     getData["candidate_hackathon_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_hackathon_name_arabic"] =  getData["candidate_hackathon_name"]
                    #     getData["candidate_hackathon_name"] =  str(translator.translator_en_ar(getData["candidate_hackathon_name"], "ar", "en")["translated_text"])

                    # if getData["candidate_hackathon_mode"] != "":
                    
                    #     if is_english(str(getData["candidate_hackathon_mode"])):
                    #         getData["candidate_hackathon_mode_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_mode"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_hackathon_mode_arabic"] =  getData["candidate_hackathon_mode"]
                    #         getData["candidate_hackathon_mode"] =  str(translator.translator_en_ar(getData["candidate_hackathon_mode"], "ar", "en")["translated_text"])
                    
                    # else:

                    #     getData["candidate_hackathon_mode_arabic"] = ""

                    # if is_english(str(getData["candidate_hackathon_organisation_name"])):
                    #     getData["candidate_hackathon_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_organisation_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_hackathon_organisation_name_arabic"] =  getData["candidate_hackathon_organisation_name"]
                    #     getData["candidate_hackathon_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_hackathon_organisation_name"], "ar", "en")["translated_text"])

                    # if getData["candidate_hackathon_certificateID"] != "":


                    #     if is_english(str(getData["candidate_hackathon_certificateID"])):
                    #         getData["candidate_hackathon_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_certificateID"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_hackathon_certificateID_arabic"] =  getData["candidate_hackathon_certificateID"]
                    #         getData["candidate_hackathon_certificateID"] =  str(translator.translator_en_ar(getData["candidate_hackathon_certificateID"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_hackathon_certificateID_arabic"] = ""

                    
                    # if getData["candidate_hackathon_type"] != "":

                    #     if is_english(str(getData["candidate_hackathon_type"])):
                    #         getData["candidate_hackathon_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_type"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_hackathon_type_arabic"] =  getData["candidate_hackathon_type"]
                    #         getData["candidate_hackathon_type"] =  str(translator.translator_en_ar(getData["candidate_hackathon_type"], "ar", "en")["translated_text"])
                    
                    # else:

                    #     getData["candidate_hackathon_type_arabic"] = ""


                    # if getData["candidate_hackathon_field"] != "":

                    #     if is_english(str(getData["candidate_hackathon_field"])):
                    #         getData["candidate_hackathon_field_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_field"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_hackathon_field_arabic"] =  getData["candidate_hackathon_field"]
                    #         getData["candidate_hackathon_field"] =  str(translator.translator_en_ar(getData["candidate_hackathon_field"], "ar", "en")["translated_text"])
                    # else:
                    #     getData["candidate_hackathon_field_arabic"] = ""


                    # if getData["candidate_hackathon_description"] != "":


                    #     if is_english(str(getData["candidate_hackathon_description"])):
                    #         getData["candidate_hackathon_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_hackathon_description"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_hackathon_description_arabic"] =  getData["candidate_hackathon_description"]
                    #         getData["candidate_hackathon_description"] =  str(translator.translator_en_ar(getData["candidate_hackathon_description"], "ar", "en")["translated_text"])


                    # else:

                    #     getData["candidate_hackathon_description_arabic"] = ""
                    
                    serializer = CandidatehackathonSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidatehackathonModel.objects.get(user_id = getData["user_id"], candidate_resume_hackathon_id= getData["candidate_resume_hackathon_id"])

                        latestResume = request.FILES.get('candidate_hackathon_participate_certificate')

                        if latestResume:

                            if userUpload.candidate_hackathon_participate_certificate:
                                userUpload.candidate_hackathon_participate_certificate.delete()

                            userUpload.candidate_hackathon_participate_certificate = latestResume


                        userUpload.candidate_hackathon_name = getData["candidate_hackathon_name"]
                        userUpload.candidate_hackathon_name_arabic = getData["candidate_hackathon_name_arabic"]
                        userUpload.candidate_hackathon_mode = getData["candidate_hackathon_mode"]
                        userUpload.candidate_hackathon_mode_arabic = getData["candidate_hackathon_mode_arabic"]
                        userUpload.candidate_hackathon_organisation_name = getData["candidate_hackathon_organisation_name"]
                        userUpload.candidate_hackathon_organisation_name_arabic = getData["candidate_hackathon_organisation_name_arabic"]
                        userUpload.candidate_hackathon_certificateID = getData["candidate_hackathon_certificateID"]
                        userUpload.candidate_hackathon_certificateID_arabic = getData["candidate_hackathon_certificateID_arabic"]
                        userUpload.candidate_hackathon_type = getData["candidate_hackathon_type"]
                        userUpload.candidate_hackathon_type_arabic = getData["candidate_hackathon_type_arabic"]
                        userUpload.candidate_hackathon_field = getData["candidate_hackathon_field"]
                        userUpload.candidate_hackathon_field_arabic = getData["candidate_hackathon_field_arabic"]
                        userUpload.candidate_hackathon_certificate_issue_date = getData["candidate_hackathon_certificate_issue_date"]
                        # userUpload.candidate_hackathon_certificate_issue_date_arabic = getData["candidate_hackathon_certificate_issue_date_arabic"]
                        userUpload.candidate_hackathon_certificateURL = getData["candidate_hackathon_certificateURL"]
                        userUpload.candidate_hackathon_description = getData["candidate_hackathon_description"]
                        userUpload.candidate_hackathon_description_arabic = getData["candidate_hackathon_description_arabic"]

                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Certificate is successfully uploaded",
                            "Data": {
                                "candidate_resume_hackathon_id" : getData["candidate_resume_hackathon_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatehackathonMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_hackathon_id
        Value : BroaderAI_resume_hackathon_srzwa0r2seekq7v
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidatehackathonModel.objects.filter(user_id = getData["user_id"], candidate_resume_hackathon_id= getData["candidate_resume_hackathon_id"]).exists():

                    userUpload = CandidatehackathonModel.objects.get(user_id = getData["user_id"], candidate_resume_hackathon_id= getData["candidate_resume_hackathon_id"])

                    
                    if userUpload.candidate_hackathon_participate_certificate:
                        userUpload.candidate_hackathon_participate_certificate.delete()

                    userUpload.candidate_hackathon_participate_certificate = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "hackathon Media is deleted",
                        "Data": {
                            "candidate_resume_hackathon_id" : getData["candidate_resume_hackathon_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatehackathonMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_hackathon_id
        Value : BroaderAI_resume_hackathon_srzwa0r2seekq7v


        Key : candidate_hackathon_participate_certificate
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidatehackathonModel.objects.filter(user_id = getData["user_id"], candidate_resume_hackathon_id= getData["candidate_resume_hackathon_id"]).exists():

                
                    userUpload = CandidatehackathonModel.objects.get(user_id = getData["user_id"], candidate_resume_hackathon_id= getData["candidate_resume_hackathon_id"])

                    latestcertificate = request.FILES.get('candidate_hackathon_participate_certificate')

                    if latestcertificate:

                        if userUpload.candidate_hackathon_participate_certificate:
                            userUpload.candidate_hackathon_participate_certificate.delete()

                        userUpload.candidate_hackathon_participate_certificate = latestcertificate

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Media is not uploaded",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)



                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_hackathon_id" : getData["candidate_resume_hackathon_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatehackathonGetAPI(APIView):
    '''
        Candidate hackathon API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidatehackathonModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidatehackathonModel.objects.filter(user_id=getData["user_id"]).values()

                    candidateExp = []


                    for exp in candidateDetail:

                        techkillExp = CandidateHackathonTechnicalSkillsModel.objects.filter(candidate_hackathon_id = exp["candidate_resume_hackathon_id"]).values()

                    
                        tech = ""
                        techdata = dict()

                        for techskill in techkillExp:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = {
                                "candidate_technical_skill_name": str(techskill["candidate_technical_skill_name"]),
                                # "candidate_job_position_id":  techskill["candidate_job_position_id"],
                                # "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = techskill["candidate_job_position_id"]).job_position_name,
                                # "candidate_job_level_id": techskill["candidate_job_level_id"],
                                # "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = techskill["candidate_job_level_id"]).job_level_name,
                            }

                        tech = tech[:-3]

                        candidateExp.append(
                            {
                                "candidate_resume_hackathon_id" : exp["candidate_resume_hackathon_id"],
                                "user_id" : exp["user_id"],
                                
                                "candidate_hackathon_name": exp["candidate_hackathon_name"],
                                "candidate_hackathon_name_arabic": exp["candidate_hackathon_name_arabic"],
                                "candidate_hackathon_mode": exp["candidate_hackathon_mode"],
                                "candidate_hackathon_mode_arabic": exp["candidate_hackathon_mode_arabic"],
                                "candidate_hackathon_organisation_name": exp["candidate_hackathon_organisation_name"],
                                "candidate_hackathon_organisation_name_arabic": exp["candidate_hackathon_organisation_name_arabic"],
                                "candidate_hackathon_certificateID": exp["candidate_hackathon_certificateID"],
                                "candidate_hackathon_certificateID_arabic": exp["candidate_hackathon_certificateID_arabic"],
                                "candidate_hackathon_type": exp["candidate_hackathon_type"],
                                "candidate_hackathon_type_arabic": exp["candidate_hackathon_type_arabic"],
                                "candidate_hackathon_field": exp["candidate_hackathon_field"],
                                "candidate_hackathon_field_arabic": exp["candidate_hackathon_field_arabic"],
                                "candidate_hackathon_participate_certificate": exp["candidate_hackathon_participate_certificate"],
                                "candidate_hackathon_certificate_issue_date": exp["candidate_hackathon_certificate_issue_date"],
                                "candidate_hackathon_certificate_issue_date_arabic": exp["candidate_hackathon_certificate_issue_date_arabic"],
                                "candidate_hackathon_certificateURL": exp["candidate_hackathon_certificateURL"],
                                "candidate_hackathon_description": exp["candidate_hackathon_description"],
                                "candidate_hackathon_description_arabic": exp["candidate_hackathon_description_arabic"],
                                
                                "candidate_technical_skills": tech,
                                "candidate_all_tech": techdata
                            }
                        )

                    if candidateDetail:
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate hackathons Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate hackathons details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatehackathonGetOneAPI(APIView):
    '''
        Candidate hackathons  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_hackathon_id": "BroaderAI_resume_hackathon_srzwa0r2seekq7v"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidatehackathonModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidatehackathonModel.objects.filter( user_id=getData["user_id"], candidate_resume_hackathon_id=getData["candidate_resume_hackathon_id"]).exists(): 

                        candidateDetail = CandidatehackathonModel.objects.filter(user_id=getData["user_id"], candidate_resume_hackathon_id=getData["candidate_resume_hackathon_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate hackathons Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and hackathons not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate hackathons  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]  

class CandidatehackathonDeleteAPI(APIView):
    '''
        hackathon API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_hackathon_id": "BroaderAI_resume_hackathon_srzwa0r2seekq7v"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidatehackathonModel.objects.filter(candidate_resume_hackathon_id = getData["candidate_resume_hackathon_id"]).exists():
                    candidateDetail = CandidatehackathonModel.objects.get(candidate_resume_hackathon_id = getData["candidate_resume_hackathon_id"])
                    
                    if candidateDetail.candidate_hackathon_participate_certificate:
                        candidateDetail.candidate_hackathon_participate_certificate.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "hackathon is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "hackathon data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  hackathon APIs (End)

####################################################

#####################################################

#  hackathon technical skills APIs (Start)

####################################################

class CandidateHackathonTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate hackathon technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
            "candidate_hackathon_id": "BroaderAI_resume_hackathon_rp0qhqzufi8qo3u",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y"
        }
    '''
    
    def post(self, request ,formate=None):
        
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_hackathon_technical_skill" + randomstr
                # getData["candidate_resume_hackathon_technical_skill_id"] = uniqueID

                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated" 

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])
                
                    serializer = CandidateHackathonTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        
                        serializer.save(candidate_resume_hackathon_technical_skill_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User hackathon technical skill is Added",
                            "Data": {
                                "candidate_resume_hackathon_technical_skill_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateHackathonTechnicalSkillsGetAPI(APIView):
    '''
        Candidate hackathon technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateHackathonTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate hackathon Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate hackathon details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateHackathonTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate hackathon technical skill API(view)
        Request : Post
        Data = {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_hackathon_id": "BroaderAI_resume_hackathon_rp0qhqzufi8qo3u"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateHackathonTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateHackathonTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_hackathon_id=getData["candidate_hackathon_id"]).exists(): 

                        candidateDetail = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_hackathon_id=getData["candidate_hackathon_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate hackathon technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and hackathon technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate hackathon technical skill is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateHackathonTechnicalSkillsDeleteAPI(APIView):
    '''
        Hackathon API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_hackathon_technical_skill_id": "BroaderAI_hackathon_technical_skilll78rzdh6l5kwd8a"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateHackathonTechnicalSkillsModel.objects.filter(candidate_resume_hackathon_technical_skill_id = getData["candidate_resume_hackathon_technical_skill_id"]).exists():
                    candidateDetail = CandidateHackathonTechnicalSkillsModel.objects.get(candidate_resume_hackathon_technical_skill_id = getData["candidate_resume_hackathon_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Hackathon technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Hackathon technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateHackathonTechnicalSkillsAllDeleteAPI(APIView):
    '''
        Hackathon API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_technical_skill_id": "BroaderAI_hackathon_technical_skilll78rzdh6l5kwd8a"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateHackathonTechnicalSkillsModel.objects.filter(candidate_resume_hackathon_technical_skill_id = getData["candidate_resume_hackathon_technical_skill_id"]).exists():
                    candidateDetail = CandidateHackathonTechnicalSkillsModel.objects.get(candidate_resume_hackathon_technical_skill_id = getData["candidate_resume_hackathon_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Hackathon technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Hackathon technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateHackathonGetOneAllDetailsAPI(APIView):

    '''
        Candidate Hackathon API(view)
        Request : Post
        Data =  {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_hackathon_id": "BroaderAI_resume_hackathon_qzq9wni0j7ht6st"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidatehackathonModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidatehackathonModel.objects.filter( user_id=getData["user_id"], candidate_resume_hackathon_id=getData["candidate_resume_hackathon_id"]).exists(): 

                        candidateDetail = CandidatehackathonModel.objects.get(user_id=getData["user_id"], candidate_resume_hackathon_id=getData["candidate_resume_hackathon_id"])

                        candidatetechnicalskill = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_hackathon_id=getData["candidate_resume_hackathon_id"]).values()


                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate project Details",
                                "Data": {
                                    "candidate_resume_hackathon_id" : getData['candidate_resume_hackathon_id'],
                                    "user_id" : getData['user_id'],
                                    "candidate_hackathon_name" :  candidateDetail.candidate_hackathon_name,
                                    "candidate_hackathon_name_arabic" :  candidateDetail.candidate_hackathon_name_arabic,
                                    "candidate_hackathon_mode" : candidateDetail.candidate_hackathon_mode,
                                    "candidate_hackathon_mode_arabic" : candidateDetail.candidate_hackathon_mode_arabic,
                                    "candidate_hackathon_organisation_name" : candidateDetail.candidate_hackathon_organisation_name,
                                    "candidate_hackathon_organisation_name_arabic" : candidateDetail.candidate_hackathon_organisation_name_arabic,

                                    "candidate_hackathon_certificateID" : candidateDetail.candidate_hackathon_certificateID,
                                    "candidate_hackathon_certificateID_arabic" : candidateDetail.candidate_hackathon_certificateID_arabic,

                                    "candidate_hackathon_type" : candidateDetail.candidate_hackathon_type,
                                    "candidate_hackathon_type_arabic" : candidateDetail.candidate_hackathon_type_arabic,

                                    "candidate_hackathon_field" : candidateDetail.candidate_hackathon_field,
                                    "candidate_hackathon_field_arabic" : candidateDetail.candidate_hackathon_field_arabic,

                                    "candidate_hackathon_certificate_issue_date" : candidateDetail.candidate_hackathon_certificate_issue_date,
                                    "candidate_hackathon_certificateURL" : candidateDetail.candidate_hackathon_certificateURL,
                                    "candidate_hackathon_description" : candidateDetail.candidate_hackathon_description,
                                    "candidate_hackathon_description_arabic" : candidateDetail.candidate_hackathon_description_arabic,

                                    "candidate_technical_skills" : candidatetechnicalskill
                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and hackathon not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate hackathon details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateHackathonTechnicalSkillsAllDeleteHackIdAPI(APIView):
    '''
        Hackathon API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_hackathon_id": "BroaderAI_hackathon_technical_skilll78rzdh6l5kwd8a"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateHackathonTechnicalSkillsModel.objects.filter(candidate_hackathon_id = getData["candidate_hackathon_id"], user_id = getData["user_id"]).exists():
                    candidateDetail = CandidateHackathonTechnicalSkillsModel.objects.filter(candidate_hackathon_id = getData["candidate_hackathon_id"], user_id = getData["user_id"])

                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Hackathon technical skills is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Hackathon technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  hackathon technical skills APIs (End)

####################################################

#####################################################

#  Contribution  APIs (Start)

####################################################
class CandidateContributionAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_contribution_topic
        Value : NLP
        
        Key : candidate_contribution_keyword
        Value : python, data, django

        Key : candidate_contribution_organisation_name
        Value : PPSU

        Key: candidate_contribution_certificateID
        Value : tgesgsbehdbh

        Key: candidate_contribution_publish_date
        Value : 2/1/11

        Key: candidate_contribution_certificate_issue_date
        Value : 1/2/12

        Key : candidate_contribution_participate_certificate
        Value : Files upload....

        Key : candidate_contribution_certificateURL
        Value : https://www.merriam-webster.com/dictionary/contribution

        Key : candidate_contribution_summary
        Value : prepare research paper
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_contribution_" + randomstr

                getData["candidate_contribution_topic_arabic"] = "Not Translated"
                getData["candidate_contribution_keyword_arabic"] = "Not Translated"
                getData["candidate_contribution_organisation_name_arabic"] = "Not Translated"
                getData["candidate_contribution_certificateID_arabic"] = "Not Translated"
                getData["candidate_contribution_summary_arabic"] = "Not Translated"


                # if is_english(str(getData["candidate_contribution_topic"])):
                #     getData["candidate_contribution_topic_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_topic"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_contribution_topic_arabic"] =  getData["candidate_contribution_topic"]
                #     getData["candidate_contribution_topic"] =  str(translator.translator_en_ar(getData["candidate_contribution_topic"], "ar", "en")["translated_text"])

                # if str(getData["candidate_contribution_keyword"]) != "":

                #     if is_english(str(getData["candidate_contribution_keyword"])):
                #         getData["candidate_contribution_keyword_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_keyword"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_contribution_keyword_arabic"] =  getData["candidate_contribution_keyword"]
                #         getData["candidate_contribution_keyword"] =  str(translator.translator_en_ar(getData["candidate_contribution_keyword"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_contribution_keyword_arabic"] = ""


                # if is_english(str(getData["candidate_contribution_organisation_name"])):
                #     getData["candidate_contribution_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_organisation_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_contribution_organisation_name_arabic"] =  getData["candidate_contribution_organisation_name"]
                #     getData["candidate_contribution_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_contribution_organisation_name"], "ar", "en")["translated_text"])

                # if str(getData["candidate_contribution_certificateID"]) != "":


                #     if is_english(str(getData["candidate_contribution_certificateID"])):
                #         getData["candidate_contribution_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_certificateID"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_contribution_certificateID_arabic"] =  getData["candidate_contribution_certificateID"]
                #         getData["candidate_contribution_certificateID"] =  str(translator.translator_en_ar(getData["candidate_contribution_certificateID"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_contribution_certificateID_arabic"] = ""


                # if str(getData["candidate_contribution_summary"]) != "":

                
                #     if is_english(str(getData["candidate_contribution_summary"])):
                #         getData["candidate_contribution_summary_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_summary"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_contribution_summary_arabic"] =  getData["candidate_contribution_summary"]
                #         getData["candidate_contribution_summary"] =  str(translator.translator_en_ar(getData["candidate_contribution_summary"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_contribution_summary_arabic"] = ""


                serializer = CandidateContributionSerializer(data=getData)
            
                if serializer.is_valid():
                    if getData["candidate_contribution_participate_certificate"] != "":
                        serializer.validated_data['candidate_contribution_participate_certificate'] = getData["candidate_contribution_participate_certificate"]


                    serializer.save(candidate_resume_contribution_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Contribution certificate is successfully uploaded",
                        "Data": {
                            "candidate_resume_contribution_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_contribution_topic
        Value : NLP
        
        Key : candidate_contribution_keyword
        Value : python, data, django

        Key : candidate_contribution_organisation_name
        Value : PPSU

        Key: candidate_contribution_certificateID
        Value : tgesgsbehdbh

        Key: candidate_contribution_publish_date
        Value : 2/1/11

        Key: candidate_contribution_certificate_issue_date
        Value : 1/2/12

        Key : candidate_contribution_participate_certificate
        Value : Files upload....

        Key : candidate_contribution_certificateID
        Value : https://www.merriam-webster.com/dictionary/contribution

        Key : candidate_contribution_summary
        Value : prepare research paper

        Key : candidate_resume_contribution_id
        Value : BroaderAI_resume_contribution_kyzl1fpgsxz5ha0
        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateContributionModel.objects.filter(user_id = getData["user_id"], candidate_resume_contribution_id= getData["candidate_resume_contribution_id"]).exists():

                    getData["candidate_contribution_topic_arabic"] = "Not Translated"
                    getData["candidate_contribution_keyword_arabic"] = "Not Translated"
                    getData["candidate_contribution_organisation_name_arabic"] = "Not Translated"
                    getData["candidate_contribution_certificateID_arabic"] = "Not Translated"
                    getData["candidate_contribution_summary_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_contribution_topic"])):
                    #     getData["candidate_contribution_topic_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_topic"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_contribution_topic_arabic"] =  getData["candidate_contribution_topic"]
                    #     getData["candidate_contribution_topic"] =  str(translator.translator_en_ar(getData["candidate_contribution_topic"], "ar", "en")["translated_text"])

                    # if str(getData["candidate_contribution_keyword"]) != "":

                    #     if is_english(str(getData["candidate_contribution_keyword"])):
                    #         getData["candidate_contribution_keyword_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_keyword"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_contribution_keyword_arabic"] =  getData["candidate_contribution_keyword"]
                    #         getData["candidate_contribution_keyword"] =  str(translator.translator_en_ar(getData["candidate_contribution_keyword"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_contribution_keyword_arabic"] =  ""

                    # if is_english(str(getData["candidate_contribution_organisation_name"])):
                    #     getData["candidate_contribution_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_organisation_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_contribution_organisation_name_arabic"] =  getData["candidate_contribution_organisation_name"]
                    #     getData["candidate_contribution_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_contribution_organisation_name"], "ar", "en")["translated_text"])

                    # if str(getData["candidate_contribution_certificateID"]) != "":



                    #     if is_english(str(getData["candidate_contribution_certificateID"])):
                    #         getData["candidate_contribution_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_certificateID"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_contribution_certificateID_arabic"] =  getData["candidate_contribution_certificateID"]
                    #         getData["candidate_contribution_certificateID"] =  str(translator.translator_en_ar(getData["candidate_contribution_certificateID"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_contribution_certificateID_arabic"] =  ""


                    # if str(getData["candidate_contribution_summary"]) != "":
                    
                    #     if is_english(str(getData["candidate_contribution_summary"])):
                    #         getData["candidate_contribution_summary_arabic"] =  str(translator.translator_en_ar(getData["candidate_contribution_summary"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_contribution_summary_arabic"] =  getData["candidate_contribution_summary"]
                    #         getData["candidate_contribution_summary"] =  str(translator.translator_en_ar(getData["candidate_contribution_summary"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_contribution_summary_arabic"] =  ""


                    serializer = CandidateContributionSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidateContributionModel.objects.get(user_id = getData["user_id"], candidate_resume_contribution_id= getData["candidate_resume_contribution_id"])

                        latestcertificate = request.FILES.get('candidate_contribution_participate_certificate')

                        if latestcertificate:

                            if userUpload.candidate_contribution_participate_certificate:
                                userUpload.candidate_contribution_participate_certificate.delete()

                            userUpload.candidate_contribution_participate_certificate = latestcertificate


                        userUpload.candidate_contribution_topic = getData["candidate_contribution_topic"].capitalize()
                        userUpload.candidate_contribution_topic_arabic = getData["candidate_contribution_topic_arabic"]
                        userUpload.candidate_contribution_keyword = getData["candidate_contribution_keyword"]
                        userUpload.candidate_contribution_keyword_arabic = getData["candidate_contribution_keyword_arabic"]
                        userUpload.candidate_contribution_organisation_name = getData["candidate_contribution_organisation_name"]
                        userUpload.candidate_contribution_organisation_name_arabic = getData["candidate_contribution_organisation_name_arabic"]
                        userUpload.candidate_contribution_certificateID = getData["candidate_contribution_certificateID"]
                        userUpload.candidate_contribution_certificateID_arabic = getData["candidate_contribution_certificateID_arabic"]
                        userUpload.candidate_contribution_certificateURL = getData["candidate_contribution_certificateURL"]
                        userUpload.candidate_contribution_publish_date = getData["candidate_contribution_publish_date"]
                        userUpload.candidate_contribution_certificate_issue_date = getData["candidate_contribution_certificate_issue_date"]
                        userUpload.candidate_contribution_summary = getData["candidate_contribution_summary"]
                        userUpload.candidate_contribution_summary_arabic = getData["candidate_contribution_summary_arabic"]

                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Certificate is successfully uploaded",
                            "Data": {
                                "candidate_resume_contribution_id" : getData["candidate_resume_contribution_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_contribution_id
        Value : BroaderAI_resume_contribution_kyzl1fpgsxz5ha0
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateContributionModel.objects.filter(user_id = getData["user_id"], candidate_resume_contribution_id= getData["candidate_resume_contribution_id"]).exists():

                    userUpload = CandidateContributionModel.objects.get(user_id = getData["user_id"], candidate_resume_contribution_id= getData["candidate_resume_contribution_id"])

                    
                    if userUpload.candidate_contribution_participate_certificate:
                        userUpload.candidate_contribution_participate_certificate.delete()

                    userUpload.candidate_contribution_participate_certificate = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "hackathon Media is deleted",
                        "Data": {
                            "candidate_resume_contribution_id" : getData["candidate_resume_contribution_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_contribution_id
        Value : BroaderAI_resume_contribution_kyzl1fpgsxz5ha0


        Key : candidate_contribution_participate_certificate
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateContributionModel.objects.filter(user_id = getData["user_id"], candidate_resume_contribution_id= getData["candidate_resume_contribution_id"]).exists():

                
                    userUpload = CandidateContributionModel.objects.get(user_id = getData["user_id"], candidate_resume_contribution_id= getData["candidate_resume_contribution_id"])

                    latestcertificate = request.FILES.get('candidate_contribution_participate_certificate')

                    if latestcertificate:

                        if userUpload.candidate_contribution_participate_certificate:
                            userUpload.candidate_contribution_participate_certificate.delete()

                        userUpload.candidate_contribution_participate_certificate = latestcertificate

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Media is not uploaded",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)



                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_contribution_id" : getData["candidate_resume_contribution_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionGetAPI(APIView):

    '''
        Candidate contribution API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):

        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateContributionModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    candidateDetail = CandidateContributionModel.objects.filter(user_id=getData["user_id"]).values()

                    candidateExp = []


                    for exp in candidateDetail:

                        techkillExp = CandidateContributionTechnicalSkillsModel.objects.filter(candidate_contribution_id = exp["candidate_resume_contribution_id"]).values()

                    
                        tech = ""
                        techdata = dict()

                        for techskill in techkillExp:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = {
                                "candidate_technical_skill_name": str(techskill["candidate_technical_skill_name"]),
                                # "candidate_job_position_id":  techskill["candidate_job_position_id"],
                                # "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = techskill["candidate_job_position_id"]).job_position_name,
                                # "candidate_job_level_id": techskill["candidate_job_level_id"],
                                # "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = techskill["candidate_job_level_id"]).job_level_name,
                            }

                        tech = tech[:-3]

                        candidateExp.append(
                            {
                                "candidate_resume_contribution_id" : exp["candidate_resume_contribution_id"],
                                "user_id" : exp["user_id"],
                                
                                "candidate_contribution_topic": exp["candidate_contribution_topic"],
                                "candidate_contribution_topic_arabic": exp["candidate_contribution_topic_arabic"],
                                "candidate_contribution_keyword": exp["candidate_contribution_keyword"],
                                "candidate_contribution_keyword_arabic": exp["candidate_contribution_keyword_arabic"],
                                "candidate_contribution_organisation_name": exp["candidate_contribution_organisation_name"],
                                "candidate_contribution_organisation_name_arabic": exp["candidate_contribution_organisation_name_arabic"],
                                "candidate_contribution_certificateID": exp["candidate_contribution_certificateID"],
                                "candidate_contribution_certificateID_arabic": exp["candidate_contribution_certificateID_arabic"],
                                "candidate_contribution_publish_date": exp["candidate_contribution_publish_date"],
                                "candidate_contribution_certificate_issue_date": exp["candidate_contribution_certificate_issue_date"],
                                "candidate_contribution_participate_certificate": exp["candidate_contribution_participate_certificate"],
                                "candidate_contribution_certificateURL": exp["candidate_contribution_certificateURL"],
                                "candidate_contribution_summary": exp["candidate_contribution_summary"],
                                "candidate_contribution_summary_arabic": exp["candidate_contribution_summary_arabic"],

                                "candidate_technical_skills": tech,
                                "candidate_all_tech": techdata
                            }
                        )


                    
                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate contributions Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate contribution details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionGetOneAPI(APIView):
    '''
        Candidate contribution  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_contribution_id": "BroaderAI_resume_contribution_farw9xjz54p2qmu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateContributionModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateContributionModel.objects.filter( user_id=getData["user_id"], candidate_resume_contribution_id=getData["candidate_resume_contribution_id"]).exists(): 

                        candidateDetail = CandidateContributionModel.objects.filter(user_id=getData["user_id"], candidate_resume_contribution_id=getData["candidate_resume_contribution_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate contribution Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and contribution not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate contribution  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]  

class CandidateContributionDeleteAPI(APIView):
    '''
        contribution API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_contribution_id": "BroaderAI_resume_contribution_farw9xjz54p2qmu"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateContributionModel.objects.filter(candidate_resume_contribution_id = getData["candidate_resume_contribution_id"]).exists():
                    candidateDetail = CandidateContributionModel.objects.get(candidate_resume_contribution_id = getData["candidate_resume_contribution_id"])
                    
                    if candidateDetail.candidate_contribution_participate_certificate:
                        candidateDetail.candidate_contribution_participate_certificate.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "contribution is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "contribution data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  contribution APIs (End)

####################################################

#####################################################

#  contribution technical skills APIs (Start)

####################################################

class CandidateContributionTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate hackathon technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
            "candidate_contribution_id": "BroaderAI_resume_contribution_kyzl1fpgsxz5ha0",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y"
        }
    '''
    
    def post(self, request ,formate=None):
        
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_contribution_technical_skill_" + randomstr
                # getData["candidate_resume_contribution_technical_skill_id"] = uniqueID

                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])
                
                    serializer = CandidateContributionTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        
                        serializer.save(candidate_resume_contribution_technical_skill_id= uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User contribution technical skill is Added",
                            "Data": {
                                "candidate_resume_contribution_technical_skill_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionTechnicalSkillsGetAPI(APIView):
    '''
        Candidate contribution technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateContributionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateContributionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate contribution Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate contribution details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate contribution technical skill API(view)
        Request : Post
        Data = {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_contribution_id": "BroaderAI_resume_contribution_kyzl1fpgsxz5ha0"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateContributionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateContributionTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_contribution_id=getData["candidate_contribution_id"]).exists(): 

                        candidateDetail = CandidateContributionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_contribution_id=getData["candidate_contribution_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate contribution technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and contribution technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate contribution technical skill is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionTechnicalSkillsDeleteAPI(APIView):
    '''
        contribution API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_contribution_technical_skill_id": "BroaderAI_contribution_technical_skill8js72d5jmb3xen7"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateContributionTechnicalSkillsModel.objects.filter(candidate_resume_contribution_technical_skill_id = getData["candidate_resume_contribution_technical_skill_id"]).exists():
                    candidateDetail = CandidateContributionTechnicalSkillsModel.objects.get(candidate_resume_contribution_technical_skill_id = getData["candidate_resume_contribution_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "contribution technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "contribution technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatecontributionGetOneAllDetailsAPI(APIView):

    '''
        Candidate contribution API(view)
        Request : Post
        Data =  {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_contribution_id": "BroaderAI_resume_contribution_kyzl1fpgsxz5ha0"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateContributionModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateContributionModel.objects.filter( user_id=getData["user_id"], candidate_resume_contribution_id=getData["candidate_resume_contribution_id"]).exists(): 

                        candidateDetail = CandidateContributionModel.objects.get(user_id=getData["user_id"], candidate_resume_contribution_id=getData["candidate_resume_contribution_id"])

                        candidatetechnicalskill = CandidateContributionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_contribution_id=getData["candidate_resume_contribution_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate contribution Details",
                                "Data": {
                                    "candidate_resume_contribution_id" : getData['candidate_resume_contribution_id'],
                                    "user_id" : getData['user_id'],
                                    "candidate_contribution_topic" :  candidateDetail.candidate_contribution_topic,
                                    "candidate_contribution_topic_arabic" :  candidateDetail.candidate_contribution_topic_arabic,

                                    "candidate_contribution_keyword" : candidateDetail.candidate_contribution_keyword,
                                    "candidate_contribution_keyword_arabic" : candidateDetail.candidate_contribution_keyword_arabic,

                                    "candidate_contribution_organisation_name" : candidateDetail.candidate_contribution_organisation_name,
                                    "candidate_contribution_organisation_name_arabic" : candidateDetail.candidate_contribution_organisation_name_arabic,

                                    "candidate_contribution_certificateID" : candidateDetail.candidate_contribution_certificateID,
                                    "candidate_contribution_certificateID_arabic" : candidateDetail.candidate_contribution_certificateID_arabic,

                                    "candidate_contribution_certificateURL" : candidateDetail.candidate_contribution_certificateURL,
                                    "candidate_contribution_publish_date" : candidateDetail.candidate_contribution_publish_date,
                                    "candidate_contribution_certificate_issue_date" : candidateDetail.candidate_contribution_certificate_issue_date,
                                    "candidate_contribution_summary" : candidateDetail.candidate_contribution_summary,
                                    "candidate_contribution_summary_arabic" : candidateDetail.candidate_contribution_summary_arabic,

                                    "candidate_technical_skills" : candidatetechnicalskill
                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and contribution not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate contribution details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateContributionTechnicalSkillsConIdDeleteAPI(APIView):
    '''
        contribution API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_contribution_id": "BroaderAI_contribution_technical_skill8js72d5jmb3xen7"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateContributionTechnicalSkillsModel.objects.filter(candidate_contribution_id = getData["candidate_contribution_id"]).exists():
                    candidateDetail = CandidateContributionTechnicalSkillsModel.objects.filter(candidate_contribution_id = getData["candidate_contribution_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "contribution technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "contribution technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  contribution technical skills APIs (End)

####################################################
#####################################################

#  workshop  APIs (Start)

####################################################
class CandidateWorkshopAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_workshop_organisation_name
        Value : gov
        
        Key : candidate_workshop_name
        Value : art and craft

        Key : candidate_workshop_type
        Value : on-site

        Key: candidate_workshop_topic
        Value : paint

        Key: candidate_workshop_certificateID
        Value : hihkmdreokrof

        Key: candidate_workshop_certificate_issue_date
        Value : 1/2/12

        Key : candidate_workshop_participate_certificate
        Value : Files upload....

        Key : candidate_workshop_certificateURL
        Value : https://www.merriam-webster.com/dictionary/workshop

        Key : candidate_workshop_duration
        Value : one day

        Key : candidate_workshop_description
        Value : created paper bag
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data


        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_workshop_" + randomstr

                getData["candidate_workshop_organisation_name_arabic"] = "Not Translated"
                getData["candidate_workshop_name_arabic"] = "Not Translated"
                getData["candidate_workshop_type_arabic"] = "Not Translated"
                getData["candidate_workshop_topic_arabic"] = "Not Translated"
                getData["candidate_workshop_certificateID_arabic"] = "Not Translated"
                getData["candidate_workshop_description_arabic"] = "Not Translated"

                # if is_english(str(getData["candidate_workshop_organisation_name"])):
                #     getData["candidate_workshop_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_organisation_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_workshop_organisation_name_arabic"] =  getData["candidate_workshop_organisation_name"]
                #     getData["candidate_workshop_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_workshop_organisation_name"], "ar", "en")["translated_text"])

                # if is_english(str(getData["candidate_workshop_name"])):
                #     getData["candidate_workshop_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_workshop_name_arabic"] =  getData["candidate_workshop_name"]
                #     getData["candidate_workshop_name"] =  str(translator.translator_en_ar(getData["candidate_workshop_name"], "ar", "en")["translated_text"])

                # if str(getData["candidate_workshop_type"]) != "":

                #     if is_english(str(getData["candidate_workshop_type"])):
                #         getData["candidate_workshop_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_type"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_workshop_type_arabic"] =  getData["candidate_workshop_type"]
                #         getData["candidate_workshop_type"] =  str(translator.translator_en_ar(getData["candidate_workshop_type"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_workshop_type_arabic"] =  ""

                # if is_english(str(getData["candidate_workshop_topic"])):
                #     getData["candidate_workshop_topic_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_topic"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_workshop_topic_arabic"] =  getData["candidate_workshop_topic"]
                #     getData["candidate_workshop_topic"] =  str(translator.translator_en_ar(getData["candidate_workshop_topic"], "ar", "en")["translated_text"])
                
                # if str(getData["candidate_workshop_certificateID"]) != "":
                
                #     if is_english(str(getData["candidate_workshop_certificateID"])):
                #         getData["candidate_workshop_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_certificateID"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_workshop_certificateID_arabic"] =  getData["candidate_workshop_certificateID"]
                #         getData["candidate_workshop_certificateID"] =  str(translator.translator_en_ar(getData["candidate_workshop_certificateID"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_workshop_certificateID_arabic"] =  ""


                # if str(getData["candidate_workshop_description"]) != "":

                #     if is_english(str(getData["candidate_workshop_description"])):
                #         getData["candidate_workshop_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_description"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_workshop_description_arabic"] =  getData["candidate_workshop_description"]
                #         getData["candidate_workshop_description"] =  str(translator.translator_en_ar(getData["candidate_workshop_description"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_workshop_description_arabic"] =  ""

                serializer = CandidateWorkshopSerializer(data=getData)
            
                if serializer.is_valid():
                    if getData["candidate_workshop_participate_certificate"] != "":
                        serializer.validated_data['candidate_workshop_participate_certificate'] = getData["candidate_workshop_participate_certificate"]


                    serializer.save(candidate_resume_workshop_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "workshop certificate is successfully uploaded",
                        "Data": {
                            "candidate_resume_workshop_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_workshop_organisation_name
        Value : gov
        
        Key : candidate_workshop_name
        Value : art and craft

        Key : candidate_workshop_type
        Value : on-site

        Key: candidate_workshop_topic
        Value : paint

        Key: candidate_workshop_certificateID
        Value : hihkmdreokrof

        Key: candidate_workshop_certificate_issue_date
        Value : 1/2/12

        Key : candidate_workshop_participate_certificate
        Value : Files upload....

        Key : candidate_workshop_certificateURL
        Value : https://www.merriam-webster.com/dictionary/workshop

        Key : candidate_workshop_duration
        Value : one day

        Key : candidate_workshop_description
        Value : prepare research paperr

        Key : candidate_resume_workshop_id
        Value : BroaderAI_resume_workshop_kyzl1fpgsxz5ha0
        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateWorkshopModel.objects.filter(user_id = getData["user_id"], candidate_resume_workshop_id= getData["candidate_resume_workshop_id"]).exists():

                    getData["candidate_workshop_organisation_name_arabic"] = "Not Translated"
                    getData["candidate_workshop_name_arabic"] = "Not Translated"
                    getData["candidate_workshop_type_arabic"] = "Not Translated"
                    getData["candidate_workshop_topic_arabic"] = "Not Translated"
                    getData["candidate_workshop_certificateID_arabic"] = "Not Translated"
                    getData["candidate_workshop_description_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_workshop_organisation_name"])):
                    #     getData["candidate_workshop_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_organisation_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_workshop_organisation_name_arabic"] =  getData["candidate_workshop_organisation_name"]
                    #     getData["candidate_workshop_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_workshop_organisation_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_workshop_name"])):
                    #     getData["candidate_workshop_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_workshop_name_arabic"] =  getData["candidate_workshop_name"]
                    #     getData["candidate_workshop_name"] =  str(translator.translator_en_ar(getData["candidate_workshop_name"], "ar", "en")["translated_text"])

                    # if str(getData["candidate_workshop_type"]) != "":

                    #     if is_english(str(getData["candidate_workshop_type"])):
                    #         getData["candidate_workshop_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_type"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_workshop_type_arabic"] =  getData["candidate_workshop_type"]
                    #         getData["candidate_workshop_type"] =  str(translator.translator_en_ar(getData["candidate_workshop_type"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_workshop_type_arabic"] =  ""
                    # if is_english(str(getData["candidate_workshop_topic"])):
                    #     getData["candidate_workshop_topic_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_topic"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_workshop_topic_arabic"] =  getData["candidate_workshop_topic"]
                    #     getData["candidate_workshop_topic"] =  str(translator.translator_en_ar(getData["candidate_workshop_topic"], "ar", "en")["translated_text"])
                    
                    # if str(getData["candidate_workshop_certificateID"]) != "":


                    #     if is_english(str(getData["candidate_workshop_certificateID"])):
                    #         getData["candidate_workshop_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_certificateID"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_workshop_certificateID_arabic"] =  getData["candidate_workshop_certificateID"]
                    #         getData["candidate_workshop_certificateID"] =  str(translator.translator_en_ar(getData["candidate_workshop_certificateID"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_workshop_certificateID_arabic"] =  ""


                    # if str(getData["candidate_workshop_description"]) != "":

                    #     if is_english(str(getData["candidate_workshop_description"])):
                    #         getData["candidate_workshop_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_workshop_description"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_workshop_description_arabic"] =  getData["candidate_workshop_description"]
                    #         getData["candidate_workshop_description"] =  str(translator.translator_en_ar(getData["candidate_workshop_description"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_workshop_description_arabic"] =  ""


                    serializer = CandidateWorkshopSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidateWorkshopModel.objects.get(user_id = getData["user_id"], candidate_resume_workshop_id= getData["candidate_resume_workshop_id"])

                        latestcertificate = request.FILES.get('candidate_workshop_participate_certificate')

                        if latestcertificate:

                            if userUpload.candidate_workshop_participate_certificate:
                                userUpload.candidate_workshop_participate_certificate.delete()

                            userUpload.candidate_workshop_participate_certificate = latestcertificate


                        userUpload.candidate_workshop_organisation_name = getData["candidate_workshop_organisation_name"].capitalize()
                        userUpload.candidate_workshop_organisation_name_arabic = getData["candidate_workshop_organisation_name_arabic"]
                        userUpload.candidate_workshop_name = getData["candidate_workshop_name"]
                        userUpload.candidate_workshop_name_arabic = getData["candidate_workshop_name_arabic"]
                        userUpload.candidate_workshop_type = getData["candidate_workshop_type"]
                        userUpload.candidate_workshop_type_arabic = getData["candidate_workshop_type_arabic"]
                        userUpload.candidate_workshop_topic = getData["candidate_workshop_topic"]
                        userUpload.candidate_workshop_topic_arabic = getData["candidate_workshop_topic_arabic"]
                        userUpload.candidate_workshop_certificateID = getData["candidate_workshop_certificateID"]
                        userUpload.candidate_workshop_certificateID_arabic = getData["candidate_workshop_certificateID_arabic"]
                        userUpload.candidate_workshop_certificateURL = getData["candidate_workshop_certificateURL"]
                        userUpload.candidate_workshop_duration = getData["candidate_workshop_duration"]
                        userUpload.candidate_workshop_certificate_issue_date = getData["candidate_workshop_certificate_issue_date"]
                        userUpload.candidate_workshop_description = getData["candidate_workshop_description"]
                        userUpload.candidate_workshop_description_arabic = getData["candidate_workshop_description_arabic"]

                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Certificate is successfully uploaded",
                            "Data": {
                                "candidate_resume_workshop_id" : getData["candidate_resume_workshop_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_workshop_id
        Value : BroaderAI_resume_workshop_gm13eolk1u3xvm2
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateWorkshopModel.objects.filter(user_id = getData["user_id"], candidate_resume_workshop_id= getData["candidate_resume_workshop_id"]).exists():

                    userUpload = CandidateWorkshopModel.objects.get(user_id = getData["user_id"], candidate_resume_workshop_id= getData["candidate_resume_workshop_id"])

                    
                    if userUpload.candidate_workshop_participate_certificate:
                        userUpload.candidate_workshop_participate_certificate.delete()

                    userUpload.candidate_workshop_participate_certificate = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Workshop Media is deleted",
                        "Data": {
                            "candidate_resume_workshop_id" : getData["candidate_resume_workshop_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_workshop_id
        Value : BroaderAI_resume_workshop_kyzl1fpgsxz5ha0


        Key : candidate_workshop_participate_certificate
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateWorkshopModel.objects.filter(user_id = getData["user_id"], candidate_resume_workshop_id= getData["candidate_resume_workshop_id"]).exists():

                
                    userUpload = CandidateWorkshopModel.objects.get(user_id = getData["user_id"], candidate_resume_workshop_id= getData["candidate_resume_workshop_id"])

                    latestcertificate = request.FILES.get('candidate_workshop_participate_certificate')

                    if latestcertificate:

                        if userUpload.candidate_workshop_participate_certificate:
                            userUpload.candidate_workshop_participate_certificate.delete()

                        userUpload.candidate_workshop_participate_certificate = latestcertificate

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Media is not uploaded",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)



                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_workshop_id" : getData["candidate_resume_workshop_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopGetOneAPI(APIView):
    '''
        Candidate workshop  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_workshop_id": "BroaderAI_resume_workshop_farw9xjz54p2qmu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateWorkshopModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateWorkshopModel.objects.filter( user_id=getData["user_id"], candidate_resume_workshop_id=getData["candidate_resume_workshop_id"]).exists(): 

                        candidateDetail = CandidateWorkshopModel.objects.filter(user_id=getData["user_id"], candidate_resume_workshop_id=getData["candidate_resume_workshop_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate workshop Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and workshop not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate workshop  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]  

class CandidateWorkshopGetAPI(APIView):
    '''
        Candidate workshop API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateWorkshopModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateWorkshopModel.objects.filter(user_id=getData["user_id"]).values()

                    candidateExp = []


                    for exp in candidateDetail:

                        techkillExp = CandidateWorkshopTechnicalSkillsModel.objects.filter(candidate_workshop_id = exp["candidate_resume_workshop_id"]).values()

                    
                        tech = ""
                        techdata = dict()

                        for techskill in techkillExp:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = {
                                "candidate_technical_skill_name": str(techskill["candidate_technical_skill_name"]),
                                # "candidate_job_position_id":  techskill["candidate_job_position_id"],
                                # "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = techskill["candidate_job_position_id"]).job_position_name,
                                # "candidate_job_level_id": techskill["candidate_job_level_id"],
                                # "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = techskill["candidate_job_level_id"]).job_level_name,
                            }

                        tech = tech[:-3]

                        candidateExp.append(
                            {
                                "candidate_resume_workshop_id" : exp["candidate_resume_workshop_id"],
                                "user_id" : exp["user_id"],
                                "candidate_workshop_name": exp["candidate_workshop_name"],
                                "candidate_workshop_name_arabic": exp["candidate_workshop_name_arabic"],
                                "candidate_workshop_type": exp["candidate_workshop_type"],
                                "candidate_workshop_type_arabic": exp["candidate_workshop_type_arabic"],
                                "candidate_workshop_organisation_name": exp["candidate_workshop_organisation_name"],
                                "candidate_workshop_organisation_name_arabic": exp["candidate_workshop_organisation_name_arabic"],
                                "candidate_workshop_topic": exp["candidate_workshop_topic"],
                                "candidate_workshop_topic_arabic": exp["candidate_workshop_topic_arabic"],
                                "candidate_workshop_certificateID": exp["candidate_workshop_certificateID"],
                                "candidate_workshop_certificateID_arabic": exp["candidate_workshop_certificateID_arabic"],
                                "candidate_workshop_certificateURL": exp["candidate_workshop_certificateURL"],
                                "candidate_workshop_participate_certificate": exp["candidate_workshop_participate_certificate"],
                                "candidate_workshop_duration": exp["candidate_workshop_duration"],
                                "candidate_workshop_certificate_issue_date": exp["candidate_workshop_certificate_issue_date"],
                                "candidate_workshop_description": exp["candidate_workshop_description"],
                                "candidate_workshop_description_arabic": exp["candidate_workshop_description_arabic"],
                                
                                "candidate_technical_skills": tech,
                                "candidate_all_tech": techdata
                            }
                        )


                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate workshops Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate workshop details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopDeleteAPI(APIView):
    '''
        workshop API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_workshop_id": "BroaderAI_resume_workshop_farw9xjz54p2qmu"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateWorkshopModel.objects.filter(candidate_resume_workshop_id = getData["candidate_resume_workshop_id"]).exists():
                    candidateDetail = CandidateWorkshopModel.objects.get(candidate_resume_workshop_id = getData["candidate_resume_workshop_id"])
                    
                    if candidateDetail.candidate_workshop_participate_certificate:
                        candidateDetail.candidate_workshop_participate_certificate.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "workshop is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "workshop data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  workshop APIs (End)

####################################################

#####################################################

#  workshop technical skills APIs (Start)

####################################################

class CandidateWorkshopTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate workshop technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
            "candidate_workshop_id": "BroaderAI_resume_workshop_31a3h9h0lo3cud0",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y"
        }
    '''
    
    def post(self, request ,formate=None):
        
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_workshop_technical_skill_" + randomstr
                # getData["candidate_resume_workshop_technical_skill_id"] = uniqueID

                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated" 

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])
                
                    serializer = CandidateWorkshopTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        
                        serializer.save(candidate_resume_workshop_technical_skill_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User workshop technical skill is Added",
                            "Data": {
                                "candidate_resume_workshop_technical_skill_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopTechnicalSkillsGetAPI(APIView):
    '''
        Candidate workshop technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate workshop Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate workshop details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate workshop technical skill API(view)
        Request : Post
        Data = {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_workshop_id": "BroaderAI_resume_contribution_kyzl1fpgsxz5ha0"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateWorkshopTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_workshop_id=getData["candidate_workshop_id"]).exists(): 

                        candidateDetail = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_workshop_id=getData["candidate_workshop_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate workshop technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and workshop technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate workshop technical skill is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopTechnicalSkillsDeleteAPI(APIView):
    '''
        contribution API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_workshop_technical_skill_id": "BroaderAI_workshop_technical_skilllnby3ni9whcpwt8"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateWorkshopTechnicalSkillsModel.objects.filter(candidate_resume_workshop_technical_skill_id = getData["candidate_resume_workshop_technical_skill_id"]).exists():
                    candidateDetail = CandidateWorkshopTechnicalSkillsModel.objects.get(candidate_resume_workshop_technical_skill_id = getData["candidate_resume_workshop_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "workshop technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "workshop technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopGetOneAllDetailsAPI(APIView):

    '''
        Candidate workshop API(view)
        Request : Post
        Data =  {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_workshop_id": "BroaderAI_resume_contribution_kyzl1fpgsxz5ha0"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateWorkshopModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateWorkshopModel.objects.filter( user_id=getData["user_id"], candidate_resume_workshop_id=getData["candidate_resume_workshop_id"]).exists(): 

                        candidateDetail = CandidateWorkshopModel.objects.get(user_id=getData["user_id"], candidate_resume_workshop_id=getData["candidate_resume_workshop_id"])

                        candidatetechnicalskill = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_workshop_id=getData["candidate_resume_workshop_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate workshop Details",
                                "Data": {
                                    "candidate_resume_workshop_id" : getData['candidate_resume_workshop_id'],
                                    "user_id" : getData['user_id'],
                                    "candidate_workshop_organisation_name" :  candidateDetail.candidate_workshop_organisation_name,
                                    "candidate_workshop_organisation_name_arabic" :  candidateDetail.candidate_workshop_organisation_name_arabic,

                                    "candidate_workshop_name" :  candidateDetail.candidate_workshop_name,
                                    "candidate_workshop_name_arabic" :  candidateDetail.candidate_workshop_name_arabic,

                                    "candidate_workshop_type" :  candidateDetail.candidate_workshop_type,
                                    "candidate_workshop_type_arabic" :  candidateDetail.candidate_workshop_type_arabic,

                                    "candidate_workshop_topic" :  candidateDetail.candidate_workshop_topic,
                                    "candidate_workshop_topic_arabic" : candidateDetail.candidate_workshop_topic_arabic,
                                    "candidate_workshop_certificateID" : candidateDetail.candidate_workshop_certificateID,
                                    "candidate_workshop_certificateID_arabic" : candidateDetail.candidate_workshop_certificateID_arabic,

                                    "candidate_workshop_certificateURL" : candidateDetail.candidate_workshop_certificateURL,
                                    "candidate_workshop_duration" : candidateDetail.candidate_workshop_duration,
                                    "candidate_workshop_certificate_issue_date" : candidateDetail.candidate_workshop_certificate_issue_date,
                                    "candidate_workshop_description" : candidateDetail.candidate_workshop_description,
                                    "candidate_workshop_description_arabic" : candidateDetail.candidate_workshop_description_arabic,

                                    "candidate_technical_skills" : candidatetechnicalskill
                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and workshop not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate workshop details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateWorkshopTechnicalSkillsDeleteWorkIdAPI(APIView):
    '''
        contribution API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_workshop_id": "BroaderAI_workshop_technical_skilllnby3ni9whcpwt8"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateWorkshopTechnicalSkillsModel.objects.filter(candidate_workshop_id = getData["candidate_workshop_id"], user_id = getData["user_id"]).exists():
                    candidateDetail = CandidateWorkshopTechnicalSkillsModel.objects.filter(candidate_workshop_id = getData["candidate_workshop_id"], user_id = getData["user_id"])
                    
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "workshop technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "workshop technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
	

#####################################################

#   Seminar APIs (Start)

####################################################

class CandidateSeminarAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_bhramizadafiya1234_ub0okzu3pc

        Key : candidate_seminar_name
        Value : amazon analysis

        Key : candidate_seminar_host
        Value : amazon analysis

        Key : candidate_seminar_type
        Value : amazon analysis

        Key : candidate_seminar_organisation_name
        Value : amazon analysis

        Key : candidate_seminar_mode
        Value : amazon analysis

        Key : candidate_seminar_topic
        Value : amazon analysis
        
        Key : candidate_seminar_certificateID
        Value : gysskjmcos

        Key : candidate_seminar_certificate_issue_date
        Value : 12/12/22

        Key : candidate_seminar_certificateURL
        Value : https://www.merriam-webster.com/dictionary/seminar

        Key : candidate_seminar_participate_certificate
        Value : Files upload....

        Key : candidate_seminar_description
        Value : created in power bi
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data


        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_seminar_" + randomstr

                getData["candidate_seminar_name_arabic"] = "Not Translated"
                getData["candidate_seminar_host_arabic"] = "Not Translated"
                getData["candidate_seminar_type_arabic"] = "Not Translated"
                getData["candidate_seminar_organisation_name_arabic"] = "Not Translated"
                getData["candidate_seminar_mode_arabic"] = "Not Translated"
                getData["candidate_seminar_topic_arabic"] = "Not Translated"
                getData["candidate_seminar_certificateID_arabic"] = "Not Translated"
                getData["candidate_seminar_description_arabic"] = "Not Translated"

                # if is_english(str(getData["candidate_seminar_name"])):
                #     getData["candidate_seminar_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_seminar_name_arabic"] =  getData["candidate_seminar_name"]
                #     getData["candidate_seminar_name"] =  str(translator.translator_en_ar(getData["candidate_seminar_name"], "ar", "en")["translated_text"])

                # if str(getData["candidate_seminar_host"]) != "":

                #     if is_english(str(getData["candidate_seminar_host"])):
                #         getData["candidate_seminar_host_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_host"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_seminar_host_arabic"] =  getData["candidate_seminar_host"]
                #         getData["candidate_seminar_host"] =  str(translator.translator_en_ar(getData["candidate_seminar_host"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_seminar_host_arabic"] =  ""

                # if str(getData["candidate_seminar_type"]) != "":


                #     if is_english(str(getData["candidate_seminar_type"])):
                #         getData["candidate_seminar_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_type"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_seminar_type_arabic"] =  getData["candidate_seminar_type"]
                #         getData["candidate_seminar_type"] =  str(translator.translator_en_ar(getData["candidate_seminar_type"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_seminar_type_arabic"] =  ""

                # if is_english(str(getData["candidate_seminar_organisation_name"])):
                #     getData["candidate_seminar_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_organisation_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_seminar_organisation_name_arabic"] =  getData["candidate_seminar_organisation_name"]
                #     getData["candidate_seminar_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_seminar_organisation_name"], "ar", "en")["translated_text"])
                
                # if str(getData["candidate_seminar_mode"]) != "":


                #     if is_english(str(getData["candidate_seminar_mode"])):
                #         getData["candidate_seminar_mode_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_mode"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_seminar_mode_arabic"] =  getData["candidate_seminar_mode"]
                #         getData["candidate_seminar_mode"] =  str(translator.translator_en_ar(getData["candidate_seminar_mode"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_seminar_mode_arabic"] =  ""

                # if is_english(str(getData["candidate_seminar_topic"])):
                #     getData["candidate_seminar_topic_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_topic"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_seminar_topic_arabic"] =  getData["candidate_seminar_topic"]
                #     getData["candidate_seminar_topic"] =  str(translator.translator_en_ar(getData["candidate_seminar_topic"], "ar", "en")["translated_text"])

                # if str(getData["candidate_seminar_certificateID"]) != "":


                #     if is_english(str(getData["candidate_seminar_certificateID"])):
                #         getData["candidate_seminar_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_certificateID"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_seminar_certificateID_arabic"] =  getData["candidate_seminar_certificateID"]
                #         getData["candidate_seminar_certificateID"] =  str(translator.translator_en_ar(getData["candidate_seminar_certificateID"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_seminar_certificateID_arabic"] =  ""

                # if str(getData["candidate_seminar_description"]) != "":


                #     if is_english(str(getData["candidate_seminar_description"])):
                #         getData["candidate_seminar_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_description"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_seminar_description_arabic"] =  getData["candidate_seminar_description"]
                #         getData["candidate_seminar_description"] =  str(translator.translator_en_ar(getData["candidate_seminar_description"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_seminar_description_arabic"] =  ""


                serializer = CandidateSeminarSerializer(data=getData)
            
                if serializer.is_valid():
                    if getData["candidate_seminar_participate_certificate"] != "":
                        serializer.validated_data['candidate_seminar_participate_certificate'] = getData["candidate_seminar_participate_certificate"]


                    serializer.save(candidate_resume_seminar_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "certificate is successfully uploaded",
                        "Data": {
                            "candidate_resume_seminar_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSeminarUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_seminar_name
        Value : amazon analysis

        Key : candidate_seminar_host
        Value : amazon analysis

        Key : candidate_seminar_type
        Value : amazon analysis

        Key : candidate_seminar_organisation_name
        Value : amazon analysis

        Key : candidate_seminar_mode
        Value : amazon analysis

        Key : candidate_seminar_topic
        Value : amazon analysis
        
        Key : candidate_seminar_certificateID
        Value : gysskjmcos

        Key : candidate_seminar_certificate_issue_date
        Value : 12/12/22

        Key : candidate_seminar_certificateURL
        Value : https://www.merriam-webster.com/dictionary/seminar

        Key : candidate_seminar_participate_certificate
        Value : Files upload....

        Key : candidate_seminar_description
        Value : created in power bi

        Key : candidate_resume_seminar_id
        Value : 

        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateSeminarModel.objects.filter(user_id = getData["user_id"], candidate_resume_seminar_id= getData["candidate_resume_seminar_id"]).exists():

                    getData["candidate_seminar_name_arabic"] = "Not Translated"
                    getData["candidate_seminar_host_arabic"] = "Not Translated"
                    getData["candidate_seminar_type_arabic"] = "Not Translated"
                    getData["candidate_seminar_organisation_name_arabic"] = "Not Translated"
                    getData["candidate_seminar_mode_arabic"] = "Not Translated"
                    getData["candidate_seminar_topic_arabic"] = "Not Translated"
                    getData["candidate_seminar_certificateID_arabic"] = "Not Translated"
                    getData["candidate_seminar_description_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_seminar_name"])):
                    #     getData["candidate_seminar_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_name_arabic"] =  getData["candidate_seminar_name"]
                    #     getData["candidate_seminar_name"] =  str(translator.translator_en_ar(getData["candidate_seminar_name"], "ar", "en")["translated_text"])

                    # if str(getData["candidate_seminar_host"]) != "":

                    #     if is_english(str(getData["candidate_seminar_host"])):
                    #         getData["candidate_seminar_host_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_host"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_seminar_host_arabic"] =  getData["candidate_seminar_host"]
                    #         getData["candidate_seminar_host"] =  str(translator.translator_en_ar(getData["candidate_seminar_host"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_host_arabic"] =  ""

                    # if str(getData["candidate_seminar_type"]) != "":


                    #     if is_english(str(getData["candidate_seminar_type"])):
                    #         getData["candidate_seminar_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_type"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_seminar_type_arabic"] =  getData["candidate_seminar_type"]
                    #         getData["candidate_seminar_type"] =  str(translator.translator_en_ar(getData["candidate_seminar_type"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_type_arabic"] =  ""

                    # if is_english(str(getData["candidate_seminar_organisation_name"])):
                    #     getData["candidate_seminar_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_organisation_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_organisation_name_arabic"] =  getData["candidate_seminar_organisation_name"]
                    #     getData["candidate_seminar_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_seminar_organisation_name"], "ar", "en")["translated_text"])
                    
                    # if str(getData["candidate_seminar_mode"]) != "":
                    
                    #     if is_english(str(getData["candidate_seminar_mode"])):
                    #         getData["candidate_seminar_mode_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_mode"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_seminar_mode_arabic"] =  getData["candidate_seminar_mode"]
                    #         getData["candidate_seminar_mode"] =  str(translator.translator_en_ar(getData["candidate_seminar_mode"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_mode_arabic"] =  ""

                    # if str(getData["candidate_seminar_topic"]) != "":
                    #     if is_english(str(getData["candidate_seminar_topic"])):
                    #         getData["candidate_seminar_topic_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_topic"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_seminar_topic_arabic"] =  getData["candidate_seminar_topic"]
                    #         getData["candidate_seminar_topic"] =  str(translator.translator_en_ar(getData["candidate_seminar_topic"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_topic_arabic"] =  ""

                    # if str(getData["candidate_seminar_certificateID"]) != "":

                    #     if is_english(str(getData["candidate_seminar_certificateID"])):
                    #         getData["candidate_seminar_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_certificateID"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_seminar_certificateID_arabic"] =  getData["candidate_seminar_certificateID"]
                    #         getData["candidate_seminar_certificateID"] =  str(translator.translator_en_ar(getData["candidate_seminar_certificateID"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_certificateID_arabic"] =  ""

                    # if str(getData["candidate_seminar_description"]) != "":

                    #     if is_english(str(getData["candidate_seminar_description"])):
                    #         getData["candidate_seminar_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_seminar_description"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_seminar_description_arabic"] =  getData["candidate_seminar_description"]
                    #         getData["candidate_seminar_description"] =  str(translator.translator_en_ar(getData["candidate_seminar_description"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_seminar_description_arabic"] =  ""

                    serializer = CandidateSeminarSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidateSeminarModel.objects.get(user_id = getData["user_id"], candidate_resume_seminar_id= getData["candidate_resume_seminar_id"])

                        latestcertificate = request.FILES.get('candidate_seminar_participate_certificate')

                        if latestcertificate:

                            if userUpload.candidate_seminar_participate_certificate:
                                userUpload.candidate_seminar_participate_certificate.delete()

                            userUpload.candidate_seminar_participate_certificate = latestcertificate


                        userUpload.candidate_seminar_name = getData["candidate_seminar_name"]
                        userUpload.candidate_seminar_name_arabic = getData["candidate_seminar_name_arabic"]

                        userUpload.candidate_seminar_host = getData["candidate_seminar_host"]
                        userUpload.candidate_seminar_host_arabic = getData["candidate_seminar_host_arabic"]

                        userUpload.candidate_seminar_type = getData["candidate_seminar_type"]
                        userUpload.candidate_seminar_type_arabic = getData["candidate_seminar_type_arabic"]

                        userUpload.candidate_seminar_organisation_name = getData["candidate_seminar_organisation_name"]
                        userUpload.candidate_seminar_organisation_name_arabic = getData["candidate_seminar_organisation_name_arabic"]

                        userUpload.candidate_seminar_mode = getData["candidate_seminar_mode"]
                        userUpload.candidate_seminar_mode_arabic = getData["candidate_seminar_mode_arabic"]

                        userUpload.candidate_seminar_topic = getData["candidate_seminar_topic"]
                        userUpload.candidate_seminar_topic_arabic = getData["candidate_seminar_topic_arabic"]

                        userUpload.candidate_seminar_certificateID = getData["candidate_seminar_certificateID"]
                        userUpload.candidate_seminar_certificateID_arabic = getData["candidate_seminar_certificateID_arabic"]

                        userUpload.candidate_seminar_certificateURL = getData["candidate_seminar_certificateURL"]
                        userUpload.candidate_seminar_certificate_issue_date = getData["candidate_seminar_certificate_issue_date"]
                        userUpload.candidate_seminar_description = getData["candidate_seminar_description"]
                        userUpload.candidate_seminar_description_arabic = getData["candidate_seminar_description_arabic"]

                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "certificate is successfully uploaded",
                            "Data": {
                                "candidate_resume_seminar_id" : getData["candidate_resume_seminar_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSeminarMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_resume_seminar_id
        Value : BroaderAI_resume_seminar_xe8qjoryb0hen6p
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateSeminarModel.objects.filter(user_id = getData["user_id"], candidate_resume_seminar_id= getData["candidate_resume_seminar_id"]).exists():

                    userUpload = CandidateSeminarModel.objects.get(user_id = getData["user_id"], candidate_resume_seminar_id= getData["candidate_resume_seminar_id"])

                    
                    if userUpload.candidate_seminar_participate_certificate:
                        userUpload.candidate_seminar_participate_certificate.delete()

                    userUpload.candidate_seminar_participate_certificate = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "seminar Media is deleted",
                        "Data": {
                            "candidate_resume_seminar_id" : getData["candidate_resume_seminar_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSeminarMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_patelyash2504_pcccyp0m1a

        Key : candidate_resume_seminar_id
        Value : BroaderAI_resume_seminar_xe8qjoryb0hen6p


        Key : candidate_seminar_participate_certificate
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateSeminarModel.objects.filter(user_id = getData["user_id"], candidate_resume_seminar_id= getData["candidate_resume_seminar_id"]).exists():

                
                    userUpload = CandidateSeminarModel.objects.get(user_id = getData["user_id"], candidate_resume_seminar_id= getData["candidate_resume_seminar_id"])

                    latestResume = request.FILES.get('candidate_seminar_participate_certificate')

                    if latestResume:

                        if userUpload.candidate_seminar_participate_certificate:
                            userUpload.candidate_seminar_participate_certificate.delete()

                        userUpload.candidate_seminar_participate_certificate = latestResume

                    else:

                        res = {
                            "Status": "error",
                    "Code": 401,
                    "Message": "Media is not uploaded",
                    "Data":[],
                    }
                        return Response(res, status=status.HTTP_201_CREATED)

                    userUpload.save()
                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_seminar_id" : getData["candidate_resume_seminar_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSeminarGetOneAPI(APIView):
    '''
        Candidate seminars  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_resume_seminar_id": "BroaderAI_resume_seminar_3z6ht1qspmbmlmm"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateSeminarModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateSeminarModel.objects.filter( user_id=getData["user_id"], candidate_resume_seminar_id=getData["candidate_resume_seminar_id"]).exists(): 

                        candidateDetail = CandidateSeminarModel.objects.filter(user_id=getData["user_id"], candidate_resume_seminar_id=getData["candidate_resume_seminar_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate seminars Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and seminars not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate seminars  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSeminarGetAPI(APIView):
    '''
        Candidate seminar API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateSeminarModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateSeminarModel.objects.filter(user_id=getData["user_id"]).values()

                    candidateExp = []


                    for exp in candidateDetail:


                        candidateExp.append(
                            {
                                "candidate_resume_seminar_id" : exp["candidate_resume_seminar_id"],
                                "user_id" : exp["user_id"],
                                "candidate_seminar_name": exp["candidate_seminar_name"],
                                "candidate_seminar_name_arabic": exp["candidate_seminar_name_arabic"],

                                "candidate_seminar_host": exp["candidate_seminar_host"],
                                "candidate_seminar_host_arabic": exp["candidate_seminar_host_arabic"],

                                "candidate_seminar_type": exp["candidate_seminar_type"],
                                "candidate_seminar_type_arabic": exp["candidate_seminar_type_arabic"],

                                "candidate_seminar_organisation_name": exp["candidate_seminar_organisation_name"],
                                "candidate_seminar_organisation_name_arabic": exp["candidate_seminar_organisation_name_arabic"],

                                "candidate_seminar_mode": exp["candidate_seminar_mode"],
                                "candidate_seminar_mode_arabic": exp["candidate_seminar_mode_arabic"],

                                "candidate_seminar_topic": exp["candidate_seminar_topic"],
                                "candidate_seminar_topic_arabic": exp["candidate_seminar_topic_arabic"],

                                "candidate_seminar_certificateID": exp["candidate_seminar_certificateID"],
                                "candidate_seminar_certificateID_arabic": exp["candidate_seminar_certificateID_arabic"],

                                "candidate_seminar_certificateURL": exp["candidate_seminar_certificateURL"],
                                "candidate_seminar_participate_certificate": exp["candidate_seminar_participate_certificate"],
                                "candidate_seminar_certificate_issue_date": exp["candidate_seminar_certificate_issue_date"],
                                "candidate_seminar_description": exp["candidate_seminar_description"],
                                "candidate_seminar_description_arabic": exp["candidate_seminar_description_arabic"]

                            }
                        )


                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate seminars Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate seminars details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateSeminarDeleteAPI(APIView):
    '''
        seminar API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_ub0okzu3pc",
                    "candidate_resume_seminar_id": "BroaderAI_resume_seminar_3z6ht1qspmbmlmm"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateSeminarModel.objects.filter(candidate_resume_seminar_id = getData["candidate_resume_seminar_id"]).exists():
                    candidateDetail = CandidateSeminarModel.objects.get(candidate_resume_seminar_id = getData["candidate_resume_seminar_id"])
                    
                    if candidateDetail.candidate_seminar_participate_certificate:
                        candidateDetail.candidate_seminar_participate_certificate.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "seminar is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "seminar data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  Competition  APIs (Start)

####################################################
class CandidateCompetitionAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_competition_organisation_name
        Value : lenskart
        
        Key : candidate_competition_name
        Value : hackathon

        Key : candidate_competition_type
        Value : pair

        Key: candidate_competition_mode
        Value : online

        Key: candidate_competition_certificateID
        Value : ftgbijmluggf

        Key: candidate_competition_certificateURL
        Value : https://www.merriam-webster.com/dictionary/Competition

        Key : candidate_competition_participate_certificate
        Value : Files upload....

        Key : candidate_competition_certificate_issue_date
        Value : 1/2/23

        Key : candidate_competition_description
        Value : have to complete in one hour
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data


        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_competition_" + randomstr

                getData["candidate_competition_organisation_name_arabic"] = "Not Translated"
                getData["candidate_competition_name_arabic"] = "Not Translated"
                getData["candidate_competition_type_arabic"] = "Not Translated"
                getData["candidate_competition_mode_arabic"] = "Not Translated"
                getData["candidate_competition_certificateID_arabic"] = "Not Translated"
                getData["candidate_competition_description_arabic"] = "Not Translated"

                # if is_english(str(getData["candidate_competition_organisation_name"])):
                #     getData["candidate_competition_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_organisation_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_competition_organisation_name_arabic"] =  getData["candidate_competition_organisation_name"]
                #     getData["candidate_competition_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_competition_organisation_name"], "ar", "en")["translated_text"])

                # if is_english(str(getData["candidate_competition_name"])):
                #     getData["candidate_competition_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_competition_name_arabic"] =  getData["candidate_competition_name"]
                #     getData["candidate_competition_name"] =  str(translator.translator_en_ar(getData["candidate_competition_name"], "ar", "en")["translated_text"])

                # if str(getData["candidate_competition_type"]) != "":


                #     if is_english(str(getData["candidate_competition_type"])):
                #         getData["candidate_competition_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_type"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_competition_type_arabic"] =  getData["candidate_competition_type"]
                #         getData["candidate_competition_type"] =  str(translator.translator_en_ar(getData["candidate_competition_type"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_competition_type_arabic"] =  ""

                # if str(getData["candidate_competition_mode"]) != "":

                #     if is_english(str(getData["candidate_competition_mode"])):
                #         getData["candidate_competition_mode_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_mode"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_competition_mode_arabic"] =  getData["candidate_competition_mode"]
                #         getData["candidate_competition_mode"] =  str(translator.translator_en_ar(getData["candidate_competition_mode"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_competition_mode_arabic"] =  ""

                # if str(getData["candidate_competition_certificateID"]) != "":
                
                #     if is_english(str(getData["candidate_competition_certificateID"])):
                #         getData["candidate_competition_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_certificateID"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_competition_certificateID_arabic"] =  getData["candidate_competition_certificateID"]
                #         getData["candidate_competition_certificateID"] =  str(translator.translator_en_ar(getData["candidate_competition_certificateID"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_competition_certificateID_arabic"] =  ""

                # if str(getData["candidate_competition_description"]) != "":

                #     if is_english(str(getData["candidate_competition_description"])):
                #         getData["candidate_competition_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_description"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_competition_description_arabic"] =  getData["candidate_competition_description"]
                #         getData["candidate_competition_description"] =  str(translator.translator_en_ar(getData["candidate_competition_description"], "ar", "en")["translated_text"])
                # else:
                #     getData["candidate_competition_description_arabic"] =  ""

                serializer = CandidateCompetitionSerializer(data=getData)
            
                if serializer.is_valid():
                    if getData["candidate_competition_participate_certificate"] != "":
                        serializer.validated_data['candidate_competition_participate_certificate'] = getData["candidate_competition_participate_certificate"]

                    serializer.save(candidate_resume_competition_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Competition certificate is successfully uploaded",
                        "Data": {
                            "candidate_resume_competition_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionUpdateAPI(APIView):

    '''{

        Candidate update Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_competition_organisation_name
        Value : lenskart
        
        Key : candidate_competition_name
        Value : hackathon

        Key : candidate_competition_type
        Value : pair

        Key: candidate_competition_mode
        Value : online

        Key: candidate_competition_certificateID
        Value : ftgbijmluggf

        Key: candidate_competition_certificateURL
        Value : https://www.merriam-webster.com/dictionary/Competition

        Key : candidate_competition_participate_certificate
        Value : Files upload....

        Key : candidate_competition_certificate_issue_date
        Value : 1/2/23

        Key : candidate_competition_description
        Value : have to complete in one hour

        Key : candidate_resume_competition_id
        Value : BroaderAI_resume_competition_8xmq7evohd4mh03
        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateCompetitionModel.objects.filter(user_id = getData["user_id"], candidate_resume_competition_id= getData["candidate_resume_competition_id"]).exists():

                    getData["candidate_competition_organisation_name_arabic"] = "Not Translated"
                    getData["candidate_competition_name_arabic"] = "Not Translated"
                    getData["candidate_competition_type_arabic"] = "Not Translated"
                    getData["candidate_competition_mode_arabic"] = "Not Translated"
                    getData["candidate_competition_certificateID_arabic"] = "Not Translated"
                    getData["candidate_competition_description_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_competition_organisation_name"])):
                    #     getData["candidate_competition_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_organisation_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_competition_organisation_name_arabic"] =  getData["candidate_competition_organisation_name"]
                    #     getData["candidate_competition_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_competition_organisation_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_competition_name"])):
                    #     getData["candidate_competition_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_competition_name_arabic"] =  getData["candidate_competition_name"]
                    #     getData["candidate_competition_name"] =  str(translator.translator_en_ar(getData["candidate_competition_name"], "ar", "en")["translated_text"])

                    # if str(getData["candidate_competition_type"]) != "":

                    #     if is_english(str(getData["candidate_competition_type"])):
                    #         getData["candidate_competition_type_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_type"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_competition_type_arabic"] =  getData["candidate_competition_type"]
                    #         getData["candidate_competition_type"] =  str(translator.translator_en_ar(getData["candidate_competition_type"], "ar", "en")["translated_text"])
                    # else:

                    #     getData["candidate_competition_type_arabic"] =  ""

                    # if str(getData["candidate_competition_mode"]) != "":

                    #     if is_english(str(getData["candidate_competition_mode"])):

                    #         getData["candidate_competition_mode_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_mode"], "en", "ar")["translated_text"])

                    #     else:

                    #         getData["candidate_competition_mode_arabic"] =  getData["candidate_competition_mode"]
                    #         getData["candidate_competition_mode"] =  str(translator.translator_en_ar(getData["candidate_competition_mode"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_competition_mode_arabic"] =  ""

                    # if str(getData["candidate_competition_certificateID"]) != "":
                    
                        
                    #     if is_english(str(getData["candidate_competition_certificateID"])):
                    #         getData["candidate_competition_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_certificateID"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_competition_certificateID_arabic"] =  getData["candidate_competition_certificateID"]
                    #         getData["candidate_competition_certificateID"] =  str(translator.translator_en_ar(getData["candidate_competition_certificateID"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_competition_certificateID_arabic"] =  ""

                    # if str(getData["candidate_competition_description"]) != "":
                    

                    #     if is_english(str(getData["candidate_competition_description"])):
                    #         getData["candidate_competition_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_competition_description"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_competition_description_arabic"] =  getData["candidate_competition_description"]
                    #         getData["candidate_competition_description"] =  str(translator.translator_en_ar(getData["candidate_competition_description"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_competition_description_arabic"] =  ""

                    serializer = CandidateCompetitionSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidateCompetitionModel.objects.get(user_id = getData["user_id"], candidate_resume_competition_id= getData["candidate_resume_competition_id"])

                        latestcertificate = request.FILES.get('candidate_competition_participate_certificate')

                        if latestcertificate:

                            if userUpload.candidate_competition_participate_certificate:
                                userUpload.candidate_competition_participate_certificate.delete()

                            userUpload.candidate_competition_participate_certificate = latestcertificate


                        userUpload.candidate_competition_organisation_name = getData["candidate_competition_organisation_name"]
                        userUpload.candidate_competition_organisation_name_arabic = getData["candidate_competition_organisation_name_arabic"]

                        userUpload.candidate_competition_name = getData["candidate_competition_name"]
                        userUpload.candidate_competition_name_arabic = getData["candidate_competition_name_arabic"]

                        userUpload.candidate_competition_type = getData["candidate_competition_type"]
                        userUpload.candidate_competition_type_arabic = getData["candidate_competition_type_arabic"]

                        userUpload.candidate_competition_mode = getData["candidate_competition_mode"]
                        userUpload.candidate_competition_mode_arabic = getData["candidate_competition_mode_arabic"]

                        userUpload.candidate_competition_certificateID = getData["candidate_competition_certificateID"]
                        userUpload.candidate_competition_certificateID_arabic = getData["candidate_competition_certificateID_arabic"]

                        userUpload.candidate_competition_certificateURL = getData["candidate_competition_certificateURL"]
                        userUpload.candidate_competition_certificate_issue_date = getData["candidate_competition_certificate_issue_date"]
                        userUpload.candidate_competition_description = getData["candidate_competition_description"]
                        userUpload.candidate_competition_description_arabic = getData["candidate_competition_description_arabic"]


                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Certificate is successfully uploaded",
                            "Data": {
                                "candidate_resume_competition_id" : getData["candidate_resume_competition_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_competition_id
        Value : BroaderAI_resume_Competition_kyzl1fpgsxz5ha0
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateCompetitionModel.objects.filter(user_id = getData["user_id"], candidate_resume_competition_id= getData["candidate_resume_competition_id"]).exists():

                    userUpload = CandidateCompetitionModel.objects.get(user_id = getData["user_id"], candidate_resume_competition_id= getData["candidate_resume_competition_id"])

                    
                    if userUpload.candidate_competition_participate_certificate:
                        userUpload.candidate_competition_participate_certificate.delete()

                    userUpload.candidate_competition_participate_certificate = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Competition Media is deleted",
                        "Data": {
                            "candidate_resume_competition_id" : getData["candidate_resume_competition_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_competition_id
        Value : BroaderAI_resume_Competition_kyzl1fpgsxz5ha0


        Key : candidate_competition_participate_certificate
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateCompetitionModel.objects.filter(user_id = getData["user_id"], candidate_resume_competition_id= getData["candidate_resume_competition_id"]).exists():

                
                    userUpload = CandidateCompetitionModel.objects.get(user_id = getData["user_id"], candidate_resume_competition_id= getData["candidate_resume_competition_id"])

                    latestcertificate = request.FILES.get('candidate_competition_participate_certificate')

                    if latestcertificate:

                        if userUpload.candidate_competition_participate_certificate:
                            userUpload.candidate_competition_participate_certificate.delete()

                        userUpload.candidate_competition_participate_certificate = latestcertificate

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Media is not uploaded",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)



                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_competition_id" : getData["candidate_resume_competition_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionGetOneAPI(APIView):
    '''
        Candidate Competition  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_competition_id": "BroaderAI_resume_Competition_farw9xjz54p2qmu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCompetitionModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateCompetitionModel.objects.filter( user_id=getData["user_id"], candidate_resume_competition_id=getData["candidate_resume_competition_id"]).exists(): 

                        candidateDetail = CandidateCompetitionModel.objects.filter(user_id=getData["user_id"], candidate_resume_competition_id=getData["candidate_resume_competition_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Competition Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and Competition not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Competition  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]  

class CandidateCompetitionDeleteAPI(APIView):
    '''
        Competition API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_competition_id": "BroaderAI_resume_Competition_farw9xjz54p2qmu"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCompetitionModel.objects.filter(candidate_resume_competition_id = getData["candidate_resume_competition_id"]).exists():
                    candidateDetail = CandidateCompetitionModel.objects.get(candidate_resume_competition_id = getData["candidate_resume_competition_id"])
                    
                    if candidateDetail.candidate_competition_participate_certificate:
                        candidateDetail.candidate_competition_participate_certificate.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Competition is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Competition data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionGetAPI(APIView):
    '''
        Candidate Competition API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_ub0okzu3pc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCompetitionModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateCompetitionModel.objects.filter(user_id=getData["user_id"]).values()

                    candidateExp = []


                    for exp in candidateDetail:

                        techkillExp = CandidateCompetitionTechnicalSkillsModel.objects.filter(candidate_competition_id = exp["candidate_resume_competition_id"]).values()

                    
                        tech = ""
                        techdata = dict()

                        for techskill in techkillExp:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = {
                                "candidate_technical_skill_name": str(techskill["candidate_technical_skill_name"]),
                                # "candidate_job_position_id":  techskill["candidate_job_position_id"],
                                # "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = techskill["candidate_job_position_id"]).job_position_name,
                                # "candidate_job_level_id": techskill["candidate_job_level_id"],
                                # "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = techskill["candidate_job_level_id"]).job_level_name,
                            }

                        tech = tech[:-3]


                        candidateExp.append(
                            {
                                "candidate_resume_competition_id" : exp["candidate_resume_competition_id"],
                                "user_id" : exp["user_id"],
                                
                                "candidate_competition_organisation_name": exp["candidate_competition_organisation_name"],
                                "candidate_competition_organisation_name_arabic": exp["candidate_competition_organisation_name_arabic"],

                                "candidate_competition_name": exp["candidate_competition_name"],
                                "candidate_competition_name_arabic": exp["candidate_competition_name_arabic"],

                                "candidate_competition_type": exp["candidate_competition_type"],
                                "candidate_competition_type_arabic": exp["candidate_competition_type_arabic"],

                                "candidate_competition_mode": exp["candidate_competition_mode"],
                                "candidate_competition_mode_arabic": exp["candidate_competition_mode_arabic"],

                                "candidate_competition_certificateID": exp["candidate_competition_certificateID"],
                                "candidate_competition_certificateID_arabic": exp["candidate_competition_certificateID_arabic"],

                                "candidate_competition_certificateURL": exp["candidate_competition_certificateURL"],
                                "candidate_competition_participate_certificate": exp["candidate_competition_participate_certificate"],
                                "candidate_competition_certificate_issue_date": exp["candidate_competition_certificate_issue_date"],
                                "candidate_competition_description": exp["candidate_competition_description"],
                                "candidate_competition_description_arabic": exp["candidate_competition_description_arabic"],


                                "candidate_technical_skills": tech,
                                "candidate_all_tech": techdata
                            }
                        )

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Competitions Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Competition details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  Competition APIs (End)

####################################################

#####################################################

#  Competition technical skills APIs (Start)

####################################################

class CandidateCompetitionTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate hackathon technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
            "candidate_competition_id": "BroaderAI_resume_Competition_kyzl1fpgsxz5ha0",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y"
        }
    '''
    
    def post(self, request ,formate=None):
        
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_competition_technical_skill_" + randomstr
                # getData["candidate_resume_competition_technical_skill_id"] = uniqueID

                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])
                
                    serializer = CandidateCompetitionTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        
                        serializer.save(candidate_resume_competition_technical_skill_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User Competition technical skill is Added",
                            "Data": {
                                "candidate_resume_competition_technical_skill_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionTechnicalSkillsGetAPI(APIView):
    '''
        Candidate Competition technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Competition Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Competition details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate Competition technical skill API(view)
        Request : Post
        Data = {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_competition_id": "BroaderAI_resume_Competition_kyzl1fpgsxz5ha0"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateCompetitionTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_competition_id=getData["candidate_competition_id"]).exists(): 

                        candidateDetail = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_competition_id=getData["candidate_competition_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Competition technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and Competition technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Competition technical skill is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionTechnicalSkillsDeleteAPI(APIView):
    '''
        Competition API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_competition_technical_skill_id": "BroaderAI_Competition_technical_skill8js72d5jmb3xen7"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCompetitionTechnicalSkillsModel.objects.filter(candidate_resume_competition_technical_skill_id = getData["candidate_resume_competition_technical_skill_id"]).exists():
                    candidateDetail = CandidateCompetitionTechnicalSkillsModel.objects.get(candidate_resume_competition_technical_skill_id = getData["candidate_resume_competition_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Competition technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Competition technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionGetOneAllDetailsAPI(APIView):

    '''
        Candidate Competition API(view)
        Request : Post
        Data =  {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_competition_id": "BroaderAI_resume_competition_ckrj01ew6s7gifm"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateCompetitionModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateCompetitionModel.objects.filter( user_id=getData["user_id"], candidate_resume_competition_id=getData["candidate_resume_competition_id"]).exists(): 

                        candidateDetail = CandidateCompetitionModel.objects.get(user_id=getData["user_id"], candidate_resume_competition_id=getData["candidate_resume_competition_id"])

                        candidatetechnicalskill = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_competition_id=getData["candidate_resume_competition_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Competition Details",
                                "Data": {
                                    "candidate_resume_competition_id" : getData['candidate_resume_competition_id'],
                                    "user_id" : getData['user_id'],
                                    "candidate_competition_organisation_name" :  candidateDetail.candidate_competition_organisation_name,
                                    "candidate_competition_organisation_name_arabic" :  candidateDetail.candidate_competition_organisation_name_arabic,
                                    "candidate_competition_name" : candidateDetail.candidate_competition_name,
                                    "candidate_competition_name_arabic" : candidateDetail.candidate_competition_name_arabic,

                                    "candidate_competition_type" : candidateDetail.candidate_competition_type,
                                    "candidate_competition_type_arabic" : candidateDetail.candidate_competition_type_arabic,

                                    "candidate_competition_mode" : candidateDetail.candidate_competition_mode,
                                    "candidate_competition_mode_arabic" : candidateDetail.candidate_competition_mode_arabic,

                                    "candidate_competition_certificateID" : candidateDetail.candidate_competition_certificateID,
                                    "candidate_competition_certificateID_arabic" : candidateDetail.candidate_competition_certificateID_arabic,

                                    "candidate_competition_certificateURL" : candidateDetail.candidate_competition_certificateURL,
                                    "candidate_competition_certificate_issue_date" : candidateDetail.candidate_competition_certificate_issue_date,
                                    "candidate_competition_description" : candidateDetail.candidate_competition_description,
                                    "candidate_competition_description_arabic" : candidateDetail.candidate_competition_description_arabic,

                                    "candidate_technical_skills" : candidatetechnicalskill
                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and Competition not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Competition details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCompetitionTechnicalSkillsCompIdDeleteAPI(APIView):
    '''
        Competition API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_competition_id": "BroaderAI_Competition_technical_skill8js72d5jmb3xen7"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCompetitionTechnicalSkillsModel.objects.filter(candidate_competition_id = getData["candidate_competition_id"], user_id=getData["user_id"]).exists():
                    candidateDetail = CandidateCompetitionTechnicalSkillsModel.objects.filter(candidate_competition_id = getData["candidate_competition_id"], user_id=getData["user_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Competition technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Competition technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  Competition technical skills APIs (End)

####################################################

#####################################################

#  Certificate  APIs (Start)

####################################################
class CandidateCertificateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_certificate_organisation_name
        Value : lenskart
        
        Key : candidate_certificate_name
        Value : hackathon

        Key: candidate_certificate_certificateID
        Value : ftgbijmluggf

        Key: candidate_certificate_certificateURL
        Value : https://www.merriam-webster.com/dictionary/Certificate

        Key : candidate_certificate_participate_certificate
        Value : Files upload....

        Key : candidate_certificate_issue_date
        Value : 1/2/23

        Key : candidate_certificate_expire_date
        Value : 1/2/23

        Key : candidate_certificate_description
        Value : have to complete in one hour
        }
    
    '''

    def post(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data


        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
            
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_resume_certificate_" + randomstr

                getData["candidate_certificate_organisation_name_arabic"] = "Not Translated"
                getData["candidate_certificate_name_arabic"] = "Not Translated"
                getData["candidate_certificate_certificateID_arabic"] = "Not Translated"
                getData["candidate_certificate_description_arabic"] = "Not Translated"


                # if is_english(str(getData["candidate_certificate_organisation_name"])):
                #     getData["candidate_certificate_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_organisation_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_certificate_organisation_name_arabic"] =  getData["candidate_certificate_organisation_name"]
                #     getData["candidate_certificate_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_certificate_organisation_name"], "ar", "en")["translated_text"])

                # if is_english(str(getData["candidate_certificate_name"])):
                #     getData["candidate_certificate_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_name"], "en", "ar")["translated_text"])

                # else:
                #     getData["candidate_certificate_name_arabic"] =  getData["candidate_certificate_name"]
                #     getData["candidate_certificate_name"] =  str(translator.translator_en_ar(getData["candidate_certificate_name"], "ar", "en")["translated_text"])
                
                # if str(getData["candidate_certificate_certificateID"]) != "":

                #     if is_english(str(getData["candidate_certificate_certificateID"])):
                #         getData["candidate_certificate_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_certificateID"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_certificate_certificateID_arabic"] =  getData["candidate_certificate_certificateID"]
                #         getData["candidate_certificate_certificateID"] =  str(translator.translator_en_ar(getData["candidate_certificate_certificateID"], "ar", "en")["translated_text"])

                # else:

                #     getData["candidate_certificate_certificateID_arabic"] =  ""

                # if str(getData["candidate_certificate_description"]) != "":

                #     if is_english(str(getData["candidate_certificate_description"])):
                #         getData["candidate_certificate_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_description"], "en", "ar")["translated_text"])

                #     else:
                #         getData["candidate_certificate_description_arabic"] =  getData["candidate_certificate_description"]
                #         getData["candidate_certificate_description"] =  str(translator.translator_en_ar(getData["candidate_certificate_description"], "ar", "en")["translated_text"])

                # else:
                #     getData["candidate_certificate_description_arabic"] =  ""


                serializer = CandidateCertificateSerializer(data=getData)
            
                if serializer.is_valid():
                    if getData["candidate_certificate_participate_certificate"] != "":
                        serializer.validated_data['candidate_certificate_participate_certificate'] = getData["candidate_certificate_participate_certificate"]



                    serializer.save(candidate_resume_certificate_id =  uniqueID)

                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Certificate certificate is successfully uploaded",
                        "Data": {
                            "candidate_resume_certificate_id" : uniqueID,
                            "user_id" :  getData["user_id"]
                        }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {"Status": "error",
                            "Code": 400,
                            "Message": list(serializer.errors.values())[0][0], 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateUpdateAPI(APIView):

    '''{

        Candidate update Form-data instead of Json
        request = post
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_certificate_organisation_name
        Value : lenskart
        
        Key : candidate_certificate_name
        Value : hackathon

        Key: candidate_certificate_certificateID
        Value : ftgbijmluggf

        Key: candidate_certificate_certificateURL
        Value : https://www.merriam-webster.com/dictionary/Certificate

        Key : candidate_certificate_participate_certificate
        Value : Files upload....

        Key : candidate_certificate_issue_date
        Value : 1/2/23

        Key : candidate_certificate_expire_date
        Value : 1/2/23

        Key : candidate_certificate_description
        Value : have to complete in one hour

        Key : candidate_resume_certificate_id
        Value : BroaderAI_resume_certificate_8xmq7evohd4mh03
        }
    
    '''

    def patch(self, request, format=None):

        converted_data = dict()

        getData = dict(request.data)

        for key, value in getData.items():
            converted_data[key] = value[0]

        getData = converted_data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateCertificateModel.objects.filter(user_id = getData["user_id"], candidate_resume_certificate_id= getData["candidate_resume_certificate_id"]).exists():

                    getData["candidate_certificate_organisation_name_arabic"] = "Not Translated"
                    getData["candidate_certificate_name_arabic"] = "Not Translated"
                    getData["candidate_certificate_certificateID_arabic"] = "Not Translated"
                    getData["candidate_certificate_description_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_certificate_organisation_name"])):
                    #     getData["candidate_certificate_organisation_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_organisation_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_certificate_organisation_name_arabic"] =  getData["candidate_certificate_organisation_name"]
                    #     getData["candidate_certificate_organisation_name"] =  str(translator.translator_en_ar(getData["candidate_certificate_organisation_name"], "ar", "en")["translated_text"])

                    # if is_english(str(getData["candidate_certificate_name"])):
                    #     getData["candidate_certificate_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_certificate_name_arabic"] =  getData["candidate_certificate_name"]
                    #     getData["candidate_certificate_name"] =  str(translator.translator_en_ar(getData["candidate_certificate_name"], "ar", "en")["translated_text"])
                    
                    # if str(getData["candidate_certificate_certificateID"]) != "":
                    
                    #     if is_english(str(getData["candidate_certificate_certificateID"])):
                    #         getData["candidate_certificate_certificateID_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_certificateID"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_certificate_certificateID_arabic"] =  getData["candidate_certificate_certificateID"]
                    #         getData["candidate_certificate_certificateID"] =  str(translator.translator_en_ar(getData["candidate_certificate_certificateID"], "ar", "en")["translated_text"])

                    # else:
                    #     getData["candidate_certificate_certificateID_arabic"] =  ""


                    # if str(getData["candidate_certificate_description"]) != "":

                    #     if is_english(str(getData["candidate_certificate_description"])):
                    #         getData["candidate_certificate_description_arabic"] =  str(translator.translator_en_ar(getData["candidate_certificate_description"], "en", "ar")["translated_text"])

                    #     else:
                    #         getData["candidate_certificate_description_arabic"] =  getData["candidate_certificate_description"]
                    #         getData["candidate_certificate_description"] =  str(translator.translator_en_ar(getData["candidate_certificate_description"], "ar", "en")["translated_text"])

                    # else:

                    #     getData["candidate_certificate_description_arabic"] =  ""

                    serializer = CandidateCertificateSerializer(data=getData)
                
                    if serializer.is_valid():

            
                        userUpload = CandidateCertificateModel.objects.get(user_id = getData["user_id"], candidate_resume_certificate_id= getData["candidate_resume_certificate_id"])

                        latestcertificate = request.FILES.get('candidate_certificate_participate_certificate')

                        if latestcertificate:

                            if userUpload.candidate_certificate_participate_certificate:
                                userUpload.candidate_certificate_participate_certificate.delete()


                            userUpload.candidate_certificate_participate_certificate = latestcertificate


                        userUpload.candidate_certificate_organisation_name = getData["candidate_certificate_organisation_name"]
                        userUpload.candidate_certificate_name = getData["candidate_certificate_name"]
                        userUpload.candidate_certificate_certificateID = getData["candidate_certificate_certificateID"]
                        userUpload.candidate_certificate_certificateURL = getData["candidate_certificate_certificateURL"]
                        userUpload.candidate_certificate_issue_date = getData["candidate_certificate_issue_date"]
                        userUpload.candidate_certificate_expire_date = getData["candidate_certificate_expire_date"]
                        userUpload.candidate_certificate_description = getData["candidate_certificate_description"]

                        userUpload.save()

                        
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message" : "Certificate is successfully uploaded",
                            "Data": {
                                "candidate_resume_certificate_id" : getData["candidate_resume_certificate_id"],
                                "user_id" :  getData["user_id"],
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateMediaDeleteAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_certificate_id
        Value : BroaderAI_resume_Certificate_kyzl1fpgsxz5ha0
        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateCertificateModel.objects.filter(user_id = getData["user_id"], candidate_resume_certificate_id= getData["candidate_resume_certificate_id"]).exists():

                    userUpload = CandidateCertificateModel.objects.get(user_id = getData["user_id"], candidate_resume_certificate_id= getData["candidate_resume_certificate_id"])

                    
                    if userUpload.candidate_certificate_participate_certificate:
                        userUpload.candidate_certificate_participate_certificate.delete()

                    userUpload.candidate_certificate_participate_certificate = ""


                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Certificate Media is deleted",
                        "Data": {
                            "candidate_resume_certificate_id" : getData["candidate_resume_certificate_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateMediaUpdateAPI(APIView):

    '''{

        Candidate insert Form-data instead of Json
        request = patch
        
        Key : user_id
        Value : BroaderAI_yash.p.yashp_mqkchemr9x

        Key : candidate_resume_certificate_id
        Value : BroaderAI_resume_Certificate_kyzl1fpgsxz5ha0


        Key : candidate_certificate_participate_certificate
        Value : Files upload....

        
        }
    
    '''

    def patch(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id = getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified: 
                
                if CandidateCertificateModel.objects.filter(user_id = getData["user_id"], candidate_resume_certificate_id= getData["candidate_resume_certificate_id"]).exists():

                
                    userUpload = CandidateCertificateModel.objects.get(user_id = getData["user_id"], candidate_resume_certificate_id= getData["candidate_resume_certificate_id"])

                    latestcertificate = request.FILES.get('candidate_certificate_participate_certificate')

                    if latestcertificate:

                        if userUpload.candidate_certificate_participate_certificate:
                            userUpload.candidate_certificate_participate_certificate.delete()

                        userUpload.candidate_certificate_participate_certificate = latestcertificate

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Media is not uploaded",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)



                    userUpload.save()

                    
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message" : "Media is successfully updated",
                        "Data": {
                            "candidate_resume_certificate_id" : getData["candidate_resume_certificate_id"],
                            "user_id" :  getData["user_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                    
                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not exist",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateGetOneAPI(APIView):
    '''
        Candidate Certificate  API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_certificate_id": "BroaderAI_resume_Certificate_farw9xjz54p2qmu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCertificateModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateCertificateModel.objects.filter( user_id=getData["user_id"], candidate_resume_certificate_id=getData["candidate_resume_certificate_id"]).exists(): 

                        candidateDetail = CandidateCertificateModel.objects.filter(user_id=getData["user_id"], candidate_resume_certificate_id=getData["candidate_resume_certificate_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Certificate Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and Certificate not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Certificate  is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]  

class CandidateCertificateGetAPI(APIView):
    '''
        Candidate Certificate API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_ub0okzu3pc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCertificateModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateCertificateModel.objects.filter(user_id=getData["user_id"]).values()

                    candidateExp = []


                    for exp in candidateDetail:

                        techkillExp = CandidateCertificateTechnicalSkillsModel.objects.filter(candidate_certificate_id = exp["candidate_resume_certificate_id"]).values()

                    
                        tech = ""
                        techdata = dict()

                        for techskill in techkillExp:
                            tech = str(techskill["candidate_technical_skill_name"]) + " , " + tech
                            techdata[techskill["candidate_technical_skill_id"]] = {
                                "candidate_technical_skill_name": str(techskill["candidate_technical_skill_name"]),
                                # "candidate_job_position_id":  techskill["candidate_job_position_id"],
                                # "candidate_job_position_name": JobPositionModel.objects.get(job_position_id = techskill["candidate_job_position_id"]).job_position_name,
                                # "candidate_job_level_id": techskill["candidate_job_level_id"],
                                # "candidate_job_level_name": JobLevelModel.objects.get(job_level_id = techskill["candidate_job_level_id"]).job_level_name,
                            }

                        tech = tech[:-3]


                        candidateExp.append(
                            {
                                "candidate_resume_certificate_id" : exp["candidate_resume_certificate_id"],
                                "user_id" : exp["user_id"],
                                
                                "candidate_certificate_organisation_name": exp["candidate_certificate_organisation_name"],
                                "candidate_certificate_organisation_name_arabic": exp["candidate_certificate_organisation_name_arabic"],

                                "candidate_certificate_name": exp["candidate_certificate_name"],
                                "candidate_certificate_name_arabic": exp["candidate_certificate_name_arabic"],

                                "candidate_certificate_certificateID": exp["candidate_certificate_certificateID"],
                                "candidate_certificate_certificateID_arabic": exp["candidate_certificate_certificateID_arabic"],

                                "candidate_certificate_certificateURL": exp["candidate_certificate_certificateURL"],
                                "candidate_certificate_participate_certificate": exp["candidate_certificate_participate_certificate"],
                                "candidate_certificate_issue_date": exp["candidate_certificate_issue_date"],
                                "candidate_certificate_expire_date": exp["candidate_certificate_expire_date"],
                                "candidate_certificate_description": exp["candidate_certificate_description"],
                                "candidate_certificate_description_arabic": exp["candidate_certificate_description_arabic"],

                                "candidate_technical_skills": tech,
                                "candidate_all_tech": techdata
                            }
                        )

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Certificates Details",
                            "Data": candidateExp
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Certificate details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
	
class CandidateCertificateDeleteAPI(APIView):
    '''
        Certificate API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                    "candidate_resume_certificate_id": "BroaderAI_resume_Certificate_farw9xjz54p2qmu"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCertificateModel.objects.filter(candidate_resume_certificate_id = getData["candidate_resume_certificate_id"]).exists():
                    candidateDetail = CandidateCertificateModel.objects.get(candidate_resume_certificate_id = getData["candidate_resume_certificate_id"])
                    
                    if candidateDetail.candidate_certificate_participate_certificate:
                        candidateDetail.candidate_certificate_participate_certificate.delete()
                        
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Certificate is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Certificate data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  Certificate APIs (End)

####################################################

#####################################################

#  Certificate technical skills APIs (Start)

####################################################

class CandidateCertificateTechnicalSkillsRegisterAPI(APIView):
    '''
        Candidate hackathon technical skill(Insert)
        Request : post
        Data = {
            "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
            "candidate_certificate_id": "BroaderAI_resume_Certificate_kyzl1fpgsxz5ha0",
            "candidate_technical_skill_id": "BroaderAI_Technical_Skills_ktwsx4do785vo4y"
        }
    '''
    
    def post(self, request ,formate=None):
        
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin and user.user_is_verified: 

                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_certificate_technical_skill_" + randomstr
                # getData["candidate_resume_certificate_technical_skill_id"] = uniqueID

                if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id= getData['candidate_technical_skill_id']).exists():
                    getData['candidate_technical_skill_name']=TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id= getData['candidate_technical_skill_id']).unique_technical_skills_name

                    getData["candidate_technical_skill_name_arabic"] = "Not Translated"

                    # if is_english(str(getData["candidate_technical_skill_name"])):
                    #     getData["candidate_technical_skill_name_arabic"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "en", "ar")["translated_text"])

                    # else:
                    #     getData["candidate_technical_skill_name_arabic"] =  getData["candidate_technical_skill_name"]
                    #     getData["candidate_technical_skill_name"] =  str(translator.translator_en_ar(getData["candidate_technical_skill_name"], "ar", "en")["translated_text"])
                
                    serializer = CandidateCertificateTechnicalSkillsSerializer(data=getData)
                    if serializer.is_valid():
                        
                        serializer.save(candidate_resume_certificate_technical_skill_id = uniqueID)
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "User Certificate technical skill is Added",
                            "Data": {
                                "candidate_resume_certificate_technical_skill_id": uniqueID,
                                "user_id": getData["user_id"]
                            }
                        }
                        return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Technical Skill is not valid",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateTechnicalSkillsGetAPI(APIView):
    '''
        Candidate Certificate technical skill API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCertificateTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:
                    candidateDetail = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).values()

                    if candidateDetail:
                        # Construct the response dictionary
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Certificate Details",
                            "Data": candidateDetail
                        }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    else:
                        res = {"Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Certificate details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateTechnicalSkillsGetOneAPI(APIView):
    '''
        Candidate Certificate technical skill API(view)
        Request : Post
        Data = {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_certificate_id": "BroaderAI_resume_Certificate_kyzl1fpgsxz5ha0"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            if CandidateCertificateTechnicalSkillsModel.objects.filter(user_id=getData["user_id"]).exists():
                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateCertificateTechnicalSkillsModel.objects.filter( user_id=getData["user_id"], candidate_certificate_id=getData["candidate_certificate_id"]).exists(): 

                        candidateDetail = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_certificate_id=getData["candidate_certificate_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Certificate technical skills Details",
                                "Data": candidateDetail
                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and Certificate technical skills not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Certificate technical skill is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateTechnicalSkillsDeleteAPI(APIView):
    '''
        Certificate API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_certificate_technical_skill_id": "BroaderAI_Certificate_technical_skill8js72d5jmb3xen7"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCertificateTechnicalSkillsModel.objects.filter(candidate_resume_certificate_technical_skill_id = getData["candidate_resume_certificate_technical_skill_id"]).exists():
                    candidateDetail = CandidateCertificateTechnicalSkillsModel.objects.get(candidate_resume_certificate_technical_skill_id = getData["candidate_resume_certificate_technical_skill_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Certificate technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Certificate technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateGetOneAllDetailsAPI(APIView):

    '''
        Candidate Certificate API(view)
        Request : Post
        Data =  {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_resume_certificate_id": "BroaderAI_resume_certificate_ckrj01ew6s7gifm"
            }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateCertificateModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin and user.user_is_verified:

                    if CandidateCertificateModel.objects.filter( user_id=getData["user_id"], candidate_resume_certificate_id=getData["candidate_resume_certificate_id"]).exists(): 

                        candidateDetail = CandidateCertificateModel.objects.get(user_id=getData["user_id"], candidate_resume_certificate_id=getData["candidate_resume_certificate_id"])

                        candidatetechnicalskill = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id=getData["user_id"], candidate_certificate_id=getData["candidate_resume_certificate_id"]).values()

                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Certificate Details",
                                "Data": {
                                    "candidate_resume_certificate_id" : getData['candidate_resume_certificate_id'],
                                    "user_id" : getData['user_id'],
                                    "candidate_certificate_organisation_name" :  candidateDetail.candidate_certificate_organisation_name,
                                    "candidate_certificate_organisation_name_arabic" :  candidateDetail.candidate_certificate_organisation_name_arabic,

                                    "candidate_certificate_name" : candidateDetail.candidate_certificate_name,
                                    "candidate_certificate_name_arabic" : candidateDetail.candidate_certificate_name_arabic,

                                    "candidate_certificate_certificateID" : candidateDetail.candidate_certificate_certificateID,
                                    "candidate_certificate_certificateID_arabic" : candidateDetail.candidate_certificate_certificateID_arabic,

                                    "candidate_certificate_certificateURL" : candidateDetail.candidate_certificate_certificateURL,
                                    "candidate_certificate_issue_date" : candidateDetail.candidate_certificate_issue_date,
                                    "candidate_certificate_expire_date" : candidateDetail.candidate_certificate_expire_date,
                                    "candidate_certificate_description" : candidateDetail.candidate_certificate_description,
                                    "candidate_certificate_description_arabic" : candidateDetail.candidate_certificate_description_arabic,

                                    "candidate_technical_skills" : candidatetechnicalskill
                                },

                            }
                            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                        else:
                            res = {"Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User and Certificate not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[],
                        }
                    return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Candidate Certificate details is not found", "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateCertificateTechnicalSkillsCertIdDeleteAPI(APIView):
    '''
        Certificate API(delete)
        Request : delete
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "candidate_certificate_id": "BroaderAI_Certificate_technical_skill8js72d5jmb3xen7"
            }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCertificateTechnicalSkillsModel.objects.filter(candidate_certificate_id = getData["candidate_certificate_id"]).exists():
                    candidateDetail = CandidateCertificateTechnicalSkillsModel.objects.filter(candidate_certificate_id = getData["candidate_certificate_id"])
                    candidateDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Certificate technical skill is successfully Deleted",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Certificate technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data":[],
                    }
                return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data":[],
                }
            return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################

#  Certificate technical skills APIs (End)

####################################################


# class CandidateResumeParsingAPI(APIView):

#     '''  
#     Candidate Resume Parsing API (POST)
#     Data =   {
#             "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
#             "candidate_resume": "BroaderAI_Certificate_technical_skill8js72d5jmb3xen7"
#         }
    
#     '''

#     def post(self, request, format=None):


#         getData = request.data

        
#         if NewUser.objects.filter(id = getData["user_id"]).exists():

#             user = NewUser.objects.get(id = getData["user_id"])


#             basicInfo = getBasicinformation(getData["candidate_resume"])

            
#             res = {"Status": "success",
                    # "Code": 201,
#                 "Message" : "Resume data is extaracted successfully!!" ,
#                 "Data" : {
#                         "Basic_information": basicInfo
#                     }
#                 }  

#             return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)

#         else:

#             res = {
# "Status": "error",
                    # "Code": 401,
                    # "Message": "User is not found",
                    # "Data":[],
                    # }
#             return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)


