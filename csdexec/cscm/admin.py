from cscm.models import Instructor, Course, CourseOutline, WeekPlan, CourseLogEntry
from django.contrib import admin 
from django.db import models
from django import forms 
from django.forms.widgets import TextInput, Textarea


# Inlines 
class WeekPlanInline(admin.TabularInline):
    model = WeekPlan
    extra = 3


class CourseLogEntryInline(admin.TabularInline):
    model = CourseLogEntry
    extra = 3
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'5'})}
    #    models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':30})},
    }
    
class CourseOutlineInline(admin.StackedInline):
    model = CourseOutline
    inlines = [WeekPlanInline] 
    
# Instructor
class InstructorAdmin(admin.ModelAdmin):
    # fields = ['name', 'designation', 'age', 'joining_date']
    list_display = ('name', 'designation')    
    
admin.site.register(Instructor, InstructorAdmin)


# Course 
class CourseAdmin(admin.ModelAdmin):
    # fields = ['instructor', 'course_name', 'credits', 'year']
    fieldsets = [
                 ('Couse Basics', {'fields' : (('course_code', 'course_name'),
                                                ('credits', 'year', 'batch'), ('semester', 'course_type', 'instructor'),
                                               ), }),
                  ('Couse Policies', {'fields' : ('grade_distribution', 'pre_reqs', 'course_url', 'lab_projects', 'prog_assignments'), }),
                  ('Class Time Spent', {'fields' : ((('class_time_spent_theory', 'class_time_spent_analysis')), (('class_time_spent_design', 'class_time_spent_ethics')),)}),
                  ('Oral and Written Communication', {'fields' : ((('communciation_details_num_reports', 'communciation_details_pages')), (('communciation_details_num_pres', 'communciation_details_num_mins')),)}),
                ]
    list_display = ('course_name', 'instructor', 'semester', 'year', 'credits')
    list_filter = ['instructor__name', 'year']
    
    save_as = True 
    inlines = [CourseOutlineInline, CourseLogEntryInline]
    
    # row-level permissions for courses. 
    # source: http://www.ibm.com/developerworks/opensource/library/os-django-admin/index.html
    def queryset(self, request):
        qs = super(CourseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor" and not request.user.is_superuser:
            kwargs["queryset"] = Instructor.objects.filter(owner=request.user)
            return db_field.formfield(**kwargs)
        return super(CourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    formfield_overrides = {
        # models.CharField: {'widget': TextInput(attrs={'size':'10'})}
        # models.TextField: {'widget': Textarea(attrs={'rows':20, 'cols':40})},
    }
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CourseAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'course_url':
          field.widget.attrs['size'] = '100'
        return field

admin.site.register(Course, CourseAdmin)


class CourseOutlineAdmin(admin.ModelAdmin):
    # fields = ['instructor', 'course_name', 'credits', 'year']
    list_filter = ['course__course_name', 'course__year']
    inlines = [WeekPlanInline]
    save_as = True 
    
    def queryset(self, request):
        qs = super(CourseOutlineAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(course__instructor__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(instructor__owner=request.user)
            return db_field.formfield(**kwargs)
        return super(CourseOutlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(CourseOutline, CourseOutlineAdmin)


class CourseLogEntryAdmin(admin.ModelAdmin): 
    list_display = ['lecture_no', 'week_no', 'lecture_date', 'course']
    list_filter = ['course__course_name', 'lecture_date']
    date_hierarchy = 'lecture_date'
     
    save_as = True 
    
    def queryset(self, request):
        qs = super(CourseLogEntryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs 
        
        # get instructor's "owner" 
        return qs.filter(course__instructor__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(instructor__owner=request.user)
            return db_field.formfield(**kwargs)
        return super(CourseLogEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CourseLogEntry, CourseLogEntryAdmin)

# Course Outline 
