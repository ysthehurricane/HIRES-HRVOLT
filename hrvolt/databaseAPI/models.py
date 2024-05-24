from django.db import models
import datetime
# Create your models here.

class SectorModel(models.Model):
    class Meta:
        db_table = "hrvolt_sector_tb"
    sector_id = models.CharField(max_length= 60, primary_key=True, default=None)
    sector_name = models.CharField(max_length=100,blank=True, null=True, default=None)  # IT, Health, etc
    sector_name_arabic = models.CharField(max_length=100,blank=True, null=True, default=None)  # IT, Health, etc
    sector_action =  models.CharField(max_length=60,blank=True,null=True,default="active")
    sector_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobPositionModel(models.Model):
    class Meta:
        db_table = "hrvolt_job_position_tb"
    sector = models.ForeignKey(SectorModel, on_delete=models.CASCADE, default=None)
    job_position_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job position
    job_position_name = models.TextField(blank=True, null=True, default=None) #python developer, react, data scientist
    job_position_name_arabic = models.TextField(blank=True, null=True, default=None) #python developer, react, data scientist
    job_position_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_position_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobLevelModel(models.Model):
    class Meta:
        db_table = "hrvolt_job_level_tb"

    job_level_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job level
    job_level_name = models.TextField(blank=True, null=True, default=None) #intern, senior, junior
    job_level_name_arabic = models.TextField(blank=True, null=True, default=None) #intern, senior, junior
    job_level_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_level_registration_date = models.DateTimeField(default=datetime.datetime.now())

class LocationModel(models.Model):
    class Meta:
        db_table = "hrvolt_location_tb"

    location_id = models.CharField(max_length=60, primary_key= True, default=None) # id of location
    location_name = models.TextField(blank=True, null=True, default=None) #surat, vadodara, mumbai
    location_name_arabic = models.TextField(blank=True, null=True, default=None) #surat, vadodara, mumbai
    location_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    location_registration_date = models.DateTimeField(default=datetime.datetime.now())

class CompanyTypeModel(models.Model):
    class Meta:
        db_table = "hrvolt_company_type_tb"

    company_type_id = models.CharField(max_length=60, primary_key= True, default=None) # id of company_type
    company_type_name = models.TextField(blank=True, null=True, default=None) #MNC, startup, Indian MNC
    company_type_name_arabic = models.TextField(blank=True, null=True, default=None) #MNC, startup, Indian MNC
    company_type_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    company_type_registration_date = models.DateTimeField(default=datetime.datetime.now())

class WorkPlaceModel(models.Model):
    class Meta:
        db_table = "hrvolt_work_place_tb"

    work_place_id = models.CharField(max_length=60, primary_key= True, default=None) # id of work_place
    work_place_name = models.TextField(blank=True, null=True, default=None) #hybrid, online, on-site
    work_place_name_arabic = models.TextField(blank=True, null=True, default=None) #hybrid, online, on-site
    work_place_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    work_place_registration_date = models.DateTimeField(default=datetime.datetime.now())

class EmploymentTypeModel(models.Model):
    class Meta:
        db_table = "hrvolt_employment_type_tb"

    employment_type_id = models.CharField(max_length=60, primary_key= True, default=None) # id of employment_type
    employment_type_name = models.TextField(blank=True, null=True, default=None) #permanent, full time
    employment_type_name_arabic = models.TextField(blank=True, null=True, default=None) #permanent, full time
    employment_type_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    employment_type_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JoiningPeriodModel(models.Model):
    class Meta:
        db_table = "hrvolt_joining_period_tb"

    joining_period_id = models.CharField(max_length=60, primary_key= True) # id of joining_period
    joining_period_name = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    joining_period_name_arabic = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    joining_period_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    joining_period_registration_date = models.DateTimeField(default=datetime.datetime.now())

class TechnicalSkillsUniqueModel(models.Model):
    class Meta:
        db_table = "hrvolt_unique_technical_skills_tb"
    unique_technical_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of unique_technical_skills
    unique_technical_skills_name = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    unique_technical_skills_name_arabic = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    unique_technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    unique_technical_skills_category_arabic = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    unique_technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    unique_technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())


