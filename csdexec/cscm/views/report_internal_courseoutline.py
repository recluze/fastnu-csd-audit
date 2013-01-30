# required for PDF generation 
from __future__ import unicode_literals

from io import BytesIO

from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, LongTable, TableStyle, PageTemplate, Image, Spacer
from reportlab.platypus.flowables import PageBreak 
from reportlab.lib import colors

from django.http import HttpResponse 

from cscm.views.FooterDocTemplate import FooterDocTemplate

import datetime 
from internal_styles import *
from cscm.helpers.loadconfigs import get_config
from cscm.helpers.functions import * 

# models 
from cscm.models import CourseLogEntry
from cscm.models import Course, CourseOutline, WeekPlan

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext
  
from django.contrib.auth.decorators import login_required 
# =============================================================================================

@login_required
def report_internal_courseoutline(request):
    class CourseSelectionForm(forms.Form):
        TEMP = (
                (1, "Course 1"),
                (2, "Course 2")
                )
        # course_name = forms.ChoiceField(choices=TEMP)
        if request.user.is_superuser: 
            course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
        else: 
            course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.filter(instructor__owner=request.user))
            
            
    c = RequestContext(request)  
    c.update(csrf(request))
    
    # if 'course_name' in request.GET and request.GET['course_name']:
    if request.method == 'POST':  
        # form submitted 
        form = CourseSelectionForm(request.POST)
        form.is_valid()
        course_name = form.cleaned_data['course_name']
        course_name = course_name[0]
        inner_response = report_internal_courseoutline_pdf(request, course_name)
        http_response = HttpResponse(inner_response, c)  
        filename = str(course_name.course_code) + "-" + str(course_name.semester) + str(course_name.year) + "-Outline.pdf"
        http_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
        return http_response  
        
    else:  

        # form not yet submitted ... display it 
        form = CourseSelectionForm()
        return render_to_response('internal_courseoutline.html' , {
                'form': form
                }, c)
         

    




# ============= PDF GEN 

def report_internal_courseoutline_pdf(request, course_name):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefile.pdf"' 
    
    buffer = BytesIO() 
    
    org = Internal()
    styleN, styleB, styleH, styleSmaller = org.getTextStyles()
    doc = FooterDocTemplate(buffer, pagesize=A4)
    frame = org.getFrame(doc)
    template = PageTemplate(id='test', frames=frame, onPage=org.get_header_footer(doccode="", pagesize=A4))
    doc.addPageTemplates([template])
    width, height = A4
    frame_width = width - ((doc.leftMargin - 20) * 2)
    
    logo_filename = os.path.join(os.path.dirname(__file__), 'images', get_config('logo_filename'))


    # Our main content holder 
    
    elements = []

    inst_name = Paragraph(get_config('inst_name'), styleH)
    dept_name = Paragraph(get_config('dept_name') + ", " + get_config('campus_name'), styleB)
    report_title = Paragraph('Course Outline', styleB)
    semester = Paragraph("(" + str(course_name.semester) + " " + str(course_name.year) + ")", styleB)
    logobox = Image(logo_filename, 100, 110)
    
    metainfo = [[logobox, inst_name],
                ['', dept_name],
                ['', report_title],
                ['', semester],
                ]
    metainfo_tablestyle = [('SPAN', (0, 0), (0, -1))]
    t1 = LongTable(metainfo, colWidths=[5 * cm, 14 * cm])
    t1.setStyle(TableStyle(metainfo_tablestyle))
    elements.append(t1)

    
    # title page 
#    inst_name_head = Paragraph('INSTITUTION', styleB)
#    inst_name = Paragraph(get_config('inst_name'), styleN)
#    dept_name_head = Paragraph('PROGRAM(S) TO BE EVALUATED', styleB)
#    dept_name = Paragraph("BS (CS)", styleN)
#    
#    metainfo_tablestyle = [
#                    # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#                    ('LINEBELOW', (1, 0), (1, -1), 0.25, colors.black),
#                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
#                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#                    ]
#    metainfo = [[inst_name_head, inst_name], [dept_name_head, dept_name]]
#    t1 = LongTable(metainfo, colWidths=[3 * cm, frame_width - (3 * cm)])
#    t1.setStyle(TableStyle(metainfo_tablestyle))
#    elements.append(t1)
    
    elements.append(Spacer(1, 0.5 * cm))
