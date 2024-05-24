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
from resumeWeightageAPI.models import *
import requests
import json

base_url = "http://127.0.0.1:8000/"

#######################################
#######################################

class CandidateReportAnalysisAPI(APIView):
    '''
        CandidateReportAnalysis API(Insert)
        Request : POST
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_ub0okzu3pc",
                    "job_position_id": "BroaderAI_job_position_3yqu18mxuo3y8m9",
                    "job_level_id": "BroaderAI_job_level_08br6wywmxzw99e",
                    "education_id": "BroaderAI_education_8jxg85w3xaz0ktu",
                    "education_field_id": "BroaderAI_education_field_8ooxu7vmb5bdym1",
                    "candidate_education_score":"2.1",
                    "candidate_education_relevancy": "yes",
                    "candidate_total_technical_skills:"5",
                    "candidate_haveto_skills": "python, django, flask",
                    "candidate_total_haveto_skills": "3",
                    "candidate_optional_skills": "nodejs, angular",
                    "candidate_total_optional_skills": "2",
                    "candidate_total_technical_skill_weightage":"2.5",
                    "candidate_total_relevant_projects": "2",
                    "candidate_total_projects": "3",
                    "candidate_project_relevant_score": "2.5",
                    "candidate_total_month_experience": "33",
                    "candidate_relevant_field_experience": "22",
                    "candidate_number_of_internship": "2",
                    "candidate_relevant_experience_score": "2",
                    "candidate_total_softskill": "5"
                    "candidate_total_softskill_score": "2.1",
                    "candidate_number_of_curriculum_activities": "9",
                    "candidate_number_of_curriculum_activity_score": "1",
                    "is_candidate_any_drop_year": "0",
                    "candidate_drop_year_penalty_score": "0",
                }
    '''
    def post(self, request ,format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin: 


                randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))


                uniqueID = "BroaderAI_candidate_report_analysis_" + randomstr
              
                serializer = CandidateReportAnalysisserializer(data=getData)
                
                if serializer.is_valid():
                    
                    serializer.save(candidate_report_analysis_id= uniqueID)
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Candidate report Details is Added",
                        "Data": {   
                            "candidate_report_analysis_id" : uniqueID,
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
                
            # else:
            #     res = {
            # "Status": "error",
            # "Code": 400,
            # "Message": "Technical Skill already exists by this user",
            # "Data":[],
            # }
            #     return Response(res, status=status.HTTP_201_CREATED)
        
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

class candidateReportGenerationAPI(APIView):
    '''
    candidateReportGeneration API (input)
    {
    'user_id' : 'BroaderAI_bhramizadafiya1234_bt3kqwljrl'
    }'''

    def post(self, request ,format=None):
        getData = request.data
        

        if NewUser.objects.filter(id=getData["user_id"]).exists():
    
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if CandidatePreferenceModel.objects.filter(user_id = getData['user_id']).exists(): 

                    if CandidateBasicEducationDetails.objects.filter(user_id = getData['user_id']).exists():

                        if CandidateTechnicalskillsModel.objects.filter(user_id = getData['user_id']).exists():

                            if CandidateProjectTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).exists():

                                if CandidateBasicExperienceModel.objects.filter(user_id = getData['user_id']).exists:

                                    if CandidateSoftskillsModel.objects.filter(user_id = getData['user_id']).exists():

                                        randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
                                        uniqueID = "BroaderAI_candidate_report_analysis_" + randomstr

                                        getData['job_position_id'] = CandidatePreferenceModel.objects.get(user_id = getData['user_id']).job_position_id
                                        getData['job_position_name'] = CandidatePreferenceModel.objects.get(user_id = getData['user_id']).job_position.job_position_name
                                        
                                        getData['job_level_id'] = CandidatePreferenceModel.objects.get(user_id = getData['user_id']).job_level_id
                                        getData['job_level_name'] = CandidatePreferenceModel.objects.get(user_id = getData['user_id']).job_level.job_level_name

                                        getData['candidate_last_education_id'] = CandidateBasicEducationDetails.objects.get(user_id = getData['user_id']).candidate_last_education_id
                                        getData['candidate_last_education_years'] = int(CandidateBasicEducationDetails.objects.get(user_id = getData['user_id']).candidate_last_education.education_years)

                                        getData['candidate_last_education_field_id'] = CandidateBasicEducationDetails.objects.get(user_id = getData['user_id']).candidate_last_education_field_id
                                        getData['candidate_last_education_field_name'] = CandidateBasicEducationDetails.objects.get(user_id = getData['user_id']).candidate_last_education_field.education_field_name


                                        candidateReportAnalysis = CandidateReportAnalysisModel(
                                                candidate_report_analysis_id = uniqueID,
                                                user_id = getData["user_id"],
                                                job_position_id = getData["job_position_id"],
                                                job_level_id = getData["job_level_id"],
                                                education_id = getData["candidate_last_education_id"],
                                                education_field_id = getData["candidate_last_education_field_id"]
                                        )

                                        candidateReportAnalysis.save()

                                        if candidateReportAnalysis.pk:


                                            getData['candidate_total_years_of_experience'] =int(CandidateBasicExperienceModel.objects.get(user_id = getData['user_id']).candidate_total_years_of_experience) * 12
                                            
                                            getData['candidate_total_years_of_experience_applied_for'] = int(CandidateBasicExperienceModel.objects.get(user_id = getData['user_id']).candidate_total_years_of_experience_applied_for) * 12
                                            
                                            getData['candidate_total_internship'] = int(CandidateBasicExperienceModel.objects.get(user_id = getData['user_id']).candidate_total_internship)

############################################################################################################################


                                            basicedu = CandidateBasicEducationDetails.objects.get(user_id = getData['user_id'])

                                            randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
                                            basiceduuniqueID = "BroaderAI_Candidate_Basic_education_hist_" + randomstr

                                            candidateBasicEduHist = CandidateBasicEducationHistoryDetails(

                                                candidate_resume_basic_education_hist_id = basiceduuniqueID,
                                                user_id = basicedu.user_id,
                                                candidate_report_analysis_id = candidateReportAnalysis.pk,
                                                candidate_last_education_id = basicedu.candidate_last_education_id,
                                                candidate_last_education_field_id = basicedu.candidate_last_education_field_id,
                                                candidate_total_years_education_hist = basicedu.candidate_total_years_education,
                                                candidate_education_year_drop_hist = basicedu.candidate_education_year_drop
                                            )

                                            print(candidateBasicEduHist , "==========+++++----'''''")

                                            candidateBasicEduHist.save()

                                            print(candidateBasicEduHist , "llllllllllllllllllll")

                                        ########################################################################
                                            
                                            mainedu = CandidateMainEducationDetails.objects.filter(user_id = getData['user_id']).values()

                                            for maineducation in mainedu:

                                                randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
                                                maineduuniqueID = "BroaderAI_Candidate_Main_education_hist_" + randomstr

                                                candidateMainEduHist = CandidateMainEducationHistoryDetails(

                                                candidate_resume_main_education_hist_id = maineduuniqueID,
                                                user_id = maineducation["user_id"],
                                                candidate_report_analysis_id = candidateReportAnalysis.pk,
                                                candidate_degree_name_hist = maineducation["candidate_degree_name"],
                                                candidate_univeresity_name_hist = maineducation["candidate_univeresity_name"],
                                                candidate_result_class_hist = maineducation["candidate_result_class"],
                                                candidate_start_year_hist = maineducation["candidate_start_year"],
                                                candidate_end_year_hist = maineducation["candidate_end_year"],
                                                candidate_summary_hist = maineducation["candidate_summary"]
                                                )

                                                candidateMainEduHist.save()

                                        ########################################################################

                                            education_api_url = base_url + 'candidateReportAnalysisApis/CandidateEducationPrediction'

                                            educationdata = {
                                                        "user_id": getData["user_id"],
                                                        "job_level_id" : getData["job_level_id"],
                                                        "education_id" : getData["candidate_last_education_id"],
                                                        "education_field_id" : getData["candidate_last_education_field_id"]
                                                    }
                                            
                                            education_response = json.loads(requests.post(education_api_url, data=educationdata).text)

                                            print(education_response , "kkkkkkkkkkkkkkkkk")
                                        

############################################################################################################################