class TechnicalSkillsMainModel(models.Model):
    class Meta:
        db_table = "hrvolt_main_technical_skills_tb"
    main_technical_skills_id = models.CharField(max_length=100, primary_key= True, default=None) # id of unique_technical_skills
    technical_skills = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None)
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    technical_skills_name = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    technical_skills_name_arabic = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    technical_skills_category_arabic = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

    
class TechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "hrvolt_technical_skills_tb"
    technical_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of technical_skills
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    technical_skills_name = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    technical_skills_name_arabic = models.TextField(blank=True, null=True, default=None) #immediate, after 2 months
    technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    technical_skills_category_arabic = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())


# class HaveToTechnicalSkillsModel(models.Model):
#     class Meta:
#         db_table = "hrvolt_have_to_technical_skills_tb"
#     have_to_technical_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of have to technical_skills
#     technical_skills = models.ForeignKey(TechnicalSkillsMainModel, on_delete=models.CASCADE,default=None) #django, python developer
#     job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
#     job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
#     have_to_technical_skills_name = models.TextField(blank=True, null=True, default=None) 
#     have_to_technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
#     have_to_technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
#     have_to_technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

# class OptionalTechnicalSkillsModel(models.Model):
#     class Meta:
#         db_table = "hrvolt_optional_technical_skills_tb"
#     optional_technical_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of have to technical_skills
#     technical_skills = models.ForeignKey(TechnicalSkillsMainModel, on_delete=models.CASCADE,default=None) #django, python developer
#     job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
#     job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
#     optional_technical_skills_name = models.TextField(blank=True, null=True, default=None) 
#     optional_technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
#     optional_technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
#     optional_technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

class HaveToTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "hrvolt_have_to_technical_skills_tb"
        
    have_to_technical_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of have to technical_skills
    technical_skills = models.ForeignKey(TechnicalSkillsMainModel, on_delete=models.CASCADE,default=None) #django, python developer
    main_unique_technical_skills = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None) #django, python developer
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    have_to_technical_skills_name = models.TextField(blank=True, null=True, default=None)
    have_to_technical_skills_name_arabic = models.TextField(blank=True, null=True, default=None)

    have_to_technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    have_to_technical_skills_category_arabic = models.TextField(blank=True, null=True, default=None) #tools, technology, framework

    have_to_technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    have_to_technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())
    
class OptionalTechnicalSkillsModel(models.Model):
    class Meta:
        db_table = "hrvolt_optional_technical_skills_tb"
    optional_technical_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of have to technical_skills
    technical_skills = models.ForeignKey(TechnicalSkillsMainModel, on_delete=models.CASCADE,default=None) #django, python developer
    main_unique_technical_skills = models.ForeignKey(TechnicalSkillsUniqueModel, on_delete=models.CASCADE,default=None) #django, python developer
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    optional_technical_skills_name = models.TextField(blank=True, null=True, default=None)
    optional_technical_skills_name_arabic = models.TextField(blank=True, null=True, default=None)

    optional_technical_skills_category = models.TextField(blank=True, null=True, default=None) #tools, technology, framework
    optional_technical_skills_category_arabic = models.TextField(blank=True, null=True, default=None) #tools, technology, framework

    optional_technical_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    optional_technical_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

class SoftSkillsModel(models.Model):
    class Meta:
        db_table = "hrvolt_soft_skills_tb"

    soft_skills_id = models.CharField(max_length=60, primary_key= True, default=None) # id of soft_skills
    soft_skills_name = models.TextField(blank=True, null=True, default=None) #leadership, teamwork, adaptability
    soft_skills_name_arabic = models.TextField(blank=True, null=True, default=None) #leadership, teamwork, adaptability

    soft_skills_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    soft_skills_registration_date = models.DateTimeField(default=datetime.datetime.now())

