from django.contrib.auth.decorators import login_required 

from cscm.helpers.functions import * 
from cscm.helpers.choices import * 

from cscm.models import Course, CourseOutline 

import datetime 
from datetime import timedelta 

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext

@login_required 
def report_qec_course_catalog(request):
    def get_outline_field(outline, var):
        try: 
            value = getattr(outline, var)
            return value
        except: 
            return '[MISSING]'
    
    def field_or_missing(field):
        if field != '': 
            return field 
        else: 
            return '[MISSING]'
    
    class ReportForm(forms.Form):
        semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
        year = forms.CharField()
        
    c = RequestContext(request)  
    c.update(csrf(request))
    
    if request.method == 'POST':  
        # form submitted 
        form = ReportForm(request.POST)
        form.is_valid()
        try:
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year'] 
            
            courses = Course.objects.\
                        filter(year=year).\
                        filter(semester=semester)
            
            catalog = [] 
            
            for course in courses:
                det = [] 
                 
                try:
                    outline = CourseOutline.objects.filter(course=course)[0] # one-to-one relation
                except Exception, err:
                    outline = ''
                    
                det.append({'Course name': field_or_missing(course.course_name)})  
                det.append({'Course code': course.course_code})
                det.append({'Objectives' : get_outline_field(outline, 'objectives')})                  
                det.append({'Outcomes' : field_or_missing(get_outline_field(outline, 'outcomes'))})
                det.append({'Pre-requisites' : course.pre_reqs})
                det.append({'Text books and references' : get_outline_field(outline, 'text_books')})
                det.append({'Recommended books' : get_outline_field(outline, 'recommended_books')})
                det.append({'Lab projects': course.lab_projects})
                
                catalog.append(det)

            # prepare list of courses [{'Course Name' : course_name, 'Course Code' : course_name }
            #                             , {...}] 
                        
            
        except ValueError, err:
             raise RuntimeError("Invalid values selected in form.")
        
        return render_to_response('qec_course_catalog.html' , {
                'catalog' : catalog,
                }, c)

    
    else:  
        # form not yet submitted ... display it 
        form = ReportForm()
        return render_to_response('qec_course_catalog.html' , {
                'form': form
                }, c)
        

