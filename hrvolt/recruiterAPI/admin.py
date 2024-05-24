from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(JobDescriptionModel)
admin.site.register(EducationJobDescriptionModel)
admin.site.register(SoftSkillJobDescriptionModel)
admin.site.register(TechnicalSkillJobDescriptionModel)
admin.site.register(CustomJobDescriptionResponsibilityModel)
admin.site.register(CustomJobDescriptionRequirementsModel)
admin.site.register(CustomJobDescriptionBenefitsModel)
admin.site.register(JobDescriptionResponsibilityModel)
# admin.site.register(JobDescriptionModel)
# admin.site.register(JobDescriptionModel)