class LanguageModel(models.Model):
    class Meta:
        db_table = "hrvolt_language_tb"

    language_id = models.CharField(max_length=60, primary_key= True, default=None) # id of language
    language_name = models.TextField(blank=True, null=True, default=None) #english , hindi, 
    language_name_arabic = models.TextField(blank=True, null=True, default=None) #english , hindi, 

    language_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    language_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobRequirementModel(models.Model):
    class Meta:
        db_table = "hrvolt_job_requirement_tb"

    job_requirement_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job_requirement
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    job_requirement_description = models.TextField(blank=True, null=True, default=None) 
    job_requirement_description_arabic = models.TextField(blank=True, null=True, default=None) 
    job_requirement_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_requirement_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobBenefitModel(models.Model):
    class Meta:
        db_table = "hrvolt_job_benefit_tb"

    job_benefit_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job_benefit
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    job_benefit_description = models.TextField(blank=True, null=True, default=None) 
    job_benefit_description_arabic = models.TextField(blank=True, null=True, default=None) 
    job_benefit_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_benefit_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobResponsibilityModel(models.Model):

    class Meta:
        db_table = "hrvolt_job_responsibility_tb"

    job_responsibility_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job_responsibility
    job_position = models.ForeignKey(JobPositionModel, on_delete=models.CASCADE, default=None) #django, python developer
    job_level = models.ForeignKey(JobLevelModel, on_delete=models.CASCADE, default=None) #intern, senior
    job_responsibility_description = models.TextField(blank=True, null=True, default=None) 
    job_responsibility_description_arabic = models.TextField(blank=True, null=True, default=None) 

    job_responsibility_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_responsibility_registration_date = models.DateTimeField(default=datetime.datetime.now())
    
class EducationModel(models.Model):
    class Meta:
        db_table = "hrvolt_education_tb"
    education_id = models.CharField(max_length= 60, primary_key=True, default=None)
    education_name = models.CharField(max_length=100,blank=True, null=True, default=None) # BSc, M.TEch
    education_name_arabic = models.CharField(max_length=100,blank=True, null=True, default=None) # BSc, M.TEch
    education_years = models.CharField(max_length=100,blank=True, null=True, default=None) # 3 years, 5 years
    education_years_arabic = models.CharField(max_length=100,blank=True, null=True, default=None) # 3 years, 5 years

    education_action =  models.CharField(max_length=60,blank=True,null=True,default="active")
    education_registration_date = models.DateTimeField(default=datetime.datetime.now())

class EducationFieldModel(models.Model):
    class Meta:
        db_table = "hrvolt_education_field_tb"
    education_field_id = models.CharField(max_length= 60, primary_key=True, default=None)
    education_field_name = models.TextField(default=None, blank=True, null=True) # computer science, data science, IT, AI, ML
    education_field_name_arabic = models.TextField(default=None, blank=True, null=True) # computer science, data science, IT, AI, ML
    sector = models.ForeignKey(SectorModel, on_delete=models.CASCADE, default=None)
    education_field_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active / deactive
    education_field_registration_date = models.DateTimeField(default=datetime.datetime.now())


class NationalityModel(models.Model):
    class Meta:
        db_table = "hrvolt_nationality_tb"
    nationality_id = models.CharField(max_length=60, primary_key= True, default=None) # id of nationality
    nationality_name = models.TextField(blank=True, null=True, default=None) #surat, vadodara, mumbai
    nationality_name_arabic = models.TextField(blank=True, null=True, default=None) #surat, vadodara, mumbai
    nationality_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    nationality_registration_date = models.DateTimeField(default=datetime.datetime.now())


class UniversityModel(models.Model):
    class Meta:
        db_table = "hrvolt_university_tb"
    university_id = models.CharField(max_length=60, primary_key= True, default=None) # id of university
    university_name = models.TextField(blank=True, null=True, default=None) #maliba, ppsu, scet
    university_name_arabic = models.TextField(blank=True, null=True, default=None) #maliba, ppsu, scet
    university_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    university_registration_date = models.DateTimeField(default=datetime.datetime.now())
    
class DegreeModel(models.Model):
    class Meta:
        db_table = "hrvolt_degree_tb"
    degree_id = models.CharField(max_length=60, primary_key= True, default=None) # id of degree
    degree_name = models.TextField(blank=True, null=True, default=None) #english , hindi, arabic
    degree_name_arabic = models.TextField(blank=True, null=True, default=None) #english , hindi, arabic
    degree_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    degree_registration_date = models.DateTimeField(default=datetime.datetime.now())