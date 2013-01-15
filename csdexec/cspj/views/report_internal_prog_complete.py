from django.contrib.auth.decorators import login_required 

from cscm.helpers.functions import * 
from cscm.helpers.choices import * 
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
def report_internal_prog_complete(request):
    
    class ReportForm(forms.Form):
        type = forms.ChoiceField(choices=STUDENT_PROJECT_TYPES)
        semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
        year = forms.CharField()
        
    c = RequestContext(request)  
    c.update(csrf(request))
    
    if request.method == 'POST':  
        # form submitted 
        form = ReportForm(request.POST)
        form.is_valid()
        try:
            type = form.cleaned_data['type']
            semester = form.cleaned_data['semester']
            year = form.cleaned_data['year'] 
            
            projects = StudentProject.objects.\
                        filter(year=year).\
                        filter(project_type=type).\
                        filter(semester=semester)
                        
            res_title = type + ' - ' + semester + ' (' + str(year) + ')'
                        
            # compile results for these projects only
            results = {}
            all_milestones = []
            
            for project in projects:
                project_result = {} 
                # get all milestones for this project
                milestones = StudentProjectMilestone.objects.\
                                filter(project=project).order_by('milestone_deadline')
                
                for milestone in milestones:
                    milestone_cat = milestone.milestone_category
                    weight = milestone_cat.weight
                    milestone_date = milestone.milestone_deadline 
                    milestone_name = milestone_cat.milestone_name
                    
                    if milestone_name not in all_milestones: 
                        all_milestones.append(milestone_name)  
                    
                    evals = StudentProjectMilestoneEvaluation.objects.\
                            filter(milestone=milestone)
                             
                    mrc = MilestoneResultsCompiler(weight, milestone_cat)
                    for eval in evals: 
                        mrc.add_student_eval(eval)
                        
                    # TODO: these need to go for this particular milestone for this project. Not to total!
                    compiled_result = mrc.get_compiled_result()[project]
                    project_result[milestone_name] = compiled_result
                results[project] = project_result   
            
            # loop over all_milestones and collect all student results for each milestone for all projects
            student_res = {}
            student_projects = {}
            all_students = [] 
            for p, pd in results.items():
                for m, project_results in pd.items(): 
                    for s, s_res in project_results.studentrecords.items():
                        # find results for each student in a particular
                        if s not in student_res.keys(): 
                            student_res[s] = {}
                        
                        compiled_std_res = student_res[s]
                        compiled_std_res[m] = s_res.weighted_total()
                        
                        student_projects[s] = p.title
                        
            # let's create a list based on student_res and all_milestones 
            result_record = []
            # add first row as student_name, [all milestones]  
            
            # now add all students 
            last_title = ''
            for s in student_res.keys(): 
                this_res = []
                this_title = student_projects[s]

                if this_title == last_title: 
                    this_title = ' - '
                    
                last_title = this_title 
                
                this_res.append(this_title)
                this_res.append(s)
                last_project = str(s)
                this_std_total = 0 
                for m in all_milestones: 
                    # get student's result for THIS milestone
                    try:  
                        this_milestone_res = "%.2f" % student_res[s][m]
                        this_std_total += student_res[s][m]
                    except KeyError: 
                        this_milestone_res = '-'
                    this_res.append(this_milestone_res)
            
                # let's add this row to cumulative record
                this_res.append("%.2f" % this_std_total)  
                result_record.append(this_res)
                        
            
        except ValueError, err:
             raise RuntimeError("Invalid values selected in form.")
        
        return render_to_response('internal_prog_complete.html' , {
                'results' : result_record,
                'milestones' : all_milestones,
                'res_title' : res_title 
                }, c)

    
    else:  
        # form not yet submitted ... display it 
        form = ReportForm()
        return render_to_response('internal_prog_complete.html' , {
                'form': form
                }, c)
        
