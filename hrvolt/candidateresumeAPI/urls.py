from django.urls import path
from . import views


from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # path('candidateResumeParsing', views.CandidateResumeParsingAPI.as_view(), name="CandidateResumeParsingAPIPage"),
    path('userResumeUpload', views.userResumeUploadAPI.as_view(), name="userResumeUploadAPIPage"),
    path('getUserResume', views.getUserResumeAPI.as_view(), name="getUserResumeAPIPage"),
    path('userCoverLetter', views.userCoverLetterAPI.as_view(), name="userCoverLetterAPIPage"),
    path('getUserCover', views.getUserCoverAPI.as_view(), name="getUserCoverAPIPage"),

    path('candidateBasicEducationRegister',views.candidateBasicEducationRegisterAPI.as_view(),name='candidateBasicEducationRegisterPage'),
    path('candidateBasicEducationUpdate',views.candidateBasicEducationUpdateAPI.as_view(),name='candidateBasicEducationUpdatePage'),
    path('candidateBasicEducationGet',views.candidateBasicEducationGetAPI.as_view(),name='candidateBasicEducationGetPage'),
    path('candidateBasicEducationDelete',views.candidateBasicEducationDeleteAPI.as_view(),name='candidateBasicEducationDeletePage'),

    path('candidateMainEducationRegisterDetails',views.candidateMainEducationRegisterAPI.as_view(),name='candidateMainEducationRegisterDetailsPage'),
    path('candidateMainEducationUpdate',views.candidateMainEducationUpdateAPI.as_view(),name='candidateMainEducationUpdatePage'),
    path('candidateGetMainEducation',views.candidateGetMainEducationAPI.as_view(),name='candidateGetMainEducationPage'),
    path('candidateGetOneMainEducation',views.candidateGetOneMainEducationAPI.as_view(),name='candidateGetMainOneEducationPage'),
    path('candidateMainEducationDelete',views.candidateMainEducationDeleteAPI.as_view(),name='candidateMainEducationDeletePage'),

    path('CandidateBasicExperienceRegister',views.CandidateBasicExperienceRegisterAPI.as_view(),name='CandidateBasicExperienceRegisterPage'),
    path('CandidateBasicExperienceUpdate',views.CandidateBasicExperienceUpdateAPI.as_view(),name='CandidateBasicExperienceUpdatePage'),
    path('CandidateBasicExperienceGet',views.CandidateBasicExperienceGetAPI.as_view(),name='CandidateBasicExperienceGetPage'),
    path('CandidateBasicExperienceGetOne',views.CandidateBasicExperienceGetOneAPI.as_view(),name='CandidateBasicExperienceGetOnePage'),
    path('CandidateBasicExperienceDelete',views.CandidateBasicExperienceDeleteAPI.as_view(),name='CandidateBasicExperienceDeletePage'),

    path('CandidateMainExperienceRegister',views.CandidateMainExperienceRegisterAPI.as_view(),name='CandidateMainExperienceRegisterPage'),
    path('CandidateMainExperienceUpdate',views.CandidateMainExperienceUpdateAPI.as_view(),name='CandidateMainExperienceUpdatePage'),
    path('CandidateMainExperienceGet',views.CandidateMainExperienceGetAPI.as_view(),name='CandidateMainExperienceGetPage'),
    path('CandidateMainExperienceGetOne',views.CandidateMainExperienceGetOneAPI.as_view(),name='CandidateMainExperienceGetOnePage'),
    path('CandidateMainExperienceDelete',views.CandidateMainExperienceDeleteAPI.as_view(),name='CandidateMainExperienceDeletePage'),

    path('CandidateMainExperienceTechnicalSkillsRegister',views.CandidateMainExperienceTechnicalSkillsRegisterAPI.as_view(),name='CandidateMainExperienceTechnicalSkillsRegisterPage'),
    path('CandidateMainExperienceTechnicalSkillsGet',views.CandidateMainExperienceTechnicalSkillsGetAPI.as_view(),name='CandidateMainExperienceTechnicalSkillsGetPage'),
    path('CandidateMainExperienceTechnicalSkillsGetOne',views.CandidateMainExperienceTechnicalSkillsGetOneAPI.as_view(),name='CandidateMainExperienceTechnicalSkillsGetOnePage'),
    path('CandidateMainExperienceTechnicalSkillsDelete',views.CandidateMainExperienceTechnicalSkillsDeleteAPI.as_view(),name='CandidateMainExperienceTechnicalSkillsDeletePage'),
    path('CandidateMainExperienceTechnicalSkillsAllDelete',views.CandidateMainExperienceTechnicalSkillsAllDeleteAPI.as_view(),name='CandidateMainExperienceTechnicalSkillsAllDeletePage'),

    path('CandidateMainExperienceGetOneAllDetails',views.CandidateMainExperienceGetOneAllDetailsAPI.as_view(),name='CandidateMainExperienceGetOneAllDetailsPage'),

    path('CandidateTechnicalskillsRegister',views.CandidateTechnicalskillsAPI.as_view(),name='CandidateTechnicalskillsRegisterPage'),
    path('CandidateTechnicalskillsGet',views.CandidateTechnicalskillsGetAPI.as_view(),name='CandidateTechnicalskillsGetPage'),
    path('CandidateTechnicalskillsDelete',views.CandidateTechnicalskillsDeleteAPI.as_view(),name='CandidateTechnicalskillsDeletePage'),
    path('CandidateTechnicalskillsAllDelete',views.CandidateTechnicalskillsAllDeleteAPI.as_view(),name='CandidateTechnicalskillsAllDeletePage'),

    path('CandidateSoftskillsRegister',views.CandidateSoftskillsAPI.as_view(),name='CandidateSoftskillsRegisterPage'),
    path('CandidateSoftskillsGet',views.CandidateSoftskillsGetAPI.as_view(),name='CandidateSoftskillsGetPage'),
    path('CandidateSoftskillsDelete',views.CandidateSoftskillsDeleteAPI.as_view(),name='CandidateSoftskillsDeletePage'),

    path('CandidateLanguageRegister',views.CandidateLanguageRegisterAPI.as_view(),name='CandidateLanguageRegisterPage'),
    path('CandidateLanguageGet',views.CandidateLanguageGetAPI.as_view(),name='CandidateLanguageGetPage'),
    path('CandidateLanguageDelete',views.CandidateLanguageDeleteAPI.as_view(),name='CandidateLanguageDeletePage'),

    path('CandidateProjectRegister',views.CandidateProjectAPI.as_view(),name='CandidateProjectRegisterPage'),
    path('CandidateProjectUpdate',views.CandidateProjectUpdateAPI.as_view(),name='CandidateProjectUpdatePage'),
    path('CandidateProjectMediaDelete',views.CandidateProjectMediaDeleteAPI.as_view(),name='CandidateProjectMediaDeletePage'),
    path('CandidateProjectMediaUpdate',views.CandidateProjectMediaUpdateAPI.as_view(),name='CandidateProjectMediaUpdatePage'),
    path('CandidateProjectGet',views.CandidateProjectGetAPI.as_view(),name='CandidateProjectGetPage'),
    path('CandidateProjectGetOne',views.CandidateProjectGetOneAPI.as_view(),name='CandidateProjectGetOnePage'),
    path('CandidateProjectDelete',views.CandidateProjectDeleteAPI.as_view(),name='CandidateProjectDeletePage'),

    path('CandidateProjectTechnicalSkillsRegister',views.CandidateProjectTechnicalSkillsRegisterAPI.as_view(),name='CandidateProjectTechnicalSkillsRegisterPage'),
    path('CandidateProjectTechnicalSkillsGet',views.CandidateProjectTechnicalSkillsGetAPI.as_view(),name='CandidateProjectTechnicalSkillsGetPage'),
    path('CandidateProjectTechnicalSkillsGetOne',views.CandidateProjectTechnicalSkillsGetOneAPI.as_view(),name='CandidateProjectTechnicalSkillsGetOnePage'),
    path('CandidateProjectTechnicalSkillsDelete',views.CandidateProjectTechnicalSkillsDeleteAPI.as_view(),name='CandidateProjectTechnicalSkillsDeletePage'),
    path('CandidateProjectTechnicalSkillsAllDelete',views.CandidateProjectTechnicalSkillsAllDeleteAPI.as_view(),name='CandidateProjectTechnicalSkillsAllDeletePage'),
    path('CandidateProjectGetOneAllDetails',views.CandidateProjectGetOneAllDetailsAPI.as_view(),name='CandidateProjectGetOneAllDetailsPage'),

    path('CandidatehackathonRegister',views.CandidatehackathonAPI.as_view(),name='CandidatehackathonRegisterPage'),
    path('CandidatehackathonUpdate',views.CandidatehackathonUpdateAPI.as_view(),name='CandidatehackathonUpdatePage'),
    path('CandidatehackathonMediaDelete',views.CandidatehackathonMediaDeleteAPI.as_view(),name='CandidatehackathonMediaDeletePage'),
    path('CandidatehackathonMediaUpdate',views.CandidatehackathonMediaUpdateAPI.as_view(),name='CandidatehackathonMediaUpdatePage'),
    path('CandidatehackathonGet',views.CandidatehackathonGetAPI.as_view(),name='CandidatehackathonGetPage'),
    path('CandidatehackathonGetOne',views.CandidatehackathonGetOneAPI.as_view(),name='CandidatehackathonGetOnePage'),
    path('CandidatehackathonDelete',views.CandidatehackathonDeleteAPI.as_view(),name='CandidatehackathonDeletePage'),

    path('CandidateHackathonTechnicalSkillsRegister',views.CandidateHackathonTechnicalSkillsRegisterAPI.as_view(),name='CandidateHackathonTechnicalSkillsRegisterPage'),
    path('CandidateHackathonTechnicalSkillsGet',views.CandidateHackathonTechnicalSkillsGetAPI.as_view(),name='CandidateHackathonTechnicalSkillsGetPage'),
    path('CandidateHackathonTechnicalSkillsGetOne',views.CandidateHackathonTechnicalSkillsGetOneAPI.as_view(),name='CandidateHackathonTechnicalSkillsGetOnePage'),
    path('CandidateHackathonTechnicalSkillsDelete',views.CandidateHackathonTechnicalSkillsDeleteAPI.as_view(),name='CandidateHackathonTechnicalSkillsDeletePage'),
    path('CandidateHackathonTechnicalSkillsAllDelete',views.CandidateHackathonTechnicalSkillsAllDeleteAPI.as_view(),name='CandidateHackathonTechnicalSkillsAllDeletePage'),
    path('CandidateHackathonTechnicalSkillsAllDeleteHack',views.CandidateHackathonTechnicalSkillsAllDeleteHackIdAPI.as_view(),name='CandidateHackathonTechnicalSkillsAllDeleteHackPage'),
    path('CandidateHackathonGetOneAllDetails',views.CandidateHackathonGetOneAllDetailsAPI.as_view(),name='CandidateHackathonGetOneAllDetailsPage'),

    path('CandidateContributionRegister',views.CandidateContributionAPI.as_view(),name='CandidateContributionRegisterPage'),
    path('CandidateContributionUpdate',views.CandidateContributionUpdateAPI.as_view(),name='CandidateContributionUpdatePage'),
    path('CandidateContributionMediaDelete',views.CandidateContributionMediaDeleteAPI.as_view(),name='CandidateContributionMediaDeletePage'),
    path('CandidateContributionMediaUpdate',views.CandidateContributionMediaUpdateAPI.as_view(),name='CandidateContributionMediaUpdatePage'),
    path('CandidateContributionGet',views.CandidateContributionGetAPI.as_view(),name='CandidateContributionGetPage'),
    path('CandidateContributionGetOne',views.CandidateContributionGetOneAPI.as_view(),name='CandidateContributionGetOnePage'),
    path('CandidateContributionDelete',views.CandidateContributionDeleteAPI.as_view(),name='CandidateContributionDeletePage'),

    path('CandidateContributionTechnicalSkillsRegister',views.CandidateContributionTechnicalSkillsRegisterAPI.as_view(),name='CandidateContributionTechnicalSkillsRegisterPage'),
    path('CandidateContributionTechnicalSkillsGet',views.CandidateContributionTechnicalSkillsGetAPI.as_view(),name='CandidateContributionTechnicalSkillsGetPage'),
    path('CandidateContributionTechnicalSkillsGetOne',views.CandidateContributionTechnicalSkillsGetOneAPI.as_view(),name='CandidateContributionTechnicalSkillsGetOnePage'),
    path('CandidateContributionTechnicalSkillsDelete',views.CandidateContributionTechnicalSkillsDeleteAPI.as_view(),name='CandidateContributionTechnicalSkillsDeletePage'),
    path('CandidateContributionTechnicalSkillsConIdDelete',views.CandidateContributionTechnicalSkillsConIdDeleteAPI.as_view(),name='CandidateContributionTechnicalSkillsConIdDeletePage'),

    path('CandidateContributionGetOneAllDetails',views.CandidatecontributionGetOneAllDetailsAPI.as_view(),name='CandidateContributionGetOneAllDetailsPage'),

    path('CandidateWorkshopRegister',views.CandidateWorkshopAPI.as_view(),name='CandidateWorkshopRegisterPage'),
    path('CandidateWorkshopUpdate',views.CandidateWorkshopUpdateAPI.as_view(),name='CandidateWorkshopUpdatePage'),
    path('CandidateWorkshopMediaDelete',views.CandidateWorkshopMediaDeleteAPI.as_view(),name='CandidateWorkshopMediaDeletePage'),
    path('CandidateWorkshopMediaUpdate',views.CandidateWorkshopMediaUpdateAPI.as_view(),name='CandidateWorkshopMediaUpdatePage'),
    path('CandidateWorkshopGet',views.CandidateWorkshopGetAPI.as_view(),name='CandidateWorkshopGetPage'),
    path('CandidateWorkshopGetOne',views.CandidateWorkshopGetOneAPI.as_view(),name='CandidateWorkshopGetOnePage'),
    path('CandidateWorkshopDelete',views.CandidateWorkshopDeleteAPI.as_view(),name='CandidateWorkshopDeletePage'),


    path('CandidateWorkshopTechnicalSkillsRegister',views.CandidateWorkshopTechnicalSkillsRegisterAPI.as_view(),name='CandidateWorkshopTechnicalSkillsRegisterPage'),
    path('CandidateWorkshopTechnicalSkillsGet',views.CandidateWorkshopTechnicalSkillsGetAPI.as_view(),name='CandidateWorkshopTechnicalSkillsGetPage'),
    path('CandidateWorkshopTechnicalSkillsGetOne',views.CandidateWorkshopTechnicalSkillsGetOneAPI.as_view(),name='CandidateWorkshopTechnicalSkillsGetOnePage'),
    path('CandidateWorkshopTechnicalSkillsDelete',views.CandidateWorkshopTechnicalSkillsDeleteAPI.as_view(),name='CandidateWorkshopTechnicalSkillsDeletePage'),
    path('CandidateWorkshopTechnicalSkillsDeleteWork',views.CandidateWorkshopTechnicalSkillsDeleteWorkIdAPI.as_view(),name='CandidateWorkshopTechnicalSkillsDeleteWorkPage'),

    path('CandidateWorkshopGetOneAllDetails',views.CandidateWorkshopGetOneAllDetailsAPI.as_view(),name='CandidateWorkshopGetOneAllDetailsPage'),

    path('CandidateSeminarRegister',views.CandidateSeminarAPI.as_view(),name='CandidateSeminarRegisterPage'),
    path('CandidateSeminarUpdate',views.CandidateSeminarUpdateAPI.as_view(),name='CandidateSeminarUpdatePage'),
    path('CandidateSeminarMediaDelete',views.CandidateSeminarMediaDeleteAPI.as_view(),name='CandidateSeminarMediaDeletePage'),
    path('CandidateSeminarMediaUpdate',views.CandidateSeminarMediaUpdateAPI.as_view(),name='CandidateSeminarMediaUpdatePage'),
    path('CandidateSeminarGet',views.CandidateSeminarGetAPI.as_view(),name='CandidateSeminarGetPage'),
    path('CandidateSeminarGetOne',views.CandidateSeminarGetOneAPI.as_view(),name='CandidateSeminarGetOnePage'),
    path('CandidateSeminarDelete',views.CandidateSeminarDeleteAPI.as_view(),name='CandidateSeminarDeletePage'),

    path('CandidateCompetitionRegister',views.CandidateCompetitionAPI.as_view(),name='CandidateCompetitionRegisterPage'),
    path('CandidateCompetitionUpdate',views.CandidateCompetitionUpdateAPI.as_view(),name='CandidateCompetitionUpdatePage'),
    path('CandidateCompetitionMediaDelete',views.CandidateCompetitionMediaDeleteAPI.as_view(),name='CandidateCompetitionMediaDeletePage'),
    path('CandidateCompetitionMediaUpdate',views.CandidateCompetitionMediaUpdateAPI.as_view(),name='CandidateCompetitionMediaUpdatePage'),
    path('CandidateCompetitionGet',views.CandidateCompetitionGetAPI.as_view(),name='CandidateCompetitionGetPage'),
    path('CandidateCompetitionGetOne',views.CandidateCompetitionGetOneAPI.as_view(),name='CandidateCompetitionGetOnePage'),
    path('CandidateCompetitionDelete',views.CandidateCompetitionDeleteAPI.as_view(),name='CandidateCompetitionDeletePage'),


    path('CandidateCompetitionTechnicalSkillsRegister',views.CandidateCompetitionTechnicalSkillsRegisterAPI.as_view(),name='CandidateCompetitionTechnicalSkillsRegisterPage'),
    path('CandidateCompetitionTechnicalSkillsGet',views.CandidateCompetitionTechnicalSkillsGetAPI.as_view(),name='CandidateCompetitionTechnicalSkillsGetPage'),
    path('CandidateCompetitionTechnicalSkillsGetOne',views.CandidateCompetitionTechnicalSkillsGetOneAPI.as_view(),name='CandidateCompetitionTechnicalSkillsGetOnePage'),
    path('CandidateCompetitionTechnicalSkillsDelete',views.CandidateCompetitionTechnicalSkillsDeleteAPI.as_view(),name='CandidateCompetitionTechnicalSkillsDeletePage'),
    path('CandidateCompetitionTechnicalSkillsCompIdDelete',views.CandidateCompetitionTechnicalSkillsCompIdDeleteAPI.as_view(),name='CandidateCompetitionTechnicalSkillsCompIdDeletePage'),
    path('CandidateCompetitionGetOneAllDetails',views.CandidateCompetitionGetOneAllDetailsAPI.as_view(),name='CandidateCompetitionGetOneAllDetailsPage'),

    path('CandidateCertificateRegister',views.CandidateCertificateAPI.as_view(),name='CandidateCertificateRegisterPage'),
    path('CandidateCertificateUpdate',views.CandidateCertificateUpdateAPI.as_view(),name='CandidateCertificateUpdatePage'),
    path('CandidateCertificateMediaDelete',views.CandidateCertificateMediaDeleteAPI.as_view(),name='CandidateCertificateMediaDeletePage'),
    path('CandidateCertificateMediaUpdate',views.CandidateCertificateMediaUpdateAPI.as_view(),name='CandidateCertificateMediaUpdatePage'),
    path('CandidateCertificateGet',views.CandidateCertificateGetAPI.as_view(),name='CandidateCertificateGetPage'),
    path('CandidateCertificateGetOne',views.CandidateCertificateGetOneAPI.as_view(),name='CandidateCertificateGetOnePage'),
    path('CandidateCertificateDelete',views.CandidateCertificateDeleteAPI.as_view(),name='CandidateCertificateDeletePage'),


    path('CandidateCertificateTechnicalSkillsRegister',views.CandidateCertificateTechnicalSkillsRegisterAPI.as_view(),name='CandidateCertificateTechnicalSkillsRegisterPage'),
    path('CandidateCertificateTechnicalSkillsGet',views.CandidateCertificateTechnicalSkillsGetAPI.as_view(),name='CandidateCertificateTechnicalSkillsGetPage'),
    path('CandidateCertificateTechnicalSkillsGetOne',views.CandidateCertificateTechnicalSkillsGetOneAPI.as_view(),name='CandidateCertificateTechnicalSkillsGetOnePage'),
    path('CandidateCertificateTechnicalSkillsDelete',views.CandidateCertificateTechnicalSkillsDeleteAPI.as_view(),name='CandidateCertificateTechnicalSkillsDeletePage'),
    path('CandidateCertificateTechnicalSkillsCertIdDelete',views.CandidateCertificateTechnicalSkillsCertIdDeleteAPI.as_view(),name='CandidateCertificateTechnicalSkillsCertIdDeletePage'),
    path('CandidateCertificateGetOneAllDetails',views.CandidateCertificateGetOneAllDetailsAPI.as_view(),name='CandidateCertificateGetOneAllDetailsPage'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
