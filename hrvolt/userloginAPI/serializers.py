from rest_framework import serializers
from .models import NewUser, UserContractModel

from django.contrib.auth.hashers import make_password, check_password
import re

import string
import random
from datetime import datetime
'''
    Serializer is used to convert json into django supported complex objects
'''
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewUser   # Model
        fields = "__all__"  # Consider all fields

        #fields = ['user_id', 'name', 'roll', 'city']
        #exclude = ["title"]

    def validate(self, data):

        user_firstname = data["first_name"]
        user_lastname = data["last_name"]
        user_email = data["email"]
        user_password = data["password"]
        user_is_recruiter = data["user_is_recruiter"]

        # Password Patterns
        Passwordpattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$")

        # Validation 
        if len(user_firstname) <= 2:
            raise serializers.ValidationError({'errorMsg':'Length of first Name should be more than 2'})
        if not user_firstname.isalpha():
            raise serializers.ValidationError({'errorMsg':'First Name is required'})
    
        if len(user_lastname) <= 2:
            raise serializers.ValidationError({'errorMsg':'Length of last Name should be more than 2'})
        if not user_lastname.isalpha():
            raise serializers.ValidationError({'errorMsg':'Last Name is required'})

        if NewUser.objects.filter(email=user_email).exists():
            raise serializers.ValidationError({'errorMsg': 'Email is already existed'})
        if user_email.find("@gmail.com") == -1:
            raise serializers.ValidationError({'errorMsg': 'Only Gmail is acceptable'})

        if len(user_password) <= 7:
            raise serializers.ValidationError({'errorMsg':'Length of password should be between 8 and 18'})

        if not re.search(Passwordpattern, user_password):
            raise serializers.ValidationError({'errorMsg':'Password should contain uppercase, lowercase, numbers and special characters'})


        # Salt string for security
        randomstr = ''.join(random.choices(string.ascii_letters +
                             string.digits, k=10))

        # Encrypt password with argon2 algorithms
        data["password"] = make_password(user_password,salt=randomstr, hasher='argon2')
        

        return data

class EmailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewUser
        fields = ['email']

    
    def validate(self, data):

        email = data["email"]
       
        if NewUser.objects.filter(email=email).exists():
            
            user = NewUser.objects.get(email=email)
            if user.user_is_verified:
                raise serializers.ValidationError({'errorMsg': 'Account is already verified'})
                
        else:    
            raise serializers.ValidationError({'errorMsg': 'Email does not existed'})
        
        return data

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewUser
        fields = ['email', 'password']

    
    def validate(self, data):

        email = data["email"]
        pwd = data["password"]
       
        if NewUser.objects.filter(email=email).exists():
            
            user = NewUser.objects.get(email=email)

            if not user.user_is_verified:
                raise serializers.ValidationError({'errorMsg': 'Account is not verified'})
            # elif not user.user_is_recruiter:
            #     raise serializers.ValidationError({'errorMsg': 'User is not a recruiter'})
            else:

                if not user.user_is_loggedin:
                    check_pwd = check_password(pwd, user.password)
                    if check_pwd:
                    
                        user.user_is_loggedin = True
                        user.last_login = datetime.now()
                        user.save()

                        
                    else:    
                        raise serializers.ValidationError({'errorMsg': "Wrong credentials"})
                else:
                    raise serializers.ValidationError({'errorMsg': "Already logged in", 'user_is_recruiter': user.user_is_recruiter})
        else:    
            raise serializers.ValidationError({'errorMsg': 'Invalid Email'})

        

        return data

class ChangePasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewUser
        fields = ['email','password']

    def validate(self, data):

        pwd = data["password"]
        email = data["email"]

        if NewUser.objects.filter(email=email).exists():
            
            user = NewUser.objects.get(email=email)
            
            if not user.user_is_verified:
                raise serializers.ValidationError({'errorMsg': 'Account is not verified'})
            else:

                if user.is_active:
                    if user.user_is_loggedin:
                        check_pwd = check_password(pwd, user.password)
                        
                        if check_pwd:
                            return data
                        else:
                            raise serializers.ValidationError({'errorMsg': 'old password is wrong'})
                    else:
                        raise serializers.ValidationError({'errorMsg': 'You are not loggedin'})
                else:
                    raise serializers.ValidationError({'errorMsg': 'Your account is not activated'})
        else:    
            raise serializers.ValidationError({'errorMsg': 'Wrong credentials'})

class UserEditProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = NewUser
        fields = ["user_birthdate","user_mobileno","user_gender", "user_summary", "user_address","user_jobtitle", "user_country", "user_pincode", "user_facebook", "user_linkedin", "user_github", "user_medium", "user_other1", "user_other2", "user_stackoverflow", "user_address"]


    def validate(self, data):

        user_birthdate = data["user_birthdate"]
        user_mobileno = data["user_mobileno"]
        user_gender =  data["user_gender"]
        user_summary = data["user_summary"]
        user_address = data["user_address"]
        user_jobtitle = data["user_jobtitle"]
        user_country = data["user_country"]
        user_pincode = data["user_pincode"]
        user_facebook = data["user_facebook"]
        user_linkedin = data["user_linkedin"]
        user_github = data["user_github"]
        user_medium = data["user_medium"]
        user_other1 = data["user_other1"]
        user_other2 = data["user_other2"]
        user_stackoverflow = data["user_stackoverflow"]

        mobile_number_pattern = re.compile("^\+?\d{1,3}?[-.\s]?\d{9,12}$")
        facebook_pattern = re.compile("^https?:\/\/(?:www\.)?facebook\.com\/[a-zA-Z0-9_\.]+\/?$")
        linkedin_pattern = re.compile("^https?:\/\/(?:www\.)?linkedin\.com\/[a-zA-Z0-9_\/-]+\/?$")
        github_pattern = re.compile("^https?:\/\/(?:www\.)?github\.com\/[a-zA-Z0-9_\-]+\/?$")
        medium_pattern = re.compile("^https?:\/\/(?:www\.)?medium\.com\/@?[a-zA-Z0-9_\-]+\/?$")
        stackoverflow_pattern = re.compile("^https?:\/\/(?:www\.)?stackoverflow\.com\/[a-zA-Z0-9_\/-]+\/?$")
        link_pattern = re.compile(
                            "^(?:http|ftp)s?://"  # scheme
                            "(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}"  # domain name
                            "(?:/[-a-zA-Z0-9_.,;:|+&@#%*()=!/?]*)?$"  # path and query string
                        )



        if len(user_mobileno) > 0:
            if not re.search(mobile_number_pattern, user_mobileno):
                raise serializers.ValidationError({'errorMsg':'Invalid Mobile no.'})

        if len(user_facebook) > 0:
            if not re.search(facebook_pattern, user_facebook):
                raise serializers.ValidationError({'errorMsg':'Invalid facebbok link'})


        if len(user_linkedin) > 0:
            if not re.search(linkedin_pattern, user_linkedin):
                raise serializers.ValidationError({'errorMsg':'Invalid linkedIn link'})

        
        if len(user_github) > 0:
            if not re.search(github_pattern, user_github):
                raise serializers.ValidationError({'errorMsg':'Invalid github link'})
            

        if len(user_medium) > 0:
            if not re.search(medium_pattern, user_medium):
                raise serializers.ValidationError({'errorMsg':'Invalid medium link'})

        if len(user_other1) > 0:
            if not re.search(link_pattern, user_other1):
                raise serializers.ValidationError({'errorMsg':'Invalid  link website 1'})


        if len(user_other2) > 0:
            if not re.search(link_pattern, user_other2):
                raise serializers.ValidationError({'errorMsg':'Invalid  link website 2'})

        
        if len(user_stackoverflow) > 0:
            if not re.search(stackoverflow_pattern, user_stackoverflow):
                raise serializers.ValidationError({'errorMsg':'Invalid stackoverflow link'})
        
        return data
    
class UserContractserializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=NewUser.objects.all(), source='user') 

    class Meta:
        model = UserContractModel
        fields = ["user_id", "contract_start_date", "contract_end_date","number_of_loggedin_allow","user_unique_api_key","isvalid"]
    
    def validate(self, data):
        return data

