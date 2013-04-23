from django.contrib.auth.decorators import login_required 

import re 

from cscm.helpers.functions import * 
from cscm.helpers.choices import * 

from cscm.models import Course, CourseOutline, WeekPlan, ProgramObjective

import datetime 
from datetime import timedelta 

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext

@login_required 
def report_qec_program_objectives(request):
    def remove_duplicate_courses(courses):
        known_course_names = []
        ret_courses = []  
        for course in courses: 
            if not course.course_name in known_course_names: 
                known_course_names.append(course.course_name )
                ret_courses.append(course)
                
        return ret_courses
    
    
    class ReportForm(forms.Form):
        # semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
        year = forms.CharField()
        
    c = RequestContext(request)  
    c.update(csrf(request))
    
    if request.method == 'POST':  
        form = ReportForm(request.POST)
        form.is_valid()

        #try:
        year  = form.cleaned_data['year']
        #except Exception: 
        #    raise RuntimeError("Invalid values in form")
        # get list of courses 
        courses = Course.objects.all().filter(year=year).order_by('-year').order_by('-semester').order_by('-course_name');
        courses = remove_duplicate_courses(courses)
        
        objs_all = ProgramObjective.objects.all().order_by('objectiveOrder')
        objs = []
        for ob in objs_all:
            objs.append(ob)
        
                 
        cdict = {}
        missed_courses = []
        
        for course in courses:
            try:
                outline = CourseOutline.objects.filter(course=course)[0] # one-to-one relation
                
                this_course = []
                this_objs = outline.corresponding_program_objectives.all()
                
                for ob in objs_all:
                    if ob in this_objs:  
                        this_course.append('&#10003;') 
                    else: 
                        this_course.append('-')  
                
                cdict[course] = this_course
                
            except IndexError, err:
                missed_courses.append(course)
            
        num_objectives = len(objs) 
        return render_to_response('qec_program_objectives.html' , {
                'cdict' : cdict,
                'missed_courses' : missed_courses,                            
                'all_objectives' : objs,
                'num_objectives': num_objectives, 
                }, c)

    
    else:  
        #form not yet submitted ... display it 
        form = ReportForm()
        
       
                
            
                    
            # cdict[c.lab_hours]  = c.credits 
        
        return render_to_response('qec_program_objectives.html' , {
                'form': form,
                }, c)
        

