from rest_framework import serializers
from .models import *
import re
import string
import random
from datetime import datetime
from userloginAPI.models import NewUser
from databaseAPI.models import *

class CandidateReportAnalysisserializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 
    job_position_id = serializers.PrimaryKeyRelatedField(queryset=JobPositionModel.objects.all(), source='job_position')
    job_level_id = serializers.PrimaryKeyRelatedField(queryset=JobLevelModel.objects.all(), source='job_level')
    class Meta:
        model = CandidateReportAnalysisModel
        fields = ["user_id", "job_position_id", "job_level_id"]
    
    def validate(self, data):
        return data