#                                             basicexp = CandidateBasicExperienceModel.objects.get(user_id = getData['user_id'])

#                                             randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                             basicexpuniqueID = "BroaderAI_basic_experience_hist_" + randomstr

#                                             candidateBasicExpHist = CandidateBasicExperienceHistoryModel(

#                                                 candidate_resume_basic_experience_hist_id = basicexpuniqueID,
#                                                 user_id = basicexp.user_id,
#                                                 candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                 candidate_total_years_of_experience_hist = basicexp.candidate_total_years_of_experience,
#                                                 candidate_total_years_of_experience_applied_for_hist = basicexp.candidate_total_years_of_experience_applied_for,
#                                                 candidate_total_internship_hist = basicexp.candidate_total_internship,
#                                                 candidate_works_companies_hist = basicexp.candidate_works_companies,
#                                                 candidate_field_transition_hist = basicexp.candidate_field_transition,
#                                                 candidate_works_startup_hist = basicexp.candidate_works_startup,
#                                                 candidate_works_MNC_hist = basicexp.candidate_works_MNC
#                                             )

#                                             candidateBasicExpHist.save()

#                                         ########################################################################
                                            
#                                             mainexp = CandidateMainExperienceModel.objects.filter(user_id = getData['user_id']).values()

#                                             for mainexper in mainexp:

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 mainexpuniqueID = "BroaderAI_main_experience_hist_" + randomstr

#                                                 candidateMainExpHist = CandidateMainExperienceHistoryModel(
#                                                 candidate_resume_main_experience_hist_id = mainexpuniqueID,
#                                                 user_id = maineducation["user_id"],
#                                                 candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                 candidate_job_position_id = mainexper["candidate_job_position_id"],
#                                                 candidate_work_place_id = mainexper["candidate_work_place_id"],
#                                                 candidate_company_name_hist = mainexper["candidate_company_name"],
#                                                 candidate_job_level_id = mainexper["candidate_job_level_id"],
#                                                 candidate_company_location_hist = mainexper["candidate_company_location"],
#                                                 candidate_job_start_year_hist = mainexper["candidate_job_start_year"],
#                                                 candidate_job_end_year_hist = mainexper["candidate_job_end_year"],
#                                                 candidate_job_description_hist = mainexper["candidate_job_description"]
#                                                 )

#                                                 candidateMainExpHist.save()
                                        
#                                         ########################################################################

#                                             exp_api_url = base_url + 'candidateReportAnalysisApis/CandidateExperiencePrediction'

#                                             expdata = {
#                                                         "user_id": getData["user_id"],
#                                                         "job_level_id" : getData["job_level_id"],
#                                                         "candidate_total_month_experience": getData['candidate_total_years_of_experience'],
#                                                         "candidate_relevant_field_experience":getData['candidate_total_years_of_experience_applied_for'],
#                                                         "candidate_number_of_internship":getData['candidate_total_internship']
#                                                     }
                                            
#                                             exp_response = json.loads(requests.post(exp_api_url, data=expdata).text)

                                            
# ############################################################################################################################

#                                             technical_api_url = base_url + 'candidateReportAnalysisApis/CandidateTechnicalPrediction'

#                                             techData = {
#                                                 "user_id": getData["user_id"],
#                                                 "job_level_id" : getData["job_level_id"],
#                                                 "job_position_id": getData['job_position_id'],
#                                                 "candidate_report_analysis_id":candidateReportAnalysis.pk
#                                             }

#                                             tech_response = json.loads(requests.post(technical_api_url, data=techData).text)


#                                             techskill = CandidateTechnicalskillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for tech in techskill:

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 techSkilluniqueID = "BroaderAI_candidate_resume_Tech_skill_hist_" + randomstr

#                                                 if candidateReportHavetoTechSkillModel.objects.filter(technical_skills_id = tech["candidate_technical_skill_id"], user_id = tech["user_id"], candidate_report_analysis_id = candidateReportAnalysis.pk).exists():

#                                                     tstatus = "haveto"
                                                    
#                                                 else:

#                                                     tstatus = "optional"

#                                                 candidatetechSkillHist = candidateReportTechSkillHistoryModel(
#                                                 candidate_report_technical_skill_history_id = techSkilluniqueID,
#                                                 user_id = tech["user_id"],
#                                                 candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                 technical_skills_name = tech['candidate_technical_skill_name'],
#                                                 candidate_technical_skill_status = tstatus
#                                                 )

#                                                 candidatetechSkillHist.save()
# ############################################################################################################################

#                                             softskill = CandidateSoftskillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for ss in softskill:
#                                                 

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 ssuniqueID = "BroaderAI_candidate_resume_Soft_skill_hist_" + randomstr

#                                                 candidateSoftSkillHist = CandidateSoftskillsHistoryModel(

#                                                     candidate_resume_soft_skills_hist_id = ssuniqueID,
#                                                     user_id = ss["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_soft_skill_name_hist = ss["candidate_soft_skill_name"],
#                                                     candidate_soft_skill_level_hist = ss["candidate_soft_skill_level"]
#                                                 )

#                                                 candidateSoftSkillHist.save()


#                                             softSkill_api_url = base_url + 'candidateReportAnalysisApis/CandidateSoftSkillPrediction'

#                                             softSkillData = {
#                                                 "job_level_id" : getData["job_level_id"],
#                                                 "user_id": getData["user_id"]
#                                             }

#                                             softSkill_response = json.loads(requests.post(softSkill_api_url, data=softSkillData).text)


                                            
# ############################################################################################################################

#                                             hackathon = CandidatehackathonModel.objects.filter(user_id = getData['user_id']).values()

#                                             for hk in hackathon:
#                                              

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 hkuniqueID = "BroaderAI_resume_hackathon_hist_" + randomstr

#                                                 candidatehackathonHist = CandidatehackathonHistoryModel(

#                                                     candidate_resume_hackathon_hist_id = hkuniqueID,
#                                                     user_id = hk["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_hackathon_name_hist = hk["candidate_hackathon_name"],
#                                                     candidate_hackathon_mode_hist = hk["candidate_hackathon_mode"],
#                                                     candidate_hackathon_organisation_name_hist = hk["candidate_hackathon_organisation_name"],
#                                                     candidate_hackathon_certificateID_hist = hk["candidate_hackathon_certificateID"],
#                                                     candidate_hackathon_type_hist = hk["candidate_hackathon_type"],
#                                                     candidate_hackathon_field_hist = hk["candidate_hackathon_field"],
#                                                     candidate_hackathon_participate_certificate_hist = hk["candidate_hackathon_participate_certificate"],
#                                                     candidate_hackathon_certificate_issue_date_hist  = hk["candidate_hackathon_certificate_issue_date"],
#                                                     candidate_hackathon_certificateURL_hist = hk["candidate_hackathon_certificateURL"],
#                                                     candidate_hackathon_description_hist = hk["candidate_hackathon_description"]
#                                                 )

#                                                 candidatehackathonHist.save()
                                            
#                                         #######################################################################
                                                
#                                             hacktech = CandidateHackathonTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for hktch in hacktech:
#                                               

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 hktechuniqueID = "BroaderAI_hackathon_technical_skill_hist_" + randomstr

#                                                 candidatehacktechHist = CandidateHackathonTechnicalSkillsHistoryModel(

#                                                     candidate_resume_hackathon_tech_skill_hist_id = hktechuniqueID,
#                                                     user_id = hktch["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_hackathon_id = hktch["candidate_hackathon_id"],
#                                                     candidate_technical_skill_id = hktch["candidate_technical_skill_id"],
#                                                     candidate_technical_skill_name_hist = hktch["candidate_technical_skill_name"]
#                                                 )

#                                                 candidatehacktechHist.save()

#                                         ##################################################################################

#                                             contribution = CandidateContributionModel.objects.filter(user_id = getData['user_id']).values()

#                                             for ct in contribution:
#                                               

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 ctuniqueID = "BroaderAI_resume_contribution_hist_" + randomstr

#                                                 candidatecontributionHist = CandidateContributionHistoryModel(

