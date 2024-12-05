from django.db import models

class Entity(models.Model):
    persons = models.JSONField(default=list)  # Store list of persons (names)
    phone_numbers = models.JSONField(default=list)  # Store phone numbers
    emails = models.JSONField(default=list)  # Store emails
    skills = models.JSONField(default=list)  # Store skills
    designations = models.JSONField(default=list)  # Store job titles
    organizations = models.JSONField(default=list)  # Store organizations
    dates = models.JSONField(default=list)  # Store various dates
    educations = models.JSONField(default=list)  # Store education qualifications
    institutes = models.JSONField(default=list)  # Store institutions
    date_of_birth = models.JSONField(default=list)  # Store dates of birth

    def __str__(self):
        return self.persons[0]
    
    
# Identified Entities:
# PERSON: Name of the individual 
# PHONE_NUMBER: Contact number 
# EMAIL: Email address 
# SKILL: List of skills 
# DESIGNATION: Job title 
# ORG: Organization 
# DATE: Various dates for experience and education 
# EDUCATION: Academic qualification 
# INSTITUTE: Institution name 
# DATE_OF_BIRTH: Date of birth