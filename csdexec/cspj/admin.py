from cscm.models import Instructor 
from cspj.models import StudentProject, StudentProjectLogEntry, Student, StudentProjectMilestone, StudentProjectMilestoneEvaluation, StudentProjectMilestoneCategory
from django.contrib import admin 
from django.forms.models import BaseInlineFormSet
from django.forms import ModelChoiceField, ModelForm, ValidationError

# from django.core.exceptions import DoesNotExist



class StudentProjectLogEntryInline(admin.TabularInline):
    model = StudentProjectLogEntry
    extra = 3
    #formfield_overrides = {
    #    models.CharField: {'widget': TextInput(attrs={'size':'5'})}
    #    models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':30})},
    #}
    
    
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'uid']
    search_fields = ['name']
    
admin.site.register(Student, StudentAdmin)


class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'semester', 'year', 'project_type', 'instructor', 'marks_evaluated', 'active']
    list_editable = ['active']
    list_filter = ['project_type']
    
    inlines = [StudentProjectLogEntryInline]
    filter_horizontal = ('students',)

    save_as = True
    
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
class StudentProjectMilestoneEvaluationForm(ModelForm):
    class Meta: 
        model = StudentProjectMilestoneEvaluation
        

    def clean(self):
        data = self.cleaned_data
        
        try:
            if data.get('evaluator_confidence') > 10 or data.get('evaluator_confidence') < 0: 
                raise ValidationError('Evaluator confidence must be between 0 and 10')
            
            if self.instance.milestone.milestone_category.milestone_type.strip() == 'Presentation':
                 # all fields must be checked
                  
                 # check if we're in FYP 
                 if self.instance.milestone.milestone_category.project_type.strip() == 'FYP':
                     if data.get('problem_difficulty') > 5 or data.get('problem_difficulty') < 0: 
                        raise ValidationError('Problem difficulty must be between 0 and 5 for presentation-type milestones in FYPs')
                     if data.get('solution_strength') > 10 or data.get('solution_strength') < 0: 
                        raise ValidationError('Solution strength must be between 0 and 10 for presentation-type milestones in FYPs')
                     if data.get('execution') > 10 or data.get('execution') < 0: 
                        raise ValidationError('Execution must be between 0 and 10 for presentation-type milestones in FYPs')
                     if data.get('issue_resolution') > 5 or data.get('issue_resolution') < 0: 
                        raise ValidationError('Issue resolution must be between 0 and 5 for presentation-type milestones in FYPs')
                     if data.get('presentation') > 5 or data.get('presentation') < 0: 
                        raise ValidationError('Presentation must be between 0 and 5 for presentation-type milestones in FYPs')
                    
                 # otherwise, we're in Thesis (just check)   
                 if self.instance.milestone.milestone_category.project_type.strip() == 'Thesis':
                     if data.get('problem_difficulty') > 10 or data.get('problem_difficulty') < 0: 
                        raise ValidationError('Problem difficulty must be between 0 and 10 for presentation-type milestones in Theses')
                     if data.get('solution_strength') > 15 or data.get('solution_strength') < 0: 
                        raise ValidationError('Solution strength must be between 0 and 15 for presentation-type milestones in Theses')
                     if data.get('execution') > 10 or data.get('execution') < 0: 
                        raise ValidationError('Execution must be between 0 and 10 for presentation-type milestones in Theses')
                     if data.get('issue_resolution') > 10 or data.get('issue_resolution') < 0: 
                        raise ValidationError('Issue resolution must be between 0 and 10 for presentation-type milestones in Theses')
                     if data.get('presentation') > 5 or data.get('presentation') < 0: 
                        raise ValidationError('Presentation must be between 0 and 5 for presentation-type milestones in Theses')
            
            else: 
                # non-presentation milestone 
                blank_fields = ['problem_difficulty', 'solution_strength', 'issue_resolution', 'presentation']
                for fld in blank_fields:
                    if True: # for both theses and FYPs  
                    # if self.instance.milestone.milestone_category.project_type.strip() == 'FYP':
                        if data.get(fld): 
                            raise ValidationError('Please only enter \'execution\' field for non-Presentation type milestones')
                        
                        
                if True: # for both theses and FYPs
                # if self.instance.milestone.milestone_category.project_type.strip() == 'FYP':
                    milestone_weight = self.instance.milestone.milestone_category.weight
                    if data.get('execution') > milestone_weight or data.get('execution') < 0: 
                        raise ValidationError('Execution must be between 0 and ' + str(milestone_weight) + ' for this milestone type.')
                 
            if self.instance.milestone.milestone_category.milestone_type.strip() != 'Presentation': 
                # TODO: make sure only supervisor can entery non-presentation evaluaitons 
                if self.instance.milestone.project.instructor != data.get('instructor'):
                    raise ValidationError('Only supervisor can enter non-presentation milestone evaluations')
        except StudentProjectMilestone.DoesNotExist: 
            pass 
        
        return self.cleaned_data    

class StudentProjectMilestoneEvaluationInline(admin.TabularInline):
    model = StudentProjectMilestoneEvaluation
    extra = 3
    form = StudentProjectMilestoneEvaluationForm
    
    def queryset(self, request):
        qs = super(StudentProjectMilestoneEvaluationInline, self).queryset(request)
        if request.user.is_superuser:
            return qs 
    
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try: 
            if db_field.name == "instructor" and not request.user.is_superuser:
                kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
                return db_field.formfield(**kwargs)
            elif db_field.name == "instructor":
                return super(StudentProjectMilestoneEvaluationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
            if db_field.name == "student": 
                if request._obj_ is not None:
                   shown_students = request._obj_.project.students
                else: 
                   shown_students = Student.objects.all()
    
                kwargs["queryset"] = shown_students
                return super(StudentProjectMilestoneEvaluationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
            
            return super(StudentProjectMilestoneEvaluationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        except StudentProject.DoesNotExist: 
            raise RuntimeError("Project is not active. Please make the project active before trying to view the report.")
 

    save_as = True  


class StudentProjectMilestoneAdmin(admin.ModelAdmin):     
    list_display = ('project', 'milestone_category', 'milestone_deadline')
    list_filter = ['project']
    list_editable = ['milestone_deadline']
    date_hierarchy = 'milestone_deadline'
    search_fields = ['project__title', 'project__year', 'project__project_type']
    
    inlines = [StudentProjectMilestoneEvaluationInline]
    save_as = True
    
    def queryset(self, request):
        qs = super(StudentProjectMilestoneAdmin, self).queryset(request)
        return qs.filter(project__active=True) 
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):    
        if db_field.name == "project":
            kwargs["queryset"] = StudentProject.active_projects
            return db_field.formfield(**kwargs)
        
        return super(StudentProjectMilestoneAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(StudentProjectMilestoneAdmin, self).get_form(request, obj, **kwargs)
    
    
class StudentProjectMilestoneEvaluationAdmin(admin.ModelAdmin):
    list_display = ['get_project', 'student', 'instructor', 'get_milestone_category']
    list_filter = ['milestone__project__title']
    search_fields = ['milestone__project__title', 'milestone__project__year']
    
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
# admin.site.register(StudentProjectMilestoneEvaluation, StudentProjectMilestoneEvaluationAdmin)

 
class StudentProjectMilestoneCategoryAdmin(admin.ModelAdmin):
    list_display = ['milestone_name', 'weight', 'project_type', 'milestone_type']
    list_filter = ['milestone_name', 'project_type']
    search_fields = ('milestone_name', 'project_type')
    save_as = True 
    
admin.site.register(StudentProjectMilestoneCategory, StudentProjectMilestoneCategoryAdmin)    