#                                                     candidate_resume_contribution_hist_id = ctuniqueID,
#                                                     user_id = ct["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_contribution_topic_hist = ct["candidate_contribution_topic"],
#                                                     candidate_contribution_keyword_hist = ct["candidate_contribution_keyword"],
#                                                     candidate_contribution_organisation_name_hist = ct["candidate_contribution_organisation_name"],
#                                                     candidate_contribution_certificateID_hist = ct["candidate_contribution_certificateID"],
#                                                     candidate_contribution_certificateURL_hist = ct["candidate_contribution_certificateURL"],
#                                                     candidate_contribution_participate_certificate_hist = ct["candidate_contribution_participate_certificate"],
#                                                     candidate_contribution_publish_date_hist  = ct["candidate_contribution_publish_date"],
#                                                     candidate_contribution_certificate_issue_date_hist  = ct["candidate_contribution_certificate_issue_date"],
#                                                     candidate_contribution_summary_hist = ct["candidate_contribution_summary"]
#                                                 )

#                                                 candidatecontributionHist.save()
                                            
#                                         #######################################################################
                                                
#                                             contritech = CandidateContributionTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for cttch in contritech:
#                                                

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 ctechuniqueID = "BroaderAI_contribution_technical_skill_hist_" + randomstr

#                                                 candidatecontritechHist = CandidateContributionTechnicalSkillsHistoryModel(

#                                                     candidate_resume_contribution_technical_skill_hist_id = ctechuniqueID,
#                                                     user_id = cttch["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_contribution_id = cttch["candidate_contribution_id"],
#                                                     candidate_technical_skill_id = cttch["candidate_technical_skill_id"],
#                                                     candidate_technical_skill_name_hist = cttch["candidate_technical_skill_name"]
#                                                 )

#                                                 candidatecontritechHist.save()
                                        
#                                         ####################################################################################
                                            
#                                             workshop = CandidateWorkshopModel.objects.filter(user_id = getData['user_id']).values()

#                                             for ws in workshop:
#                                                 

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 wsuniqueID = "BroaderAI_resume_workshop_hist_" + randomstr

#                                                 candidateworkshopHist = CandidateWorkshopHistoryModel(

#                                                     candidate_resume_workshop_hist_id = wsuniqueID,
#                                                     user_id = ws["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_workshop_organisation_name_hist = ws["candidate_workshop_organisation_name"],
#                                                     candidate_workshop_name_hist = ws["candidate_workshop_name"],
#                                                     candidate_workshop_type_hist = ws["candidate_workshop_type"],
#                                                     candidate_workshop_topic_hist = ws["candidate_workshop_topic"],
#                                                     candidate_workshop_certificateID_hist = ws["candidate_workshop_certificateID"], 
#                                                     candidate_workshop_certificateURL_hist = ws["candidate_workshop_certificateURL"],
#                                                     candidate_workshop_participate_certificate_hist = ws["candidate_workshop_participate_certificate"],
#                                                     candidate_workshop_duration_hist = ws["candidate_workshop_duration"],
#                                                     candidate_workshop_certificate_issue_date_hist = ws["candidate_workshop_certificate_issue_date"],
#                                                     candidate_workshop_description_hist =  ws["candidate_workshop_description"]
#                                                 )

#                                                 candidateworkshopHist.save()
                                            
#                                         #######################################################################
                                                
#                                             workshoptech = CandidateWorkshopTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for workshoptch in workshoptech:
#                                               

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 worktechuniqueID = "BroaderAI_workshop_technical_skill_hist_" + randomstr

#                                                 candidateworkshoptechHist = CandidateWorkshopTechnicalSkillsHistoryModel(

#                                                     candidate_resume_workshop_technical_skill_hist_id = worktechuniqueID,
#                                                     user_id = workshoptch["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_workshop_id = workshoptch["candidate_workshop_id"],
#                                                     candidate_technical_skill_id = workshoptch["candidate_technical_skill_id"],
#                                                     candidate_technical_skill_name_hist = workshoptch["candidate_technical_skill_name"]
#                                                 )

#                                                 candidateworkshoptechHist.save()

#                                         ##################################################################################
                                                
#                                             seminar = CandidateSeminarModel.objects.filter(user_id = getData['user_id']).values()

#                                             for sem in seminar:
#                                                 

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 semuniqueID = "BroaderAI_resume_seminar_hist_" + randomstr

#                                                 candidateseminarHist = CandidateSeminarHistoryModel(

#                                                     candidate_resume_seminar_hist_id = semuniqueID,
#                                                     user_id = sem["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_seminar_name_hist = sem["candidate_seminar_name"],
#                                                     candidate_seminar_host_hist = sem["candidate_seminar_host"],
#                                                     candidate_seminar_type_hist = sem["candidate_seminar_type"],
#                                                     candidate_seminar_organisation_name_hist = sem["candidate_seminar_organisation_name"],
#                                                     candidate_seminar_mode_hist = sem["candidate_seminar_mode"],
#                                                     candidate_seminar_topic_hist = sem["candidate_seminar_topic"],
#                                                     candidate_seminar_certificateID_hist = sem["candidate_seminar_certificateID"], 
#                                                     candidate_seminar_certificateURL_hist = sem["candidate_seminar_certificateURL"],
#                                                     candidate_seminar_participate_certificate_hist = sem["candidate_seminar_participate_certificate"],
#                                                     candidate_seminar_certificate_issue_date_hist  = sem["candidate_seminar_certificate_issue_date"],
#                                                     candidate_seminar_description_hist = sem["candidate_seminar_description"]
#                                                 )

#                                                 candidateseminarHist.save()
                                            
#                                         #######################################################################
                                                
#                                             competition = CandidateCompetitionModel.objects.filter(user_id = getData['user_id']).values()

#                                             for comp in competition:

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 compuniqueID = "BroaderAI_resume_competition_hist_" + randomstr

#                                                 candidatecompetitionHist = CandidateCompetitionHistoryModel(

#                                                     candidate_resume_competition_hist_id = compuniqueID,
#                                                     user_id = comp["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_competition_organisation_name_hist = comp["candidate_competition_organisation_name"],
#                                                     candidate_competition_name_hist = comp["candidate_competition_name"],
#                                                     candidate_competition_type_hist = comp["candidate_competition_type"],
#                                                     candidate_competition_mode_hist = comp["candidate_competition_mode"],
#                                                     candidate_competition_certificateID_hist = comp["candidate_competition_certificateID"],
#                                                     candidate_competition_certificateURL_hist = comp["candidate_competition_certificateURL"],
#                                                     candidate_competition_participate_certificate_hist = comp["candidate_competition_participate_certificate"],
#                                                     candidate_competition_certificate_issue_date_hist  = comp["candidate_competition_certificate_issue_date"],
#                                                     candidate_competition_description_hist =  comp["candidate_competition_description"]
#                                                 )

#                                                 candidatecompetitionHist.save()
                                            
#                                         #######################################################################
                                                
#                                             competitiontech = CandidateCompetitionTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for competitiontch in competitiontech:
#                                               

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 comptechuniqueID = "BroaderAI_competition_technical_skill_hist_" + randomstr

#                                                 candidatecompetitiontechHist = CandidateCompetitionTechnicalSkillsHistoryModel(

#                                                     candidate_resume_competition_tech_skill_hist_id = comptechuniqueID,
#                                                     user_id = competitiontch["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_competition_id = competitiontch["candidate_competition_id"],
#                                                     candidate_technical_skill_id = competitiontch["candidate_technical_skill_id"],
#                                                     candidate_technical_skill_name_hist = competitiontch["candidate_technical_skill_name"]
#                                                     )

#                                                 candidatecompetitiontechHist.save()

#                                         ##################################################################################
                                                
#                                             certificate = CandidateCertificateModel.objects.filter(user_id = getData['user_id']).values()

#                                             for certi in certificate:
#                                               

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 certiuniqueID = "BroaderAI_resume_certificate_hist_" + randomstr

#                                                 candidatecertificateHist = CandidateCertificateHistoryModel(

#                                                     candidate_resume_certificate_hist_id = certiuniqueID,
#                                                     user_id = certi["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_certificate_organisation_name_hist = certi["candidate_certificate_organisation_name"],
#                                                     candidate_certificate_name_hist = certi["candidate_certificate_name"],
#                                                     candidate_certificate_certificateID_hist = certi["candidate_certificate_certificateID"],
#                                                     candidate_certificate_certificateURL_hist = certi["candidate_certificate_certificateURL"],
#                                                     candidate_certificate_participate_certificate_hist = certi["candidate_certificate_participate_certificate"], 
#                                                     candidate_certificate_issue_date_hist = certi["candidate_certificate_issue_date"],
#                                                     candidate_certificate_expire_date_hist = certi["candidate_certificate_expire_date"],
#                                                     candidate_certificate_description_hist = certi["candidate_certificate_description"]
#                                                 )

