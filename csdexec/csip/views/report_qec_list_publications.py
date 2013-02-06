from django.contrib.auth.decorators import login_required 

from cscm.helpers.functions import * 
from cscm.helpers.choices import * 

from cscm.models import Course, CourseOutline 
from csip.models import InstructorPublication

import datetime 
from datetime import timedelta
import calendar  

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext

@login_required 
def report_qec_list_publications(request):
    class ReportForm(forms.Form):
        # semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
        year = forms.CharField()
        
    c = RequestContext(request)  
    c.update(csrf(request))
    
    if request.method == 'POST':  
        # form submitted 
        form = ReportForm(request.POST)
        form.is_valid()
        try:
            try: 
                year = form.cleaned_data['year']
                from_date = datetime.date(int(year), 1, 1)
                to_date = datetime.date(int(year), 12, 31)
                
                pubs = InstructorPublication.objects.\
                        filter(pub_date__gt=from_date).\
                        filter(pub_date__lt=to_date)
            except AttributeError: 
                
                pubs = InstructorPublication.objects.all().order_by('-pub_date')
            
            publist = [] 
            
            for pub in pubs:               
                publist.append(pub.get_citation(html=True))

            # prepare list of courses [{'Course Name' : course_name, 'Course Code' : course_name }
            #                             , {...}] 
                        
            
        except ValueError, err:
             raise RuntimeError("Invalid values selected in form.")
        
        return render_to_response('qec_list_publications.html' , {
                'pubs' : publist,
                }, c)

    
    else:  
        # form not yet submitted ... display it 
        form = ReportForm()
        return render_to_response('qec_list_publications.html' , {
                'form': form
                }, c)
        

