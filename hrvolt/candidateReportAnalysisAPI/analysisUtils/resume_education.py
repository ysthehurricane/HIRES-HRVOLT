from databaseAPI.models import *
from candidateresumeAPI.models import *


class ResumeAnalysisEducation:
    def __init__(self, job_level, education_id, education_field_id, sector_id):
        self.fields = EducationFieldModel.objects.filter(education_field_id=education_field_id, sector=sector_id)
        self.i_diploma_penalty = 0.35
        self.i_3year_penalty = 0.65
        self.i_4year_penalty = 0.75
        self.i_post_graduate_penalty = 1.15
        self.i_phd_penalty = 1.2
        self.i_diploma_score = 0.7
        self.i_3year_score = 1.3
        self.i_4year_score = 1.5
        self.i_post_graduate_score = 2.3
        self.i_phd_score = 2.4
        self.j_diploma_penalty = 0.2
        self.j_3year_penalty = 0.4
        self.j_4year_penalty = 0.5
        self.j_post_graduate_penalty = 0.65
        self.j_phd_penalty = 0.75
        self.j_diploma_score = 0.4
        self.j_3year_score = 0.8
        self.j_4year_score = 1
        self.j_post_graduate_score = 1.3
        self.j_phd_score = 1.5
        self.s_diploma_penalty = 0.1
        self.s_3year_penalty = 0.2
        self.s_4year_penalty = 0.25
        self.s_post_graduate_penalty = 0.3
        self.s_phd_penalty = 0.35
        self.s_diploma_score = 0.2
        self.s_3year_score = 0.4
        self.s_4year_score = 0.5
        self.s_post_graduate_score = 0.6
        self.s_phd_score = 0.7
        self.job_level =job_level.lower()
        self.education_years  = education_years. lower()
        self.education_field_name = education_field_name.lower()
        self.education_score = []
    # Function to assign weightage
    def education_weightage(self):
        if self.job_level == "internship":
            if self.education_years  == "diploma":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.i_diploma_penalty)
                else:
                    self.education_score.append(self.i_diploma_score)
            elif self.education_years  == "3 year bachelor":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.i_3year_penalty)
                else:
                    self.education_score.append(self.i_3year_score)
            elif self.education_years  == "4 year bachelor":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.i_4year_penalty)
                else:
                    self.education_score.append(self.i_4year_score)
            elif self.education_years  == "post graduate":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.i_post_graduate_penalty)
                else:
                    self.education_score.append(self.i_post_graduate_score)
            elif self.education_years  == "phd":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.i_phd_penalty)
                else:
                    self.education_score.append(self.i_phd_score)
        elif self.job_level == "junior":
            if self.education_years  == "diploma":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.j_diploma_penalty)
                else:
                    self.education_score.append(self.j_diploma_score)
            elif self.education_years  == "3 year bachelor":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.j_3year_penalty)
                else:
                    self.education_score.append(self.j_3year_score)
            elif self.education_years  == "4 year bachelor":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.j_4year_penalty)
                else:
                    self.education_score.append(self.j_4year_score)
            elif self.education_years  == "post graduate":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.j_post_graduate_penalty)
                else:
                    self.education_score.append(self.j_post_graduate_score)
            elif self.education_years  == "phd":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.j_phd_penalty)
                else:
                    self.education_score.append(self.j_phd_score)
        if self.job_level == "senior":
            if self.education_years  == "diploma":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.s_diploma_penalty)
                else:
                    self.education_score.append(self.s_diploma_score)
            elif self.education_years  == "3 year bachelor":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.s_3year_penalty)
                else:
                    self.education_score.append(self.s_3year_score)
            elif self.education_years  == "4 year bachelor":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.s_4year_penalty)
                else:
                    self.education_score.append(self.s_4year_score)
            elif self.education_years  == "post graduate":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.s_post_graduate_penalty)
                else:
                    self.education_score.append(self.s_post_graduate_score)
            elif self.education_years  == "phd":
                if self.education_field_name not in self.fields:
                    self.education_score.append(self.s_phd_penalty)
                else:
                    self.education_score.append(self.s_phd_score)
        return{
            "education_score" : self.education_score,
        }
    # Function to check relevance
    def education_relevance(self):
        if self.education_field_name.lower() in self.fields:
            return {
                "edu_relevancy": "match found",
            }
        else:
            return {
                "edu_relevancy": "match not found",
            }