#                                                 candidatecertificateHist.save()
                                            
#                                         #######################################################################
                                                
#                                             certificatetech = CandidateCertificateTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).values()

#                                             for certificatetch in certificatetech:

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 certitechuniqueID = "BroaderAI_certificate_technical_skill_hist_" + randomstr

#                                                 candidatecertificatetechHist = CandidateCertificateTechnicalSkillsHistoryModel(

#                                                     candidate_resume_certificate_tech_skill_hist_id = certitechuniqueID,
#                                                     user_id = certificatetch["user_id"],
#                                                     candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                     candidate_certificate_id = certificatetch["candidate_certificate_id"],
#                                                     candidate_technical_skill_id = certificatetch["candidate_technical_skill_id"],
#                                                     candidate_technical_skill_name_hist = certificatetch["candidate_technical_skill_name"]
#                                                    )

#                                                 candidatecertificatetechHist.save()

#                                         ##################################################################################

                                                

#                                             curricular_api_url = base_url + 'candidateReportAnalysisApis/CandidateCurricularActivitiesPrediction'

#                                             currActData = {
#                                                 "user_id": getData["user_id"],
#                                                 "job_level_id" : getData["job_level_id"]
#                                             }

#                                             currAct_response = json.loads(requests.post(curricular_api_url, data=currActData).text)
# ############################################################################################################################

#                                             anyDrop_api_url = base_url + 'candidateReportAnalysisApis/AnyDropPrediction'

#                                             anyDropData = {
#                                                 "user_id": getData["user_id"],
#                                                 "job_level_id" : getData["job_level_id"]
#                                             }

#                                             anyDrop_response = json.loads(requests.post(anyDrop_api_url, data=anyDropData).text)

# ############################################################################################################################

#                                             project_api_url = base_url + 'candidateReportAnalysisApis/ProjectPrediction'

#                                             projectData = {
#                                                 "user_id": getData["user_id"],
#                                                 "job_level_id" : getData["job_level_id"],
#                                                 "job_position_id" : getData["job_position_id"],
#                                                 "candidate_report_analysis_id": candidateReportAnalysis.pk
#                                             }

#                                             project_response = json.loads(requests.post(project_api_url, data=projectData).text)
                                           
                                            
#                                             Project = CandidateProjectModel.objects.filter(user_id = getData['user_id']).values()

#                                             for Proj in Project:

#                                                 randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                 ProjectuniqueID = "BroaderAI_candidate_resume_project_hist_" + randomstr

#                                                 canRel = candidateReportAnalysisProjectRelevancyModel.objects.get(user_id = Proj['user_id'], candidate_resume_project_id = Proj["candidate_resume_project_id"] ,candidate_report_analysis_id = candidateReportAnalysis.pk,)
                                                

#                                                 candidateProjectHist = candidateReportAnalysisProjectHistoryModel(
#                                                 candidate_report_project_hist_id = ProjectuniqueID,
#                                                 user_id = Proj["user_id"],
#                                                 candidate_report_analysis_id = candidateReportAnalysis.pk,
#                                                 candidate_project_name = Proj["candidate_project_name"],
#                                                 candidate_project_start_date  = Proj["candidate_project_start_date"],
#                                                 candidate_project_end_date  = Proj["candidate_project_end_date"],
#                                                 candidate_project_url = Proj["candidate_project_url"],
#                                                 candidate_project_description = Proj["candidate_project_description"],
#                                                 candidate_project_relevant = canRel.candidate_project_relevant
#                                                 )

#                                                 candidateProjectHist.save()
                                                

#                                                 if candidateReportAnalysisProjectRelevantSkillsModel.objects.filter(user_id = Proj["user_id"], candidate_report_analysis_id = candidateReportAnalysis.pk, candidate_resume_project_id = Proj["candidate_resume_project_id"] ).exists():


#                                                     projectTechs = candidateReportAnalysisProjectRelevantSkillsModel.objects.filter(user_id = Proj["user_id"], candidate_report_analysis_id = candidateReportAnalysis.pk, candidate_resume_project_id = Proj["candidate_resume_project_id"] ).values()

#                                                     for ptch in projectTechs:

#                                                         randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                         tuniqueID = "BroaderAI_candidate_resume_proj_tech_hist_" + randomstr

#                                                         can_tech = candidateReportAnalysisProjectTechnicalSkillHistoryModel(
#                                                             candidate_report_project_tech_skill_hist_id = tuniqueID,
#                                                             user_id = ptch["user_id"],
#                                                             candidate_report_analysis_id = ptch["candidate_report_analysis_id"],
#                                                             candidate_report_project_history_id = candidateProjectHist.pk,
#                                                             candidate_technical_skill_name = ptch["candidate_technical_skill_name"],
#                                                             candidate_project_technical_skill_relevant = "yes"
#                                                         )

#                                                         can_tech.save()

#                                                 if candidateReportAnalysisProjectNonRelevantSkillsModel.objects.filter(user_id = Proj["user_id"], candidate_report_analysis_id = candidateReportAnalysis.pk, candidate_resume_project_id = Proj["candidate_resume_project_id"] ).exists():


#                                                     nonprojectTechs = candidateReportAnalysisProjectNonRelevantSkillsModel.objects.filter(user_id = Proj["user_id"], candidate_report_analysis_id = candidateReportAnalysis.pk, candidate_resume_project_id = Proj["candidate_resume_project_id"] ).values()

#                                                     for ptch in nonprojectTechs:

#                                                         randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
#                                                         tuniqueID = "BroaderAI_candidate_resume_proj_tech_hist_" + randomstr

#                                                         no_can_tech = candidateReportAnalysisProjectTechnicalSkillHistoryModel(
#                                                             candidate_report_project_tech_skill_hist_id = tuniqueID,
#                                                             user_id = ptch["user_id"],
#                                                             candidate_report_analysis_id = ptch["candidate_report_analysis_id"],
#                                                             candidate_report_project_history_id = candidateProjectHist.pk,
#                                                             candidate_technical_skill_name = ptch["candidate_technical_skill_name"],
#                                                             candidate_project_technical_skill_relevant = "no"
#                                                         )

#                                                         no_can_tech.save()

# ############################################################################################################################

#                                             candidateReportData = CandidateReportAnalysisModel.objects.get(candidate_report_analysis_id = candidateReportAnalysis.pk)

#                                             candidateReportData.job_position_id = getData["job_position_id"]
#                                             candidateReportData.job_level_id = getData["job_level_id"]
#                                             candidateReportData.education_id = getData["candidate_last_education_id"]
#                                             candidateReportData.education_field_id = getData["candidate_last_education_field_id"]
#                                             candidateReportData.candidate_education_score = str(education_response['Data']['education_score'])
#                                             candidateReportData.candidate_education_relevancy = education_response['Data']['education_relevancy']
#                                             candidateReportData.candidate_total_technical_skills = tech_response['Data']['total_technical_skills']
#                                             candidateReportData. candidate_total_haveto_skills = tech_response['Data']['total_haveto_technical_skills']
#                                             candidateReportData.candidate_total_optional_skills = tech_response['Data']['total_optional_technical_skills']
#                                             candidateReportData.candidate_total_technical_skill_weightage = tech_response['Data']['technical_prediction_score']
#                                             candidateReportData.candidate_total_relevant_projects = project_response['Data']['Total_relevant_projects']
#                                             candidateReportData.candidate_total_projects = project_response['Data']['Total_project']
#                                             candidateReportData.candidate_project_relevant_score = project_response['Data']['Project_prediction_score']
#                                             candidateReportData.candidate_total_month_experience = getData['candidate_total_years_of_experience']
#                                             candidateReportData.candidate_relevant_field_experience = getData['candidate_total_years_of_experience_applied_for']
#                                             candidateReportData.candidate_number_of_internship = getData['candidate_total_internship']
#                                             candidateReportData.candidate_relevant_experience_score = exp_response['Data']['experience_score']
#                                             candidateReportData.candidate_total_softskill = softSkill_response['Data']['total_soft_skills']
#                                             candidateReportData.candidate_total_softskill_score = softSkill_response['Data']['soft_skill_score']
#                                             candidateReportData.candidate_number_of_curriculum_activities = currAct_response['Data']['total_curricular_activities']
#                                             candidateReportData.candidate_number_of_curriculum_activity_score = currAct_response['Data']['curricular_activites_score']
#                                             candidateReportData.is_candidate_any_drop_year = anyDrop_response['Data']['any_drop_status']
#                                             candidateReportData.candidate_drop_year_penalty_score = anyDrop_response['Data']['any_drop_score']


