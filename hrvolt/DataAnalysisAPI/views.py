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
from databaseAPI.models import *
from candidateresumeAPI.models import *
from candidateresumeAPI.serializers import *
from databaseAPI.serializers import *
from candidatePreferenceAPI.models import *
from recruiterAPI.models import *
import json
from hrvolt.emailsend import mailSend
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from django.db.models import Count

from collections import Counter
    
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from calendar import month_name

#######################################
#######################################

class TopProjectAPI(APIView):

    def post(self, request ,format=None):

        project_count_per_user = CandidateProjectModel.objects.values('user_id').annotate(project_count=Count('candidate_resume_project_id'))

    
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "project is Added",
                "Data": project_count_per_user
                }
        return Response(res, status=status.HTTP_201_CREATED)

class TotalDegreeAPI(APIView):

    def post(self, request, format=None):
        degree_details = CandidateMainEducationDetails.objects.all()

        degree_counts = degree_details.values('candidate_degree_name').annotate(total_degree=Count('candidate_degree_name'))

        degree_count_map = {entry['candidate_degree_name']: entry['total_degree'] for entry in degree_counts}

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "degree details retrieved successfully",
                "Data": {
                    "Total degree Counts": degree_count_map
                },
            }

        return Response(res, status=status.HTTP_201_CREATED)


class TotalWorkPlacePreferenceAPI(APIView):

    def post(self, request, format=None):
        wrkplace_details = CandidateMainExperienceModel.objects.all()

        wrkplace_counts = wrkplace_details.values('candidate_work_place__work_place_name').annotate(total_wrkplace=Count('candidate_work_place'))

        wrkplace_count_map = {entry['candidate_work_place__work_place_name']: entry['total_wrkplace'] for entry in wrkplace_counts}

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Work Place details retrieved successfully",
                "Data": {
                    "Total Work Place Counts": wrkplace_count_map
                },
            }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalTechSkillPreferenceAPI(APIView):

    def post(self, request, format=None):
        tech_details = CandidateTechnicalskillsModel.objects.all()

        tech_counts = tech_details.values('candidate_technical_skill__unique_technical_skills_name').annotate(total_tech=Count('candidate_technical_skill'))

        tech_count_map = {entry['candidate_technical_skill__unique_technical_skills_name']: entry['total_tech'] for entry in tech_counts}

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Technical Skills details retrieved successfully",
                "Data": {
                    "technical_skills_counts": tech_count_map
                },
            }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalSoftSkillPreferenceAPI(APIView):

    def post(self, request, format=None):
        soft_details = CandidateSoftskillsModel.objects.all()

        soft_counts = soft_details.values('candidate_soft_skill_name').annotate(total_soft=Count('candidate_soft_skill'))

        soft_count_map = {entry['candidate_soft_skill_name']: entry['total_soft'] for entry in soft_counts}

        sorted_soft_count = dict(sorted(soft_count_map.items(), key=lambda x: x[1], reverse=True)[:7])


        res = {
                "Status": "success",
                "Code": 201,
                "Message": "softnical Skills details retrieved successfully",
                "Data": {
                    "soft_skills_counts": sorted_soft_count
                },
            }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalLanguageAPI(APIView):

    def post(self, request, format=None):

        lang_details = CandidateLanguageModel.objects.all()

        lang_counts = lang_details.values('candidate_language_name').annotate(total_lang=Count('candidate_language_name')).order_by('-total_lang')[:5]

        lang_count_map = {entry['candidate_language_name']: entry['total_lang'] for entry in lang_counts}

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Language details retrieved successfully",
                "Data": {
                    "Top_Five_Languages": lang_count_map
                },
            }

        return Response(res, status=status.HTTP_201_CREATED)   

