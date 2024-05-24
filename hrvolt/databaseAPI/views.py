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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
#######################################
#######################################

class SectorAPI(APIView):
    '''
        Sector API(INSERT)
        Request : POST
        Data =  {
                    "sector_name": "Health care",
                    "sector_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not SectorModel.objects.filter(sector_name=getData["sector_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_sector_" + randomstr
            getData["sector_id"] = uniqueID
            serializer = SectorSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(sector_id=getData["sector_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Sector is Added",
                    "Data": {   "sector_id" : getData['sector_id']
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
                    "Message": "Sector is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class SectorUpdateAPI(APIView):
    '''
        Sector API(Update)
        Request : Patch
        Data =  {
                    "sector_id": "BroaderAI_sector_m8kbwab2rehksfm",
                    "sector_name": "Information Technology",
                    "sector_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not SectorModel.objects.filter(sector_name=getData["sector_name"].lower()).exists():

            if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():
                serializer = SectorSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = SectorModel.objects.get(sector_id = getData["sector_id"])
                    LastUpdateData.sector_name=getData["sector_name"].lower()
                    LastUpdateData.sector_action = getData["sector_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Sector is Updated",
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
                    "Message": "Sector data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class SectorGetAPI(APIView):
    '''
        Sector API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        sectorDetails = SectorModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Sector Details",
                "Data": sectorDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class SectorGetOneAPI(APIView):
    '''
        Get One Sector API(View)
        Request : POST
        Data =  {
                    "sector_id": "BroaderAI_sector_ks5th0xuavqnehs"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():
            sectorDetail = SectorModel.objects.get(sector_id = getData["sector_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Sector Detail",
                    "Data": {
                        "sector_id": getData["sector_id"],
                        "sector_name": sectorDetail.sector_name,
                        "sector_action": sectorDetail.sector_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class SectorGetActionAPI(APIView):
    '''
        Get Action Sector API(View)
        Request : POST
        Data =  {
                    "sector_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        sectorDetails = SectorModel.objects.filter(sector_action = getData["sector_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Sector Detail",
                "Data": sectorDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class SectorDeleteAPI(APIView):
    '''
        Sector API(delete)
        Request : delete
        Data =  {
                    "sector_id":"BroaderAI_sector_ks5th0xuavqnehs"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():
            sectorDetail = SectorModel.objects.get(sector_id = getData["sector_id"])
            sectorDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Sector is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class SectorGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        sectorDetails = SectorModel.objects.all()
        if search_query:
            sectorDetails = sectorDetails.filter(Q(sector_name__istartswith=search_query))

        paginator = Paginator(sectorDetails, limit)
        try:
            sectorDetails = paginator.page(page)
        except PageNotAnInteger:
            sectorDetails = paginator.page(1)
        except EmptyPage:
            sectorDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'sector_id': sector.sector_id, 'sector_name': sector.sector_name,'sector_name_arabic':sector.sector_name_arabic,
                            'sector_action': sector.sector_action, 'sector_registration_date': sector.sector_registration_date}
                           for sector in sectorDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "sector Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page},
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Job Position#

class JobPositionAPI(APIView):

    '''
        job Position API(INSERT)
        Request : POST
        Data =  {
                    "sector_id": "BroaderAI_sector_ks5th0xuavqnehs",
                    "job_position_name": "Python Developer",
                    "job_position_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():

            if not JobPositionModel.objects.filter(sector_id=getData["sector_id"],job_position_name=getData["job_position_name"].lower()).exists():
        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "BroaderAI_job_position_" + randomstr
                getData["job_position_id"] = uniqueID

                serializer = JobPositionSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(job_position_id=getData["job_position_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Position is Added",
                        "Data": {   "job_position_id" : getData['job_position_id']
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
                    "Message": "Job Position is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobPositionUpdateAPI(APIView):
    '''
        Job Position API(Update)
        Request : Patch
        Data =  {
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_position_name": "Data Scientist",
                    "sector_id": "BroaderAI_sector_m8kbwab2rehksfm",
                    "job_position_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request
        if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            if not JobPositionModel.objects.filter(sector_id=getData["sector_id"], job_position_name=getData["job_position_name"].lower()).exists():
                if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():
                    serializer = JobPositionSerializer(data=getData)
                    if serializer.is_valid():
                        LastUpdateData = JobPositionModel.objects.get(job_position_id = getData["job_position_id"])
                        LastUpdateData.job_position_name = getData["job_position_name"].lower()
                        LastUpdateData.sector_id = getData["sector_id"]
                        LastUpdateData.job_position_action = getData["job_position_action"]
                        LastUpdateData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Position is Updated",
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
                        "Message": "Sector is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Sector data with Job Position field is already exists",
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

class JobPositionGetAPI(APIView):
    '''
        JobPosition API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        jobPositionDetails = JobPositionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Position Details",
                "Data": jobPositionDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JobPositionGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            jobPositionDetail = JobPositionModel.objects.get(job_position_id = getData["job_position_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "job Position Field Detail",
                    "Data": {
                        "job_position_id": getData["job_position_id"],
                        "job_position_name": jobPositionDetail.job_position_name,
                        "sector_id": jobPositionDetail.sector_id,
                        "sector_name": jobPositionDetail.sector.sector_name,
                        "job_position_action": jobPositionDetail.job_position_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "job Position Field data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobPositionGetSectorAPI(APIView):
    '''
        Get Field Sector API(View)
        Request : POST
        Data =  {
                    "sector_id": "BroaderAI_sector_ks5th0xuavqnehs"
                    "job_position_action": "active"                          # "deactive" / "all"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobPositionModel.objects.filter(sector_id = getData["sector_id"]).exists():
            if getData["job_position_action"] == "active":
                jobPositionDetail = JobPositionModel.objects.filter(sector_id = getData["sector_id"], job_position_action = "active").values()
            elif getData["job_position_action"] == "deactive":
                jobPositionDetail = JobPositionModel.objects.filter(sector_id = getData["sector_id"], job_position_action = "deactive").values()
            else:
                jobPositionDetail = JobPositionModel.objects.filter(sector_id = getData["sector_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Sectorwise Job Position Detail",
                    "Data": jobPositionDetail
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

class JobPositionDeleteAPI(APIView):
    '''
        JobPosition API(delete)
        Request : delete
        Data =  {
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            jobPositionDetail = JobPositionModel.objects.get(job_position_id = getData["job_position_id"])
            jobPositionDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Position is successfully Deleted",
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

class JobPositionGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        jobPositionDetails = JobPositionModel.objects.all()
        if search_query:
            jobPositionDetails = jobPositionDetails.filter(Q(job_position_name__istartswith=search_query))

        paginator = Paginator(jobPositionDetails, limit)
        try:
            jobPositionDetails = paginator.page(page)
        except PageNotAnInteger:
            jobPositionDetails = paginator.page(1)
        except EmptyPage:
            jobPositionDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'sector_id':jobPos.sector_id,'job_position_id': jobPos.job_position_id, 'job_position_name': jobPos.job_position_name,'job_position_name_arabic':jobPos.job_position_name_arabic,
                            'job_position_action': jobPos.job_position_action, 'job_position_registration_date': jobPos.job_position_registration_date}
                           for jobPos in jobPositionDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "job Position Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Job Level#

class JobLevelAPI(APIView):
    '''
        Job level API(INSERT)
        Request : POST
        Data =  {
                    "job_level_name": "Intern",
                    "job_level_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not JobLevelModel.objects.filter(job_level_name=getData["job_level_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_job_level_" + randomstr
            getData["job_level_id"] = uniqueID
            serializer = JobLevelSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(job_level_id=getData["job_level_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Level is Added",
                    "Data": {   "job_level_id" : getData['job_level_id']
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
                    "Message": "Job level is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class JobLevelUpdateAPI(APIView):
    '''
        JobLevel API(Update)
        Request : Patch
        Data =  {
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr",
                    "job_level_name": "Junior",
                    "job_level_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not JobLevelModel.objects.filter(job_level_name=getData["job_level_name"].lower()).exists():

            if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                serializer = JobLevelSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = JobLevelModel.objects.get(job_level_id = getData["job_level_id"])
                    LastUpdateData.job_level_name=getData["job_level_name"].lower()
                    LastUpdateData.job_level_action = getData["job_level_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Level is Updated",
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
                    "Message": "Job Level data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Level is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobLevelGetAPI(APIView):
    '''
        JobLevel API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        jobLevelDetails = JobLevelModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Level Details",
                "Data": jobLevelDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JobLevelGetOneAPI(APIView):
    '''
        Get One JobLevel API(View)
        Request : POST
        Data =  {
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            jobLevelDetail = JobLevelModel.objects.get(job_level_id = getData["job_level_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Level Detail",
                    "Data": {
                        "job_level_id": getData["job_level_id"],
                        "job_level_name": jobLevelDetail.job_level_name,
                        "job_level_action": jobLevelDetail.job_level_action
                    }
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

class JobLevelGetActionAPI(APIView):
    '''
        Get Action JobLevel API(View)
        Request : POST
        Data =  {
                    "job_level_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        jobLevelDetails = JobLevelModel.objects.filter(job_level_action = getData["job_level_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "job Level Detail",
                "Data": jobLevelDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JobLevelDeleteAPI(APIView):
    '''
        JobLevel API(delete)
        Request : delete
        Data =  {
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            jobLevelDetail = JobLevelModel.objects.get(job_level_id = getData["job_level_id"])
            jobLevelDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Level is successfully Deleted",
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

class JobLevelGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        jobLevelDetails = JobLevelModel.objects.all()
        if search_query:
            jobLevelDetails = jobLevelDetails.filter(Q(job_level_name__istartswith=search_query))

        paginator = Paginator(jobLevelDetails, limit)
        try:
            jobLevelDetails = paginator.page(page)
        except PageNotAnInteger:
            jobLevelDetails = paginator.page(1)
        except EmptyPage:
            jobLevelDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'job_level_id': jobLevel.job_level_id, 'job_level_name': jobLevel.job_level_name,'job_level_name_arabic':jobLevel.job_level_name_arabic,
                            'job_level_action': jobLevel.job_level_action, 'job_level_registration_date': jobLevel.job_level_registration_date}
                           for jobLevel in jobLevelDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "job Level Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Location#

class LocationAPI(APIView):
    '''
        Location API(INSERT)
        Request : POST
        Data =  {
                    "location_name": "Surat",
                    "location_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not LocationModel.objects.filter(location_name=getData["location_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_location_" + randomstr
            getData["location_id"] = uniqueID
            serializer = LocationSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(location_id=getData["location_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Location is Added",
                    "Data": {   "location_id" : getData['location_id']
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
                    "Message": "Location is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class LocationUpdateAPI(APIView):
    '''
        Location API(Update)
        Request : Patch
        Data =  {
                    "location_id": "BroaderAI_location_jinkty65gau6zrl",
                    "location_name": "Kolkata",
                    "location_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not LocationModel.objects.filter(location_name=getData["location_name"].lower()).exists():

            if LocationModel.objects.filter(location_id = getData["location_id"]).exists():
                serializer = LocationSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = LocationModel.objects.get(location_id = getData["location_id"])
                    LastUpdateData.location_name=getData["location_name"].lower()
                    LastUpdateData.location_action = getData["location_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Location is Updated",
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
                    "Message": "Location data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Location is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class LocationGetAPI(APIView):
    '''
        location_ API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        locationDetails = LocationModel.objects.values()
        
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Location Details",
                "Data": locationDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class LocationGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        locationDetails = LocationModel.objects.all()
        if search_query:
            locationDetails = locationDetails.filter(Q(location_name__istartswith=search_query))

        paginator = Paginator(locationDetails, limit)
        try:
            locationDetails = paginator.page(page)
        except PageNotAnInteger:
            locationDetails = paginator.page(1)
        except EmptyPage:
            locationDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'location_id': location.location_id, 'location_name': location.location_name,'location_name_arabic':location.location_name_arabic,
                            'location_action': location.location_action, 'location_registration_date': location.location_registration_date}
                           for location in locationDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Location Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

class LocationGetOneAPI(APIView):
    '''
        Get One Location API(View)
        Request : POST
        Data =  {
                    "location_id": "BroaderAI_location_jinkty65gau6zrl"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if LocationModel.objects.filter(location_id = getData["location_id"]).exists():
            locationDetail = LocationModel.objects.get(location_id = getData["location_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Location Detail",
                    "Data": {
                        "location_id": getData["location_id"],
                        "location_name": locationDetail.location_name,
                        "location_action": locationDetail.location_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Location data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class LocationGetActionAPI(APIView):
    '''
        Get Action Location API(View)
        Request : POST
        Data =  {
                    "location_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        locationDetails = LocationModel.objects.filter(location_action = getData["location_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Location Detail",
                "Data": locationDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class LocationDeleteAPI(APIView):
    '''
        Location API(delete)
        Request : delete
        Data =  {
                    "location_id": "BroaderAI_location_jinkty65gau6zrl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if LocationModel.objects.filter(location_id = getData["location_id"]).exists():
            locationDetail = LocationModel.objects.get(location_id = getData["location_id"])
            locationDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Location is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Location data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Company Type#

class CompanyTypeAPI(APIView):
    '''
        Company Type API(INSERT)
        Request : POST
        Data =  {
                    "company_type_name": "Startup",
                    "company_type_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not CompanyTypeModel.objects.filter(company_type_name=getData["company_type_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_Company_Type_" + randomstr
            getData["company_type_id"] = uniqueID
            serializer = CompanyTypeSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(company_type_id=getData["company_type_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Company Type is Added",
                    "Data": {   "company_type_id" : getData['company_type_id']
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
                    "Message": "Company Type is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class CompanyTypeUpdateAPI(APIView):
    '''
        Company Type API(Update)
        Request : Patch
        Data =  {
                    "company_type_id": "BroaderAI_Company_Type_x44cbhr40khevez",
                    "company_type_name": "MNC",
                    "company_type_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not CompanyTypeModel.objects.filter(company_type_name=getData["company_type_name"].lower()).exists():

            if CompanyTypeModel.objects.filter(company_type_id = getData["company_type_id"]).exists():
                serializer = CompanyTypeSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = CompanyTypeModel.objects.get(company_type_id = getData["company_type_id"])
                    LastUpdateData.company_type_name=getData["company_type_name"].lower()
                    LastUpdateData.company_type_action = getData["company_type_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Company Type is Updated",
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
                    "Message": "Company Type data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Company Type is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class CompanyTypeGetAPI(APIView):
    '''
        CompanyType API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        companyTypeDetails = CompanyTypeModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "CompanyType Details",
                "Data": companyTypeDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class  CompanyTypeGetOneAPI(APIView):
    '''
        Get One  CompanyType API(View)
        Request : POST
        Data =  {
                    "company_type_id": "BroaderAI_Company_Type_x44cbhr40khevez"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if CompanyTypeModel.objects.filter(company_type_id = getData["company_type_id"]).exists():
            companyTypeDetail = CompanyTypeModel.objects.get(company_type_id = getData["company_type_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Company Type Detail",
                    "Data": {
                        "company_type_id": getData["company_type_id"],
                        "company_type_name": companyTypeDetail.company_type_name,
                        "company_type_action": companyTypeDetail.company_type_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Company Type data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class CompanyTypeGetActionAPI(APIView):
    '''
        Get Action CompanyType API(View)
        Request : POST
        Data =  {
                    "company_type_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        companyTypeDetails = CompanyTypeModel.objects.filter(company_type_action = getData["company_type_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Company Type Detail",
                "Data": companyTypeDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class CompanyTypeDeleteAPI(APIView):
    '''
        CompanyType API(delete)
        Request : delete
        Data =  {
                    "company_type_id": "BroaderAI_Company_Type_x44cbhr40khevez"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if CompanyTypeModel.objects.filter(company_type_id = getData["company_type_id"]).exists():
            companyTypeDetail = CompanyTypeModel.objects.get(company_type_id = getData["company_type_id"])
            companyTypeDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Company Type is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Company Type data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class CompanyTypeGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        compTypeDetails = CompanyTypeModel.objects.all()
        if search_query:
            compTypeDetails = compTypeDetails.filter(Q(company_type_name__istartswith=search_query))

        paginator = Paginator(compTypeDetails, limit)
        try:
            compTypeDetails = paginator.page(page)
        except PageNotAnInteger:
            compTypeDetails = paginator.page(1)
        except EmptyPage:
            compTypeDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'company_type_id': type.company_type_id, 'company_type_name': type.company_type_name,'company_type_name_arabic':type.company_type_name_arabic,
                            'company_type_action': type.company_type_action, 'company_type_registration_date': type.company_type_registration_date}
                           for type in compTypeDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Company Type Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Work Place#

class WorkPlaceAPI(APIView):
    '''
        Work Place API(INSERT)
        Request : POST
        Data =  {
                    "work_place_name": "Hybrid",
                    "work_place_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not WorkPlaceModel.objects.filter(work_place_name=getData["work_place_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_Work_Place_" + randomstr
            getData["work_place_id"] = uniqueID
            serializer = WorkPlaceSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(work_place_id=getData["work_place_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Work Place is Added",
                    "Data": {   "work_place_id" : getData['work_place_id']
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
                    "Message": "Work Place is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class WorkPlaceUpdateAPI(APIView):
    '''
        Work Place API(Update)
        Request : Patch
        Data =  {
                    "work_place_id": "BroaderAI_Work_Place_i97aujqs5va3rzv",
                    "work_place_name": "on-site",
                    "work_place_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not WorkPlaceModel.objects.filter(work_place_name=getData["work_place_name"].lower()).exists():

            if WorkPlaceModel.objects.filter(work_place_id = getData["work_place_id"]).exists():
                serializer = WorkPlaceSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = WorkPlaceModel.objects.get(work_place_id = getData["work_place_id"])
                    LastUpdateData.work_place_name=getData["work_place_name"].lower()
                    LastUpdateData.work_place_action = getData["work_place_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Work Place is Updated",
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
                    "Message": "Work Place data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Work Place is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class WorkPlaceGetAPI(APIView):
    '''
        WorkPlace API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        workPlaceDetails = WorkPlaceModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "WorkPlace Details",
                "Data": workPlaceDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class WorkPlaceGetOneAPI(APIView):
    '''
        Get One WorkPlace API(View)
        Request : POST
        Data =  {
                    "work_place_id": "BroaderAI_Work_Place_i97aujqs5va3rzv"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if WorkPlaceModel.objects.filter(work_place_id = getData["work_place_id"]).exists():
            workPlaceDetail = WorkPlaceModel.objects.get(work_place_id = getData["work_place_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Work Place Detail",
                    "Data": {
                        "work_place_id": getData["work_place_id"],
                        "work_place_name": workPlaceDetail.work_place_name,
                        "work_place_action": workPlaceDetail.work_place_action
                    }
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

class WorkPlaceGetActionAPI(APIView):
    '''
        Get Action Work Place API(View)
        Request : POST
        Data =  {
                    "work_place_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        workPlaceDetails = WorkPlaceModel.objects.filter(work_place_action = getData["work_place_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "job Level Detail",
                "Data": workPlaceDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class WorkPlaceDeleteAPI(APIView):
    '''
        WorkPlace API(delete)
        Request : delete
        Data =  {
                    "work_place_id": "BroaderAI_Work_Place_i97aujqs5va3rzv"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if WorkPlaceModel.objects.filter(work_place_id = getData["work_place_id"]).exists():
            WorkPlaceDetail = WorkPlaceModel.objects.get(work_place_id = getData["work_place_id"])
            WorkPlaceDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Work Place is successfully Deleted",
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

class WorkPlaceGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        wrkplace = WorkPlaceModel.objects.all()
        if search_query:
            wrkplace = wrkplace.filter(Q(work_place_name__istartswith=search_query))

        paginator = Paginator(wrkplace, limit)
        try:
            wrkplace = paginator.page(page)
        except PageNotAnInteger:
            wrkplace = paginator.page(1)
        except EmptyPage:
            wrkplace = paginator.page(paginator.num_pages)

        serialized_data = [{'work_place_id': type.work_place_id, 'work_place_name': type.work_place_name,'work_place_name_arabic':type.work_place_name_arabic,
                            'work_place_action': type.work_place_action, 'work_place_registration_date': type.work_place_registration_date}
                           for type in wrkplace]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Work Place Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Employment Type#

class EmploymentTypeAPI(APIView):
    '''
        Employment Type API(INSERT)
        Request : POST
        Data =  {
                    "employment_type_name": "Part-Time",
                    "employment_type_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not EmploymentTypeModel.objects.filter(employment_type_name=getData["employment_type_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_Employment_Type_" + randomstr
            getData["employment_type_id"] = uniqueID
            serializer = EmploymentTypeSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(employment_type_id=getData["employment_type_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Employment Type is Added",
                    "Data": {   "employment_type_id" : getData['employment_type_id']
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
                    "Message": "Employment Type is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class EmploymentTypeUpdateAPI(APIView):
    '''
        Employment Type API(Update)
        Request : Patch
        Data =  {
                    "employment_type_id": "BroaderAI_Employment_Type_ek1o32xm49uu5s6",
                    "employment_type_name": "Full-Time",
                    "employment_type_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not EmploymentTypeModel.objects.filter(employment_type_name=getData["employment_type_name"].lower()).exists():

            if EmploymentTypeModel.objects.filter(employment_type_id = getData["employment_type_id"]).exists():
                serializer = EmploymentTypeSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = EmploymentTypeModel.objects.get(employment_type_id = getData["employment_type_id"])
                    LastUpdateData.employment_type_name=getData["employment_type_name"].lower()
                    LastUpdateData.employment_type_action = getData["employment_type_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Employment type is Updated",
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
                    "Message": "Employment type data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Employment type is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EmploymentTypeGetAPI(APIView):
    '''
        Employment Type API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        employmentTypeDetails = EmploymentTypeModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Employment Type Details",
                "Data": employmentTypeDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class EmploymentTypeGetOneAPI(APIView):
    '''
        Get One EmploymentType API(View)
        Request : POST
        Data =  {
                   "employment_type_id": "BroaderAI_Employment_Type_ek1o32xm49uu5s6"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if EmploymentTypeModel.objects.filter(employment_type_id = getData["employment_type_id"]).exists():
            employmentTypeDetail = EmploymentTypeModel.objects.get(employment_type_id = getData["employment_type_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Employment Type Detail",
                    "Data": {
                        "employment_type_id": getData["employment_type_id"],
                        "employment_type_name": employmentTypeDetail.employment_type_name,
                        "employment_type_action": employmentTypeDetail.employment_type_action
                    }
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

class EmploymentTypeActionAPI(APIView):
    '''
        Get Action EmploymentType API(View)
        Request : POST
        Data =  {
                    "employment_type_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        employmentTypeDetails = EmploymentTypeModel.objects.filter(employment_type_action = getData["employment_type_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Employment type Detail",
                "Data": employmentTypeDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class EmploymentTypeDeleteAPI(APIView):
    '''
        EmploymentType API(delete)
        Request : delete
        Data =  {
                    "employment_type_id": "BroaderAI_Employment_Type_ek1o32xm49uu5s6"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if EmploymentTypeModel.objects.filter(employment_type_id = getData["employment_type_id"]).exists():
            employmentTypeDetail = EmploymentTypeModel.objects.get(employment_type_id = getData["employment_type_id"])
            employmentTypeDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Employment Type is successfully Deleted",
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

class EmploymentTypeGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        empType = EmploymentTypeModel.objects.all()
        if search_query:
            empType = empType.filter(Q(employment_type_name__istartswith=search_query))

        paginator = Paginator(empType, limit)
        try:
            empType = paginator.page(page)
        except PageNotAnInteger:
            empType = paginator.page(1)
        except EmptyPage:
            empType = paginator.page(paginator.num_pages)

        serialized_data = [{'employment_type_id': type.employment_type_id, 'employment_type_name': type.employment_type_name,'employment_type_name_arabic':type.employment_type_name_arabic,
                            'employment_type_action': type.employment_type_action, 'employment_type_registration_date': type.employment_type_registration_date}
                           for type in empType]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "employment type Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Joining Period#

class JoiningPeriodAPI(APIView):
    '''
        Joining Period API(INSERT)
        Request : POST
        Data =  {
                    "joining_period_name": "Immediate",
                    "joining_period_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not JoiningPeriodModel.objects.filter(joining_period_name = getData["joining_period_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_Joining_Period_" + randomstr
            getData["joining_period_id"] = uniqueID
            serializer = JoiningPeriodSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(joining_period_id = getData["joining_period_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Joining Period is Added",
                    "Data": {   "joining_period_id" : getData['joining_period_id']
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
                    "Message": "Joining Period is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class JoiningPeriodUpdateAPI(APIView):
    '''
        JoiningPeriod API(Update)
        Request : Patch
        Data =  {
                    "joining_period_id": "BroaderAI_Joining_Period_ea8s5zbih1wk8vs",
                    "joining_period_name": "immediate join",
                    "joining_period_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not JoiningPeriodModel.objects.filter(joining_period_name=getData["joining_period_name"].lower()).exists():

            if JoiningPeriodModel.objects.filter(joining_period_id = getData["joining_period_id"]).exists():
                serializer = JoiningPeriodSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = JoiningPeriodModel.objects.get(joining_period_id = getData["joining_period_id"])
                    LastUpdateData.joining_period_name=getData["joining_period_name"].lower()
                    LastUpdateData.joining_period_action = getData["joining_period_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Joining Period is Updated",
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
                    "Message": "Joining Period data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Joining Period is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JoiningPeriodGetAPI(APIView):
    '''
        JoiningPeriod API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        joiningPeriodDetails = JoiningPeriodModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Joining Period Details",
                "Data": joiningPeriodDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JoiningPeriodGetOneAPI(APIView):
    '''
        Get One JoiningPeriod API(View)
        Request : POST
        Data =  {
                    "joining_period_id": "BroaderAI_Joining_Period_ea8s5zbih1wk8vs"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JoiningPeriodModel.objects.filter(joining_period_id = getData["joining_period_id"]).exists():
            JoiningPeriodDetail = JoiningPeriodModel.objects.get(joining_period_id = getData["joining_period_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Joining Period Detail",
                    "Data": {
                        "joining_period_id": getData["joining_period_id"],
                        "joining_period_name": JoiningPeriodDetail.joining_period_name,
                        "joining_period_action": JoiningPeriodDetail.joining_period_action
                    }
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

class JoiningPeriodGetActionAPI(APIView):
    '''
        Get Action JoiningPeriod API(View)
        Request : POST
        Data =  {
                    "joining_period_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        joiningPeriodDetails = JoiningPeriodModel.objects.filter(joining_period_action = getData["joining_period_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Joining Period Detail",
                "Data": joiningPeriodDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JoiningPeriodDeleteAPI(APIView):
    '''
        JoiningPeriod API(delete)
        Request : delete
        Data =  {
                    "joining_period_id": "BroaderAI_Joining_Period_ea8s5zbih1wk8vs"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JoiningPeriodModel.objects.filter(joining_period_id = getData["joining_period_id"]).exists():
            JoiningPeriodDetail = JoiningPeriodModel.objects.get(joining_period_id = getData["joining_period_id"])
            JoiningPeriodDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Joining Period is successfully Deleted",
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

class JoiningPeriodGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        joinTime = JoiningPeriodModel.objects.all()
        if search_query:
            joinTime = joinTime.filter(Q(joining_period_name__istartswith=search_query))

        paginator = Paginator(joinTime, limit)
        try:
            joinTime = paginator.page(page)
        except PageNotAnInteger:
            joinTime = paginator.page(1)
        except EmptyPage:
            joinTime = paginator.page(paginator.num_pages)

        serialized_data = [{'joining_period_id': type.joining_period_id, 'joining_period_name': type.joining_period_name,'joining_period_name_arabic':type.joining_period_name_arabic,
                            'joining_period_action': type.joining_period_action, 'joining_period_registration_date': type.joining_period_registration_date}
                           for type in joinTime]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Joining Period Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)



########################################################################
# Unique technical skill #

class UniqueTechnicalSkillsAPI(APIView):
    '''
        UniqueTechnicalSkills API(Insert)
        Request : POST
        Data = {
                    "unique_technical_skills_name": "Python",
                    "unique_technical_skills_category": "Language"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if not TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_name = getData["unique_technical_skills_name"].lower()).exists():
            randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))
            uniqueID = "BroaderAI_Unique_Technical_Skills_" + randomstr

            
            getData["unique_technical_skills_id"] = uniqueID

            serializer = UniqueTechnicalSkillsDetailsSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(unique_technical_skills_id=getData["unique_technical_skills_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills is Added",
                    "Data": {
                        "unique_technical_skills_id": getData["unique_technical_skills_id"]
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
                "Message": "Technical Skills is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class UniqueTechnicalSkillsGetAPI(APIView):
    '''
        unique TechnicalSkills API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        UniqueTechnicalSkillsDetails = TechnicalSkillsUniqueModel.objects.values()

        mainTech = []
        for unq in UniqueTechnicalSkillsDetails:
            mainTech.append({
            "technical_skills_id": unq["unique_technical_skills_id"],
            "technical_skills_name": unq["unique_technical_skills_name"],
            "technical_skills_category": unq["unique_technical_skills_category"],
            "technical_skills_action": unq["unique_technical_skills_action"],
            "technical_skills_registration_date": unq["unique_technical_skills_action"]
        })


        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Unique Technical Skills Details",
                "Data": mainTech
            }
        return Response(res, status=status.HTTP_201_CREATED)

class UniqueTechnicalSkillsGetOneAPI(APIView):
    '''
        unique Get One Field API(View)
        Request : POST
        Data =  {
                    "unique_technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData["unique_technical_skills_id"]).exists():
            UniqueTechnicalSkillsDetail = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id = getData["unique_technical_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Unique Technical Skills Field Detail",
                    "Data": {
                        "unique_technical_skills_id": getData["unique_technical_skills_id"],
                        "unique_technical_skills_name": UniqueTechnicalSkillsDetail.unique_technical_skills_name,
                        "unique_technical_skills_category": UniqueTechnicalSkillsDetail.unique_technical_skills_category,
                        "unique_technical_skills_action": UniqueTechnicalSkillsDetail.unique_technical_skills_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class UniqueTechnicalSkillsUpdateAPI(APIView):
    '''
        unique TechnicalSkills Update API(Insert)
        Request : PATCH
        Data = {
                    "unique_technical_skills_id": "BroaderAI_Unique_Technical_Skills_z27g9bebepjfuk3",
                    "unique_technical_skills_name": "python",
                    "unique_technical_skills_category": "language"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data
        if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData["unique_technical_skills_id"]).exists():
            serializer = UniqueTechnicalSkillsDetailsSerializer(data=getData)
            if serializer.is_valid():
                UniqueTechnicalSkillsData = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id = getData["unique_technical_skills_id"])
                UniqueTechnicalSkillsData.unique_technical_skills_name = getData["unique_technical_skills_name"]
                UniqueTechnicalSkillsData.unique_technical_skills_category = getData["unique_technical_skills_category"]
                UniqueTechnicalSkillsData.save()
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Unique Technical Skills is Updated",
                    "Data": {
                        "unique_technical_skills_id": getData["unique_technical_skills_id"]
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
                "Message": "Unique Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class UniqueTechnicalSkillsDeleteAPI(APIView):
    '''
        unique TechnicalSkills API(delete)
        Request : delete
        Data =  {
                    "unique_technical_skills_id": "BroaderAI_Unique_Technical_Skills_z27g9bebepjfuk3"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData["unique_technical_skills_id"]).exists():
            UniqueTechnicalSkillsDetail = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id = getData["unique_technical_skills_id"])
            UniqueTechnicalSkillsDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Unique Technical Skills is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Unique Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class UniqueTechnicalSkillsGetOneByNameAPI(APIView):
    '''
        unique Get One Field API(View)
        Request : POST
        Data =  {
                    "unique_technical_skills_name": "python"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_name = getData["unique_technical_skills_name"]).exists():
            UniqueTechnicalSkillsDetail = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_name = getData["unique_technical_skills_name"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Unique Technical Skills Field Detail",
                    "Data": {
                        "unique_technical_skills_id": UniqueTechnicalSkillsDetail.unique_technical_skills_id,
                        "unique_technical_skills_name": getData["unique_technical_skills_name"],
                        "unique_technical_skills_category": UniqueTechnicalSkillsDetail.unique_technical_skills_category,
                        "unique_technical_skills_action": UniqueTechnicalSkillsDetail.unique_technical_skills_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class UniqueTechnicalSkillsGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        technicalSkillDetails = TechnicalSkillsUniqueModel.objects.all()
        if search_query:
            technicalSkillDetails = technicalSkillDetails.filter(Q(unique_technical_skills_name__istartswith=search_query))

        paginator = Paginator(technicalSkillDetails, limit)
        try:
            technicalSkillDetails = paginator.page(page)
        except PageNotAnInteger:
            technicalSkillDetails = paginator.page(1)
        except EmptyPage:
            technicalSkillDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'unique_technical_skills_id': technicalSkill.unique_technical_skills_id, 'unique_technical_skills_name': technicalSkill.unique_technical_skills_name, 'unique_technical_skills_name_arabic':technicalSkill.unique_technical_skills_name_arabic,'unique_technical_skills_category':technicalSkill.unique_technical_skills_category,'unique_technical_skills_category_arabic':technicalSkill.unique_technical_skills_category_arabic,
                            'unique_technical_skills_action': technicalSkill.unique_technical_skills_action, 'unique_technical_skills_registration_date': technicalSkill.unique_technical_skills_registration_date}
                           for technicalSkill in technicalSkillDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "technical Skill Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################


########################################################################
# Main technical skill #

class MainTechnicalSkillsAPI(APIView):
    '''
        TechnicalSkills API(Insert)
        Request : POST
        Data = {
                    "unique_technical_skills_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr",
                }
    '''
    def post(self, request ,format=None):
        
        getData = request.data

        if not TechnicalSkillsMainModel.objects.filter(technical_skills_id = getData["unique_technical_skills_id"].lower(),job_position_id = getData["job_position_id"],job_level_id = getData["job_level_id"]).exists():

            if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData["unique_technical_skills_id"]).exists():

                techskills = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id = getData["unique_technical_skills_id"])

                getData["technical_skills_id"] = techskills.unique_technical_skills_id
                getData["technical_skills_name"] = techskills.unique_technical_skills_name
                getData["technical_skills_category"] = techskills.unique_technical_skills_category

                getData["technical_skills_name_arabic"] = techskills.unique_technical_skills_name_arabic
                getData["technical_skills_category_arabic"] = techskills.unique_technical_skills_category_arabic


                getData["technical_skills_action"] = techskills.unique_technical_skills_action


                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))

                uniqueID = "BroaderAI_Main_Technical_Skills_" + randomstr
                getData["main_technical_skills_id"] = uniqueID

                mainTech = TechnicalSkillsMainModel(
                    main_technical_skills_id = uniqueID,
                    technical_skills_id = getData["technical_skills_id"],
                    job_position_id = getData["job_position_id"],
                    job_level_id = getData["job_level_id"],
                    technical_skills_name = getData["technical_skills_name"],
                    technical_skills_category =getData["technical_skills_category"],
                    technical_skills_name_arabic = getData["technical_skills_name_arabic"],
                    technical_skills_category_arabic = getData["technical_skills_category_arabic"],
                    technical_skills_action = getData["technical_skills_action"],
                )

                mainTech.save()
                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Technical Skills is Added",
                        "Data": {
                            "technical_skills_id": getData["technical_skills_id"],
                            "main_technical_skills_id": getData["main_technical_skills_id"]
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Technical Skills is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsGetAPI(APIView):
    '''
        Main TechnicalSkills API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        MainTechnicalSkillsDetails = TechnicalSkillsMainModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Main Technical Skills Details",
                "Data": MainTechnicalSkillsDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "main_technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsMainModel.objects.filter(main_technical_skills_id = getData["main_technical_skills_id"]).exists():
            mainTechnicalSkillsDetail = TechnicalSkillsMainModel.objects.get(main_technical_skills_id = getData["main_technical_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Technical Skills Field Detail",
                    "Data": {
                        "main_technical_skills_id": getData["main_technical_skills_id"],
                        "job_position_name": mainTechnicalSkillsDetail.job_position.job_position_name,
                        "job_position_id": mainTechnicalSkillsDetail.job_position_id,
                        "job_level_id": mainTechnicalSkillsDetail.job_level_id,
                        "job_level_name": mainTechnicalSkillsDetail.job_level.job_level_name,
                        "technical_skills_id" : mainTechnicalSkillsDetail.technical_skills_id,
                        "technical_skills_name": mainTechnicalSkillsDetail.technical_skills_name,
                        "technical_skills_category":mainTechnicalSkillsDetail.technical_skills_category,
                        "technical_skills_action": mainTechnicalSkillsDetail.technical_skills_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsMainModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            mainTechnicalSkillsDetail = TechnicalSkillsMainModel.objects.filter(job_position_id = getData["job_position_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Technical Skills Field Detail",
                    "Data": mainTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsGetfromJobLevelAPI(APIView):
    '''
        Get from job Level Field API(View)
        Request : POST
        Data =  {
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsMainModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            mainTechnicalSkillsDetail = TechnicalSkillsMainModel.objects.filter(job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Technical Skills Field Detail",
                    "Data": mainTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsMainModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            mainTechnicalSkillsDetail = TechnicalSkillsMainModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Technical Skills Field Detail",
                    "Data": mainTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsUpdateAPI(APIView):
    '''
        TechnicalSkills Update API(Insert)
        Request : PATCH
        Data = {
                    "main_technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu",
                    "technical_skills_id" :,
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr",
                    "technical_skills_name": "Python",
                    "technical_skills_category": "Language"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data
        if TechnicalSkillsMainModel.objects.filter(main_technical_skills_id = getData["main_technical_skills_id"]).exists():
            if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData['technical_skills_id']).exists():
                if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                    if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                        serializer = MainTechnicalSkillsDetailsSerializer(data=getData)
                        if serializer.is_valid():
                            mainTechnicalSkillsData = TechnicalSkillsMainModel.objects.get(main_technical_skills_id = getData["main_technical_skills_id"])
                            mainTechnicalSkillsData.job_position_id = getData["job_position_id"]
                            mainTechnicalSkillsData.job_level_id = getData["job_level_id"]
                            mainTechnicalSkillsData.technical_skills_name = getData["technical_skills_name"]
                            mainTechnicalSkillsData.technical_skills_category = getData["technical_skills_category"]
                            mainTechnicalSkillsData.save()
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Technical Skills is Updated",
                                "Data": {
                                    "main_technical_skills_id": getData["main_technical_skills_id"]
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
                        "Message": "Unique technical skill data is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Main Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsDeleteAPI(APIView):
    '''
        main TechnicalSkills API(delete)
        Request : delete
        Data =  {
                    "main_technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if TechnicalSkillsMainModel.objects.filter(main_technical_skills_id = getData["main_technical_skills_id"]).exists():
            mainTechnicalSkillsDetail = TechnicalSkillsMainModel.objects.get(main_technical_skills_id = getData["main_technical_skills_id"])
            mainTechnicalSkillsDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Main Technical Skills is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

# class UniqueMainTechnicalSkillsGetOneAPI(APIView):
    '''
        unique Get One Field API(View)
        Request : POST
        Data =  {
                    "unique_technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsUniqueModel.objects.filter(unique_technical_skills_id = getData["unique_technical_skills_id"]).exists():
            UniqueTechnicalSkillsDetail = TechnicalSkillsUniqueModel.objects.get(unique_technical_skills_id = getData["unique_technical_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Unique Technical Skills Field Detail",
                    "Data": {
                        "unique_technical_skills_id": getData["unique_technical_skills_id"],
                        "unique_technical_skills_name": UniqueTechnicalSkillsDetail.unique_technical_skills_name,
                        "unique_technical_skills_category": UniqueTechnicalSkillsDetail.unique_technical_skills_category,
                        "unique_technical_skills_action": UniqueTechnicalSkillsDetail.unique_technical_skills_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class MainTechnicalSkillsGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        maintechnicalSkillDetails = TechnicalSkillsMainModel.objects.all()
        if search_query:
            maintechnicalSkillDetails = maintechnicalSkillDetails.filter(Q(technical_skills_name__istartswith=search_query))

        paginator = Paginator(maintechnicalSkillDetails, limit)
        try:
            maintechnicalSkillDetails = paginator.page(page)
        except PageNotAnInteger:
            maintechnicalSkillDetails = paginator.page(1)
        except EmptyPage:
            maintechnicalSkillDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'main_technical_skills_id':technicalSkill.main_technical_skills_id,'technical_skills_id': technicalSkill.technical_skills_id,'job_position_id':technicalSkill.job_position_id,'job_level_id':technicalSkill.job_level_id, 'technical_skills_name': technicalSkill.technical_skills_name, 'technical_skills_name_arabic':technicalSkill.technical_skills_name_arabic,'technical_skills_category':technicalSkill.technical_skills_category,'technical_skills_category_arabic':technicalSkill.technical_skills_category_arabic,
                            'technical_skills_action': technicalSkill.technical_skills_action, 'technical_skills_registration_date': technicalSkill.technical_skills_registration_date}
                           for technicalSkill in maintechnicalSkillDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "technical Skill Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################

########################################################################
#Technical Skills#

class TechnicalSkillsAPI(APIView):
    '''
        TechnicalSkills API(Insert)
        Request : POST
        Data = {
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr",
                    "technical_skills_name": "Python",
                    "technical_skills_category": "Language"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if not TechnicalSkillsModel.objects.filter(technical_skills_name = getData["technical_skills_name"].lower(),job_position_id = getData["job_position_id"],job_level_id = getData["job_level_id"]).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))
                            
            uniqueID = "BroaderAI_Technical_Skills_" + randomstr
            getData["technical_skills_id"] = uniqueID
            serializer = TechnicalSkillsDetailsSerializer(data=getData)

            if serializer.is_valid():

                serializer.save(technical_skills_id=getData["technical_skills_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills is Added",
                    "Data": {
                        "technical_skills_id": getData["technical_skills_id"]
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
                "Message": "Technical Skills is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsGetAPI(APIView):
    '''
        TechnicalSkills API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        TechnicalSkillsDetails = TechnicalSkillsModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Technical Skills Details",
                "Data": TechnicalSkillsDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
            TechnicalSkillsDetail = TechnicalSkillsModel.objects.get(technical_skills_id = getData["technical_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills Field Detail",
                    "Data": {
                        "technical_skills_id": getData["technical_skills_id"],
                        "job_position_name": TechnicalSkillsDetail.job_position.job_position_name,
                        "job_position_id": TechnicalSkillsDetail.job_position_id,
                        "job_level_id": TechnicalSkillsDetail.job_level_id,
                        "job_level_name": TechnicalSkillsDetail.job_level.job_level_name,
                        "technical_skills_name": TechnicalSkillsDetail.technical_skills_name,
                        "technical_skills_action": TechnicalSkillsDetail.technical_skills_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsGetUniqueAPI(APIView):
    '''
        TechnicalSkills API(View)
        Request: GET
    '''
    def get(self, request, format=None):
        # Retrieve unique technical skills names
        unique_technical_skills = TechnicalSkillsModel.objects.values_list('technical_skills_name', flat=True).distinct()
        
        unique_technical_skills_data = [
            {
                "technical_skills_name": skill,
                "technical_skills_category": "language",  
                "technical_skills_action": "active",  
                
            }
            for skill in unique_technical_skills
        ]
        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Unique Technical Skills Details",
            "Data": unique_technical_skills_data
        }
        return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            TechnicalSkillsDetail = TechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills Field Detail",
                    "Data": TechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsGetfromJobLevelAPI(APIView):
    '''
        Get from job Level Field API(View)
        Request : POST
        Data =  {
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            TechnicalSkillsDetail = TechnicalSkillsModel.objects.filter(job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills Field Detail",
                    "Data": TechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if TechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            TechnicalSkillsDetail = TechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills Field Detail",
                    "Data": TechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsUpdateAPI(APIView):

    '''
        TechnicalSkills Update API(Insert)
        Request : PATCH
        Data = {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu",
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr",
                    "technical_skills_name": "Python",
                    "technical_skills_category": "Language"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if TechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists(): 

                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():

                   
                    serializer = TechnicalSkillsDetailsSerializer(data=getData)

                    if serializer.is_valid():
                        TechnicalSkillsData = TechnicalSkillsModel.objects.get(technical_skills_id = getData["technical_skills_id"])
                        TechnicalSkillsData.job_position_id = getData["job_position_id"]
                        TechnicalSkillsData.job_level_id = getData["job_level_id"]
                        TechnicalSkillsData.technical_skills_name = getData["technical_skills_name"]
                        TechnicalSkillsData.technical_skills_category = getData["technical_skills_category"]

                        TechnicalSkillsData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Technical Skills is Updated",
                            "Data": {
                                "technical_skills_id": getData["technical_skills_id"]
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
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillsDeleteAPI(APIView):
    '''
        TechnicalSkills API(delete)
        Request : delete
        Data =  {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if TechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
            TechnicalSkillsDetail = TechnicalSkillsModel.objects.get(technical_skills_id = getData["technical_skills_id"])
            TechnicalSkillsDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Technical Skills is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)


########################################################################
#Have_to Technical Skills#

class HaveToTechnicalSkillsAPI(APIView):
    '''
        Have To Technical Skills API(Insert)
        Request : POST
        Data = {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data

        if not OptionalTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():

            if not HaveToTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
                
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                
                uniqueID = "BroaderAI_Have_To_Technical_Skills_" + randomstr
                getData["have_to_technical_skills_id"] = uniqueID

                techSkillData = TechnicalSkillsMainModel.objects.get(main_technical_skills_id = getData["technical_skills_id"])

                getData["technical_skills_id"] = getData["technical_skills_id"]
                getData["main_unique_technical_skills_id"] = techSkillData.technical_skills_id
                getData["job_position_id"] = techSkillData.job_position_id
                getData["job_level_id"] = techSkillData.job_level_id
                getData["have_to_technical_skills_name"] = techSkillData.technical_skills_name
                getData["have_to_technical_skills_category"] = techSkillData.technical_skills_category
                getData["have_to_technical_skills_name_arabic"] = techSkillData.technical_skills_name_arabic
                getData["have_to_technical_skills_category_arabic"] = techSkillData.technical_skills_category_arabic

                serializer = HaveToTechnicalSkillsDetailsSerializer(data=getData)


                if serializer.is_valid():

                    serializer.save(have_to_technical_skills_id=getData["have_to_technical_skills_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Have to Technical Skills is Added",
                        "Data": {
                            "have_to_technical_skills_id": getData["have_to_technical_skills_id"]
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
                    "Message": "Have to Technical Skills is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Already in Optional Technical Skill",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class HaveToTechnicalSkillsGetAPI(APIView):
    '''
        HaveToTechnicalSkills API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        HaveToTechnicalSkillsDetails = HaveToTechnicalSkillsModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "HaveTo Technical Skills Details",
                "Data": HaveToTechnicalSkillsDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class HaveToTechnicalSkillsGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "have_to_technical_skills_id": "BroaderAI_Have_To_Technical_Skills_th70cmh7cjtyb5a"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if HaveToTechnicalSkillsModel.objects.filter(have_to_technical_skills_id = getData["have_to_technical_skills_id"]).exists():
            haveToTechnicalSkillsDetail = HaveToTechnicalSkillsModel.objects.get(have_to_technical_skills_id = getData["have_to_technical_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Have To Technical Skills Field Detail",
                    "Data": {
                        "have_to_technical_skills_id": getData["have_to_technical_skills_id"],
                        "job_position_name": haveToTechnicalSkillsDetail.job_position.job_position_name,
                        "job_position_id": haveToTechnicalSkillsDetail.job_position_id,
                        "job_level_id": haveToTechnicalSkillsDetail.job_level_id,
                        "job_level_name": haveToTechnicalSkillsDetail.job_level.job_level_name,
                        "have_to_technical_skills_name": haveToTechnicalSkillsDetail.have_to_technical_skills_name,
                        "have_to_technical_skills_category": haveToTechnicalSkillsDetail.have_to_technical_skills_category
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Have to Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class HaveToTechnicalSkillsGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if HaveToTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            HaveToTechnicalSkillsDetail = HaveToTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "HaveToTechnical Skills Field Detail",
                    "Data": HaveToTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "HaveToTechnical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class HaveToTechnicalSkillsGetfromJobLevelAPI(APIView):
    '''
        Get from job Level Field API(View)
        Request : POST
        Data =  {
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if HaveToTechnicalSkillsModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            HaveToTechnicalSkillsDetail = HaveToTechnicalSkillsModel.objects.filter(job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "HaveToTechnical Skills Field Detail",
                    "Data": HaveToTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "HaveToTechnical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class HaveToTechnicalSkillsGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if HaveToTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            HaveToTechnicalSkillsDetail = HaveToTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "HaveTo Technical Skills Field Detail",
                    "Data": HaveToTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "HaveTo Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class HaveToTechnicalSkillsDeleteAPI(APIView):
    '''
        HaveTo TechnicalSkills API(delete)
        Request : delete
        Data =  {
                    "have_to_technical_skills_id": "BroaderAI_Have_To_Technical_Skills_cyqwf4shwzb2hnt"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if HaveToTechnicalSkillsModel.objects.filter(have_to_technical_skills_id = getData["have_to_technical_skills_id"]).exists():
            HaveToTechnicalSkillsDetail = HaveToTechnicalSkillsModel.objects.get(have_to_technical_skills_id = getData["have_to_technical_skills_id"])
            HaveToTechnicalSkillsDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Have To Technical Skills is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Have To Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class HaveToOptionalTechnicalSkillsAPI(APIView):
    '''
        Have To to optional Technical Skills API(Insert)
        Request : POST
        Data = {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        print('ppp',getData)
 
        if HaveToTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
            print('-------')

            if not OptionalTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
      
                techSkillData = TechnicalSkillsMainModel.objects.get(main_technical_skills_id = getData["technical_skills_id"])
              
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                
                uniqueID = "BroaderAI_Optional_Technical_Skills_" + randomstr
               

                optionalTechnicalData = OptionalTechnicalSkillsModel(
                    optional_technical_skills_id = uniqueID,
                    technical_skills_id = techSkillData.technical_skills_id,
                    job_position_id = techSkillData.job_position_id,
                    job_level_id = techSkillData.job_level_id,
                    optional_technical_skills_name= techSkillData.technical_skills_name,
                    optional_technical_skills_category = techSkillData.technical_skills_category,
                    optional_technical_skills_action = techSkillData.technical_skills_action
                )
                havetotechSkillData = HaveToTechnicalSkillsModel.objects.get(technical_skills_id = getData["technical_skills_id"])
                print(havetotechSkillData,"mmmmmmm")
                havetotechSkillData.delete()
                optionalTechnicalData.save()

                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Skill move to optional from Have to Skill is Added",
                    "Data":[],
                }
                return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Already present in optional Skills",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Not Present in Have to skills",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Optional Technical Skills#

class OptionalTechnicalSkillsAPI(APIView):
    '''
        Optional Technical Skills API(Insert)
        Request : POST
        Data = {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if not HaveToTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
            if not OptionalTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():

                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                
                uniqueID = "BroaderAI_Optional_Technical_Skills_" + randomstr
                getData["optional_technical_skills_id"] = uniqueID

                techSkillData = TechnicalSkillsMainModel.objects.get(main_technical_skills_id = getData["technical_skills_id"])

                getData["technical_skills_id"] = getData["technical_skills_id"]
                getData["main_unique_technical_skills_id"] = techSkillData.technical_skills_id
                getData["job_position_id"] = techSkillData.job_position_id
                getData["job_level_id"] = techSkillData.job_level_id
                getData["optional_technical_skills_name"] = techSkillData.technical_skills_name
                getData["optional_technical_skills_category"] = techSkillData.technical_skills_category
                getData["optional_technical_skills_name_arabic"] = techSkillData.technical_skills_name_arabic
                getData["optional_technical_skills_category_arabic"] = techSkillData.technical_skills_category_arabic

                serializer = OptionalTechnicalSkillsDetailsSerializer(data=getData)

                if serializer.is_valid():

                    serializer.save(optional_technical_skills_id=getData["optional_technical_skills_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Optional Technical Skills is Added",
                        "Data": {
                            "optional_technical_skills_id": getData["optional_technical_skills_id"]
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
                    "Message": "Optional Technical Skills is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Already in Have To Technical Skill",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class OptionalTechnicalSkillsGetAPI(APIView):
    '''
        OptionalTechnicalSkills API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        OptionalTechnicalSkillsDetails = OptionalTechnicalSkillsModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Optional Technical Skills Details",
                "Data": OptionalTechnicalSkillsDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class OptionalTechnicalSkillsGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "optional_technical_skills_id": "BroaderAI_Optional_Technical_Skills_d3yecu57b0o5bd4"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if OptionalTechnicalSkillsModel.objects.filter(optional_technical_skills_id = getData["optional_technical_skills_id"]).exists():
            OptionalTechnicalSkillsDetail = OptionalTechnicalSkillsModel.objects.get(optional_technical_skills_id = getData["optional_technical_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Optional Technical Skills Field Detail",
                    "Data": {
                        "optional_technical_skills_id": getData["optional_technical_skills_id"],
                        "job_position_name": OptionalTechnicalSkillsDetail.job_position.job_position_name,
                        "job_position_id": OptionalTechnicalSkillsDetail.job_position_id,
                        "job_level_id": OptionalTechnicalSkillsDetail.job_level_id,
                        "job_level_name": OptionalTechnicalSkillsDetail.job_level.job_level_name,
                        "optional_technical_skills_name": OptionalTechnicalSkillsDetail.optional_technical_skills_name,
                        "optional_technical_skills_category": OptionalTechnicalSkillsDetail.optional_technical_skills_category
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Optional Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class OptionalTechnicalSkillsGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if OptionalTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            OptionalTechnicalSkillsDetail = OptionalTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "OptionalTechnical Skills Field Detail",
                    "Data": OptionalTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "OptionalTechnical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class OptionalTechnicalSkillsGetfromJobLevelAPI(APIView):
    '''
        Get from job Level Field API(View)
        Request : POST
        Data =  {
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if OptionalTechnicalSkillsModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            OptionalTechnicalSkillsDetail = OptionalTechnicalSkillsModel.objects.filter(job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "OptionalTechnical Skills Field Detail",
                    "Data": OptionalTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "OptionalTechnical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class OptionalTechnicalSkillsGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_jtuktdwito44rpp",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if OptionalTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            OptionalTechnicalSkillsDetail = OptionalTechnicalSkillsModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Optional Technical Skills Field Detail",
                    "Data": OptionalTechnicalSkillsDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Optional Technical Skills data is not found",
                "Data":[],
                }

class OptionalHaveToTechnicalSkillsAPI(APIView):
    '''
        Optional to Have to Technical Skills API(Insert)
        Request : POST
        Data = {
                    "technical_skills_id": "BroaderAI_Technical_Skills_afkp6pwtup2g5xu"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        
        if OptionalTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():

            if not HaveToTechnicalSkillsModel.objects.filter(technical_skills_id = getData["technical_skills_id"]).exists():
                techSkillData = TechnicalSkillsModel.objects.get(main_technical_skills_id = getData["technical_skills_id"])
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
                                
                uniqueID = "BroaderAI_Have_To_Technical_Skills_" + randomstr
               

                havetoTechnicalData = HaveToTechnicalSkillsModel(
                    have_to_technical_skills_id = uniqueID,
                    technical_skills_id = techSkillData.technical_skills_id,
                    job_position_id = techSkillData.job_position_id,
                    job_level_id = techSkillData.job_level_id,
                    have_to_technical_skills_name= techSkillData.technical_skills_name,
                    have_to_technical_skills_category = techSkillData.technical_skills_category,
                    have_to_technical_skills_action = techSkillData.technical_skills_action
                )
                optionaltechSkillData = OptionalTechnicalSkillsModel.objects.get(technical_skills_id = getData["technical_skills_id"])
                optionaltechSkillData.delete()
                havetoTechnicalData.save()

                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Skill move to have to from optional Skill is Added",
                    "Data":[],
                }
                return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Already present in have to  Skills",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Not Present in optional skills",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class OptionalTechnicalSkillsDeleteAPI(APIView):
    '''
        Optional TechnicalSkills API(delete)
        Request : delete
        Data =  {
                    "optional_technical_skills_id": "BroaderAI_Optional_Technical_Skills_uh55mdks65svx12"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if OptionalTechnicalSkillsModel.objects.filter(optional_technical_skills_id = getData["optional_technical_skills_id"]).exists():
            
            optionalTechnicalSkillsDetail = OptionalTechnicalSkillsModel.objects.get(optional_technical_skills_id = getData["optional_technical_skills_id"])
            optionalTechnicalSkillsDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Optional Technical Skills is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Optional Technical Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Soft Skills#

class SoftSkillsAPI(APIView):
    '''
        Soft Skills API(INSERT)
        Request : POST
        Data =  {
                    "soft_skills_name": "Leadership",
                    "soft_skills_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not SoftSkillsModel.objects.filter(soft_skills_name = getData["soft_skills_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_Soft_Skills_" + randomstr
            getData["soft_skills_id"] = uniqueID
            serializer = SoftSkillsSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(soft_skills_id = getData["soft_skills_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Soft Skills is Added",
                    "Data": {   "soft_skills_id" : getData['soft_skills_id']
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
                    "Message": "Soft Skills is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class SoftSkillsUpdateAPI(APIView):
    '''
        SoftSkills API(Update)
        Request : Patch
        Data =  {
                    "soft_skills_id": "BroaderAI_Soft_Skills_wmdb9u96x5vmdwc",
                    "soft_skills_name": "Teamwork",
                    "soft_skills_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not SoftSkillsModel.objects.filter(soft_skills_name=getData["soft_skills_name"].lower()).exists():

            if SoftSkillsModel.objects.filter(soft_skills_id = getData["soft_skills_id"]).exists():
                serializer = SoftSkillsSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = SoftSkillsModel.objects.get(soft_skills_id = getData["soft_skills_id"])
                    LastUpdateData.soft_skills_name=getData["soft_skills_name"].lower()
                    LastUpdateData.soft_skills_action = getData["soft_skills_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Soft Skills is Updated",
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
                    "Message": "Soft Skills data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Soft Skills is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class SoftSkillsGetAPI(APIView):
    '''
        SoftSkills API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        softSkillsDetails = SoftSkillsModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Soft Skills Details",
                "Data": softSkillsDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class SoftSkillsGetOneAPI(APIView):

    '''
        Get One SoftSkills API(View)
        Request : POST
        Data =  {
                    "soft_skills_id": "BroaderAI_Soft_Skills_wmdb9u96x5vmdwc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if SoftSkillsModel.objects.filter(soft_skills_id = getData["soft_skills_id"]).exists():
            softSkillsDetail = SoftSkillsModel.objects.get(soft_skills_id = getData["soft_skills_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Soft Skills Detail",
                    "Data": {
                        "soft_skills_id": getData["soft_skills_id"],
                        "soft_skills_name": softSkillsDetail.soft_skills_name,
                        "soft_skills_action": softSkillsDetail.soft_skills_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Soft Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class SoftSkillsGetActionAPI(APIView):
    '''
        Get Action SoftSkills API(View)
        Request : POST
        Data =  {
                    "soft_skills_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        softSkillsDetails = SoftSkillsModel.objects.filter(soft_skills_action = getData["soft_skills_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Soft Skills Detail",
                "Data": softSkillsDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class SoftSkillsDeleteAPI(APIView):

    '''
        SoftSkills API(delete)
        Request : delete
        Data =  {
                   "soft_skills_id": "BroaderAI_Soft_Skills_wmdb9u96x5vmdwc"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if SoftSkillsModel.objects.filter(soft_skills_id = getData["soft_skills_id"]).exists():
            softSkillsDetail = SoftSkillsModel.objects.get(soft_skills_id = getData["soft_skills_id"])
            softSkillsDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Soft Skills is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Soft Skills data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class SoftSkillsGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        softSkillDetails = SoftSkillsModel.objects.all()
        if search_query:
            softSkillDetails = softSkillDetails.filter(Q(soft_skills_name__istartswith=search_query))

        paginator = Paginator(softSkillDetails, limit)
        try:
            softSkillDetails = paginator.page(page)
        except PageNotAnInteger:
            softSkillDetails = paginator.page(1)
        except EmptyPage:
            softSkillDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'soft_skills_id':softSkill.soft_skills_id,'soft_skills_name': softSkill.soft_skills_name, 'soft_skills_name_arabic':softSkill.soft_skills_name_arabic,
                            'soft_skills_action': softSkill.soft_skills_action, 'soft_skills_registration_date': softSkill.soft_skills_registration_date}
                           for softSkill in softSkillDetails]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Soft Skill Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)


########################################################################
 # Language #

class LanguageRegisterAPI(APIView):
    '''
        language API(INSERT)
        Request : POST
        Data =  {
                    "language_name": "english",
                    "language_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not LanguageModel.objects.filter(language_name = getData["language_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_language_" + randomstr
            getData["language_id"] = uniqueID
            serializer = LanguageSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(language_id = getData["language_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "language is Added",
                    "Data": {   "language_id" : getData['language_id']
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
                    "Message": "language is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class LanguageUpdateAPI(APIView):
    '''
        Language API(Update)
        Request : Patch
        Data =  {
                    "language_id": "BroaderAI_language_wmdb9u96x5vmdwc",
                    "language_name": "Teamwork",
                    "language_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not LanguageModel.objects.filter(language_name=getData["language_name"].lower()).exists():

            if LanguageModel.objects.filter(language_id = getData["language_id"]).exists():
                serializer = LanguageSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = LanguageModel.objects.get(language_id = getData["language_id"])
                    LastUpdateData.language_name=getData["language_name"].lower()
                    LastUpdateData.language_action = getData["language_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "language is Updated",
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
                    "Message": "language data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "language is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class LanguageGetAPI(APIView):
    '''
        Language API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        LanguageDetails = LanguageModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Language Details",
                "Data": LanguageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class LanguageGetOneAPI(APIView):

    '''
        Get One Language API(View)
        Request : POST
        Data =  {
                    "language_id": "BroaderAI_language_wmdb9u96x5vmdwc"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if LanguageModel.objects.filter(language_id = getData["language_id"]).exists():
            LanguageDetail = LanguageModel.objects.get(language_id = getData["language_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "language Detail",
                    "Data": {
                        "language_id": getData["language_id"],
                        "language_name": LanguageDetail.language_name,
                        "language_action": LanguageDetail.language_action
                    }
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

class LanguageGetActionAPI(APIView):
    '''
        Get Action Language API(View)
        Request : POST
        Data =  {
                    "language_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        LanguageDetails = LanguageModel.objects.filter(language_action = getData["language_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "language Detail",
                "Data": LanguageDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class LanguageDeleteAPI(APIView):

    '''
        Language API(delete)
        Request : delete
        Data =  {
                   "language_id": "BroaderAI_language_wmdb9u96x5vmdwc"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if LanguageModel.objects.filter(language_id = getData["language_id"]).exists():
            LanguageDetail = LanguageModel.objects.get(language_id = getData["language_id"])
            LanguageDetail.delete()
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

class LanguageGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        lang = LanguageModel.objects.all()
        if search_query:
            lang = lang.filter(Q(language_name__istartswith=search_query))

        paginator = Paginator(lang, limit)
        try:
            lang = paginator.page(page)
        except PageNotAnInteger:
            lang = paginator.page(1)
        except EmptyPage:
            lang = paginator.page(paginator.num_pages)

        serialized_data = [{'language_id':language.language_id,'language_name': language.language_name, 'language_name_arabic':language.language_name_arabic,
                            'language_action': language.language_action, 'language_registration_date': language.language_registration_date}
                           for language in lang]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Language Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)

########################################################################
#Job Requirement#

class JobRequirementAPI(APIView):
    '''
        JobRequirementAPI API(Insert)
        Request : POST
        Data = {
                    "job_position_id": "BroaderAI_job_position_3cgqmz8fp6vhc26",
                    "job_level_id": "BroaderAI_job_level_xu67gtz3c87zspr",
                    "job_requirement_description": "required 2 years  of experience",
                    "job_requirement_action": "active"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data

        if not JobRequirementModel.objects.filter(job_requirement_description = getData["job_requirement_description"].lower(),job_position_id = getData["job_position_id"],job_level_id = getData["job_level_id"]).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))
                            
            uniqueID = "BroaderAI_Job_Requirement_" + randomstr
            getData["job_requirement_id"] = uniqueID
            serializer = JobRequirementSerializer(data=getData)

            if serializer.is_valid():

                serializer.save(job_requirement_id=getData["job_requirement_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Requirement is Added",
                    "Data": {
                        "job_requirement_id": getData["job_requirement_id"]
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
                "Message": "Job Requirement is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementGetAPI(APIView):
    '''
        JobRequirement API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        JobRequirementDetails = JobRequirementModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Requirement Details",
                "Data": JobRequirementDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "job_requirement_id": "BroaderAI_Job_Requirement_lc8n9q48aaflkxt"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobRequirementModel.objects.filter(job_requirement_id = getData["job_requirement_id"]).exists():
            jobRequirementDetail = JobRequirementModel.objects.get(job_requirement_id = getData["job_requirement_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Requirement Field Detail",
                    "Data": {
                        "job_requirement_id": getData["job_requirement_id"],
                        "job_position_name": jobRequirementDetail.job_position.job_position_name,
                        "job_position_id": jobRequirementDetail.job_position_id,
                        "job_level_id": jobRequirementDetail.job_level_id,
                        "job_level_name": jobRequirementDetail.job_level.job_level_name,
                        "job_requirement_description": jobRequirementDetail.job_requirement_description,
                        "job_requirement_action": jobRequirementDetail.job_requirement_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Requirement data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementUpdateAPI(APIView):

    '''
        JobRequirement Update API(Insert)
        Request : PATCH
        Data = {
                    "job_requirement_id": "BroaderAI_Job_Requirement_lc8n9q48aaflkxt",
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_requirement_description": "in-depth knowledge",
                    "job_requirement_action": "active"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobRequirementModel.objects.filter(job_requirement_id = getData["job_requirement_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists(): 

                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():

                   
                    serializer = JobRequirementSerializer(data=getData)

                    if serializer.is_valid():
                        jobRequirementData = JobRequirementModel.objects.get(job_requirement_id = getData["job_requirement_id"])
                        jobRequirementData.job_position_id = getData["job_position_id"]
                        jobRequirementData.job_level_id = getData["job_level_id"]
                        jobRequirementData.job_requirement_description = getData["job_requirement_description"]
                        jobRequirementData.job_requirement_action = getData["job_requirement_action"]

                        jobRequirementData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Requirement is Updated",
                            "Data": {
                                "job_requirement_id": getData["job_requirement_id"]
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
                "Message": "Job Requirement data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_requirement_action": "active"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobRequirementModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            JobRequirementDetail = JobRequirementModel.objects.filter(job_position_id = getData["job_position_id"], job_requirement_action = getData["job_requirement_action"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Requirement Field Detail",
                    "Data": JobRequirementDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Requirement data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_requirement_action": "active"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobRequirementModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            jobRequirementDetail = JobRequirementModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"], job_requirement_action = getData["job_requirement_action"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Requirement Field Detail",
                    "Data": jobRequirementDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Requirement data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementDeleteAPI(APIView):
    '''
        JobRequirement API(delete)
        Request : delete
        Data =  {
                    "job_requirement_id": "BroaderAI_Job_Requirement_c6va820mzfwwnz3"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobRequirementModel.objects.filter(job_requirement_id = getData["job_requirement_id"]).exists():
            JobRequirementDetail = JobRequirementModel.objects.get(job_requirement_id = getData["job_requirement_id"])
            JobRequirementDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Requirement is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Requirement data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobRequirementGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        jobRequirement = JobRequirementModel.objects.all()
        
        if search_query:
            jobRequirement = jobRequirement.filter(Q(job_requirement_description__istartswith=search_query))

        paginator = Paginator(jobRequirement, limit)
        try:
            jobRequirement = paginator.page(page)
        except PageNotAnInteger:
            jobRequirement = paginator.page(1)
        except EmptyPage:
            jobRequirement = paginator.page(paginator.num_pages)


        serialized_data = [{'job_requirement_id':jobReq.job_requirement_id,'job_position_id':jobReq.job_position_id,'job_level_id':jobReq.job_level_id,'job_requirement_description': jobReq.job_requirement_description, 'job_requirement_description_arabic':jobReq.job_requirement_description_arabic,
                            'job_requirement_action': jobReq.job_requirement_action, 'job_requirement_registration_date': jobReq.job_requirement_registration_date}
                           for jobReq in jobRequirement]


        res = {
            "Status": "success",
            "Code": 201,
            "Message": "job Requirement Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)


########################################################################
#Job Benefit#

class JobBenefitAPI(APIView):
    '''
        JobBenefitAPI API(Insert)
        Request : POST
        Data = {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_benefit_description": "salary will increased by 2% hike",
                    "job_benefit_action": "active"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if not JobBenefitModel.objects.filter(job_benefit_description = getData["job_benefit_description"].lower(),job_position_id = getData["job_position_id"],job_level_id = getData["job_level_id"]).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))
                            
            uniqueID = "BroaderAI_Job_Benefit_" + randomstr
            getData["job_benefit_id"] = uniqueID
            serializer = JobBenefitSerializer(data=getData)

            if serializer.is_valid():

                serializer.save(job_benefit_id=getData["job_benefit_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Benefit is Added",
                    "Data": {
                        "job_benefit_id": getData["job_benefit_id"]
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
                "Message": "Job Benefit is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitGetAPI(APIView):
    '''
        JobBenefit API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        JobBenefitDetails = JobBenefitModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Benefit Details",
                "Data": JobBenefitDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "job_benefit_id": "BroaderAI_Job_Benefit_rglherved1w03s6"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobBenefitModel.objects.filter(job_benefit_id = getData["job_benefit_id"]).exists():
            jobBenefitDetail = JobBenefitModel.objects.get(job_benefit_id = getData["job_benefit_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Benefit Field Detail",
                    "Data": {
                        "job_benefit_id": getData["job_benefit_id"],
                        "job_position_name": jobBenefitDetail.job_position.job_position_name,
                        "job_position_id": jobBenefitDetail.job_position_id,
                        "job_level_id": jobBenefitDetail.job_level_id,
                        "job_level_name": jobBenefitDetail.job_level.job_level_name,
                        "job_benefit_description": jobBenefitDetail.job_benefit_description,
                        "job_benefit_action": jobBenefitDetail.job_benefit_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Benefit data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitUpdateAPI(APIView):

    '''
        JobBenefit Update API(Insert)
        Request : PATCH
        Data = {
                    "job_benefit_id": "BroaderAI_Job_Benefit_rglherved1w03s6",
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_benefit_description": "salary will increased by 20% hike",
                    "job_benefit_action": "active"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobBenefitModel.objects.filter(job_benefit_id = getData["job_benefit_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists(): 

                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():

                   
                    serializer = JobBenefitSerializer(data=getData)

                    if serializer.is_valid():
                        JobBenefitData = JobBenefitModel.objects.get(job_benefit_id = getData["job_benefit_id"])
                        JobBenefitData.job_position_id = getData["job_position_id"]
                        JobBenefitData.job_level_id = getData["job_level_id"]
                        JobBenefitData.job_benefit_description = getData["job_benefit_description"]
                        JobBenefitData.job_benefit_action = getData["job_benefit_action"]

                        JobBenefitData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Benefit is Updated",
                            "Data": {
                                "job_benefit_id": getData["job_benefit_id"]
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
                "Message": "Job Benefit data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_benefit_action": "active"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobBenefitModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            JobBenefitDetail = JobBenefitModel.objects.filter(job_position_id = getData["job_position_id"], job_benefit_action = getData["job_benefit_action"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Benefit Field Detail",
                    "Data": JobBenefitDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Benefit data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_benefit_action": "active"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobBenefitModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            jobBenefitDetail = JobBenefitModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"], job_benefit_action = getData["job_benefit_action"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Benefit Field Detail",
                    "Data": jobBenefitDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Benefit data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitDeleteAPI(APIView):
    '''
        JobBenefit API(delete)
        Request : delete
        Data =  {
                    "job_benefit_id": "BroaderAI_Job_Benefit_qvzr7swledkyxe3"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobBenefitModel.objects.filter(job_benefit_id = getData["job_benefit_id"]).exists():
            JobBenefitDetail = JobBenefitModel.objects.get(job_benefit_id = getData["job_benefit_id"])
            JobBenefitDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Benefit is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Benefit data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobBenefitGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        JobBenefit = JobBenefitModel.objects.all()
        if search_query:
            JobBenefit = JobBenefit.filter(Q(job_benefit_description__istartswith=search_query))

        paginator = Paginator(JobBenefit, limit)
        try:
            JobBenefit = paginator.page(page)
        except PageNotAnInteger:
            JobBenefit = paginator.page(1)
        except EmptyPage:
            JobBenefit = paginator.page(paginator.num_pages)

        serialized_data = [{'job_benefit_id':jobBene.job_benefit_id,'job_position_id':jobBene.job_position_id,'job_level':jobBene.job_level_id,'job_benefit_description': jobBene.job_benefit_description, 'job_benefit_description_arabic':jobBene.job_benefit_description_arabic,
                            'job_benefit_action': jobBene.job_benefit_action, 'job_benefit_registration_date': jobBene.job_benefit_registration_date}
                           for jobBene in JobBenefit]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "job Benefit Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)


########################################################################
#Job Responsibility#

class JobResponsibilityAPI(APIView):
    '''
        JobResponsibilityAPI API(Insert)
        Request : POST
        Data = {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_responsibility_description": "need to take part in activities",
                    "job_responsibility_action": "active"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if not JobResponsibilityModel.objects.filter(job_responsibility_description = getData["job_responsibility_description"].lower(),job_position_id = getData["job_position_id"],job_level_id = getData["job_level_id"]).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=15))
                            
            uniqueID = "BroaderAI_Job_Responsibility_" + randomstr
            getData["job_responsibility_id"] = uniqueID
            serializer = JobResponsibilitySerializer(data=getData)

            if serializer.is_valid():

                serializer.save(job_responsibility_id=getData["job_responsibility_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Responsibility is Added",
                    "Data": {
                        "job_responsibility_id": getData["job_responsibility_id"]
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
                "Message": "Job Responsibility is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityGetAPI(APIView):
    '''
        JobResponsibility API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        JobResponsibilityDetails = JobResponsibilityModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Responsibility Details",
                "Data": JobResponsibilityDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "job_responsibility_id": "BroaderAI_Job_Responsibility_wfbzuajko79wvya"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobResponsibilityModel.objects.filter(job_responsibility_id = getData["job_responsibility_id"]).exists():
            jobResponsibilityDetail = JobResponsibilityModel.objects.get(job_responsibility_id = getData["job_responsibility_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Responsibility Field Detail",
                    "Data": {
                        "job_responsibility_id": getData["job_responsibility_id"],
                        "job_position_name": jobResponsibilityDetail.job_position.job_position_name,
                        "job_position_id": jobResponsibilityDetail.job_position_id,
                        "job_level_id": jobResponsibilityDetail.job_level_id,
                        "job_level_name": jobResponsibilityDetail.job_level.job_level_name,
                        "job_responsibility_description": jobResponsibilityDetail.job_responsibility_description,
                        "job_responsibility_action": jobResponsibilityDetail.job_responsibility_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message":"Job Responsibility data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityGetfromJobPositionAPI(APIView):
    '''
        Get from job position Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_responsibility_action": "active"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobResponsibilityModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            JobResponsibilityDetail = JobResponsibilityModel.objects.filter(job_position_id = getData["job_position_id"], job_responsibility_action = getData["job_responsibility_action"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Responsibility Field Detail",
                    "Data": JobResponsibilityDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Responsibility data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get from job position and job Level Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_responsibility_action": "active"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobResponsibilityModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"]).exists():
            jobResponsibilityDetail = JobResponsibilityModel.objects.filter(job_position_id = getData["job_position_id"], job_level_id = getData["job_level_id"], job_responsibility_action = getData["job_responsibility_action"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Responsibility Field Detail",
                    "Data": jobResponsibilityDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Responsibility data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityUpdateAPI(APIView):

    '''
        JobResponsibility Update API(Insert)
        Request : PATCH
        Data = {
                    "job_responsibility_id": "BroaderAI_Job_Responsibility_wfbzuajko79wvya",
                    "job_position_id": "BroaderAI_job_position_ke38kgqxen3upem",
                    "job_level_id": "BroaderAI_job_level_lt0klszzj1t8kjc",
                    "job_responsibility_description": "need attentions in meetings",
                    "job_responsibility_action": "active"
                }
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if JobResponsibilityModel.objects.filter(job_responsibility_id = getData["job_responsibility_id"]).exists():
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists(): 

                if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():

                   
                    serializer = JobResponsibilitySerializer(data=getData)

                    if serializer.is_valid():
                        jobResponsibilityData = JobResponsibilityModel.objects.get(job_responsibility_id = getData["job_responsibility_id"])
                        jobResponsibilityData.job_position_id = getData["job_position_id"]
                        jobResponsibilityData.job_level_id = getData["job_level_id"]
                        jobResponsibilityData.job_responsibility_description = getData["job_responsibility_description"]
                        jobResponsibilityData.job_responsibility_action = getData["job_responsibility_action"]

                        jobResponsibilityData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Job Responsibility is Updated",
                            "Data": {
                                "job_responsibility_id": getData["job_responsibility_id"]
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
                "Message": "Job Responsibility data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityDeleteAPI(APIView):

    '''
        JobResponsibility API(delete)
        Request : delete
        Data =  {
                    "job_responsibility_id": "BroaderAI_Job_Responsibility_f4bf5anj2sut7hw"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobResponsibilityModel.objects.filter(job_responsibility_id = getData["job_responsibility_id"]).exists():
            JobResponsibilityDetail = JobResponsibilityModel.objects.get(job_responsibility_id = getData["job_responsibility_id"])
            JobResponsibilityDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Responsibility is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Responsibility data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class JobResponsibilityGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]

        jobResDetail = JobResponsibilityModel.objects.all()

        if search_query:
            jobResDetail = jobResDetail.filter(Q(job_responsibility_description__istartswith=search_query))

        paginator = Paginator(jobResDetail, limit)

        try:
            jobResDetail = paginator.page(page)
        except PageNotAnInteger:
            jobResDetail = paginator.page(1)
        except EmptyPage:
            jobResDetail = paginator.page(paginator.num_pages)

        serialized_data = [{'job_responsibility_id':respons.job_responsibility_id,'job_position_id':respons.job_position_id,'job_level':respons.job_level_id,'job_responsibility_description': respons.job_responsibility_description, 'job_responsibility_description_arabic':respons.job_responsibility_description_arabic,
                            'job_responsibility_action': respons.job_responsibility_action, 'job_responsibility_registration_date': respons.job_responsibility_registration_date}
                           for respons in jobResDetail]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "job Responsibility Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)
    
#######################################
# Education -- BE, ME, BSC, etc
#######################################
class EducationAPI(APIView):
    '''
        Education API(INSERT)
        Request : POST
        Data =  {
                    "education_name": "M.TECH",
                    "education_years": "5 years",
                    "education_action": "active"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if not EducationModel.objects.filter(education_name=getData["education_name"].lower()).exists():
            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_education_" + randomstr
            getData["education_id"] = uniqueID
            serializer = EducationSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(education_id=getData["education_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education is Added",
                    "Data": {   "education_id" : getData['education_id']
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

class EducationUpdateAPI(APIView):
    '''
        Education API(Update)
        Request : Patch
        Data =  {
                "education_id": "BroaderAI_education_cy8wozxg1w5s9bw",
                "education_name": "M.TECH",
                "education_years": "5 years",
                "education_action": "active"
            }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request
        if not EducationModel.objects.filter(education_name=getData["education_name"].lower(), education_years=getData["education_years"].lower()).exists():
            if EducationModel.objects.filter(education_id = getData["education_id"]).exists():
                serializer = EducationSerializer(data=getData)
                if serializer.is_valid():
                    LastUpdateData = EducationModel.objects.get(education_id = getData["education_id"])
                    LastUpdateData.education_name=getData["education_name"].lower()
                    LastUpdateData.education_years=getData["education_years"]
                    LastUpdateData.education_action = getData["education_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education is Updated",
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
                    "Message": "Education data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education data is already exist",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationGetAPI(APIView):
    '''
        Education API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        educationDetails = EducationModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Education Details",
                "Data": educationDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class EducationGetOneAPI(APIView):
    '''
        Get One Education API(View)
        Request : POST
        Data =  {
                    "education_id": "BroaderAI_yashpp3622_eibf9nnjma"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if EducationModel.objects.filter(education_id = getData["education_id"]).exists():
            educationDetail = EducationModel.objects.get(education_id = getData["education_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education Detail",
                    "Data": {
                        "education_id": getData["education_id"],
                        "education_name": educationDetail.education_name,
                        "education_years": educationDetail.education_years,
                        "education_action": educationDetail.education_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationGetActionAPI(APIView):
    '''
        Get Action Education API(View)
        Request : POST
        Data =  {
                    "education_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        educationDetails = EducationModel.objects.filter(education_action = getData["education_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Education Detail",
                "Data": educationDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class EducationDeleteAPI(APIView):
    '''
        Education API(delete)
        Request : delete
        Data =  {
                    "education_id":"BroaderAI_Lasteducation2f6rfvw6whe2j6h"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if EducationModel.objects.filter(education_id = getData["education_id"]).exists():
            educationDetail = EducationModel.objects.get(education_id = getData["education_id"])
            educationDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        education = EducationModel.objects.all()
        if search_query:
            education = education.filter(Q(education_name__istartswith=search_query))

        paginator = Paginator(education, limit)
        try:
            education = paginator.page(page)
        except PageNotAnInteger:
            education = paginator.page(1)
        except EmptyPage:
            education = paginator.page(paginator.num_pages)

        serialized_data = [{'education_id':edu.education_id,'education_name': edu.education_name, 'education_name_arabic':edu.education_name_arabic,'education_years':edu.education_years,'education_years_arabic':edu.education_years_arabic,
                            'education_action': edu.education_action, 'education_registration_date': edu.education_registration_date}
                           for edu in education]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Education Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)
  
#######################################

#######################################
# Education Field -- Computer Science, Data science, Information Technology , etc
#######################################
class EducationFieldAPI(APIView):
    '''
        Education Field API(INSERT)
        Request : POST
        Data =  {
                    "education_field_name": "Data Science"
                    "sector_id": "BroaderAI_education_yashpp3622_eibf9nnjma"
                    "education_field_action": "active"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():
            if not EducationFieldModel.objects.filter(sector_id=getData["sector_id"], education_field_name=getData["education_field_name"].lower()).exists():
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_education_field_" + randomstr
                getData["education_field_id"] = uniqueID
                serializer = EducationFieldSerializer(data=getData)
                if serializer.is_valid():
                    serializer.save(education_field_id=getData["education_field_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Education Field is Added",
                        "Data": {   "education_field_id" : getData['education_field_id']
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
                    "Message": "Sector data with education field is already exists",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationFieldUpdateAPI(APIView):
    '''
        Education Field API(Update)
        Request : Patch
        Data =  {
                    "education_field_id": "BroaderAI_education_yashpp3622_eibf9nnjma",
                    "education_field_name": "M.TECH"
                    "sector_id": "BroaderAI_education_yashpp3622_eibf9nnjma"
                    "education_field_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request
        if EducationFieldModel.objects.filter(education_field_id = getData["education_field_id"]).exists():
            if not EducationFieldModel.objects.filter(sector_id=getData["sector_id"], education_field_name=getData["education_field_name"].lower()).exists():
                if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():
                    serializer = EducationFieldSerializer(data=getData)
                    if serializer.is_valid():
                        LastUpdateData = EducationFieldModel.objects.get(education_field_id = getData["education_field_id"])
                        LastUpdateData.education_field_name = getData["education_field_name"].lower()
                        LastUpdateData.sector_id = getData["sector_id"]
                        LastUpdateData.education_field_action = getData["education_field_action"]
                        LastUpdateData.save()
                        res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Education is Updated",
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
                        "Message": "Education Sector is not found",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Sector data with education field is already exists",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationFieldGetAPI(APIView):
    '''
        Education Field API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        educationFieldDetails = EducationFieldModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Education Field Details",
                "Data": educationFieldDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class EducationFieldGetOneAPI(APIView):
    '''
        Get One Education Field API(View)
        Request : POST
        Data =  {
                    "education_field_id": "BroaderAI_education_field_iup4xsiwtnw2uip"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if EducationFieldModel.objects.filter(education_field_id = getData["education_field_id"]).exists():
            educationDetail = EducationFieldModel.objects.get(education_field_id = getData["education_field_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education Field Detail",
                    "Data": {
                        "education_field_id": getData["education_field_id"],
                        "education_field_name": educationDetail.education_field_name,
                        "sector_id": educationDetail.sector_id,
                        "education_field_action": educationDetail.education_field_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education Field data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationFieldGetSectorAPI(APIView):
    '''
        Get Education Field Sector API(View)
        Request : POST
        Data =  {
                    "sector_id": "BroaderAI_yashpp3622_eibf9nnjma"
                    "education_field_action": "active"                          # "deactive" / "all"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if EducationFieldModel.objects.filter(sector_id = getData["sector_id"]).exists():
            if getData["education_field_action"] == "active":
                educationFieldDetail = EducationFieldModel.objects.filter(sector_id = getData["sector_id"], education_field_action = "active").values()
            elif getData["education_field_action"] == "deactive":
                educationFieldDetail = EducationFieldModel.objects.filter(sector_id = getData["sector_id"], education_field_action = "deactive").values()
            else:
                educationFieldDetail = EducationFieldModel.objects.filter(sector_id = getData["sector_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Sectorwise Education Field Detail",
                    "Data": educationFieldDetail
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education Field data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationFieldDeleteAPI(APIView):
    '''
        Education API(delete)
        Request : delete
        Data =  {
                    "education_field_id":"BroaderAI_Lasteducation2f6rfvw6whe2j6h"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data

        if EducationFieldModel.objects.filter(education_field_id = getData["education_field_id"]).exists():
            educationFieldDetail = EducationFieldModel.objects.get(education_field_id = getData["education_field_id"])
            educationFieldDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Education Field is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Education Field data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class EducationFieldGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        eduField = EducationFieldModel.objects.all()
        if search_query:
            eduField = eduField.filter(Q(education_field_name__istartswith=search_query))

        paginator = Paginator(eduField, limit)
        try:
            eduField = paginator.page(page)
        except PageNotAnInteger:
            eduField = paginator.page(1)
        except EmptyPage:
            eduField = paginator.page(paginator.num_pages)

        serialized_data = [{'education_field_id':edu.education_field_id,'education_field_name': edu.education_field_name, 'education_field_name_arabic':edu.education_field_name_arabic,'sector_id':edu.sector_id,'education_field_action': edu.education_field_action, 'education_field_registration_date': edu.education_field_registration_date}
                           for edu in eduField]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Education Field Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)


########################################################################
# Nationality #

class NationalityRegisterAPI(APIView):
    '''
        nationality API(INSERT)
        Request : POST
        Data =  {
                    "nationality_name": "Surat",
                    "nationality_action": "active"
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        if not NationalityModel.objects.filter(nationality_name=getData["nationality_name"].lower()).exists():
            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "BroaderAI_nationality_" + randomstr
            getData["nationality_id"] = uniqueID
            serializer = NationalitySerializer(data=getData)
            if serializer.is_valid():
                serializer.save(nationality_id=getData["nationality_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "nationality is Added",
                    "Data": {   "nationality_id" : getData['nationality_id']
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
                    "Message": "nationality is already exits",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

class NationalityUpdateAPI(APIView):
    '''
        nationality API(Update)
        Request : Patch
        Data =  {
                    "nationality_id": "BroaderAI_nationality_jinkty65gau6zrl",
                    "nationality_name": "Kolkata",
                    "nationality_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request
        if not NationalityModel.objects.filter(nationality_name=getData["nationality_name"].lower()).exists():
            if NationalityModel.objects.filter(nationality_id = getData["nationality_id"]).exists():
                serializer = NationalitySerializer(data=getData)
                if serializer.is_valid():
                    LastUpdateData = NationalityModel.objects.get(nationality_id = getData["nationality_id"])
                    LastUpdateData.nationality_name=getData["nationality_name"].lower()
                    LastUpdateData.nationality_action = getData["nationality_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "nationality is Updated",
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
                    "Message": "nationality data is not found",
                    "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "nationality is already exits",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class NationalityGetAPI(APIView):
    '''
        location_ API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        nationalityDetails = NationalityModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Nationality Details",
                "Data": nationalityDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)

class NationalityGetOneAPI(APIView):
    '''
        Get One nationality API(View)
        Request : POST
        Data =  {
                    "nationality_id": "BroaderAI_nationality_jinkty65gau6zrl"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if NationalityModel.objects.filter(nationality_id = getData["nationality_id"]).exists():
            nationalityDetail = NationalityModel.objects.get(nationality_id = getData["nationality_id"])
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "nationality Detail",
                    "Data": {
                        "nationality_id": getData["nationality_id"],
                        "nationality_name": nationalityDetail.nationality_name,
                        "nationality_action": nationalityDetail.nationality_action
                    }
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "nationality data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class NationalityGetActionAPI(APIView):
    '''
        Get Action nationality API(View)
        Request : POST
        Data =  {
                    "nationality_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        nationalityDetails = NationalityModel.objects.filter(nationality_action = getData["nationality_action"]).values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "nationality Detail",
                "Data": nationalityDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
        
class NationalityDeleteAPI(APIView):
    '''
        nationality API(delete)
        Request : delete
        Data =  {
                    "nationality_id": "BroaderAI_nationality_jinkty65gau6zrl"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if NationalityModel.objects.filter(nationality_id = getData["nationality_id"]).exists():
            nationalityDetail = NationalityModel.objects.get(nationality_id = getData["nationality_id"])
            nationalityDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "nationality is successfully Deleted",
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "nationality data is not found",
                "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

class NationalityGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        nationDetail = NationalityModel.objects.all()
        if search_query:
            nationDetail = nationDetail.filter(Q(nationality_name__istartswith=search_query))

        paginator = Paginator(nationDetail, limit)
        try:
            nationDetail = paginator.page(page)
        except PageNotAnInteger:
            nationDetail = paginator.page(1)
        except EmptyPage:
            nationDetail = paginator.page(paginator.num_pages)

        serialized_data = [{'nationality_id':nation.nationality_id,'nationality_name': nation.nationality_name, 'nationality_name_arabic':nation.nationality_name_arabic,
                            'nationality_action': nation.nationality_action, 'nationality_registration_date': nation.nationality_registration_date}
                           for nation in nationDetail]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Nationality Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)
 


#######################################
# univeristy -- ppsu, maliba, scet, svnit , etc
#######################################

class UniversityRegisterAPI(APIView):
    '''
        univeristy API(INSERT)
        Request : POST
        Data =  {
                    "university_name" :"scet",
                    "university_action":"active"
                }
    '''
    def post(self, request ,format=None):

        try:

            getData = request.data
            
            if not UniversityModel.objects.filter(university_name = getData["university_name"].lower()).exists():

                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_university_" + randomstr
                getData["university_id"] = uniqueID
                serializer = UniversitySerializer(data=getData)
                if serializer.is_valid():
                    serializer.save(university_id = getData["university_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "University is Added",
                        "Data": {   "university_id" : getData['university_id']
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
                        "Message": "University is already exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass

class UniversityGetAPI(APIView):
    '''
        University API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        try:

            getData = request.data
            universityDetails = UniversityModel.objects.values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "University Details",
                    "Data": universityDetails
                }
            return Response(res, status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass

class UniversityGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        uniDetail = UniversityModel.objects.all()
        if search_query:
            uniDetail = uniDetail.filter(Q(university_name__istartswith=search_query))

        paginator = Paginator(uniDetail, limit)
        try:
            uniDetail = paginator.page(page)
        except PageNotAnInteger:
            uniDetail = paginator.page(1)
        except EmptyPage:
            uniDetail = paginator.page(paginator.num_pages)

        serialized_data = [{'university_id':uni.university_id,'university_name': uni.university_name, 'university_name_arabic':uni.university_name_arabic,
                            'university_action': uni.university_action, 'university_registration_date': uni.university_registration_date}
                           for uni in uniDetail]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "University Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)
 

#######################################
# degree -- master in IT, Bachelor in CE, etc
#######################################


class DegreeRegisterAPI(APIView):
    '''
        degree API(INSERT)
        Request : POST
        Data =  {
                    "degree_name" :"scet",
                    "degree_action":"active"
                }
    '''
    def post(self, request ,format=None):

        try:

            getData = request.data
            
            if not DegreeModel.objects.filter(degree_name = getData["degree_name"].lower()).exists():

                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
                uniqueID = "BroaderAI_degree_" + randomstr
                getData["degree_id"] = uniqueID
                serializer = DegreeSerializer(data=getData)
                if serializer.is_valid():
                    serializer.save(degree_id = getData["degree_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "degree is Added",
                        "Data": {   "degree_id" : getData['degree_id']
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
                        "Message": "degree is already exits",
                        "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass

class DegreeGetAPI(APIView):
    '''
        degree API(View)
        Request : GET
    ''' 
    def get(self, request, format=None):
        
        try:

            getData = request.data
            degreeDetails = DegreeModel.objects.values()
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "degree Details",
                    "Data": degreeDetails
                }
            return Response(res, status=status.HTTP_201_CREATED)

        except Exception as e:
            # logging.error('Error: ',e)
            pass
    
class DegreeGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        degreeDetail = DegreeModel.objects.all()
        if search_query:
            degreeDetail = degreeDetail.filter(Q(degree_name__istartswith=search_query))

        paginator = Paginator(degreeDetail, limit)
        try:
            degreeDetail = paginator.page(page)
        except PageNotAnInteger:
            degreeDetail = paginator.page(1)
        except EmptyPage:
            degreeDetail = paginator.page(paginator.num_pages)

        serialized_data = [{'degree_id':deg.degree_id,'degree_name': deg.degree_name, 'degree_name_arabic':deg.degree_name_arabic,
                            'degree_action': deg.degree_action, 'degree_registration_date': deg.degree_registration_date}
                           for deg in degreeDetail]

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Degree Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page}
        }

        return Response(res, status=status.HTTP_201_CREATED)
 