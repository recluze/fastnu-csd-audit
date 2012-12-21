from csip.models import *
from django.contrib import admin 


class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'designation', 'department')
    
    def queryset(self, request):
        qs = super(InstructorProfileAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(InstructorProfile, InstructorProfileAdmin)



class InstructorEducationAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'degree', 'year', 'university', 'institution')
    def queryset(self, request):
        qs = super(InstructorEducationAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorEducationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(InstructorEducation, InstructorEducationAdmin)


#class InstructorPublicationAdmin(admin.ModelAdmin):
#    list_display = ('instructor', 'degree', 'year', 'university', 'institution')

class InstructorPublicationAdmin(admin.ModelAdmin): 
    list_display = ('instructor', 'title', 'journal', 'pub_date', 'pub_type', 'impact_factor')
    def queryset(self, request):
        qs = super(InstructorPublicationAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorPublicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)   
admin.site.register(InstructorPublication, InstructorPublicationAdmin)


class InstructorConsultancyAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(InstructorConsultancyAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorConsultancyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(InstructorConsultancy, InstructorConsultancyAdmin)



class InstructorEventParticipationAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'title', 'type', 'start_date', 'duration')
    def queryset(self, request):
        qs = super(InstructorEventParticipationAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorEventParticipationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(InstructorEventParticpation, InstructorEventParticipationAdmin)



class InstructorEmploymentAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'position', 'organization', 'start_date', 'end_date', 'duration')
    def queryset(self, request):
        qs = super(InstructorEmploymentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorEmploymentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(InstructorEmployment, InstructorEmploymentAdmin)



class InstructorOtherActivityAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(InstructorOtherActivityAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(InstructorOtherActivityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(InstructorOtherActivity, InstructorOtherActivityAdmin)





class StudentThesesAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(StudentThesesAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(StudentThesesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(StudentTheses, StudentThesesAdmin)


