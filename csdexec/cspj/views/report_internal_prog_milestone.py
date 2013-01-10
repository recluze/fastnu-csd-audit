from django.contrib.auth.decorators import login_required 

from cscm.helpers.functions import * 
from cspj.models import * 

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
            evals = StudentProjectMilestoneEvaluation.objects.filter(milestone__milestone_category=milestone_cat).filter(milestone__milestone_deadline=milestone_date).order_by('milestone__project')
            weight = milestone_cat.weight
            
            r = {} 
            
            for eval in evals: 
                student = eval.student
                project = eval.milestone.project
                title = eval.milestone.project.title
                if project not in r: 
                    r[project] = ProjectRecord(title)
                   
                # pr is project record 
                prd = r[project]
                srs = prd.studentrecords
                
                # create new student record if we don't already have it  
                if student not in srs.keys(): 
                    srs[student] = StudentRecord(student.name, 'FYP', weight)

                # sr is student record
                sr = srs[student]
                    
                # incorporate this record into the accumulation of student record
                ec = eval.evaluator_confidence
                if abs(ec - 0) < 0.000001:  ec = 0.000001  # too low confidence. Ignore 
                 
                pd = eval.problem_difficulty if eval.problem_difficulty else 0
                so = eval.solution_strength if eval.solution_strength else 0 
                ex = eval.execution if eval.execution else 0
                ir = eval.issue_resolution if eval.issue_resolution else 0
                pr = eval.presentation  if eval.presentation else 0
                co = eval.comments 
                 
                sr.pd = ((sr.ec * sr.pd) + (ec * pd) ) / (sr.ec + ec)
                sr.so = ( (sr.ec * sr.so) + (ec * so) )/ (sr.ec + ec) 
                sr.ex = ( (sr.ec * sr.ex) + (ec * ex) ) / (sr.ec + ec)
                sr.ir = ( (sr.ec * sr.ir) + (ec * ir) )/ (sr.ec + ec)
                sr.pr = ( (sr.ec * sr.pr) + (ec * pr) )/ (sr.ec + ec)
                prd.co = prd.co + '\n' + co 
                
                
                # update total evaluator confidence 
                sr.ec += ec

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
        

class StudentRecord():
    def __init__(self, studentname, project_type, weight):
        self.tconf = 0
        self.ec = 0 
        self.pd = 0 
        self.so = 0
        self.ex = 0 
        self.ir = 0 
        self.pr = 0 
        
        self.project_type = project_type 
        self.name = studentname
        self.weight = weight 
        
    def total(self):
        if self.project_type == 'FYP':
            total = 0 
            total += (self.pd)
            total += (self.so) 
            total += (self.ex) 
            total += (self.ir) 
            total += (self.pr)
            return total 
        
    def weighted_total(self):
        if self.project_type == 'FYP':
            return self.total() / 35 * self.weight   



class ProjectRecord():
    def __init__(self, projecttitle):
        self.studentrecords = {}
        self.co = '' 
        self.title = projecttitle

    def num_students(self):
        try: 
            n = 0 
            for k, v in self.studentrecords.items():
                n += 1 
        except Exception, e: 
            raise RuntimeError(e)
        return n 
    
