from django.shortcuts import render
from django.http import HttpResponse

from .models import NewUser, UserEmailVerification
from databaseAPI.models import *

from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password

import string
import random
import json

from hrvolt.emailsend import mailSend

from datetime import datetime, timedelta

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserContractModel, UserLoggedModel  # Import your model for API keys
from django.utils import timezone

from platformAPI.models import contractLoggedInModel

class APIKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):

        api_key = request.META.get('HTTP_X_API_KEY')

        if not api_key:
            return None
        try:
            jwt_auth = JWTAuthentication()

            user, jwt_token = jwt_auth.authenticate(request)

            if user is None:
                raise AuthenticationFailed('Authentication failed')
        except:
            raise AuthenticationFailed('Authentication failed')
        
        try:
            api_key_obj = UserContractModel.objects.get(user_unique_api_key=api_key)
        except UserContractModel.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
    
        if not NewUser.objects.filter(id=api_key_obj.user_id).exists():
            raise AuthenticationFailed('User is not valid or active')
        
        if not UserContractModel.objects.filter(user_id=api_key_obj.user_id, user_unique_api_key=api_key).exists():
            raise AuthenticationFailed('Invalid user and API Key')
        
        if contractLoggedInModel.objects.filter(user_id=api_key_obj.user_id, user_unique_api_key=api_key).exists():

            if contractLoggedInModel.objects.filter(user_id=api_key_obj.user_id, user_unique_api_key=api_key, is_loggedin=False).exists():
                raise AuthenticationFailed('You are not loggedIn in Device!')
            
        else:
            raise AuthenticationFailed('You are not logged in!')


        contract_end_date = datetime.strptime(api_key_obj.contract_end_date, '%d/%m/%y').date()
 
        current_date = datetime.now().date()
        
        if contract_end_date < current_date:
            raise AuthenticationFailed('API key has expired')
        
        # logged = int(api_key_obj.number_of_loggedin_allow)
        
        # if logged <= 0:
        #     raise AuthenticationFailed('Number of allowed logins exceeded')
        
        # existing_loggin_entry = UserLoggedModel.objects.filter(
        #     user=api_key_obj.user,
        #     hr_contract=api_key_obj,
        #     user_device_ip= request.META.get('REMOTE_ADDR')
        # ).first()
        
        # if existing_loggin_entry:
        #     loggin_entry = existing_loggin_entry
        # else:

        #     randomstr = ''.join(random.choices(string.ascii_lowercase +
        #                             string.digits, k=15))
        #     uniqueID = "BroaderAI_logged_id_" + randomstr 

        #     loggin_entry = UserLoggedModel.objects.create(
        #         hr_logged_id=uniqueID,
        #         user=api_key_obj.user,
        #         hr_contract=api_key_obj,
        #         user_device_ip=request.META.get('REMOTE_ADDR')
        #     )

        #     logged -= 1

        #     api_key_obj.number_of_loggedin_allow = str(logged)
        #     api_key_obj.save()

        

        return api_key_obj.user, None


class UserRegisterAPI(APIView):

    '''
        User sign up api
        request = post
        data:
        {
            "first_name": "yash",
            "last_name": "patel",
            "email":"patel4@gmail.com",
            "password":"Patel2@",
            "user_is_recruiter": true
        }
    '''

    # request comes from post method
    def post(self, request, format=None):
        
        getData = request.data # data comes from post request
        
        # random string for joining with user id
        randomstr = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))

                            
        # unique_id = "BroaderAI_(user_email)_(randomstr)" 

        uniqueID = "BroaderAI_"+getData["email"].split("@")[0]+"_"+randomstr
        getData["id"] = uniqueID
        getData["username"] = getData["email"].split("@")[0].lower()
        # print(getData["username"])
        serializer = UserSerializer(data=getData) # convert json data into python object   

        if serializer.is_valid(): # Check validation
            
            serializer.save() # insert new record in database

            # Response format
            res = {"Status": "success",
                    "Code": 201,
                    "Message": "Candidate is registerd", 
                    "Data":{
                        "id": uniqueID,
                        "user_email": getData["email"],
                        "user_is_recruiter": getData["user_is_recruiter"]
                    },
                    }
            return Response(res, status=status.HTTP_201_CREATED)

        res = {"Status": "error",
                "Code": 200,
                "Message": list(serializer.errors.values())[0][0], 
                "Data":[],
            }
        return Response(res, status=status.HTTP_201_CREATED)


