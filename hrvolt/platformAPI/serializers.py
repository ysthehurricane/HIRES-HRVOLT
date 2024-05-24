# serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainSerializer(serializers.Serializer):
    useremail = serializers.CharField()

