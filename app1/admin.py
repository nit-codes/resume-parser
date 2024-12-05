from django.contrib import admin
from .models import Entity


class EntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'persons', 'phone_numbers', 'emails', 'skills', 'designations','organizations','dates','educations','institutes','date_of_birth')
    search_fields = ('persons',)
    
admin.site.register(Entity, EntityAdmin)
