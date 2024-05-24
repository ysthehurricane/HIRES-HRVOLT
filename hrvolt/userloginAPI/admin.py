from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

fields = list(UserAdmin.fieldsets)
fields[1] = ("Personal Info", {
    "fields": ("id", "first_name", "last_name", "email","user_is_verified","user_is_loggedin") 
})
UserAdmin.fieldsets  = tuple(fields)

admin.site.register(NewUser, UserAdmin)