#    elements.append(Paragraph('A. COURSE DESCRIPTION', styleH))
#    elements.append(Paragraph('(Fill out the following table for each course in your computer science curriculum. A filled out form should not be more than 2-3 pages.', styleN))
#    elements.append(Spacer(1, 0.5 * cm))


    # =================== TABLE DATA 
    c = course_name 
    try:
        co = CourseOutline.objects.filter(course=c)[0] # one-to-one relation
    except Exception, err:
        raise RuntimeError("Course outlines not defined for " + str(course_name)) 

    datas = []
    # topics_covered_details = get_formatted_course_outline(c, co)
    course_info = [
                   ['<b>Course Code</b>' , c.course_code] ,
                   ['<b>Course Title</b>' , c.course_name],
                   ['<b>Prerequisites by Course(s) and Topics</b>', clean_string(c.pre_reqs, False)],
                   ['<b>Assessment Instruments with Weights</b> (homework, quizzes, midterms, final, programming assignments, lab work etc.)', clean_string(c.grade_distribution, False)],
                   ['<b>Course Coordinator</b>' , c.instructor.name],
                   ['<b>Course Objectives</b>' , clean_string(co.objectives, False)],
                   ['<b>Course Outcomes</b>' , clean_string(co.outcomes, False)],
                   ['<b>URL</b> (if any)' , c.course_url, styleSmaller],
                   ['<b>Textbook</b> (or laboratory manual for laboratory courses)' , clean_string(co.text_books, False)],
                   ['<b>Reference Material</b>' , clean_string(co.recommended_books, False)],
                   ['<b>Course Policies</b>' , clean_string(co.course_policies)],
                   ['<b>Other Information</b>' , clean_string(co.other_information)],
                   # ['<b>Topics Covered in the Course with Number of lectures on Each Topic</b>(assume 15 week instruction and one-hour lectures)', topics_covered_details],
                   # ['<b>Laboratory Projects/Experiments Done in the Course</b>', c.lab_projects],
                   # ['<b>Programming Assignments Done in the Course</b>', c.prog_assignments],
                ]

    for k in course_info: 
        headpara = Paragraph(k[0], styleN)
        if len(k) > 2 : 
            use_style = k[2]
        else: 
            use_style = styleN 
            
        datas.append([headpara , Paragraph(k[1] if k[1] != '' else '-', use_style)])

    t = LongTable(datas, colWidths=[5 * cm, 12 * cm])
    t.setStyle(org.getTableStyle())
    elements.append(t)
         
    # topics covered in the course
    credits = c.credits
     
    try :
        datas = [[Paragraph('<b>Topics Covered in the Course with Number of lectures on Each Topic</b>', styleN),
                  Paragraph('Week No. (Duration)', styleB),
                  Paragraph('Topics', styleB),
                  ]]
         
        wp = WeekPlan.objects.filter(course_outline=co)
        for w in wp: 
            datas.append(['', Paragraph(unicode(w.week_no) + ' (' + unicode(credits) + ' hrs)', styleB), Paragraph(clean_string(unicode(w.topics)), styleN)])
     
             
        metainfo_tablestyle_topics = [
                        ('INNERGRID', (1, 0), (2, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (0, -1), 0.25, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        # ('SPAN', (0, 0), (0, 3))
                        ]
        # t.setStyle(TableStyle(metainfo_tablestyle_topics))
        t = LongTable(datas, colWidths=[5 * cm, 2 * cm, 10 * cm])
        
        t.setStyle(metainfo_tablestyle_topics)
        elements.append(t)
    except Exception: 
        raise RuntimeError("No Topics Found in the list.")


    datas = []
    # topics_covered_details = get_formatted_course_outline(c, co)
    course_info = [
                   ['<b>Laboratory Projects/Experiments Done in the Course</b>', clean_string(c.lab_projects)],
                   ['<b>Programming Assignments Done in the Course</b>', clean_string(c.prog_assignments)],
                ]

    for k in course_info: 
        headpara = Paragraph(k[0], styleN)
        datas.append([headpara , Paragraph(k[1], styleN)])

    t = LongTable(datas, colWidths=[5 * cm, 12 * cm])
    t.setStyle(org.getTableStyle())
    elements.append(t)

    
    
        
    doc.build(elements)
    
    
    # OUTPUT FILE 
    # doc.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response



def get_formatted_course_outline(c, co):
    formatted_outline = ""
    credits = c.credits
    wp = WeekPlan.objects.filter(course_outline=co)
    for w in wp: 
        formatted_outline += "<b>Week No. " + str(w.week_no) + " - (" + str(credits) + " hours) </b><br />"
        formatted_outline += "    " + clean_string(w.topics) + " <br />"
    
    return formatted_outline