class UserRegisterdemoAPI(APIView):

    '''
        User sign up api
        request = post
        data:
        {
            "first_name": "yash",
            "last_name": "patel",
            "email":"patel4@gmail.com",
            "password":"Patel2@",
            "user_is_recruiter": true,
            "user_is_verified" : true,
            "user_is_loggedin" : true
        }
    '''

    # request comes from post method
    def post(self, request, format=None):
        
        getData = request.data # data comes from post request
        
        # random string for joining with user id
        randomstr = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))

                            
        # unique_id = "BroaderAI_(user_email)_(randomstr)" 

        uniqueID = "BroaderAI_"+getData["email"].split("@")[0]+"_"+randomstr
        getData["id"] = uniqueID
        getData["username"] = getData["email"].split("@")[0].lower()

        candidates = NewUser(
            username = getData["username"],
            id = getData["id"],
            first_name = getData["first_name"],
            last_name = getData["last_name"],
            email = getData["email"],
            password = getData["password"],
            user_is_recruiter = getData["user_is_recruiter"],
            user_is_verified = getData["user_is_verified"],
            user_is_loggedin = getData["user_is_loggedin"]
        )

        candidates.save()
        
        res = {"Status": "success",
                "Code": 201,
                "Message": "Candidate is registerd", 
                "Data":{
                    "id": uniqueID,
                    "user_email": getData["email"],
                    "user_is_recruiter": getData["user_is_recruiter"]
                },
            }

        return Response(res, status=status.HTTP_201_CREATED)

class UserIdGetAPI(APIView):
    def post(self, request, format=None):
        user_ids = NewUser.objects.values_list('id', flat=True)
        user_id_list = list(user_ids)
        
        res = {"Status": "success",
               "Code": 201, 
               "Message": "Candidate Data Get",
                "Data":{
                    "user_id_list": user_id_list
                },
            }
        return Response(res, status=status.HTTP_201_CREATED)
    

