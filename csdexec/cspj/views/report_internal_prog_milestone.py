from django.contrib.auth.decorators import login_required 

from cscm.helpers.functions import * 
from cspj.models import * 
from cspj.views.milestone_results import * 

import datetime 
from datetime import timedelta 

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext

@login_required 
def report_internal_prog_milestone(request):
    
    class QecCourseLogForm(forms.Form):
        # course_name = forms.ChoiceField(choices=TEMP)
        # if request.user.is_superuser: 
        milestone_cat = forms.ModelMultipleChoiceField(queryset=StudentProjectMilestoneCategory.objects.all())
        all_dates = []
        ses = StudentProjectMilestoneEvaluation.objects.all()

        for se in ses: 
            deadline = se.milestone.milestone_deadline
            deadline_tup = (deadline, deadline)
            if deadline_tup not in all_dates: 
                all_dates.append(deadline_tup)
        
        milestone_date = forms.ChoiceField(choices=all_dates)
        
    c = RequestContext(request)  
    c.update(csrf(request))
    
    if request.method == 'POST':  
        # form submitted 
        form = QecCourseLogForm(request.POST)
        form.is_valid()
        try: 
            milestone_cat = form.cleaned_data['milestone_cat']
            milestone_cat = milestone_cat [0]
            milestone_date = form.cleaned_data['milestone_date']
            weight = milestone_cat.weight
            
            evals = StudentProjectMilestoneEvaluation.objects.\
                        filter(milestone__milestone_category=milestone_cat).\
                        filter(milestone__milestone_deadline=milestone_date).\
                        order_by('milestone__project')
                        
            
            # compile results for this milestone only 
            mrc = MilestoneResultsCompiler(weight, milestone_cat)
            for eval in evals: 
                mrc.add_student_eval(eval)
            r = mrc.get_compiled_result()

        except ValueError, err:
             raise RuntimeError("Invalid values selected in form.")
        
        return render_to_response('internal_prog_milestone.html' , {
                'milestone_cat' : milestone_cat,
                'milestone_date' : milestone_date,
                'results' : r,
                'weight' : weight
                }, c)

    
    else:  
        # form not yet submitted ... display it 
        form = QecCourseLogForm()
        return render_to_response('internal_prog_milestone.html' , {
                'form': form
                }, c)
        
