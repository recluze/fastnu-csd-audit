from cscm.models import Instructor 
from cspj.models import StudentProject, StudentProjectLogEntry
from django.contrib import admin 



class StudentProjectLogEntryInline(admin.TabularInline):
    model = StudentProjectLogEntry
    extra = 3
    #formfield_overrides = {
    #    models.CharField: {'widget': TextInput(attrs={'size':'5'})}
    #    models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':30})},
    #}
    
    
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'semester', 'year', 'instructor']
    inlines = [StudentProjectLogEntryInline]
    
    def queryset(self, request):
        qs = super(StudentProjectAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(StudentProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(StudentProject, StudentProjectAdmin)

    
    
class StudentProjectLogEntryAdmin(admin.ModelAdmin):
    list_display = ['session_no', 'session_date', 'project']
        
    def queryset(self, request):
        qs = super(StudentProjectLogEntryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(project__instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(project__owner=request.user)
            return db_field.formfield(**kwargs)
        return super(StudentProjectLogEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(StudentProjectLogEntry, StudentProjectLogEntryAdmin)
