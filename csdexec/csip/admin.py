from csip.models import *
from django.contrib import admin 


class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'designation', 'department')
    
admin.site.register(InstructorProfile, InstructorProfileAdmin)



class InstructorEducationAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'degree', 'year', 'university', 'institution')
    
admin.site.register(InstructorEducation, InstructorEducationAdmin)


#class InstructorPublicationAdmin(admin.ModelAdmin):
#    list_display = ('instructor', 'degree', 'year', 'university', 'institution')
    
admin.site.register(InstructorPublication)

admin.site.register(InstructorConsultancy)



class InstructorEventParticpationAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'title', 'type', 'start_date', 'duration')
admin.site.register(InstructorEventParticpation, InstructorEventParticpationAdmin)



class InstructorEmploymentAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'position', 'organization', 'start_date', 'end_date', 'duration')
admin.site.register(InstructorEmployment, InstructorEmploymentAdmin)
