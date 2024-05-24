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
import datetime

###########################################################################

class CandidatePreferenceAPI(APIView):
    '''
        CandidatePreference API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr"
                }
    '''
    def post(self, request ,format=None):
        
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
           
          
            if not CandidatePreferenceModel.objects.filter(user_id= getData["user_id"]).exists():

                if JobPositionModel.objects.filter(job_position_id= getData["job_position_id"]).exists():

                    if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

                        if not CandidatePreferenceModel.objects.filter(user_id= getData["user_id"], job_position_id= getData["job_position_id"], job_level_id= getData["job_level_id"]).exists():
                            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))
                                            
                            uniqueID = "BroaderAI_candidate_preference_" + randomstr

                            getData["candidate_preference_id"] = uniqueID

                            # if "candidate_preference_registration_date" not in getData:
                            #     getData["candidate_preference_registration_date"] = datetime.datetime.now()



                            serializer = CandidatePreferenceSerializer(data=getData)

                            if serializer.is_valid():

                                serializer.save(candidate_preference_id=getData["candidate_preference_id"])

                                prefdata = CandidatePreferenceModel.objects.get(candidate_preference_id=getData["candidate_preference_id"])

                                if "candidate_preference_registration_date" in getData:
                                    prefdata.candidate_preference_registration_date = getData["candidate_preference_registration_date"]
                                    prefdata.save()

                                res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Candidate is Added",
                                    "Data": {
                                        "candidate_preference_id": getData["candidate_preference_id"]
                                    }
                                }
                                return Response(res, status=status.HTTP_201_CREATED)

                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 400,
                                    "Message": list(serializer.errors.values())[0][0], 
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Data is already exists",
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
                    "Message": "Candidate Preference is already exits",
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

