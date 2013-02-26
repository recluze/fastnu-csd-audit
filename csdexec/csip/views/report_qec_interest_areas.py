import re
from tl.rename.case import transform_sentence_case


from django.contrib.auth.decorators import login_required 

from cscm.helpers.functions import * 
from cscm.helpers.choices import * 

from csip.models import InstructorProfile

import datetime 
from datetime import timedelta 

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext

@login_required 
def report_qec_interest_areas(request):    
    
#    class ReportForm(forms.Form):
#        semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
#        year = forms.CharField()
#        
#    c = RequestContext(request)  
#    c.update(csrf(request))
    
        
    all_areas = {}
    inst_areas = []

    instructors = InstructorProfile.objects.all()

    
    for i in instructors: 
         areas = i.areas_of_interest
         inst_areas.append(['<b>' + unicode(i) + '</b> (' + i.designation + '): ', areas.strip().replace('\n', '; ')])
         
         areas = re.split("\n", areas)
         
         for a in areas:
             if a.upper() != a:  # leave all caps alone 
                a = a.strip().lower()
             if a == '': continue 
             
             try: 
                 all_areas[a] = all_areas[a] + 1
             except: 
                 all_areas[a] = 1


    areas = {}
    for area, count in all_areas.items():
        if area.upper() != area: # leave all caps alone 
            area = transform_sentence_case([area])[0]
        areas[area] = count
        
    


    # prepare list of courses [{'Course Name' : course_name, 'Course Code' : course_name }
    #                             , {...}] 
                
    return render_to_response('qec_interest_areas.html' , {
        'areas' : areas,
        'inst_areas' : inst_areas,
        })