#                                             candidateReportData.save()

                    
                            
#                                             res={'Message': "successfully worked",
#                                                  "Candidate_report_id": candidateReportAnalysis.pk,
#                                                 "educationData": education_response,
#                                                 "expData": exp_response,
#                                                 "techData": tech_response,
#                                                 "softSkillData": softSkill_response,
#                                                 "curricluarData": currAct_response,
#                                                 "anyDropData": anyDrop_response,
#                                                 "projectData": project_response,
#                                                 }


                                            res = {
                                                "Status": "success",
                                                "Code": 201,
                                                "Message": "successfully worked",
                                                "Data":[],
                                            }
                                            return Response(res, status=status.HTTP_201_CREATED)
                                        

                                        else:
                                            res = {
                                                "Status": "error",
                                                "Code": 401,
                                                "Message": "Something goes wrong !!",
                                                "Data":[],
                                                }
                                            return Response(res, status=status.HTTP_201_CREATED)
                                
                                    
                                    else:
                                        res = {
                                            "Status": "error",
                                            "Code": 401,
                                            "Message": "Soft Skills is not found for this User. Kindly add record in resume form!",
                                            "Data":[],
                                            }
                                        return Response(res, status=status.HTTP_201_CREATED)
                                
                                else:
                                    res = {
                                        "Status": "error",
                                        "Code": 401,
                                        "Message": "Experience is not found for this User. Kindly add record in resume form!",
                                        "Data":[],
                                        }
                                    return Response(res, status=status.HTTP_201_CREATED)
                                
                            else:
                                res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Project Technical Skills is not found for this User. Kindly add record in resume form!",
                                    "Data":[],
                                    }
                                return Response(res, status=status.HTTP_201_CREATED)
                        
                        
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Technical Skills is not found for this User. Kindly add record in resume form!",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)

                    
                    else:
                        res = {
                            "Status": "error",
                    "Code": 401,
                            "Message": "Education is not found for this User. Kindly add record in resume form!",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "job position and job level is not found for this User. Kindly add record in preference form!",
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
        
#########################################
        
######################################## 

class CandidateEducationPredictionAPI(APIView):

    '''

        CandidateEducationPrediction API(Insert)
        Request : POST
        Data = {
            "user_id":
            "job_level_id" :,
            "education_id" :,
            "education_field_id" :,
        }
    
    
    '''

    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():

                    if EducationModel.objects.filter(education_id = getData['education_id']).exists():

                        
                        candidateMainWeightage = MainEducationWeightageModel.objects.get(job_level_id = getData["job_level_id"])


                        candidateCategoryWeightage = EducationCategoriesWeightageModel.objects.get(education_id = getData["education_id"], main_education_weightage_id = candidateMainWeightage.main_education_weightage_id)

                        if EducationFieldModel.objects.filter(education_field_id = getData['education_field_id']).exists() and EducationFieldModel.objects.get(education_field_id = getData["education_field_id"]).education_field_name != "other":

                            education_score = float(candidateCategoryWeightage.education_categories_weightage)

                            if education_score >  float(candidateMainWeightage.main_education_total_weightage):
                                education_score = float(candidateMainWeightage.main_education_total_weightage)

                            education_relevancy = "Relevant"
                            education_name = EducationFieldModel.objects.get(education_field_id = getData["education_field_id"]).education_field_name

                        else:
                            education_score = float(candidateCategoryWeightage.education_categories_weightage) / 2
                            education_relevancy = "Not_Relevant"
                            education_name = "Other"

                        # # candidate_education_year_drop = CandidateBasicEducationDetails.objects.get(user_id = getData['user_id']).candidate_education_year_drop
                        candidate_education_year_drop = random.randint(0,1)
                    
                        candidateWeightage = AnyDropWeightageModel.objects.get(job_level_id = getData['job_level_id'])

                        any_drop_score = candidate_education_year_drop * float(candidateWeightage.any_drop_weightage)

                        education_score = education_score - any_drop_score
                        if education_score < 0 :
                            education_score = 0.1
                        
                        res= {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Education prediction record",
                            "Data": {
                                "job_level_id" : getData["job_level_id"],
                                "job_level_name" : JobLevelModel.objects.get(job_level_id = getData["job_level_id"]).job_level_name,
                                "education_id" : getData["education_id"],
                                "education_name" : EducationModel.objects.get(education_id = getData["education_id"]).education_name,
                                "education_field_id" : getData['education_field_id'],
                                "education_field_name" : education_name,
                                "education_score" : education_score,
                                "education_score_at_100_scale" : (education_score  * 100) / float(candidateMainWeightage.main_education_total_weightage),
                                "education_relevancy": education_relevancy
                            }
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
                        "Message": "Job level is not found",
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

#########################################
        
########################################
        
class CandidateExperiencePredictionAPI(APIView):

    '''

        CandidateEducationPrediction API(Insert)
        Request : POST
        Data = {
            "job_level_id" :,
            "candidate_total_month_experience":
            "candidate_relevant_field_experience":
            "candidate_number_of_internship:
        }
    
    
    '''

    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():


                    candidateMainWeightage = MainExperienceWeightageModel.objects.get(job_level_id = getData["job_level_id"])
                    print('pp',candidateMainWeightage)

                    internCalculation = float(getData["candidate_total_month_experience"]) * float(candidateMainWeightage.per_month_experience_weightage)
                    print(internCalculation,'lllllll')

                    if internCalculation > float(candidateMainWeightage.Total_experience_weightage):
                        internship_score = float(candidateMainWeightage.Total_experience_weightage)
                    else:
                        internship_score = internCalculation

                    if float(getData["candidate_relevant_field_experience"]) > 6.0:
                        experience_score = internship_score - (1 - (float(getData["candidate_relevant_field_experience"]) / float(getData["candidate_total_month_experience"])))

                    
                    else:
                        experience_score = internship_score - (0.5 - (float(getData["candidate_relevant_field_experience"]) / float(getData["candidate_total_month_experience"])))

                    print(getData["candidate_total_month_experience"],'kkkkk')
                    print(getData["candidate_relevant_field_experience"],'yyyy')
                    non_relevant_experience = float(getData["candidate_total_month_experience"])- float(getData["candidate_relevant_field_experience"])
                    print(non_relevant_experience,"ppppp")
                    print(candidateMainWeightage.Non_relevant_experience_weightage, 'sssssssss')
                    non_relevant_experience_score = non_relevant_experience * float(candidateMainWeightage.Non_relevant_experience_weightage)
                    print(non_relevant_experience_score,"ooooo")
                    final_experience_score = experience_score + non_relevant_experience_score

                    if candidateMainWeightage.job_level.job_level_name == "intern":
                        if final_experience_score > float(candidateMainWeightage.Total_experience_weightage):
                            final_experience_score = float(candidateMainWeightage.Total_experience_weightage)

                    elif candidateMainWeightage.job_level.job_level_name == "junior":
                        if final_experience_score > float(candidateMainWeightage.Total_experience_weightage):
                            internship_calculation = float(getData["candidate_number_of_internship"]) * float(candidateMainWeightage.per_internship_weightage)

                            if internship_calculation > float(candidateMainWeightage.Total_internship_weightage):
                                final_experience_score = float(candidateMainWeightage.Total_experience_weightage) + float(candidateMainWeightage.Total_internship_weightage)
                            else:
                                final_experience_score = float(candidateMainWeightage.Total_experience_weightage) + internship_calculation
                        
                        else:
                            internship_calculation = float(getData["candidate_number_of_internship"]) * float(candidateMainWeightage.per_internship_weightage)

                            if internship_calculation > float(candidateMainWeightage.Total_internship_weightage):
                                final_experience_score = final_experience_score + float(candidateMainWeightage.Total_internship_weightage)
                            else:
                                final_experience_score = final_experience_score + internship_calculation

                        if final_experience_score > float(candidateMainWeightage.Total_experience_weightage):
                            final_experience_score = float(candidateMainWeightage.Total_experience_weightage)

                    elif candidateMainWeightage.job_level.job_level_name == "senior":
                        if final_experience_score > float(candidateMainWeightage.Total_experience_weightage):
                            final_experience_score = float(candidateMainWeightage.Total_experience_weightage)

                    res= {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Experience prediction record",
                    "Data": {
                        "job_level_id" : getData["job_level_id"],
                        "job_level_name" : JobLevelModel.objects.get(job_level_id = getData["job_level_id"]).job_level_name,
                        "experience_score":final_experience_score,
                        "experience_score_at_100_scale" : (final_experience_score  * 100) / float(candidateMainWeightage.Total_experience_weightage)
                        
                    }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)
            
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level is not found",
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

#######################################################
        
#######################################################

class CandidateTechnicalPredictionAPI(APIView):

    '''

        CandidateTechnicalPrediction API(Insert)
        Request : POST
        Data = {
            "job_level_id" :,
            "job_position_id" :,
            "user_id":,
            "candidate_report_analysis_id": "analysis_report_1234"
        }
    
    
    '''

    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():

                    if JobPositionModel.objects.filter(job_position_id = getData['job_position_id']).exists():

                        if not candidateReportHavetoTechSkillModel.objects.filter(user_id = getData['user_id'],candidate_report_analysis_id = getData["candidate_report_analysis_id"]).exists() or not candidateReportOptionalTechSkillModel.objects.filter(user_id = getData['user_id'], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).exists():

                            techskill = CandidateTechnicalskillsModel.objects.filter(user_id = getData['user_id']).values()

                            have_to_techskills = []
                            optional_to_techskills = []

                            for tech in techskill:
                                if HaveToTechnicalSkillsModel.objects.filter(job_position_id = getData['job_position_id'], job_level_id = getData['job_level_id'], technical_skills_id = tech["candidate_technical_skill_id"] ).exists():

                                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                                    uniqueID = "BroaderAI_have_to_candidate_prediction_technical_skill_" + randomstr

                                    havetoSkill = candidateReportHavetoTechSkillModel(
                                        candidate_report_haveto_tech_skill_id = uniqueID,
                                        user_id = getData["user_id"],
                                        candidate_report_analysis_id = getData["candidate_report_analysis_id"],
                                        technical_skills_id = tech["candidate_technical_skill_id"],
                                        have_to_technical_skills_name = tech["candidate_technical_skill_name"],

                                    )

                                    havetoSkill.save()

                                    have_to_techskills.append(tech["candidate_technical_skill_name"])

                                else:

                                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                                    uniqueID = "BroaderAI_optional_to_candidate_prediction_technical_skill_" + randomstr

                                    optionalSkill = candidateReportOptionalTechSkillModel(
                                        candidate_report_optional_tech_skill_id =uniqueID,
                                        user_id = getData["user_id"],
                                        candidate_report_analysis_id = getData["candidate_report_analysis_id"],
                                        technical_skills_id = tech["candidate_technical_skill_id"],
                                        optional_technical_skills_name = tech["candidate_technical_skill_name"],

                                    )

                                    optionalSkill.save()

                                    optional_to_techskills.append(tech["candidate_technical_skill_name"])

                            techWeightage = TechnicalSkillWeightageModel.objects.get(job_level_id = getData['job_level_id'])

                            have_to_total_score = float(techWeightage.per_haveto_technical_skill_weightage) *  len(have_to_techskills)
                            optional_total_score = float(techWeightage.per_optional_technical_skill_weightage) *  len(optional_to_techskills)
                            technical_prediction_score = have_to_total_score + optional_total_score

                            if technical_prediction_score > float(techWeightage.Total_technical_skill_weightage):
                                technical_prediction_score = float(techWeightage.Total_technical_skill_weightage)


                            res = { 

                                "Status": "success",
                                "Code": 201,
                                "Message":"Technical skill prediction record",
                                "Data": {
                                    "job_level_id" : getData['job_level_id'],
                                    "job_position_id" : getData["job_position_id"],
                                    "total_technical_skills": len(have_to_techskills) + len(optional_to_techskills),
                                    "total_haveto_technical_skills": len(have_to_techskills),
                                    "total_optional_technical_skills": len(optional_to_techskills),
                                    "haveto_skills" : have_to_techskills,
                                    "optional_skills" : optional_to_techskills,
                                    "have_to_total_score" : have_to_total_score,
                                    "optional_total_score" : optional_total_score,
                                    "technical_prediction_score" : technical_prediction_score,
                                    "have_to_total_score_at_100_scale" : (have_to_total_score  * 100) / float(techWeightage.Total_technical_skill_weightage),
                                    "optional_total_score_at_100_scale" : (optional_total_score  * 100) / float(techWeightage.Total_technical_skill_weightage),
                                    "technical_prediction_score_at_100_scale" : (technical_prediction_score  * 100) / float(techWeightage.Total_technical_skill_weightage)
                                    
                                }
                            }

                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Have to and optional skills already exists with this report",
                                "Data":[],
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        

                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job level is not found",
                            "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level is not found",
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
        
#########################################################
        
#########################################################  

class CandidateSoftSkillPredictionAPI(APIView):

    '''

        Candidate Soft Skill Prediction API(Insert)
        Request : POST
        Data = {
            "job_level_id" :,
            "user_id":
        }
    
    
    '''

    def post(self, request ,format=None):

        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():
                        
                    candidate_soft_skill = len(CandidateSoftskillsModel.objects.filter(user_id = getData['user_id']).values())

                    candidateMainWeightage = SoftSkillWeightageModel.objects.get(job_level_id = getData["job_level_id"])

                    internCalculation = float(candidate_soft_skill) * float(candidateMainWeightage.per_soft_skill_weightage)

                    if candidateMainWeightage.job_level.job_level_name == "intern":
                        soft_skill_cal = internCalculation
                        if soft_skill_cal > float(candidateMainWeightage.Total_soft_skill_weightage):
                            soft_skill_score = float(candidateMainWeightage.Total_soft_skill_weightage)
                        else:
                            soft_skill_score = soft_skill_cal

                    elif candidateMainWeightage.job_level.job_level_name == "junior":
                        soft_skill_cal = internCalculation
                        if soft_skill_cal > float(candidateMainWeightage.Total_soft_skill_weightage):
                            soft_skill_score = float(candidateMainWeightage.Total_soft_skill_weightage)
                        else:
                            soft_skill_score = soft_skill_cal

                    elif candidateMainWeightage.job_level.job_level_name == "senior":
                        soft_skill_cal = internCalculation
                        if soft_skill_cal > float(candidateMainWeightage.Total_soft_skill_weightage):
                            soft_skill_score = float(candidateMainWeightage.Total_soft_skill_weightage)
                        else:
                            soft_skill_score = soft_skill_cal

                    res= {
                    "Status": "success",
                    "Code": 201,
                    "Message": "soft skill prediction record",
                    "Data": {
                        "job_level_id" : getData["job_level_id"],
                        "job_level_name" : JobLevelModel.objects.get(job_level_id = getData["job_level_id"]).job_level_name,
                        "total_soft_skills":candidate_soft_skill,
                        "soft_skill_score":soft_skill_score,
                        "soft_skill_score_at_100_scale" : (soft_skill_score  * 100) / float(candidateMainWeightage.Total_soft_skill_weightage)
                        
                    }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level is not found",
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
        
#########################################################
        
######################################################### 

class CandidateCurricularActivitiesPredictionAPI(APIView):

    '''

        Candidate curriculum activity Prediction API(Insert)
        Request : POST
        Data = {
            "job_level_id" :,
            "user_id":
        }
    
    
    '''

    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():
               
                    Hackathon = len(CandidatehackathonModel.objects.filter(user_id = getData['user_id']).values())

                    Contribution = len(CandidateContributionModel.objects.filter(user_id = getData['user_id']).values())

                    Workshop = len(CandidateWorkshopModel.objects.filter(user_id = getData['user_id']).values())

                    Seminar = len(CandidateSeminarModel.objects.filter(user_id = getData['user_id']).values())

                    Competition = len(CandidateCompetitionModel.objects.filter(user_id = getData['user_id']).values())

                    Certificate = len(CandidateCertificateModel.objects.filter(user_id = getData['user_id']).values())

                    candidate_curriculum_activities = Hackathon + Contribution + Workshop + Seminar + Competition + Certificate

                    candidateWeightage = CurricularActivitiesWeightageModel.objects.get(job_level_id = getData['job_level_id'])

                    curricular_activites_score =candidate_curriculum_activities * float(candidateWeightage.per_curricular_activity_weightage)

                    if curricular_activites_score > float(candidateWeightage.Total_curricular_activity_weightage):
                        curricular_activites_score = float(candidateWeightage.Total_curricular_activity_weightage)

                
                    res= {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Curricular Activity prediction record",
                    "Data": {
                        "job_level_id" : getData["job_level_id"],
                        "job_level_name" : JobLevelModel.objects.get(job_level_id = getData["job_level_id"]).job_level_name,
                        "total_curricular_activities" : candidate_curriculum_activities,
                        "curricular_activites_score": curricular_activites_score,
                        "curricular_activites_score_at_100_scale" : (curricular_activites_score  * 100) / float(candidateWeightage.Total_curricular_activity_weightage)
                        
                    }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level is not found",
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
#########################################################
        
#########################################################
     
class AnyDropPredictionAPI(APIView):

    '''

        Candidate any drop Prediction API(Insert)
        Request : POST
        Data = {
            "job_level_id" :,
            "user_id":
        }
    
    
    '''

    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():
               
                    candidate_education_year_drop = CandidateBasicEducationDetails.objects.get(user_id = getData['user_id']).candidate_education_year_drop
                    
                    candidateWeightage = AnyDropWeightageModel.objects.get(job_level_id = getData['job_level_id'])

                    any_drop_score = candidate_education_year_drop * float(candidateWeightage.any_drop_weightage)

                    res= {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Any Drop prediction record",
                    "Data": {
                        "job_level_id" : getData["job_level_id"],
                        "job_level_name" : JobLevelModel.objects.get(job_level_id = getData["job_level_id"]).job_level_name,
                        "any_drop_status" : candidate_education_year_drop,
                        "any_drop_score": any_drop_score
                        # "any_drop_score_at_100_scale" : (any_drop_score  * 100) / float(candidateWeightage.any_drop_weightage)
                        
                    }
                    }

                    return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level is not found",
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

#########################################################
        
#########################################################

     
class ProjectPredictionAPI(APIView):

    '''

        Candidate project Prediction API(Insert)
        Request : POST
        Data = {
            "job_level_id" :,
            "user_id":
            "job_position_id" :,
            "candidate_report_analysis_id": "analysis_report_1234"
        }
    
    
    '''

    def post(self, request ,format=None):
        getData = request.data

        if NewUser.objects.filter(id=getData["user_id"]).exists():
        
            user = NewUser.objects.get(id=getData["user_id"])
        
            if user.user_is_loggedin:

                if JobLevelModel.objects.filter(job_level_id = getData['job_level_id']).exists():

                    project_techskill = CandidateProjectTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).values()

                    projects = []
                    project_technical_skills = dict()

                    for prj in project_techskill:
                        projects.append(prj["candidate_project_id"])
                    

                    projects = list(set(projects))

                    for idx, pr in enumerate(projects):

                        prTechs = CandidateProjectTechnicalSkillsModel.objects.filter(candidate_project_id = pr).values()
                        
                        project_tech_skills = dict()
                        
                        for ptech in prTechs:

                            project_tech_skills[ptech["candidate_technical_skill_id"]] = [ptech["candidate_technical_skill_name"], ptech["candidate_resume_project_technical_skill_id"]]
                    
                        project_technical_skills[pr] = project_tech_skills
        
                    projects_details =dict() 

                    project_prediction_details = dict() 

                    prj_rel_skills = [] 
                    prj_non_rel_skills = [] 

                    total_relevent_projs = 0
                    
                    for key, val in  project_technical_skills.items():

                        prj_rel_skills = [] 
                        prj_non_rel_skills = []


                        for tech_key, tech_val in val.items(): 

                            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))
                        
                            if HaveToTechnicalSkillsModel.objects.filter(job_position_id = getData['job_position_id'], job_level_id = getData['job_level_id'], technical_skills_id = tech_key ).exists():

                                uniqueID = "BroaderAI_relevant_proj_candidate_pred_tech_skill_" + randomstr

                                relevantskill = candidateReportAnalysisProjectRelevantSkillsModel(
                                    candidate_report_project_relevant_skills_id = uniqueID,
                                    user_id = getData["user_id"],
                                    candidate_resume_project_technical_skill_id =  tech_val[1],
                                    candidate_report_analysis_id = getData["candidate_report_analysis_id"],
                                    candidate_resume_project_id = key,
                                    candidate_technical_skill_id = tech_key,
                                    candidate_technical_skill_name = tech_val[0],
                                    candidate_job_position_id = getData["job_position_id"],
                                    candidate_job_level_id = getData["job_level_id"]
                                )

                                relevantskill.save()
                                prj_rel_skills.append(tech_val[0])

                            else:

                                uniqueID = "BroaderAI_relevant_proj_candidate_pred_tech_skill_" + randomstr

                                nonrelevantskill = candidateReportAnalysisProjectNonRelevantSkillsModel(
                                    candidate_report_project_non_relevant_skills_id = uniqueID,
                                    user_id = getData["user_id"],
                                    candidate_resume_project_technical_skill_id =  tech_val[1],
                                    candidate_report_analysis_id = getData["candidate_report_analysis_id"],
                                    candidate_resume_project_id = key,
                                    candidate_technical_skill_id = tech_key,
                                    candidate_technical_skill_name = tech_val[0],
                                    candidate_job_position_id = getData["job_position_id"],
                                    candidate_job_level_id = getData["job_level_id"]
                                )


                                nonrelevantskill.save()
                                prj_non_rel_skills.append(tech_val[0])
                                
                        total_prj_tech_skills = len(prj_rel_skills) + len(prj_non_rel_skills)


                        if len(prj_rel_skills) > (total_prj_tech_skills / 2):

                            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))

                            uniqueID = "BroaderAI_project_relevant_" + randomstr

                            projrel = candidateReportAnalysisProjectRelevancyModel(
                                candidate_report_project_relevancy_id = uniqueID,
                                user_id = getData["user_id"],
                                candidate_resume_project_id = key,
                                candidate_report_analysis_id = getData["candidate_report_analysis_id"],
                                candidate_project_relevant = "Yes"
                            )

                            projrel.save()

                            total_relevent_projs = total_relevent_projs + 1
                            
                            project_prediction_details[key] = {
                                "relevant_tech_skills": prj_rel_skills,
                                "non_relevant_tech_skills": prj_non_rel_skills,
                                "project_relevancy": "Yes"
                            }

                        else:

                            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                        string.digits, k=15))

                            uniqueID = "BroaderAI_project_relevant_" + randomstr

                            projrel = candidateReportAnalysisProjectRelevancyModel(
                                candidate_report_project_relevancy_id = uniqueID,
                                user_id = getData["user_id"],
                                candidate_resume_project_id = key,
                                candidate_report_analysis_id = getData["candidate_report_analysis_id"],
                                candidate_project_relevant = "No"
                            )

                            total_relevent_projs = total_relevent_projs


                            projrel.save()

                            project_prediction_details[key] = {
                                "relevant_tech_skills": prj_rel_skills,
                                "non_relevant_tech_skills": prj_non_rel_skills,
                                "project_relevancy": "No"
                            }

                    candweightage = ProjectWeightageModel.objects.get(job_level_id = getData['job_level_id'])

                    project_pred_score = float(candweightage.per_project_weightage) * total_relevent_projs

                    if project_pred_score > float(candweightage.Total_project_weightage):
                        project_pred_score = float(candweightage.Total_project_weightage)

                    if candweightage.Total_project_weightage != 0:
                        prediction_score_at_100 = (project_pred_score  * 100) / float(candweightage.Total_project_weightage) 
                    else:
                        prediction_score_at_100 = 0

                    res= {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Project prediction record",
                    "Data": {
                        "Project_prediction_details": project_prediction_details,
                        "Total_project": len(project_prediction_details),
                        "Total_relevant_projects": total_relevent_projs,
                        "Total_non_relevant_projects": len(project_prediction_details) - total_relevent_projs,
                        "Project_prediction_score": project_pred_score,
                        "Project_prediction_score_at_100_scale" :prediction_score_at_100
                        }
                    }
                        
                    return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level is not found",
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
##########################################################
        
