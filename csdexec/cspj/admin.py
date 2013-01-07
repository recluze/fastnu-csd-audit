from cscm.models import Instructor 
from cspj.models import StudentProject, StudentProjectLogEntry, Student, StudentProjectMilestone, StudentProjectMilestoneEvaluation, StudentProjectMilestoneCategory
from django.contrib import admin 
from django.forms.models import BaseInlineFormSet
from django.forms import ModelChoiceField



class StudentProjectLogEntryInline(admin.TabularInline):
    model = StudentProjectLogEntry
    extra = 3
    #formfield_overrides = {
    #    models.CharField: {'widget': TextInput(attrs={'size':'5'})}
    #    models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':30})},
    #}
    
    
    
#class StudentAdmin(admin.ModelAdmin):
#    pass 
    
admin.site.register(Student)


class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'semester', 'year', 'project_type', 'instructor']
    list_filter = ['project_type']
    
    inlines = [StudentProjectLogEntryInline]
    filter_horizontal = ('students',)

    
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



# INDIVIDUAL EVALUATIONS 
class StudentProjectMilestoneEvaluationInlineFormset(BaseInlineFormSet):
#    def add_fields(self, form, index):
#        super(StudentProjectMilestoneEvaluationInlineFormset, self).add_fields(form, index)
#        students = Student.objects.none()
#        if form.instance:
#            try:   
#                milestone = form.instance.milestone
#            except StudentProjectMilestone.DoesNotExist:
#                pass 
#            else: 
#               students = milestone.project.students
#        form.fields['student'].label = 'Student'
#        form.fields['student'].queryset = students
    pass

class StudentProjectMilestoneEvaluationInline(admin.TabularInline):
    model = StudentProjectMilestoneEvaluation
    # formset = StudentProjectMilestoneEvaluationInlineFormset
    extra = 3
    
    def queryset(self, request):
        qs = super(StudentProjectMilestoneEvaluationInline, self).queryset(request)
        if request.user.is_superuser:
            return qs 
    
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        elif db_field.name == "instructor":
            return super(StudentProjectMilestoneEvaluationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
        if db_field.name == "student": 
            if request._obj_ is not None:
               shown_students = request._obj_.project.students  

            kwargs["queryset"] = shown_students
            return super(StudentProjectMilestoneEvaluationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
        return super(StudentProjectMilestoneEvaluationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_object(self, request, model):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id = int(object_id)
        except ValueError:
            return None
        ret_obj = model.objects.get(pk=object_id)
        return ret_obj
    
    save_as = True  


class StudentProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ('project', 'milestone_category', 'milestone_deadline')
    
    inlines = [StudentProjectMilestoneEvaluationInline]
    save_as = True
    
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(StudentProjectMilestoneAdmin, self).get_form(request, obj, **kwargs)
    
    
class StudentProjectMilestoneEvaluationAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        qs = super(StudentProjectMilestoneEvaluationAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
    
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(StudentProjectMilestoneEvaluationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    save_as = True  
    
admin.site.register(StudentProjectMilestone, StudentProjectMilestoneAdmin)    
admin.site.register(StudentProjectMilestoneEvaluation, StudentProjectMilestoneEvaluationAdmin) 
admin.site.register(StudentProjectMilestoneCategory)    