class UserloggedInUpdateAPI(APIView):
    '''
        User sign up api
        request = patch
        data:
        {
            "user_id": "",
            "user_is_loggedin: true
        }
    '''
    def patch(self, request, format=None):
        getData = request.data
        if NewUser.objects.filter(id = getData["user_id"]).exists():
            userDetails = NewUser.objects.get(id = getData["user_id"])
            userDetails.user_is_loggedin = getData["user_is_loggedin"]
            userDetails.save()
            res = {
                "Status": "success",
                "Code": 201,
                "Message": "User loggedIn is updated",
                "Data": {
                    "id": getData["user_id"],
                    "email": userDetails.email,
                    "user_is_recruiter":userDetails.user_is_recruiter
                }
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {"Status": "error",
                "Code": 401,
                "Message": "User is not found", 
                "Data":[],
            }
            return Response(res, status=status.HTTP_201_CREATED)
        
class EmailVerificationAPI(APIView):

    '''
        Sending email verification code API
        request = post
        data = {
                "id": "BroaderAI_patelyash2504_qiseymr4mo",
                "email":"patelyash2504@gmail.com"
                }
    '''

    def post(self, request, format=None):
        
        getData = request.data # Get data from API request in json
        print(getData)
        serializer = EmailSerializer(data=getData) # Convert json data into python object

        if serializer.is_valid(): # Check validation

             # Generating code for email verification   
            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=6))


            # Check weather user exist or not in register table
            if NewUser.objects.filter(id = getData["id"]).exists():
                
                # Check weather user exist or not in email veriication code table
                if UserEmailVerification.objects.filter(user_id = getData["id"]).exists():

                    print('==========')
                    userVerification = UserEmailVerification.objects.get(user_id = getData["id"])
                    
                    # Check Code expiration time --- code only valid for 10 min
                    FMT = "%H:%M:%S"
                    current_time = datetime.now().strftime(FMT)
                    store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                    store_time = store_time.strftime(FMT)
                    diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)
                    
                    
                    '''
                        if code is expired then new code with generate and updated in database
                    '''
                    if diff:
                        randomstr = userVerification.OTP_verify
                        print(randomstr,'ppppp')
                    else:
                        userVerification.OTP_verify = randomstr
                        userVerification.expire_time = datetime.now() + timedelta(minutes=10)
                        userVerification.save()
                        print(userVerification,'mmmmmmmmmm')

                else:
                    # if user data is not exist in verification table then insert it
                    userVerification = UserEmailVerification(
                                        user_id = getData["id"],
                                        OTP_verify = randomstr,
                                        expire_time = datetime.now() + timedelta(minutes=10)
                                            )
                    userVerification.save() 

                print(userVerification,"kkkkkkkkk")

                # Send a mail to user along with verification code
                if userVerification.user_id:
                    print(userVerification.user_id,"ssssss")
                    print(getData["email"],"xxxxxxxx")
                    emailStatus = mailSend(request, getData, randomstr)
                    print(emailStatus,'aaaaaaa')
                    if emailStatus:

                        # Response format
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Verification code is sent to your email. Kindly check it out", 
                                "Data":{
                                    "id": getData["id"]
                                }
                            }
                        return Response(res, status=status.HTTP_200_OK)

                    else:
                        res = {"Status": "error",
                                "Code": 401,
                                "Message": "Email sending error", 
                                "Data":[],
                                }

                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {"Status": "error",
                            "Code": 401,
                            "Message": "User is not found", 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {"Status": "error",
                        "Code": 401,
                        "Message": "User is not found", 
                        "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)
                
        res = {"Status": "error",
                "Code": 400,
                "Message": list(serializer.errors.values())[0][0], 
                "Data":[],
            }
        return Response(res, status=status.HTTP_201_CREATED)

class EmailVerificationCompletionAPI(APIView):

    '''
        Compare verification code and verified user account api
        request = patch (partial update) (used for only some columns needs to be updated)
        data = {
                "id": "BroaderAI_patelyash2504_qiseymr4mo",
                "OTP_code":"738bqq"
            }
    '''
    def patch(self, request, format=None):

        getData = request.data

        # Check weather user exist or not in register table
        if NewUser.objects.filter(id = getData["id"]).exists():

            # Check weather user exist or not in email veriication code table
            if UserEmailVerification.objects.filter(user_id = getData["id"]).exists():

                userVerification = UserEmailVerification.objects.get(user_id = getData["id"])

                # Check Code expiration time --- code only valid for 10 min
                FMT = "%H:%M:%S"
                current_time = datetime.now().strftime(FMT)
                store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                store_time = store_time.strftime(FMT)

                diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)


                '''
                    if code is expired then new code with generate and updated in database
                '''

                if diff:

                    if userVerification.OTP_verify == getData["OTP_code"]:

                        myuser = NewUser.objects.get(id = getData["id"])
                        myuser.user_is_verified = True
                        myuser.save()

                        res = {
                                "Status": "success",
                                "Code": 201,    
                                "Message": "Your account is verified", 
                                "Data":{
                                    "id": getData["id"]
                                }
                                }
                        return Response(res, status=status.HTTP_200_OK)

                    else:
                        res = {"Status": "error",
                                "Code": 401,
                                "Message": "Verification Code doesn't match", 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {"Status": "error",
                            "Code": 401,
                            "Message": "Verification code is expired", 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {"Status": "error",
                        "Code": 401,
                        "Message": "User is not found", 
                        "Data":[],
                    }

                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {"Status": "error",
                    "Code": 401,
                    "Message": "User is not found", 
                    "Data":[],
            }
            return Response(res, status=status.HTTP_201_CREATED)

class UserLoginAPI(APIView):

    '''
        User login API
        request = post
        data = {
                    "email":"patelyash2504@gmail.com",
                    "password":"Patelyash12@"
                }
    '''

    def post(self, request, format=None):

        getData = request.data

        print(getData)
        print("yyyy")
        serializer = LoginSerializer(data=getData)

        if serializer.is_valid(): # Check validation

            user = NewUser.objects.get(email=getData["email"])
            
            # Response format
            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "You are successfully login", 
                    "Data":{
                        "id": user.id,
                        "email": getData["email"],
                        "user_is_recruiter":user.user_is_recruiter
                    }
                }
                
            return Response(res, status=status.HTTP_201_CREATED)

        res = {"Status": "error",
                "Code": 200,
                "Message": list(serializer.errors.values())[0][0], 
                "Data":[],
            }
        return Response(res, status=status.HTTP_201_CREATED)


    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class UserLogoutAPI(APIView):

    def patch(self, request, format=None):

        getData = request.data
        if NewUser.objects.filter(id = getData["id"]).exists():
            
            user = NewUser.objects.get(id = getData["id"])

            if user.user_is_loggedin:
                
                user.user_is_loggedin = False
                user.save()

                if user.id:
                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "Succeessfully logout",
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {"Status": "error",
                            "Code": 401,
                            "Message": "Something goes wrong while logout", 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            else:
                
                res = {"Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in", 
                        "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {"Status": "error",
                "Code": 401,
                "Message": "User is not found", 
                "Data":[],
            }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

class UserForgetPasswordAPI(APIView):
    '''
        Forget Password API
        request = post
        data = {
                    "email":"patelyash2504@gmail.com"
                }
    '''

    def post(self, request, format=None):

        getData = request.data


        if NewUser.objects.filter(email=getData['email']).exists():
            

            user = NewUser.objects.get(email=getData['email'])
            print(user,"lll")
            if not user.user_is_loggedin:

                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

                if UserEmailVerification.objects.filter(user_id = user.id).exists():

                        userVerification = UserEmailVerification.objects.get(user_id = user.id)
                        
                        # Check Code expiration time --- code only valid for 10 min
                        FMT = "%H:%M:%S"
                        current_time = datetime.now().strftime(FMT)
                        store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                        store_time = store_time.strftime(FMT)
                        diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)

                        
                        '''
                            if code is expired then new code with generate and updated in database
                        '''
                        if diff:
                            randomstr = userVerification.OTP_verify
                        else:
                            userVerification.OTP_verify = randomstr
                            userVerification.expire_time = datetime.now() + timedelta(minutes=10)
                            userVerification.save()

                else:
                
                # if user data is not exist in verification table then insert it
                    userVerification = UserEmailVerification(
                                        user_id = user.id,
                                        OTP_verify = randomstr,
                                        expire_time = datetime.now() + timedelta(minutes=10)
                                            )
                    userVerification.save() 


                # Send a mail to user along with verification code
                if userVerification.user_id:
                    
                    myuser = dict()
                    myuser["id"] = user.id
                    emailStatus = mailSend(request, myuser, randomstr)
                    print(emailStatus,"ss")
                    if emailStatus:

                        # Response format
                        res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Verification code is sent to your email. Kindly check it out", 
                                "Data":{
                                    "id": user.email
                                }
                            }
                        return Response(res, status=status.HTTP_200_OK)

                    else:
                        res = {"Status": "error",
                                "Code": 401,
                                "Message": "Email sending error", 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {"Status": "error",
                            "Code": 401,
                            "Message": "User is not found", 
                            "Data":[],
                        }
                   
                    return Response(res, status=status.HTTP_201_CREATED)

            else:
                res = {"Status": "error",
                        "Code": 401,
                        "Message": "User is already loggedin", 
                        "Data":[],
                        }  
                return Response(res, status=status.HTTP_201_CREATED)      
        else:
            res = {"Status": "error",
                    "Code": 401,
                    "Message": "Email does not existed", 
                    "Data":[],
                } 
            return Response(res, status=status.HTTP_201_CREATED)

class ForgotPasswordChangedAPI(APIView):

    '''
        Create new password
        request = post
        data = {
                "email":"patelyash2504@gmail.com",
                "user_new_password":"Patelyash12@",
                "OTP_code": "Patelyash12@"
            } 
    '''

    def post(self, request, format=None):

        getData = request.data

        if NewUser.objects.filter(email=getData['email']).exists():

            user = NewUser.objects.get(email=getData['email'])

            if not user.user_is_loggedin:
           
                # Check weather user exist or not in email veriication code table
                if UserEmailVerification.objects.filter(user_id = user.id).exists():

                    userVerification = UserEmailVerification.objects.get(user_id = user.id)

                    # Check Code expiration time --- code only valid for 10 min
                    FMT = "%H:%M:%S"
                    current_time = datetime.now().strftime(FMT)
                    store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                    store_time = store_time.strftime(FMT)

                    diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)


                    '''
                        if code is expired then new code with generate and updated in database
                    '''

                    if diff:

                        if userVerification.OTP_verify == getData["OTP_code"]:

                            # Salt string for security
                            randomstr = ''.join(random.choices(string.ascii_letters +
                                                string.digits, k=10))

                            user.password = make_password(getData["user_new_password"],salt=randomstr, hasher='argon2')
                            user.save()

                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Your Password is changed. please login with new Password",
                                "Data":[]
                                    }
                            return Response(res, status=status.HTTP_201_CREATED)

                        else:
                            res = {"Status": "error",
                                    "Code": 401,
                                    "Message": "Verification Code doesn't match", 
                                    "Data":[],
                                    }
                            return Response(res, status=status.HTTP_201_CREATED)

                    else:
                        res = {"Status": "error",
                                "Code": 401,
                                "Message": "Verification code is expired", 
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_201_CREATED)

                else:
                    res = {"Status": "error",
                            "Code": 401,
                            "Message": "User is not found", 
                            "Data":[],
                        }
                    return Response(res, status=status.HTTP_201_CREATED)
            
            else:
                res = {"Status": "error",
                        "Code": 401,
                        "Message": "User is already loggedin", 
                        "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED) 

        else:
            res = {"Status": "error",
                "Code": 200,
                "Message": "Email does not existed", 
                "Data":[],
            }  
            raise Response(res)

class UserChangePasswordAPI(APIView):
    '''
        Change Password
        request = patch
        data = {
                "id": "BroaderAI_patelyash2504_qiseymr4mo",
                "email":"patelyash2504@gmail.com",
                "password":"Patelyash12@",
                "user_new_password": "Patelyash12@"
            }
    '''

    def patch(self, request, format=None):
        getData = request.data

        if NewUser.objects.filter(id = getData["id"]).exists():
            serializer = ChangePasswordSerializer(data=getData)

            if serializer.is_valid():
                
                user = NewUser.objects.get(id = getData["id"])

                newpwd = getData["user_new_password"]

                randomstr = ''.join(random.choices(string.ascii_letters +
                             string.digits, k=10))

                # Encrypt password with argon2 algorithms
                encrpt_pass = make_password(newpwd,salt=randomstr, hasher='argon2')
                user.password = encrpt_pass
                user.save()

                res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Your password is successfully changed.", 
                        "Data":{
                            "id": getData["id"],
                            "user_email": getData["email"]
                        }
                    }
                return Response(res, status=status.HTTP_201_CREATED)

            res = {"Status": "error",
                "Code": 400,
                "Message": list(serializer.errors.values())[0][0], 
                "Data":[],
            }
            return Response(res, status=status.HTTP_201_CREATED)


        else:
            res = {"Status": "error",
                "Code": 401,
                "Message": "User is not found", 
                "Data":[],
            }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class UserEditProfileAPI(APIView):

    '''
        User edit profile api
        request = patch
        data:
        {
            "id" : "BroaderAI_patelyash2504_ny5pq7a78s",
            "user_birthdate": "2000-04-30",
            "user_mobileno" : "8462351478",
            "user_gender"  : "m",
            "user_summary" : "abc",
            "user_address" : "abc",
            "user_jobtitle" : "[a,b,v,d]",
            "user_country" : "india",
            "user_pincode" : "395478",
            "user_facebook" : "https://www.facebook.com/markzuckerberg/",
            "user_linkedin" : "https://www.linkedin.com/in/billgates/",
            "user_github" : "https://www.github.com/octocat/",
            "user_medium" : "https://www.medium.com/@natfriedman",
            "user_other1" : "https://www.broaderai.com",
            "user_other2" : "http://stackoverflow.com/users/123456/john-doe",
            "user_stackoverflow" : "https://stackoverflow.com/users/123456/john-doe"

        }
    '''

    # request comes from post method
    def patch(self, request, format=None):
        
        getData = request.data

        if NewUser.objects.filter(id = getData["id"]).exists():

            user = NewUser.objects.get(id = getData["id"])

            user.user_birthdate = getData["user_birthdate"]
            user.user_mobileno = getData["user_mobileno"]
            user.user_gender =  getData["user_gender"]
            user.user_summary = getData["user_summary"]
            user.user_address = getData["user_address"]
            user.user_jobtitle = getData["user_jobtitle"]
            user.user_country = getData["user_country"]
            user.user_pincode = getData["user_pincode"]
            user.user_facebook = getData["user_facebook"]
            user.user_linkedin = getData["user_linkedin"]
            user.user_github = getData["user_github"]
            user.user_medium = getData["user_medium"]
            user.user_other1 = getData["user_other1"]
            user.user_other2 = getData["user_other2"]
            user.user_stackoverflow = getData["user_stackoverflow"]
            
            user.save()

            res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "User Profile is updated.", 
                    "Data":{
                        "id": getData["id"]
                    }
                }

            return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {"Status": "error",
                "Code": 401,
                "Message": "User is not found", 
                "Data":[],
            }
            return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


