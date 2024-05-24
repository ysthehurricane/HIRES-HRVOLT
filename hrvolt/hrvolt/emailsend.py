
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from . import settings

from rest_framework import serializers
from userloginAPI.models import NewUser

def mailSend(request, myuser, randomstr):
    try:
        user = NewUser.objects.get(id=myuser["id"])

        email_subject = "Verify your Email @ HR Volt Login!!"
        message_html = render_to_string('email_confirmation.html', {
            'name': user.first_name + " " + user.last_name,
            'code': randomstr
        })

        email = EmailMessage(
            email_subject,
            message_html,
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        email.content_subtype = "html"  # Set the content type to HTML
        
        email.send()

        return True

    except Exception as e:
        print("error", e)
        raise serializers.ValidationError({"user_email_send": "Email send error"})
        

# def mailSend(request, myuser, randomstr):
    
#     try:

        
#         user = NewUser.objects.get(id=myuser["id"])


#         email_subject = "Verify your Email @ HR Volt Login!!"
#         message2 = render_to_string('email_confirmation.html',{
            
#             'name': user.first_name+" "+ user.last_name,
#             'code': randomstr
#         })
#         email = EmailMessage(
#         email_subject,
#         message2,
#         settings.EMAIL_HOST_USER,
#         [user.email],
#         )

#         email.fail_silently = True
#         email.send()


#         return True

#     except:

#         raise serializers.ValidationError({"user_email_send":"Email send error"})