#########################################################

    
class CandidateReportGetAPI(APIView):
    '''
        Candidate Report API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        candidateReportDetails = CandidateReportAnalysisModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Report Details",
                "Data": candidateReportDetails
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class CandidateReportGetOneAPI(APIView):
    '''
        Candidate basic experience API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug",
                    "candidate_report_analysis_id": "BroaderAI_basic_experience_gsywuycgi3ydhpb"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():

            if CandidateReportAnalysisModel.objects.filter(user_id=getData["user_id"]).exists():

                user = NewUser.objects.get(id=getData["user_id"])

                if user.user_is_loggedin:

                    if CandidateReportAnalysisModel.objects.filter( user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).exists(): 

                        candidateDetail = CandidateReportAnalysisModel.objects.get(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"])
                        
                        candidateReport = {
                            "Report_id" : candidateDetail.candidate_report_analysis_id,
                            "user_id" : candidateDetail.user_id,
                            "job_level" : candidateDetail.job_level_id,
                            "job_position" : candidateDetail.job_position_id
                        }


                        educationDetail= CandidateBasicEducationHistoryDetails.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()
                        
                        educationMainDetail = CandidateMainEducationHistoryDetails.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        edudetail = {
                            "Basic_education_details": educationDetail,
                            "Main_education_details": educationMainDetail,
                            "Education_pred": {
                                            "edu_relevancy" : candidateDetail.candidate_education_relevancy,
                                            "edu_score": candidateDetail.candidate_education_score,
                                            "drop_score" : candidateDetail.candidate_drop_year_penalty_score
                                        }
                        }


                        havetotechskill = candidateReportTechSkillHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"],candidate_technical_skill_status ="haveto").values()

                        optionaltechskill = candidateReportTechSkillHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"],candidate_technical_skill_status ="optional").values()
                    

                        techdetail = {
                            "Technical_Skill_details" : {
                                "haveto_technical_skills" : havetotechskill,
                                "optional_technical_skills" : optionaltechskill
                            },
                            "Technical_Skill_pred" :{
                                "total_technical_skill" : candidateDetail.candidate_total_technical_skills,
                                "total_haveto_skill" : candidateDetail.candidate_total_haveto_skills, 
                                "total_optional_skill" : candidateDetail.candidate_total_optional_skills,
                                "technical_skill_score" : candidateDetail.candidate_total_technical_skill_weightage
                            }
                        }

                        relprojectdetail = candidateReportAnalysisProjectHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"],candidate_project_relevant = "Yes").values()

                        nonrelprojectdetail = candidateReportAnalysisProjectHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"], candidate_project_relevant ="No").values()

                        project = {
                            "Project_details" : {
                                "relevant_projects" : relprojectdetail,
                                "non_relevant_projects" : nonrelprojectdetail
                            },
                            "Project_pred" : {
                                "total_relevant_project" : candidateDetail.candidate_total_relevant_projects,
                                "candidate_total_projects" : candidateDetail.candidate_total_projects,
                                "candidate_project_relevant_score" : candidateDetail.candidate_project_relevant_score
                            }
                        }

                        experienceDetail= CandidateBasicExperienceHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()
                        
                        experienceMainDetail = CandidateMainExperienceHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()
                        

                        expdetail = {
                            "Basic_experience_details": experienceDetail,
                            "Main_experience_details": experienceMainDetail,
                            "Experience_pred": {
                                            "candidate_total_month_experience" : candidateDetail.candidate_total_month_experience,
                                            "candidate_relevant_field_experience": candidateDetail.candidate_relevant_field_experience,
                                            "candidate_number_of_internship" : candidateDetail.candidate_number_of_internship,
                                            "candidate_relevant_experience_score" : candidateDetail.candidate_relevant_experience_score
                                        }
                        } 

                        softskillDetail = CandidateSoftskillsHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        ssdetail = {
                            "Soft_skill_Details" : softskillDetail,
                            "Soft_skill_pred" : {
                                "candidate_total_softskill":candidateDetail.candidate_total_softskill,
                                "candidate_total_softskill_score":candidateDetail.candidate_total_softskill_score
                            }
                        }

                        curactdetail = {
                            "candidate_number_of_curriculum_activities" : candidateDetail.candidate_number_of_curriculum_activities,
                            "candidate_number_of_curriculum_activity_score" : candidateDetail.candidate_number_of_curriculum_activity_score
                        }
                        
                        hackathonDetail = CandidatehackathonHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        hackdetail = {
                            "hackathonDetail":hackathonDetail
                        }

                        contributionDetail = CandidateContributionHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        contridetail = {
                            "contributionDetail":contributionDetail
                        }

                        wsdetail = CandidateWorkshopHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        workshopDetail = {
                            "workshopDetail": wsdetail
                        }

                        semdetail = CandidateSeminarHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        seminarDetail = {
                            "seminarDetail": semdetail
                        }

                        compdetail = CandidateCompetitionHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()


                        competitionDetail = {
                            "competitionDetail": compdetail
                        }

                        certidetail = CandidateCertificateHistoryModel.objects.filter(user_id=getData["user_id"], candidate_report_analysis_id = getData["candidate_report_analysis_id"]).values()

                        certificateDetail = {
                            "certificateDetail": certidetail
                        }



                        if candidateDetail:
                            # Construct the response dictionary
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Candidate report Details",
                                "Data": {
                                    "Candidate_Report" : candidateReport,
                                    "Education_Detail" : edudetail,
                                    "Technical_Skills_Detail" : techdetail,
                                    "Project_Detail" : project,
                                    "Experience_Detail" : expdetail,
                                    "Soft_Skills_Detail": ssdetail,
                                    "Hackathon_Detail": hackdetail,
                                    "Contribution_Detail":contridetail,
                                    "Workshop_Detail": workshopDetail,
                                    "Seminar_Detail": seminarDetail,
                                    "Competition_Detail": competitionDetail,
                                    "Certificate_Detail": certificateDetail,
                                    "Curricular_Act_Details": curactdetail
                                }
                               
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
                            "Message": "User and report not found",
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
                    "Message": "Candidate report details is not found", "Data": None}
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

