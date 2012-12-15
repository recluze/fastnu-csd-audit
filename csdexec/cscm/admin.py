from cscm.models import Instructor, Course, CourseOutline, WeekPlan, CourseLogEntry
from django.contrib import admin 

# Inlines 
class WeekPlanInline(admin.TabularInline):
    model = WeekPlan
    extra = 3


class CourseLogEntryInline(admin.TabularInline):
    model = CourseLogEntry
    extra = 3
    
    
class CourseOutlineInline(admin.StackedInline):
    model = CourseOutline
    inlines = [WeekPlanInline] 
    
# Instructor
class InstructorAdmin(admin.ModelAdmin):
    # fields = ['name', 'designation']
    list_display = ('name', 'designation')
    
    
admin.site.register(Instructor, InstructorAdmin)


# Course 
class CourseAdmin(admin.ModelAdmin):
    # fields = ['instructor', 'course_name', 'credits', 'year']
    fieldsets = [
                 ('Couse Basics', {'fields' : (('course_code', 'course_name', 'instructor'),
                                                ('credits', 'year', 'batch', 'semester', 'course_type'),
                                               ),}),
                  ('Couse Policies', {'fields' : ('grade_distribution', 'pre_reqs', 'course_url', 'lab_projects', 'prog_assignments'),}),
                  ('Class Time Spent', {'fields' : ((('class_time_spent_theory', 'class_time_spent_analysis')), (('class_time_spent_design', 'class_time_spent_ethics')),)}),
                  ('Oral and Written Communication', {'fields' : ((('communciation_details_num_reports', 'communciation_details_pages')), (('communciation_details_num_pres', 'communciation_details_num_mins')),)}),
                ]
    list_display = ('course_name', 'instructor', 'semester', 'year', 'credits')
    list_filter = ['instructor__name', 'year']
    inlines = [CourseOutlineInline, CourseLogEntryInline]
    
admin.site.register(Course, CourseAdmin)


class CourseOutlineAdmin(admin.ModelAdmin):
    # fields = ['instructor', 'course_name', 'credits', 'year']
    list_filter = ['course__course_name', 'course__year']
    inlines = [WeekPlanInline]
    
admin.site.register(CourseOutline, CourseOutlineAdmin)


class CourseLogEntryAdmin(admin.ModelAdmin): 
    list_display = ['lecture_no', 'course']
    list_filter = ['course__course_name', 'lecture_date']
    date_hierarchy = 'lecture_date'

admin.site.register(CourseLogEntry, CourseLogEntryAdmin)

# Course Outline 
