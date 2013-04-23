from django.contrib.auth.decorators import login_required 

import re 

from cscm.helpers.functions import * 
from cscm.helpers.choices import * 

from cscm.models import Course, CourseOutline, WeekPlan

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
        
    def get_course_structure(c):
        try: 
            # weeks = outline.week_plan_set
            lab_hours = c.lab_hours 
            credits = c.credits
            theory_hours = credits - lab_hours 
            return 'Theory: ' + str(theory_hours) + '  / Lab: ' + str(lab_hours)
        #    value = getattr(outline, var)
        #    return value
        except: 
            return '[MISSING]'
        
    def get_outline_week_plan(co):
        formatted_outline = ""
        # credits = c.credits
        try: 
            wp = WeekPlan.objects.filter(course_outline=co)
            for w in wp: 
                # formatted_outline += "<b>Week No. " + str(w.week_no) + " - (" + str(credits) + " hours) </b><br />"
                # this_plan = re.sub('\<[^<]+?\>', '', w.topics.strip('&lt;br /&gt;'))
                this_plan = w.topics
                formatted_outline += "    " + clean_string(this_plan)
                
        except ValueError: 
            formatted_outline = '[MISSING]' 
        
        return formatted_outline
    
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
                det.append({'Course Structure': get_course_structure(course)})
                det.append({'Credit hours': field_or_missing(course.credits)})
                det.append({'Objectives' : get_outline_field(outline, 'objectives')})                  
                # det.append({'Outcomes' : field_or_missing(get_outline_field(outline, 'outcomes'))})
                det.append({'Pre-requisites' : field_or_missing(course.pre_reqs)})
                det.append({'Text books and references' : field_or_missing(get_outline_field(outline, 'text_books'))})
                det.append({'Recommended books' : field_or_missing(get_outline_field(outline, 'recommended_books'))})
                det.append({'Lab projects': field_or_missing(course.lab_projects)})
                det.append({'Weekly Plan' : get_outline_week_plan(outline).strip('&lt;br /&gt;')})
                
                catalog.append(det)

            # prepare list of courses [{'Course Name' : course_name, 'Course Code' : course_name }
            #                             , {...}] 
                        
            
        #except ValueError, err:
        except RuntimeWarning:
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
        

