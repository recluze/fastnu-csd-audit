from django.http import HttpResponse
from django.shortcuts import render_to_response  
#from django import forms 

def display_complete_report_list(request):
    # if 'report' in request.GET and request.GET['report']:
    #    report = request.GET['report']
    #    pass
    # else:  
    #    # output complete list of reports
    #    pass 
    return render_to_response('main_report_list.html') 
    