class CandidatePreferenceUpdateAPI(APIView):
    '''
        CandidatePreference API(Insert)
        Request : patch
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
          
                if CandidatePreferenceModel.objects.filter(user_id= getData["user_id"]).exists():

                    if JobPositionModel.objects.filter(job_position_id= getData["job_position_id"]).exists():

                        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

                            serializer = CandidatePreferenceSerializer(data=getData)

                            if serializer.is_valid():
                                updateData = CandidatePreferenceModel.objects.get(user_id = getData["user_id"])
                                updateData.user_id = getData["user_id"]
                                updateData.job_position_id = getData["job_position_id"]
                                updateData.job_level_id = getData["job_level_id"]
                                updateData.save()
                                res = {
                                    "Status": "success",
                                    "Code": 201,
                                    "Message": "Candidate is Updated",
                                    "Data": getData
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
                                "Message": "Job Level is not exits",
                                "Data":[],}
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
                        "Message": "Candidate Preference is already exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidatePreferenceGetAPI(APIView):
    '''
        CandidatePreference API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        candidatePreferenceDetails = CandidatePreferenceModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Preference Details",
                "Data": candidatePreferenceDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
        
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatePreferenceGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidatePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidatePreferenceDetail = CandidatePreferenceModel.objects.get(user_id = getData["user_id"])

                    job_position_name = JobPositionModel.objects.get(job_position_id = candidatePreferenceDetail.job_position_id).job_position_name

                    job_level_name = JobLevelModel.objects.get(job_level_id = candidatePreferenceDetail.job_level_id).job_level_name
                
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Preference Field Detail",
                            "Data": {
                                "user_id": getData["user_id"],
                                "candidate_preference_id": candidatePreferenceDetail.candidate_preference_id,
                                "job_position_id": candidatePreferenceDetail.job_position_id,
                                "job_level_id": candidatePreferenceDetail.job_level_id,
                                "job_position_name": job_position_name,
                                "job_level_name": job_level_name
                            }
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Candidate Preference Field data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidatePreferenceDeleteAPI(APIView):
    '''
        CandidatePreference API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:
                
                if JobPositionModel.objects.filter(job_position_id= getData["job_position_id"]).exists():

                        if JobLevelModel.objects.filter(job_level_id= getData["job_level_id"]).exists():

                            if CandidatePreferenceModel.objects.filter(job_position_id= getData["job_position_id"], job_level_id= getData["job_level_id"], user_id = getData["user_id"]).exists():

                                CandidatePreferenceDetail = CandidatePreferenceModel.objects.get(job_position_id= getData["job_position_id"], job_level_id= getData["job_level_id"], user_id = getData["user_id"])
                                CandidatePreferenceDetail.delete()
                                res = {
                                        "Status": "success",
                                        "Code": 201,
                                        "Message": "Candidate job position and level is successfully Deleted",
                                        "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Candidate job position and level data is not found",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "job Level data is not found",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "job position data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#################################################################################


class CandidateEmploymentTypePreferenceAPI(APIView):
    '''
        Candidate employment type Preference API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "employment_type_id": "BroaderAI_Employment_Type_8iriq04aqtr67xb"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
           
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:

                if EmploymentTypeModel.objects.filter(employment_type_id = getData["employment_type_id"]).exists():

                    if not CandidateEmploymentTypePreferenceModel.objects.filter(employment_type_id = getData["employment_type_id"], user_id = getData["user_id"] ).exists():
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                        
                        uniqueID = "BroaderAI_candidate_employment_type_preference_" + randomstr
                        getData["candidate_employment_type_preference_id"] = uniqueID

                        employmentTypeData= EmploymentTypeModel.objects.get(employment_type_id = getData["employment_type_id"])
                        getData["employment_type_name"] = employmentTypeData.employment_type_name
                        
                        
                        serializer = CandidateEmploymentTypePreferenceSerializer(data=getData)
                        if serializer.is_valid():

                            serializer.save(candidate_employment_type_preference_id=getData["candidate_employment_type_preference_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Employment Type is Added",
                                "Data": {
                                    "candidate_employment_type_preference_id": getData["candidate_employment_type_preference_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Data is Already exists",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Employment Type id is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateEmploymentTypePreferenceGetAPI(APIView):
    '''
        CandidateEmploymentTypePreference API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        CandidateEmploymentTypePreferenceDetails = CandidateEmploymentTypePreferenceModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "CandidateEmploymentType Preference Details",
                "Data": CandidateEmploymentTypePreferenceDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateEmploymentTypePreferenceGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateEmploymentTypePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateEmploymentTypePreferenceDetail = CandidateEmploymentTypePreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "CandidateEmploymentType Preference Field Detail",
                            "Data": candidateEmploymentTypePreferenceDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "error",
                            "Code": 204,
                            "Message": "Candidate Employment Type Preference Field data is not found",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateEmploymentTypePreferenceDeleteAPI(APIView):
    '''
        CandidateEmploymentTypePreference API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "employment_type_id": "BroaderAI_Employment_Type_8iriq04aqtr67xb"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if EmploymentTypeModel.objects.filter(employment_type_id = getData["employment_type_id"]).exists():

                    if CandidateEmploymentTypePreferenceModel.objects.filter(employment_type_id = getData["employment_type_id"], user_id = getData["user_id"]).exists():
                        candidateEmploymentTypePreferenceDetail = CandidateEmploymentTypePreferenceModel.objects.get(employment_type_id = getData["employment_type_id"], user_id = getData["user_id"])
                        candidateEmploymentTypePreferenceDetail.delete()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Employment Type is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                        "Code": 401,
                            "Message": "Candidate Employment Type data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Employment Type data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#################################################################################

class CandidatePreferenceLocationAPI(APIView):
    '''
        CandidatePreference Location API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "location_id": "BroaderAI_location_739ueon6v5x9m35"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
           
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:
                if LocationModel.objects.filter(location_id = getData["location_id"]).exists():

                    if not CandidatePreferenceLocationModel.objects.filter(location_id = getData["location_id"], user_id = getData["user_id"] ).exists():
           
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                        
                        uniqueID = "BroaderAI_candidate_preference_location_" + randomstr
                        getData["candidate_preference_location_id"] = uniqueID

                        locationData= LocationModel.objects.get(location_id = getData["location_id"])
                        getData["location_name"] = locationData.location_name

                        serializer = CandidatePreferenceLocationSerializer(data=getData)

                        if serializer.is_valid():

                            serializer.save(candidate_preference_location_id=getData["candidate_preference_location_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Location is Added",
                                "Data": {
                                    "candidate_preference_location_id": getData["candidate_preference_location_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Data is Already exists",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Location id is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidatePreferenceLocationGetAPI(APIView):

    '''
        CandidatePreference Location API(View)
        Request : GET
    '''
    def post(self, request, format=None):
        getData = request.data
        candidatePreferenceLocationDetails = CandidatePreferenceLocationModel.objects.values()

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Preference Location Details",
                "Data": candidatePreferenceLocationDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatePreferenceLocationGetOneAPI(APIView):

    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
    
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            
            if user.user_is_loggedin and user.user_is_verified:

                if CandidatePreferenceLocationModel.objects.filter(user_id = getData["user_id"]).exists():

                    candidatePreferenceLocationDetail = CandidatePreferenceLocationModel.objects.filter(user_id = getData["user_id"]).values()
                
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate location Preference Field Detail",
                            "Data": candidatePreferenceLocationDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

                else:

                    res = {
                            "Status": "error",
                            "Code": 204,
                            "Message": "Candidate location Type Preference Field data is not found",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidatePreferenceLocationDeleteAPI(APIView):
    '''
        CandidatePreferenceLocation API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "location_id": "BroaderAI_location_739ueon6v5x9m35"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if LocationModel.objects.filter(location_id = getData["location_id"]).exists():

                    if CandidatePreferenceLocationModel.objects.filter(location_id = getData["location_id"], user_id = getData["user_id"]).exists():
                        CandidatePreferenceLocationDetail = CandidatePreferenceLocationModel.objects.get(location_id = getData["location_id"], user_id = getData["user_id"])  
                        CandidatePreferenceLocationDetail.delete()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate location is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate location data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "location data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#################################################################################

class CandidateCompanyPreferenceAPI(APIView):
    '''
        Candidate Company type Preference API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "company_type_id": "BroaderAI_Company_Type_m9af27doac0zw8e"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
           
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:
                if CompanyTypeModel.objects.filter(company_type_id = getData["company_type_id"]).exists():

                    if not CandidateCompanyPreferenceModel.objects.filter(company_type_id = getData["company_type_id"], user_id = getData["user_id"] ).exists():
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                        
                        uniqueID = "BroaderAI_candidate_company_type_preference_" + randomstr
                        getData["candidate_company_preference_id"] = uniqueID

                        companyTypeData= CompanyTypeModel.objects.get(company_type_id = getData["company_type_id"])
                        getData["company_type_name"] = companyTypeData.company_type_name
                        
                        serializer = CandidateCompanyPreferenceSerializer(data=getData)

                        if serializer.is_valid():

                            serializer.save(candidate_company_preference_id=getData["candidate_company_preference_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Company Type is Added",
                                "Data": {
                                    "candidate_company_preference_id": getData["candidate_company_preference_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Data is Already exists",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company Type id is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateCompanyPreferenceGetOneAPI(APIView):

    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCompanyPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateCompanyPreferenceDetail = CandidateCompanyPreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Company Preference Field Detail",
                            "Data": candidateCompanyPreferenceDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "error",
                            "Code": 204,
                            "Message": "Candidate Company Preference Field data is not found",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateCompanyPreferenceDeleteAPI(APIView):

    '''
        Candidate Company Preference API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "company_type_id": "BroaderAI_Company_Type_ijtrhi3v4hrtiyf"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CompanyTypeModel.objects.filter(company_type_id = getData["company_type_id"]).exists():

                    if CandidateCompanyPreferenceModel.objects.filter(company_type_id = getData["company_type_id"], user_id = getData["user_id"]).exists():
                        candidateCompanyPreferenceDetail = CandidateCompanyPreferenceModel.objects.get(company_type_id = getData["company_type_id"], user_id = getData["user_id"])
                        candidateCompanyPreferenceDetail.delete()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Company type is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate Company type data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Company type data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

######################################################################################

class CandidateCompanySectorPreferenceAPI(APIView):
    '''
        Candidate employment type Preference API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "sector_id": "BroaderAI_sector_dwmfjrii16aibmd"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
           
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:

                print(getData["sector_id"])
                if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():

                    if not CandidateCompanySectorPreferenceModel.objects.filter(sector_id = getData["sector_id"], user_id = getData["user_id"] ).exists():
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                        
                        uniqueID = "BroaderAI_candidate_company_sector_preference_" + randomstr
                        getData["candidate_company_sector_preference_id"] = uniqueID

                        sectorData= SectorModel.objects.get(sector_id = getData["sector_id"])
                        getData["sector_name"] = sectorData.sector_name
                        
                        serializer = CandidateCompanySectorPreferenceSerializer(data=getData)

                        if serializer.is_valid():

                            serializer.save(candidate_company_sector_preference_id=getData["candidate_company_sector_preference_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate company sector is Added",
                                "Data": {
                                    "candidate_company_sector_preference_id": getData["candidate_company_sector_preference_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Data is Already exists",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "company sector id is not exists",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateCompanySectorPreferenceGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateCompanySectorPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateCompanySectorPreferenceDetail = CandidateCompanySectorPreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Company Sector Preference Field Detail",
                            "Data": candidateCompanySectorPreferenceDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "error",
                            "Code": 204,
                            "Message": "Candidate Company Sector Preference Field data is not found",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateCompanySectorPreferenceDeleteAPI(APIView):
    '''
        CandidateCompanySectorPreference API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "sector_id": "BroaderAI_sector_nfpfnwo1d3698ak"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():

                    if CandidateCompanySectorPreferenceModel.objects.filter(sector_id = getData["sector_id"], user_id = getData["user_id"]).exists():
                        candidateCompanySectorPreferenceDetail = CandidateCompanySectorPreferenceModel.objects.get(sector_id = getData["sector_id"], user_id = getData["user_id"])
                        candidateCompanySectorPreferenceDetail.delete()
                        res = {
                               "Status": "success",
                                "Code": 201,
                                "Message": "Candidate company sector is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate company sector data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "company sector data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]    

#####################################################################################

class CandidateWorkplacePreferenceAPI(APIView):
    '''
        Candidate employment type Preference API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "work_place_id": "BroaderAI_Employment_Type_8iriq04aqtr67xb"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
           
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:
                if WorkPlaceModel.objects.filter(work_place_id = getData["work_place_id"]).exists():

                    if not CandidateWorkplacePreferenceModel.objects.filter(work_place_id = getData["work_place_id"], user_id = getData["user_id"] ).exists():
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                        
                        uniqueID = "BroaderAI_candidate_workplace_preference_" + randomstr
                        getData["candidate_workplace_preference_id"] = uniqueID

                        WorkplaceData= WorkPlaceModel.objects.get(work_place_id = getData["work_place_id"])
                        getData["work_place_name"] = WorkplaceData.work_place_name
                        
                        serializer = CandidateWorkplacePreferenceSerializer(data=getData)

                        if serializer.is_valid():

                            serializer.save(candidate_workplace_preference_id=getData["candidate_workplace_preference_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Work Place is Added",
                                "Data": {
                                    "candidate_workplace_preference_id": getData["candidate_workplace_preference_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Data is Already exists",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Work Place id is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateWorkplacePreferenceGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateWorkplacePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateWorkplacePreferenceDetail = CandidateWorkplacePreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Work place Preference Field Detail",
                            "Data": candidateWorkplacePreferenceDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "error",
                            "Code": 204,
                            "Message": "Candidate Work Place Preference Field data is not found",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateWorkplacePreferenceDeleteAPI(APIView):
    '''
        CandidateWorkplacePreference API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "work_place_id": "BroaderAI_Work_Place_fgwxtimk0gq8lkq"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if WorkPlaceModel.objects.filter(work_place_id = getData["work_place_id"]).exists():

                    if CandidateWorkplacePreferenceModel.objects.filter(work_place_id = getData["work_place_id"], user_id = getData["user_id"]).exists():
                        candidateWorkplacePreferenceDetail = CandidateWorkplacePreferenceModel.objects.get(work_place_id = getData["work_place_id"], user_id = getData["user_id"])
                        candidateWorkplacePreferenceDetail.delete()
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Work Place is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate Work Place data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Work Place data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

#####################################################################################

class CandidateJoiningPeriodPreferenceAPI(APIView):
    '''
        Candidate Joining Period Preference API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "joining_period_id": "BroaderAI_Joining_Period_k96lqld1ahb2ord"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
           
            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:
                if JoiningPeriodModel.objects.filter(joining_period_id = getData["joining_period_id"]).exists():

                    if not CandidateJoiningPeriodPreferenceModel.objects.filter(joining_period_id = getData["joining_period_id"], user_id = getData["user_id"] ).exists():
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                                        
                        uniqueID = "BroaderAI_candidate_joining_period_preference_" + randomstr
                        getData["candidate_joining_period_preference_id"] = uniqueID

                        JoiningPeriodData= JoiningPeriodModel.objects.get(joining_period_id = getData["joining_period_id"])
                        getData["joining_period_name"] = JoiningPeriodData.joining_period_name
                        
                        serializer = CandidateJoiningPeriodPreferenceSerializer(data=getData)

                        if serializer.is_valid():

                            serializer.save(candidate_joining_period_preference_id=getData["candidate_joining_period_preference_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Joining Period is Added",
                                "Data": {
                                    "candidate_joining_period_preference_id": getData["candidate_joining_period_preference_id"]
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": list(serializer.errors.values())[0][0], 
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Data is Already exists",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Joining Period id is not exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateJoiningPeriodPreferenceGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateJoiningPeriodPreferenceDetail = CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = getData["user_id"]).values()
                
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "CandidateJoiningPeriod Preference Field Detail",
                            "Data": candidateJoiningPeriodPreferenceDetail
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "error",
                            "Code": 204,
                            "Message": "Candidate Joining Period Preference Field data is not found",
                            "Data": []
                        }

                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

class CandidateJoiningPeriodPreferenceDeleteAPI(APIView):
    '''
        CandidateJoiningPeriodPreference API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem",
                    "joining_period_id": "BroaderAI_Joining_Period_k96lqld1ahb2ord"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])
            if user.user_is_loggedin and user.user_is_verified:

                if JoiningPeriodModel.objects.filter(joining_period_id = getData["joining_period_id"]).exists():

                    if CandidateJoiningPeriodPreferenceModel.objects.filter(joining_period_id = getData["joining_period_id"], user_id = getData["user_id"]).exists():

                        candidateJoiningPeriodPreferenceDetail = CandidateJoiningPeriodPreferenceModel.objects.get(joining_period_id = getData["joining_period_id"], user_id = getData["user_id"])
                        candidateJoiningPeriodPreferenceDetail.delete()

                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate Joining Period is successfully Deleted",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Candidate Joining Period data is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Joining Period data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

######################################################################################

class CandidatePreferenceResetDeleteAPI(APIView):
    '''
        Candidate Preference reset API(delete)
        Request : delete
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    ''' 
    def delete(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:

                # if CandidatePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                #     candidateJoiningPeriodPreferenceDetail = CandidatePreferenceModel.objects.filter(user_id = getData["user_id"])
                #     candidateJoiningPeriodPreferenceDetail.delete()

                if CandidateEmploymentTypePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateEmploymentTypePreferenceDetail = CandidateEmploymentTypePreferenceModel.objects.filter(user_id = getData["user_id"])
                    candidateEmploymentTypePreferenceDetail.delete()

                if CandidatePreferenceLocationModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidatePreferenceLocationDetail = CandidatePreferenceLocationModel.objects.filter(user_id = getData["user_id"])
                    candidatePreferenceLocationDetail.delete()

                if CandidateCompanyPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateCompanyPreferenceDetail = CandidateCompanyPreferenceModel.objects.filter(user_id = getData["user_id"])
                    candidateCompanyPreferenceDetail.delete()

                if CandidateCompanySectorPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateCompanySectorPreferenceDetail = CandidateCompanySectorPreferenceModel.objects.filter(user_id = getData["user_id"])
                    candidateCompanySectorPreferenceDetail.delete()

                if CandidateWorkplacePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateWorkplacePreferenceDetail = CandidateWorkplacePreferenceModel.objects.filter(user_id = getData["user_id"])
                    candidateWorkplacePreferenceDetail.delete()

                if CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = getData["user_id"]).exists():
                    candidateJoiningPeriodPreferenceDetail = CandidateJoiningPeriodPreferenceModel.objects.filter(user_id = getData["user_id"])
                    candidateJoiningPeriodPreferenceDetail.delete()

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User is not loggedin",
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

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidatePreferenceGetAllAPI(APIView):
    '''
        Candidate Preference reset API(post)
        Request : post
        Data =  {
                    "user_id": "BroaderAI_bhramizadafiya1234_vatrra5lem"
                }
    '''
    def post(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():

            user = NewUser.objects.get(id=getData["user_id"])

            if user.user_is_loggedin and user.user_is_verified:

                if CandidatePreferenceModel.objects.filter(user_id = getData["user_id"]).exists():

                    if CandidatePreferenceModel.objects.filter(user_id=getData["user_id"]).exists():

                        candidatePreferenceDetail = CandidatePreferenceModel.objects.filter(user_id = getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    if CandidateEmploymentTypePreferenceModel.objects.filter(user_id=getData["user_id"]).exists():
                        candidateEmpTypeDetail = CandidateEmploymentTypePreferenceModel.objects.filter(user_id=getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    if CandidatePreferenceLocationModel.objects.filter(user_id=getData["user_id"]).exists():
                        candidateLocationDetail = CandidatePreferenceLocationModel.objects.filter(user_id=getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    if CandidateCompanyPreferenceModel.objects.filter(user_id=getData["user_id"]).exists():
                        candidateCompTypeDetail = CandidateCompanyPreferenceModel.objects.filter(user_id=getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    if CandidateCompanySectorPreferenceModel.objects.filter(user_id=getData["user_id"]).exists():
                        candidateCompsectorDetail = CandidateCompanySectorPreferenceModel.objects.filter(user_id=getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    if CandidateWorkplacePreferenceModel.objects.filter(user_id=getData["user_id"]).exists():
                        candidateWorkPlaceDetail = CandidateWorkplacePreferenceModel.objects.filter(user_id=getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    if CandidateJoiningPeriodPreferenceModel.objects.filter(user_id=getData["user_id"]).exists():
                        candidatejointimeDetail = CandidateJoiningPeriodPreferenceModel.objects.filter(user_id=getData["user_id"]).values()

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "User not found",
                            "Data":[],
                            }
                        return Response(res, content_type='application/json', status=status.HTTP_201_CREATED)
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate Preference Details:",
                            "Data" : {
                                "candidatePreferenceDetail" : candidatePreferenceDetail,
                                "candidateEmpTypeDetail" : candidateEmpTypeDetail,
                                "candidateLocationDetail" : candidateLocationDetail,
                                "candidateCompTypeDetail" : candidateCompTypeDetail,
                                "candidateCompSectorDetail" : candidateCompsectorDetail,
                                "candidateWorkplaceDetail" : candidateWorkPlaceDetail,
                                "candidatejointimeDetail" :candidatejointimeDetail
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
                    "Message": "User is not loggedIn",
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