##########################################################
        
#########################################################

class CandidateProfileScoreAPI(APIView):
    '''
        Candidate profile score API(view)
        Request : Post
        Data = {
                    "user_id": "BroaderAI_bhramizadafiya1234_b21m81xbug"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        score = 0
        
        if NewUser.objects.filter(id=getData["user_id"]).exists():
            score = score + 10

        if CandidateBasicEducationDetails.objects.filter(user_id = getData['user_id']).exists():
            score = score + 10

        if CandidateMainEducationDetails.objects.filter(user_id = getData['user_id']).exists():
            score = score + 10

        if CandidateBasicExperienceModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 10
        
        if CandidateMainExperienceModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 5

        if CandidateMainExperienceTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 5

        if CandidateTechnicalskillsModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 15

        if CandidateSoftskillsModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 10

        if CandidateProjectModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 10

        if CandidateProjectTechnicalSkillsModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 5

        if CandidatehackathonModel.objects.filter(user_id = getData['user_id']).exists() or CandidateContributionModel.objects.filter(user_id = getData['user_id']).exists() or CandidateWorkshopModel.objects.filter(user_id = getData['user_id']).exists() or CandidateSeminarModel.objects.filter(user_id = getData['user_id']).exists() or CandidateCompetitionModel.objects.filter(user_id = getData['user_id']).exists() or CandidateCertificateModel.objects.filter(user_id = getData['user_id']).exists():
            score = score + 10

        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Candidate Profile score",
                "Data": score
            }
        return Response(res, status=status.HTTP_201_CREATED)
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]



    