class EmployTypePrefAPI(APIView):

    def post(self, request, format=None):
        emptype_details = CandidateEmploymentTypePreferenceModel.objects.all()

        emptype_counts = emptype_details.values('employment_type_name').annotate(total_emptype=Count('employment_type_name'))

        emptype_count_map = {entry['employment_type_name']: entry['total_emptype'] for entry in emptype_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Employment Type details retrieved successfully",
            "Data": {
                "TotalEmploymentTypeCounts": emptype_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)   

class NationalityAPI(APIView):

    def post(self, request, format=None):

        nation_counts = NewUser.objects.values('user_country').annotate(total_nation=Count('user_country')).order_by('-total_nation')[:5]

        nation_count_map = {entry['user_country']: entry['total_nation'] for entry in nation_counts}

        nationality_names = NationalityModel.objects.filter(nationality_id__in=nation_count_map.keys()).values('nationality_id', 'nationality_name')

        nationality_name_map = {entry['nationality_id']: entry['nationality_name'] for entry in nationality_names}

        nation_count_map_with_names = {nationality_name_map.get(k, k): v for k, v in nation_count_map.items()}

        if "None" in nation_count_map_with_names.keys():
            del nation_count_map_with_names[None]

    

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Nationality details retrieved successfully",
            "Data": {
                "TopFiveNationalities": nation_count_map_with_names
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class JobPositionPreferAPI(APIView):

    def post(self, request, format=None):
        jobPos_details = CandidatePreferenceModel.objects.all()

        jobPos_counts = jobPos_details.values('job_position__job_position_name').annotate(total_jobPos=Count('job_position'))

        jobPos_count_map = {entry['job_position__job_position_name']: entry['total_jobPos'] for entry in jobPos_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Job Position details by user",
            "Data": {
                "Total Job Position Counts per user": jobPos_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalJobPositionAPI(APIView):

    def post(self, request, format=None):
        jobPos_details = JobPositionModel.objects.all()

        jobPos_counts = jobPos_details.values('job_position_name').annotate(total_jobPos=Count('job_position_name'))

        jobPos_count_map = {entry['job_position_name']: entry['total_jobPos'] for entry in jobPos_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Total Job Position ",
            "Data":{
                "Total Job Position":len(jobPos_counts),
                "Total Job Position Counts": jobPos_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class JobLevelPreferAPI(APIView):

    def post(self, request, format=None):
        jobLevel_details = CandidatePreferenceModel.objects.all()

        jobLevel_counts = jobLevel_details.values('job_level__job_level_name').annotate(total_jobLevel=Count('job_level'))

        jobLevel_count_map = {entry['job_level__job_level_name']: entry['total_jobLevel'] for entry in jobLevel_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Job Level details by user",
            "Data": {
                "Total Job Level Counts per user": jobLevel_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalJobLevelAPI(APIView):

    def post(self, request, format=None):
        jobLevel_details = JobLevelModel.objects.all()

        jobLevel_counts = jobLevel_details.values('job_level_name').annotate(total_jobLevel=Count('job_level_name'))

        jobLevel_count_map = {entry['job_level_name']: entry['total_jobLevel'] for entry in jobLevel_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Total Job Level ",
            "Data":{
                "Total Job Level":len(jobLevel_counts),
                "Total Job Level Counts": jobLevel_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

######################################################################
    ### EDUCATION

class TotalUniqueEducationAPI(APIView):

    def post(self, request ,format=None):

        education_details = CandidateBasicEducationDetails.objects.all()
        
        serializer = CandidateBasicEducationDetailsSerializer(education_details, many=True)

        serialized_data = serializer.data

        unique_education_levels = set(detail['candidate_last_education_id'] for detail in serialized_data)
        unique_education_fields = set(detail['candidate_last_education_field_id'] for detail in serialized_data)

        education_level_names = EducationModel.objects.filter(candidatebasiceducationdetails__candidate_last_education__in=unique_education_levels).values('candidatebasiceducationdetails__candidate_last_education', 'candidatebasiceducationdetails__candidate_last_education__education_name')
        
        education_field_names = EducationFieldModel.objects.filter(candidatebasiceducationdetails__candidate_last_education_field__in=unique_education_fields).values('candidatebasiceducationdetails__candidate_last_education_field', 'candidatebasiceducationdetails__candidate_last_education_field__education_field_name')

        education_level_name_map = {edu['candidatebasiceducationdetails__candidate_last_education']: edu['candidatebasiceducationdetails__candidate_last_education__education_name'] for edu in education_level_names}
        education_field_name_map = {field['candidatebasiceducationdetails__candidate_last_education_field']: field['candidatebasiceducationdetails__candidate_last_education_field__education_field_name'] for field in education_field_names}

        for detail in serialized_data:
            detail['education_name'] = education_level_name_map.get(detail['candidate_last_education_id'])
            detail['education_field_name'] = education_field_name_map.get(detail['candidate_last_education_field_id'])

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Education details retrieved successfully",
            "Data": {
                "serialized_data": serialized_data,
                "TotalUniqueEducationLevels": len(unique_education_levels),
                "TotalUniqueEducationFields": len(unique_education_fields),
                "education_name": list(set(detail['education_name'] for detail in serialized_data if 'education_name' in detail)),
                "education_field_name": list(set(detail['education_field_name'] for detail in serialized_data if 'education_field_name' in detail))
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalEducationAPI(APIView):

    def post(self, request, format=None):
        education_details = CandidateBasicEducationDetails.objects.all()

        education_counts = education_details.values('candidate_last_education__education_name').annotate(total_education=Count('candidate_last_education'))

        education_count_map = {entry['candidate_last_education__education_name']: entry['total_education'] for entry in education_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Education details retrieved successfully",
            "Data":{
                "Total Education Counts": education_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class EducationbyJobLevelAPI(APIView):
    '''
    candidate education by job level
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        getData = request.data
        response_data = []

        candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()

        for record in candidateData:
            user_id = record['user_id']

            candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id=user_id)
            educationdata = EducationModel.objects.get(education_id=candidateBasicEducationData.candidate_last_education_id)
            educationfielddata = EducationFieldModel.objects.get(education_field_id=candidateBasicEducationData.candidate_last_education_field_id)

            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Basic Education Detail",
                "Data": {
                    "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                    "user_id": user_id,
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
            response_data.append(res)


        return Response(response_data, status=status.HTTP_201_CREATED)

class EducationbyJobPositionAPI(APIView):
    '''
    candidate education by job position
    request : Post
    data = {
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        getData = request.data
        response_data = []

        candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()

        for record in candidateData:
            user_id = record['user_id']

            candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id=user_id)
            educationdata = EducationModel.objects.get(education_id=candidateBasicEducationData.candidate_last_education_id)
            educationfielddata = EducationFieldModel.objects.get(education_field_id=candidateBasicEducationData.candidate_last_education_field_id)

            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Basic Education Detail",
                "Data": {
                    "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                    "user_id": user_id,
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
            response_data.append(res)


        return Response(response_data, status=status.HTTP_201_CREATED)

class EducationDashboardAPI(APIView):
    '''
    candidate education dashboard
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):

        getData = request.data
        response_data = []
        education_counts = Counter()
        user_counts = Counter()

        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"],job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()         

        for record in candidateData:
            user_id = record['user_id']

            if CandidateBasicEducationDetails.objects.filter(user_id=user_id).exists():

                candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id=user_id)
                educationdata = EducationModel.objects.get(education_id=candidateBasicEducationData.candidate_last_education_id)
                educationfielddata = EducationFieldModel.objects.get(education_field_id=candidateBasicEducationData.candidate_last_education_field_id)

                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Candidate Basic Education Detail",
                    "Data": {
                        "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                        "user_id": user_id,
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
                
                response_data.append(res)
                education_counts.update({educationdata.education_name: 1})

                user_counts.update({user_id: 1})

        total_education_counts = dict(education_counts)
        total_user_count = len(user_counts)

        result = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Basic Education",
            "Data": {
                "response_data":response_data,
                "Total_Education_Counts": total_education_counts,
                "User Count": total_user_count,
            }
        }


        return Response(result, status=status.HTTP_201_CREATED)

######################################################################
    ### EDUCATION FIELD

class EducationFieldDashboardAPI(APIView):
    '''
    candidate education dashboard
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):

        getData = request.data
        response_data = []
        eduField_counts = Counter()
        user_counts = Counter()

        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"],job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()         

        for record in candidateData:

            user_id = record['user_id']

            if CandidateBasicEducationDetails.objects.filter(user_id=user_id).exists():

                candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id=user_id)
                educationfielddata = EducationFieldModel.objects.get(education_field_id=candidateBasicEducationData.candidate_last_education_field_id)

                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Candidate Basic Education Detail",
                    "Data": {
                        "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                        "user_id": user_id,
                        "candidate_last_education_field_id": candidateBasicEducationData.candidate_last_education_field_id,
                        "candidate_last_education_field_name": educationfielddata.education_field_name,
                        "candidate_last_education_field_name_arabic": educationfielddata.education_field_name_arabic
                    }
                }
                
                response_data.append(res)
                eduField_counts.update({educationfielddata.education_field_name: 1})

                user_counts.update({user_id: 1})

        total_eduField_counts = dict(eduField_counts)
        UserCount = len(user_counts)

        result = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Basic Education",
            "Data": {
                "response_data":response_data,
                "TotalEduFieldCounts": total_eduField_counts,
                "UserCount": UserCount,
            }
        }

        return Response(result, status=status.HTTP_201_CREATED)

class EducationFieldbyJobLevelAPI(APIView):
    '''
    candidate education field by job level
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        getData = request.data
        response_data = []

        candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()

        for record in candidateData:
            user_id = record['user_id']

            candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id=user_id)
            educationfielddata = EducationFieldModel.objects.get(education_field_id=candidateBasicEducationData.candidate_last_education_field_id)

            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Basic Education Detail",
                "Data": {
                    "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                    "user_id": user_id,
                    "candidate_last_education_field_id": candidateBasicEducationData.candidate_last_education_field_id,
                    "candidate_last_education_field_name": educationfielddata.education_field_name,
                    "candidate_last_education_field_name_arabic": educationfielddata.education_field_name_arabic
                }
            }
            response_data.append(res)


        return Response(response_data, status=status.HTTP_201_CREATED)

class EducationFieldbyJobPositionAPI(APIView):
    '''
    candidate education field by job position
    request : Post
    data = {
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        getData = request.data
        response_data = []

        candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()

        for record in candidateData:
            user_id = record['user_id']

            candidateBasicEducationData = CandidateBasicEducationDetails.objects.get(user_id=user_id)
            educationfielddata = EducationFieldModel.objects.get(education_field_id=candidateBasicEducationData.candidate_last_education_field_id)

            res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Basic Education Detail",
                "Data": {
                    "candidate_resume_basic_education_id": candidateBasicEducationData.candidate_resume_basic_education_id,
                    "user_id": user_id,
                    "candidate_last_education_field_id": candidateBasicEducationData.candidate_last_education_field_id,
                    "candidate_last_education_field_name": educationfielddata.education_field_name,
                    "candidate_last_education_field_name_arabic": educationfielddata.education_field_name_arabic
                }
            }
            response_data.append(res)


        return Response(response_data, status=status.HTTP_201_CREATED)
    
class TotalEducationFieldAPI(APIView):

    def post(self, request, format=None):
        education_details = CandidateBasicEducationDetails.objects.all()

        education_field_counts = education_details.values('candidate_last_education_field__education_field_name').annotate(total_eduField=Count('candidate_last_education_field'))

        education_field_count_map = {entry['candidate_last_education_field__education_field_name']: entry['total_eduField'] for entry in education_field_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Education Field details retrieved successfully",
            "Data":{
                "Total Education Field Counts": education_field_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

######################################################################
    ### MAIN EDUCATION

class TotalUniversityAPI(APIView):

    def post(self, request, format=None):
        university_details = CandidateMainEducationDetails.objects.all()

        university_counts = university_details.values('candidate_univeresity_name').annotate(total_university=Count('candidate_univeresity_name'))

        university_count_map = {entry['candidate_univeresity_name']: entry['total_university'] for entry in university_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "university details retrieved successfully",
            "Data": {
                "Total university Counts": university_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class MainEducationDashboardAPI(APIView):
    '''
    candidate education dashboard
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        

        getData = request.data
        response_data = []
        university_counts = Counter()
        degree_counts = Counter()
        user_counts = Counter()

        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"],job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()         


        for record in candidateData:
            user_id = record['user_id']

            finalData = []
            

            candidateMainEducationData = CandidateMainEducationDetails.objects.filter(user_id=user_id).values()
            for data in candidateMainEducationData:
                finalData.append(data)
                # Count universities and degrees
                university_counts.update({data['candidate_univeresity_name']: 1})
                degree_counts.update({data['candidate_degree_name']: 1})

            # Count each user only once
            user_counts.update({user_id: 1})

            response_data.append(finalData)

        total_university_counts = dict(university_counts.most_common(5))
        total_degree_counts = dict(degree_counts.most_common(5))
        UserCount = len(user_counts)



        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Main Education Detail",
            "Data": {
                "response_data":response_data,
                "TotalUniversityCounts": total_university_counts,
                "TotalDegreeCounts": total_degree_counts,
                "UserCount": UserCount,
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class TotalDegreeAPI(APIView):

    def post(self, request, format=None):
        degree_details = CandidateMainEducationDetails.objects.all()

        degree_counts = degree_details.values('candidate_degree_name').annotate(total_degree=Count('candidate_degree_name'))

        degree_count_map = {entry['candidate_degree_name']: entry['total_degree'] for entry in degree_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "degree details retrieved successfully",
            "Data":{
                "Total degree Counts": degree_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

######################################################################
    ### TECHNICAL SKILLS

class TotalTechSkillPreferenceAPI(APIView):

    def post(self, request, format=None):
        tech_details = CandidateTechnicalskillsModel.objects.all()

        tech_counts = tech_details.values('candidate_technical_skill__unique_technical_skills_name').annotate(total_tech=Count('candidate_technical_skill'))

        tech_count_map = {entry['candidate_technical_skill__unique_technical_skills_name']: entry['total_tech'] for entry in tech_counts}

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Technical Skills details retrieved successfully",
            "Data": {
                "Total Technical Skills Counts": tech_count_map
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

class TechnicalSkillDashboardAPI(APIView):
    '''
    candidate education dashboard
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        

        getData = request.data
        response_data = []
        user_counts = Counter()

        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"],job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()         


        tech = []
        for record in candidateData:

            user_id = record['user_id']
            
            finalData = []

            candidateTechSkillData = CandidateTechnicalskillsModel.objects.filter(user_id=user_id).values()
            
            for data in candidateTechSkillData:
                finalData.append(data)
                tech.append(data["candidate_technical_skill_name"])
        
            user_counts.update({user_id: 1})
            response_data.append(finalData)
       

        skill_counts = Counter(tech)
        result = dict(skill_counts)
        result_users = dict(user_counts)
        UserCount = len(result_users)

        sorted_tech_count = dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])


        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Technical Skills Detail",
            "Data": {
                "response_data":response_data,
                "tech_count":sorted_tech_count,
                "UserCount":UserCount
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)
    
######################################################################
    ### PROJECT 

class ProjectCountPerUserAPI(APIView):

    def post(self, request ,format=None):

        project_count_per_user = CandidateProjectModel.objects.values('user_id').annotate(project_count=Count('candidate_resume_project_id'))

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "project is Added",
                "Data": project_count_per_user
                }
        return Response(res, status=status.HTTP_201_CREATED)
    
class ProjectDurationDashboardAPI(APIView):
    '''
    candidate project dashboard
    request: Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        getData = request.data
        response_data = []
        user_counts = Counter()
        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"], job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()

        duration_data = {}
        proj = []

        for record in candidateData:
            user_id = record['user_id']
            finalData = []
            
            candidateProjData = CandidateProjectModel.objects.filter(user_id=user_id).values()

            for data in candidateProjData:
                start_date = datetime.strptime(data['candidate_project_start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['candidate_project_end_date'], "%Y-%m-%d")
                proj.append(data["candidate_resume_project_id"])
                duration = (end_date - start_date).days

                if duration <= 90:
                    duration_range = "1-3 months"
                elif 91 <= duration <= 180:
                    duration_range = "4-6 months"
                elif 181 <= duration <= 365:
                    duration_range = "7-12 months"
                else:
                    duration_range = "More than 1 year"

                if duration_range in duration_data:
                    duration_data[duration_range] += 1
                else:
                    duration_data[duration_range] = 1


                finalData.append(data)
            user_counts.update({user_id: 1})
            response_data.append(finalData)

        proj_count = Counter(proj)
        total_proj_count = len(proj_count)
        result_users = dict(user_counts)
        UserCount = len(result_users)

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Project Details",
            "Data": {
                "response_data":response_data,
                "DurationData": duration_data,
                "UserCount":UserCount,
                "total_proj_count":total_proj_count
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

######################################################################
    ### EXPERIENCE
     
class ExperienceDurationDashboardAPI(APIView):
    '''
    candidate education dashboard
    request: Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        getData = request.data
        response_data = []
        user_counts = Counter()

        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"], job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()

        duration_data = {"total_years": {}, "relevant_field_years": {}}

        for record in candidateData:
            user_id = record['user_id']
            finalData = []

            candidateExpData = CandidateBasicExperienceModel.objects.filter(user_id=user_id).values()

            for data in candidateExpData:
                candidate_total_years_of_experience = data['candidate_total_years_of_experience']
                candidate_total_years_of_experience_applied_for = data['candidate_total_years_of_experience_applied_for']

                if int(candidate_total_years_of_experience) <= 2:
                    total_years_range = "0-2 years of experience"
                elif 3 <= int(candidate_total_years_of_experience) <= 5:
                    total_years_range = "3-5 years of experience"
                elif 6 <= int(candidate_total_years_of_experience) <= 8:
                    total_years_range = "6-8 years of experience"
                else:
                    total_years_range = "More than 9 years"

                if total_years_range in duration_data["total_years"]:
                    duration_data["total_years"][total_years_range] += 1
                else:
                    duration_data["total_years"][total_years_range] = 1

                if int(candidate_total_years_of_experience_applied_for) <= 2:
                    relevant_field_range = "0-2 years of experience"
                elif 3 <= int(candidate_total_years_of_experience_applied_for) <= 5:
                    relevant_field_range = "3-5 years of experience"
                elif 6 <= int(candidate_total_years_of_experience_applied_for) <= 8:
                    relevant_field_range = "6-8 years of experience"
                else:
                    relevant_field_range = "More than 9 years"

                if relevant_field_range in duration_data["relevant_field_years"]:
                    duration_data["relevant_field_years"][relevant_field_range] += 1
                else:
                    duration_data["relevant_field_years"][relevant_field_range]  = 1

                finalData.append(data)
            user_counts.update({user_id: 1})
            response_data.append(finalData)
        result_users = dict(user_counts)
        UserCount = len(result_users)

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Experience Details",
            "Data": {
                "response_data":response_data,
                "DurationData": duration_data,
                "UserCount":UserCount
            },
        }

        return Response(res, status=status.HTTP_201_CREATED)

######################################################################
    ### JOINING PERIOD

class JoiningPeriodDashboardAPI(APIView):
    '''
    candidate JoiningPeriod dashboard
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):
        

        getData = request.data
        response_data = []
        user_counts = Counter()

        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"],job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()         

        period = []
        for record in candidateData:
            user_id = record['user_id']

            finalData = []

            candidateJoinTimeData = CandidateJoiningPeriodPreferenceModel.objects.filter(user_id=user_id).values()
        
            for data in candidateJoinTimeData:
                finalData.append(data)
                period.append(data["joining_period_name"])

                user_counts.update({user_id: 1})

            response_data.append(finalData)

        jointime_counts = Counter(period)
        joinPeriod_counts = dict(jointime_counts)
        total_joinperiod_count = len(period)
        result_users = dict(user_counts)
        UserCount = len(result_users)

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Joining Period Detail",
            "Data": {
                "response_data":response_data,
                "joinPeriod_counts":joinPeriod_counts,
                "UserCount":UserCount,
                "total_joinperiod_count":total_joinperiod_count
                },
        }

        return Response(res, status=status.HTTP_201_CREATED)

######################################################################
    ### WORK PLACE

class WorkPlaceDashboardAPI(APIView):
    '''
    candidate WorkPlace dashboard
    request : Post
    data = {
            "job_level_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            "job_position_id": "BroaderAI_job_position_u2dp6mt8fz2sf3t"
            }           
    '''
    def post(self, request, format=None):

        getData = request.data
        response_data = []
        user_counts = Counter()


        if getData["job_level_id"] != "" and getData["job_position_id"] == "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"]).values()
        elif getData["job_level_id"] == "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_position_id=getData["job_position_id"]).values()
        elif getData["job_level_id"] != "" and getData["job_position_id"] != "":
            candidateData = CandidatePreferenceModel.objects.filter(job_level_id=getData["job_level_id"],job_position_id=getData["job_position_id"]).values()
        else:
            candidateData = CandidatePreferenceModel.objects.all().values()         

        workplace = []
        for record in candidateData:
            user_id = record['user_id']

            finalData = []

            candidateWrkPlaceData = CandidateWorkplacePreferenceModel.objects.filter(user_id=user_id).values()
        
            for data in candidateWrkPlaceData:
              
                finalData.append(data)
                workplace.append(data["work_place_name"])
                user_counts.update({user_id: 1})

            response_data.append(finalData)

        workPlace_counts = Counter(workplace)
        workPlace_counts = dict(workPlace_counts)
        total_workPlace_count = len(workplace)
    
        result_users = dict(user_counts)
        UserCount = len(result_users)

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Candidate Work Place Detail",
            "Data": {
                "response_data":response_data,
                "UserCount":UserCount,
                "total_workPlace_count":total_workPlace_count,
                "workPlace_counts":workPlace_counts
                },
        }

        return Response(res, status=status.HTTP_201_CREATED)


class JobDescriptionCandidateListAPI(APIView):

    '''
    candidate list
    request : Post
    data = {
            "job_description_id": "BroaderAI_job_level_u2dp6mt8fz2sf3t",
            }           
    '''

    def post(self, request, format=None):

        getData = request.data

        if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():

            jobDescriptionData = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])

            if CandidatePreferenceModel.objects.filter(job_position_id = jobDescriptionData.job_position_id, job_level_id = jobDescriptionData.job_level_id).exists():

                candidates = CandidatePreferenceModel.objects.filter(job_position_id = jobDescriptionData.job_position_id, job_level_id = jobDescriptionData.job_level_id).values()


                userDetails = []

                if len(candidates) > 0:

                    for candidate in candidates:
                        userBasicInfo = NewUser.objects.get(id=candidate["user_id"])
                        userTechSkills = CandidateTechnicalskillsModel.objects.filter(user_id=candidate["user_id"]).values()

                        techskill = ' ,'.join([ useTech["candidate_technical_skill_name"].upper() for useTech in userTechSkills])[:-1]


                        if CandidateUserResumeUpload.objects.filter(user_id=candidate["user_id"]).values(): 

                            userResume = CandidateUserResumeUpload.objects.get(user_id=candidate["user_id"])
                            userResume = str(userResume.candidate_resumeUpload)

                        else:
                            userResume = ""


                        # resumepath = os.path.join(settings.BASE_PATH, str(userResume.candidate_resumeUpload))
                        # print(resumepath) 

                        res = {
                            "user_id": candidate["user_id"],
                            "user_name": userBasicInfo.first_name + " " + userBasicInfo.last_name,
                            "user_position": JobPositionModel.objects.get(job_position_id = jobDescriptionData.job_position_id).job_position_name,
                            "user_level": JobLevelModel.objects.get(job_level_id = jobDescriptionData.job_level_id).job_level_name,
                            "user_tech": techskill,
                            "user_resume": settings.BASE_URL + userResume
                        }

                        userDetails.append(res)

                    
                    output = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Candidate list",
                            "Data": userDetails
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
                    "Status": "error",
                    "Code": 401,
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
            
            

class JobDescriptionTotalCandidateListAPI(APIView):

    '''
    candidate list
    request : Post
    
    '''

    def post(self, request, format=None):

        users = NewUser.objects.filter(user_is_recruiter = False).values()

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "List of candidates",
            "Data": {
                "users":users,
                "Total_candidates": len(users)
            }, 
        }
        
        return Response(res, status=status.HTTP_201_CREATED)



class JobPositionOnTimeBasisAPI(APIView):

    def post(self, request, format=None):

        result = []

        # Fetch unique years and months from CandidatePreferenceModel
        years_months = CandidatePreferenceModel.objects.annotate(
            year=ExtractYear('candidate_preference_registration_date'),
            month=ExtractMonth('candidate_preference_registration_date')
        ).values('year', 'month').distinct()

        # Sort the years and months in descending order
        years_months = sorted(years_months, key=lambda x: (x['year'], x['month']), reverse=True)

        for year_month in years_months:
            year = year_month['year']
            month_number = year_month['month']
            month_name_str = month_name[month_number]

            # Calculate total job positions and job levels for the month
            monthly_data = CandidatePreferenceModel.objects.filter(
                candidate_preference_registration_date__year=year,
                candidate_preference_registration_date__month=month_number
            ).aggregate(
                total_job_positions=Count('job_position', distinct=True),
                total_job_levels=Count('job_level', distinct=True)
            )

            # Calculate job positions count for the month
            job_positions = CandidatePreferenceModel.objects.filter(
                candidate_preference_registration_date__year=year,
                candidate_preference_registration_date__month=month_number
            ).values('job_position__job_position_name').annotate(
                count=Count('job_position__job_position_name')
            ).order_by()

            # Calculate job levels count for the month
            job_levels = CandidatePreferenceModel.objects.filter(
                candidate_preference_registration_date__year=year,
                candidate_preference_registration_date__month=month_number
            ).values('job_level__job_level_name').annotate(
                count=Count('job_level__job_level_name')
            ).order_by()

            # Create a dictionary for the month's data
            monthly_data_dict = {
                'year': year,
                'month': month_name_str,
                'total_job_positions': monthly_data['total_job_positions'],
                'total_job_levels': monthly_data['total_job_levels'],
                'job_positions': {entry['job_position__job_position_name']: entry['count'] for entry in job_positions},
                'job_levels': {entry['job_level__job_level_name']: entry['count'] for entry in job_levels},
            }

            result.append(monthly_data_dict)
            

        res = {
            "Status": "success",
            "Code": 201,
            "Message": "Time wise Job Position Data",
            "Data": result
        }

        return Response(result[0:6], status=status.HTTP_201_CREATED)



class JobPositionLevelLastSixMonthsAPI(APIView):

    def post(self, request, format=None):

        result = []

        # Calculate the current date
        current_date = datetime.now()

        # Calculate the starting date for the last six months
        start_date = current_date - timedelta(days=180)

        # Fetch unique years and months from CandidatePreferenceModel for the last six months
        years_months = CandidatePreferenceModel.objects.filter(
            candidate_preference_registration_date__gte=start_date
        ).annotate(
            year=ExtractYear('candidate_preference_registration_date'),
            month=ExtractMonth('candidate_preference_registration_date')
        ).values('year', 'month').distinct()

        # Sort the years and months in descending order
        years_months = sorted(years_months, key=lambda x: (x['year'], x['month']), reverse=True)

        # Initialize dictionaries to store yearly, quarterly counts, current year, and last year counts
        yearly_counts = {}
        quarterly_counts = {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0}
        current_year_count = 0
        last_year_count = 0

        # Initialize dictionaries to store top job positions and job levels
        top_job_positions = {}
        top_job_levels = {}

        # Iterate over the last six months
        for i in range(5, -1, -1):
            # Calculate the year and month for the current iteration
            year = current_date.year
            month_number = current_date.month - i
            if month_number <= 0:
                year -= 1
                month_number += 12

            # Check if the current year and month are in the fetched data
            if {'year': year, 'month': month_number} in years_months:
                # Calculate total job positions and job levels for the month
                monthly_data = CandidatePreferenceModel.objects.filter(
                    candidate_preference_registration_date__year=year,
                    candidate_preference_registration_date__month=month_number
                ).aggregate(
                    total_job_positions=Count('job_position', distinct=True),
                    total_job_levels=Count('job_level', distinct=True)
                )

                # Update quarterly count
                quarter = (month_number - 1) // 3  # Determine the quarter
                quarterly_counts[f'q{quarter + 1}'] += monthly_data['total_job_positions']

                # Update yearly count
                yearly_counts.setdefault(str(year), 0)
                yearly_counts[str(year)] += monthly_data['total_job_positions']

                # Update current year and last year counts
                if year == current_date.year:
                    current_year_count += monthly_data['total_job_positions']
                elif year == current_date.year - 1:
                    last_year_count += monthly_data['total_job_positions']

                # Calculate job positions count for the month
                job_positions = CandidatePreferenceModel.objects.filter(
                    candidate_preference_registration_date__year=year,
                    candidate_preference_registration_date__month=month_number
                ).values('job_position__job_position_name').annotate(
                    count=Count('job_position__job_position_name')
                ).order_by()

                # Calculate job levels count for the month
                job_levels = CandidatePreferenceModel.objects.filter(
                    candidate_preference_registration_date__year=year,
                    candidate_preference_registration_date__month=month_number
                ).values('job_level__job_level_name').annotate(
                    count=Count('job_level__job_level_name')
                ).order_by()

                # Update top job positions dictionary
                for entry in job_positions:
                    job_position_name = entry['job_position__job_position_name']
                    count = entry['count']
                    top_job_positions.setdefault(job_position_name, 0)
                    top_job_positions[job_position_name] += count

                # Update top job levels dictionary
                for entry in job_levels:
                    job_level_name = entry['job_level__job_level_name']
                    count = entry['count']
                    top_job_levels.setdefault(job_level_name, 0)
                    top_job_levels[job_level_name] += count

                # Create a dictionary for the month's data
                monthly_data_dict = {
                    'year': year,
                    'month': month_name[month_number],
                    'total_job_positions': monthly_data['total_job_positions'],
                    'total_job_levels': monthly_data['total_job_levels'],
                    'job_positions': {entry['job_position__job_position_name']: entry['count'] for entry in job_positions},
                    'job_levels': {entry['job_level__job_level_name']: entry['count'] for entry in job_levels},
                }
            else:
                # If no data is found for the month, create a dictionary with zero values
                monthly_data_dict = {
                    'year': year,
                    'month': month_name[month_number],
                    'total_job_positions': 0,
                    'total_job_levels': 0,
                    'job_positions': {},
                    'job_levels': {},
                }

            result.append(monthly_data_dict)

        # Sort yearly counts in descending order
        yearly_counts = dict(sorted(yearly_counts.items(), key=lambda item: int(item[0]), reverse=True))

        # Sort top job positions and job levels in descending order and get the top 6
        top_job_positions = dict(sorted(top_job_positions.items(), key=lambda item: item[1], reverse=True)[:6])
        top_job_levels = dict(sorted(top_job_levels.items(), key=lambda item: item[1], reverse=True)[:6])

        # Add yearly, quarterly, current year, last year counts, top job positions, and top job levels to the result
        result.append({
            'yearly_counts': yearly_counts,
            'quarterly_counts': quarterly_counts,
            'current_year_count': current_year_count,
            'last_year_count': last_year_count,
            'top_job_positions': top_job_positions,
            'top_job_levels': top_job_levels
        })


        topJobs = []

        for key, val in top_job_positions.items():

            topJobs.append({
                "name" : key,
                "value": val
            })


        topJobsLevel = []

        for key, val in top_job_levels.items():

            topJobsLevel.append({
                "name" : key,
                "value": val
            })


        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Time wise Job Position Data",
                "Data": {
                    "result": result,
                    'yearly_counts': yearly_counts,
                    "q1": quarterly_counts["q1"],
                    "q2": quarterly_counts["q2"],
                    "q3": quarterly_counts["q3"],
                    "q4": quarterly_counts["q4"],
                    'current_year_count': current_year_count,
                    'last_year_count': last_year_count,
                    'top_job_positions': top_job_positions,
                    'top_job_levels': top_job_levels,
                    "top_job_positions_pie": topJobs,
                    "top_job_levels_pie": topJobsLevel,


                }
            }

        return Response(res, status=status.HTTP_201_CREATED)



        



