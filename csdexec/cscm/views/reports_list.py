from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response  
from django.contrib.auth.decorators import login_required
#from django import forms 

@login_required
def display_complete_report_list(request):
    # if 'report' in request.GET and request.GET['report']:
    #    report = request.GET['report']
    #    pass
    # else:  
    #    # output complete list of reports
    #    pass 
    return render_to_response('main_report_list.html') 
    
