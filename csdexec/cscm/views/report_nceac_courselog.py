from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext

from cscm.models import Course
from cscm.views.report_nceac_courselog_pdf import *
  
#from django import forms 

def report_nceac_courselog(request):
    c = RequestContext(request)  
    c.update(csrf(request))
    
    # if 'course_name' in request.GET and request.GET['course_name']:
    if request.method == 'POST':  
        # form submitted 
        form = NceacCourseLogForm(request.POST)
        form.is_valid()
        course_name = form.cleaned_data['course_name']
        course_name = course_name[0]
        inner_response = report_nceac_courselog_pdf(request, course_name)
        http_response = HttpResponse(inner_response, c)  
        filename = "clf_" + str(course_name.course_code) +  "-" + str(course_name.semester)+ str(course_name.year) + ".pdf"
        http_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
        return http_response  
        
    else:  
        # form not yet submitted ... display it 
        form = NceacCourseLogForm()
        return render_to_response('nceac_courselog.html' , {
                'form': form
                }, c)
         




class NceacCourseLogForm(forms.Form):
    TEMP = (
            (1, "Course 1"),
            (2, "Course 2")
            )
    # course_name = forms.ChoiceField(choices=TEMP)
    course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
    pass
