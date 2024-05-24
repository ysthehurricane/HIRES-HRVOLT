"""hrvolt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userloginAPI import views


from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userLoginApis/', include('userloginAPI.urls'), name="userlogin"),
    path('databaseApis/', include('databaseAPI.urls'), name="databaseApiPage"),
    path('candidatePreferenceApis/', include('candidatePreferenceAPI.urls'), name="candidatePreferencePage"),
    path('candidateResumeApis/', include('candidateresumeAPI.urls'), name="candidateresumeDetails"),
    path('candidateReportAnalysisApis/', include('candidateReportAnalysisAPI.urls'), name="candidateReportAnalysisPage"),
    path('resumeWeightageAPIApis/', include('resumeWeightageAPI.urls'), name="resumeWeightageAPIPage"),
    path('MLcandidateReportAnalysisApis/', include('MLcandidateReportAnalysisAPI.urls'), name="MLcandidateReportAnalysisPage"),
    path('recruiterApis/', include('recruiterAPI.urls'), name="recruiterPage"),
    path('platformApis/', include('platformAPI.urls'), name="platformPage"),
    path('DataAnalysisApis/', include('DataAnalysisAPI.urls'), name="DataAnalysisPage"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