class ViewUserProfileAPI(APIView):

    '''
        User view profile api
        request = post
        data:
        {
            "id" : "abc",
        }
    '''

    # request comes from post method
    def post(self, request, format=None):
        
        getData = request.data

        if NewUser.objects.filter(id = getData["id"]).exists():
            
            user = NewUser.objects.get(id=getData["id"])

            if user.user_is_loggedin:

                if user.user_country is not None:
                    print(user.user_country , "aaaa")
                    
                    nationalityData = NationalityModel.objects.get(nationality_id = user.user_country).nationality_name
                    print(nationalityData,"bbbbbbbbb")
                else:

                    nationalityData = ""


                userdetails = {
                    "user_firstname": user.first_name,
                    "user_lastname": user.last_name,
                    "user_email": user.email,
                    "user_birthdate": user.user_birthdate,
                    "user_mobileno": user.user_mobileno,
                    "user_gender":  user.user_gender,
                    "user_summary": user.user_summary,
                    "user_address": user.user_address,
                    "user_jobtitle": user.user_jobtitle,
                    "user_country": user.user_country,
                    "user_nationality": nationalityData,
                    "user_pincode": user.user_pincode,
                    "user_facebook": user.user_facebook,
                    "user_linkedin": user.user_linkedin,
                    "user_github": user.user_github,
                    "user_medium": user.user_medium,
                    "user_other1": user.user_other1,
                    "user_other2": user.user_other2,
                    "user_stackoverflow": user.user_stackoverflow,
                    "user_is_loggedin": user.user_is_loggedin,
                    "user_is_recruiter": user.user_is_recruiter,


                }
                
                res = {"Status": "success",
                        "Code": 201,
                        "Message": "User detail", 
                        "Data": userdetails}

            else:
                res = {"Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in", 
                        "Data":[],
                    }
                return Response(res, status=status.HTTP_201_CREATED)

        else:
            res = {"Status": "error",
                    "Code": 401,
                    "Message": "User is not found", 
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)

        return Response(res, status=status.HTTP_201_CREATED)

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
                        
