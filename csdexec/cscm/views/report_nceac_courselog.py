# required for PDF generation 
from __future__ import unicode_literals

from io import BytesIO

from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, LongTable, TableStyle, PageTemplate
from reportlab.platypus.flowables import PageBreak 
from reportlab.lib import colors

from django.http import HttpResponse 

from cscm.views.FooterDocTemplate import FooterDocTemplate

import datetime 
from cscm.views.nceac_styles import *
from cscm.helpers.loadconfigs import get_config
from cscm.helpers.functions import * 

# models 

from cscm.models import CourseLogEntry
from cscm.models import Course

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext
  
from django.contrib.auth.decorators import login_required 
# =============================================================================================
@login_required 
def report_nceac_courselog(request):
    class NceacCourseLogForm(forms.Form):
        TEMP = (
                (1, "Course 1"),
                (2, "Course 2")
                )
        if request.user.is_superuser: 
            course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
        else: 
            course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.filter(instructor__owner=request.user))
        
    
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
        filename = "clf_" + str(course_name.course_code) + "-" + str(course_name.semester) + str(course_name.year) + ".pdf"
        http_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
        return http_response  
        
    else:  

        # form not yet submitted ... display it 
        form = NceacCourseLogForm()
        return render_to_response('nceac_courselog.html' , {
                'form': form
                }, c)
         





# ============= PDF GEN 

def report_nceac_courselog_pdf(request, course_name):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefile.pdf"' 
    
    buffer = BytesIO() 
    
    org = Nceac()
    styleN, styleB, styleH, styleSmaller = org.getTextStyles()
    doc = FooterDocTemplate(buffer, pagesize=A4)
    frame = org.getFrame(doc)
    template = PageTemplate(id='test', frames=frame, onPage=org.get_header_footer(doccode="NCEAC.DOC.008"))
    doc.addPageTemplates([template])
    
    # Our main content holder 
    
    elements = []
    
    # title page 
    inst_name_head = Paragraph('Name of the Institution', styleB)
    inst_name = Paragraph(get_config('inst_name'), styleN)
    dept_name_head = Paragraph('Department', styleB)
    dept_name = Paragraph(get_config('dept_name'), styleN)
    
    metainfo_tablestyle = [
                    # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('LINEBELOW', (1, 0), (1, -1), 0.25, colors.black),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]
    metainfo = [[inst_name_head, inst_name], [dept_name_head, dept_name]]
    t1 = LongTable(metainfo, colWidths=[3 * cm, 12 * cm])
    t1.setStyle(TableStyle(metainfo_tablestyle))
    elements.append(t1)
    
    elements.append(PageBreak())

    
    # =================== TABLE DATA 
    datas = []
    headDate = Paragraph('Date', styleB)
    headDuration = Paragraph('Duration', styleB)
    headTopics = Paragraph('Topics Covered', styleB)
    headEval = Paragraph('Evaluation Instruments Used', styleB)
    headSign = Paragraph('Signature', styleB)
    emptypara = Paragraph(' ', styleN)
    
    datas = [[headDate, headDuration, headTopics, headEval, headSign]]
    
    # courselogentry_data = CourseLogEntry.objects.all()
    courselogentry_data = course_name.courselogentry_set.all()
    

    # for x in range(1, 50):
    #    datas.append(
    #        [x, x + 1, x + 2, x + 4, x + 5]
    #    )
    for i in courselogentry_data: 
        # entered_logs += 1
        l_date = Paragraph(str(i.lecture_date.strftime("%d-%m, %Y")), styleSmaller)
        l_duration = Paragraph(str(i.duration), styleSmaller)
        l_topics_covered = Paragraph(clean_string(i.topics_covered), styleSmaller)
        l_eval = Paragraph(clean_string(i.evaluation_instruments), styleSmaller)
        
        datas.append([l_date, l_duration, l_topics_covered, l_eval, emptypara])
    
    #for i in range(entered_logs, 16): 
    #    data.append([[emptypara, emptypara, emptypara, emptypara, emptypara]])
        
    t = LongTable(datas, colWidths=[1.5 * cm, 2 * cm, 8 * cm, 3 * cm, 3 * cm], repeatRows=1)
    
    t.setStyle(TableStyle(org.getTableStyle()))
    elements.append(t)
    doc.build(elements)
    
    
    # OUTPUT FILE 
    # doc.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
