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
    list_display = ('course_name', 'instructor', 'semester', 'year', 'credits')
    inlines = [CourseOutlineInline, CourseLogEntryInline]
    
admin.site.register(Course, CourseAdmin)


class CourseOutlineAdmin(admin.ModelAdmin):
    # fields = ['instructor', 'course_name', 'credits', 'year']
    # list_display = ('course_name', 'instructor', 'semester', 'year', 'credits')
    inlines = [WeekPlanInline]
    
admin.site.register(CourseOutline, CourseOutlineAdmin)


admin.site.register(CourseLogEntry)

# Course Outline 