class GetUserdataAPI(APIView):
    def post(self,format=None):                            
        user = NewUser.objects.order_by('-pk').last()
        
        user_data = {
        'id': user.id
    }
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "User detail",
                "Data": user_data}
        return Response(res, status=status.HTTP_201_CREATED)
    
class UserContractRegisterAPI(APIView):
    '''
        user contract register API(delete)
        Request : post
        Data =   {
                "user_id": "BroaderAI_yash.p.yashp_mqkchemr9x",
                "total_month": 3
                "number_of_loggedin_allow" : 10
                "isvalid" : true
            }
    '''
    def post(self, request ,formate=None):     

        getData = request.data

        if NewUser.objects.filter(id = getData["user_id"]).exists():
            user = NewUser.objects.get(id=getData["user_id"])  

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))
            uniqueID = "BroaderAI_user_contract_" + randomstr 

            start_date = datetime.now().strftime('%d/%m/%y')
            getData["contract_start_date"] = start_date

            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
            getData["user_unique_api_key"] = random_str

            total_month = getData.get("total_month", 1)
            end_date = (datetime.now() + timedelta(days=total_month * 30)).strftime("%d/%m/%y")

            getData["contract_end_date"] = end_date
            
            serializer = UserContractserializer(data=getData)
                
            if serializer.is_valid():
                
                serializer.save(hr_contract_id= uniqueID)
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "User Contract is Added",
                    "Data": {   
                        "hr_contract_id" : uniqueID,
                        "user_id": getData["user_id"],
                        "contract_start_date":getData["contract_start_date"],
                        "contract_end_date":getData["contract_end_date"],
                        "user_unique_api_key": getData["user_unique_api_key"]
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
            res = {"Status": "error",
                    "Code": 401,
                    "Message": "User is not found", 
                    "Data":[],
                }
            return Response(res, status=status.HTTP_201_CREATED)                    
       
class UserContractGetAPI(APIView):
    '''
        Job Description API(View)
        Request : POST
    '''
    def post(self, request, format=None):
        getData = request.data
        userContractDetails = UserContractModel.objects.values()
        res = {
                "Status": "success",
                "Code": 201,
                "Message": "Job Description Details",
                "Data": userContractDetails
            }
        return Response(res, status=status.HTTP_201_CREATED) 
    

# class DeleteLoggedUserAPI(APIView):

#     def post(self, request, *args, **kwargs):
#         api_key = request.META.get('HTTP_X_API_KEY')

#         if not api_key:
#             return Response({'error': 'API key is missing'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             api_key_obj = UserContractModel.objects.get(user_unique_api_key=api_key)
#         except UserContractModel.DoesNotExist:
#             return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)

#         logged = int(api_key_obj.number_of_loggedin_allow)

#         if logged <= 0:
#             # Delete the user when the number_of_loggedin_allow is exceeded
#             user_id = api_key_obj.user_id
#             try:
#                 user = NewUser.objects.get(id=user_id)
#                 user.delete()
#                 return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
#             except NewUser.DoesNotExist:
#                 raise Http404

#         return Response({'message': 'Number of allowed logins not exceeded'}, status=status.HTTP_200_OK)
    
    