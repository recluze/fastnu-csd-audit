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
from nceac_styles import *
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
def report_nceac_coursedesc(request):
    class NceacCourseLogForm(forms.Form):
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
        form = NceacCourseLogForm(request.POST)
        form.is_valid()
        course_name = form.cleaned_data['course_name']
        course_name = course_name[0]
        inner_response = report_nceac_courselog_pdf(request, course_name)
        http_response = HttpResponse(inner_response, c)  
        filename = "coursedesc_" + str(course_name.course_code) + "-" + str(course_name.semester) + str(course_name.year) + ".pdf"
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
    template = PageTemplate(id='test', frames=frame, onPage=org.get_header_footer(doccode="NCEAC.FORM.001-C"))
    doc.addPageTemplates([template])
    width, height = A4
    frame_width = width - ((doc.leftMargin - 20) * 2)
    
    # Our main content holder 
    
    elements = []

    
    # title page 
    inst_name_head = Paragraph('INSTITUTION', styleB)
    inst_name = Paragraph(get_config('inst_name'), styleN)
    dept_name_head = Paragraph('PROGRAM(S) TO BE EVALUATED', styleB)
    dept_name = Paragraph("BS (CS)", styleN)
    
    metainfo_tablestyle = [
                    # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('LINEBELOW', (1, 0), (1, -1), 0.25, colors.black),
                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]
    metainfo = [[inst_name_head, inst_name], [dept_name_head, dept_name]]
    t1 = LongTable(metainfo, colWidths=[3 * cm, frame_width - (3 * cm)])
    t1.setStyle(TableStyle(metainfo_tablestyle))
    elements.append(t1)
    
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph('A. COURSE DESCRIPTION', styleH))
    elements.append(Paragraph('(Fill out the following table for each course in your computer science curriculum. A filled out form should not be more than 2-3 pages.', styleN))
    elements.append(Spacer(1, 0.5 * cm))


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
                   ['<b>URL</b> (if any)' , c.course_url],
                   ['<b>Current Catalog Description</b>' , '?'],
                   ['<b>Textbook</b> (or laboratory manual for laboratory courses)' , clean_string(co.text_books, False)],
                   ['<b>Reference Material</b>' , clean_string(co.recommended_books, False)],
                   ['<b>Course Goals</b>' , clean_string(co.objectives)],
                   # ['<b>Topics Covered in the Course with Number of lectures on Each Topic</b>(assume 15 week instruction and one-hour lectures)', topics_covered_details],
                   # ['<b>Laboratory Projects/Experiments Done in the Course</b>', c.lab_projects],
                   # ['<b>Programming Assignments Done in the Course</b>', c.prog_assignments],
                ]

    for k in course_info: 
        headpara = Paragraph(k[0], styleN)
        datas.append([headpara , Paragraph(k[1], styleN)])

    t = LongTable(datas, colWidths=[5 * cm, 12 * cm])
    t.setStyle(org.getTableStyle())
    elements.append(t)
         
    # topics covered in the course
    credits = c.credits
     
    try :
        datas = [[Paragraph('<b>Topics Covered in the Course with Number of lectures on Each Topic</b>(assume 15 week instruction and one-hour lectures)', styleN),
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
                        ('SPAN', (0, 0), (0, 3))
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
                   ['<b>Laboratory Projects/Experiments Done in the Course</b>', c.lab_projects],
                   ['<b>Programming Assignments Done in the Course</b>', c.prog_assignments],
                ]

    for k in course_info: 
        headpara = Paragraph(k[0], styleN)
        datas.append([headpara , Paragraph(k[1], styleN)])

    t = LongTable(datas, colWidths=[5 * cm, 12 * cm])
    t.setStyle(org.getTableStyle())
    elements.append(t)

    
    # class time spent details
      
    headpara = Paragraph('Class Time Spent on (in credit hours)', styleB)  
    hp_theory = Paragraph('Theory', styleB)
    hp_analysis = Paragraph('Problem Analysis', styleB)
    hp_design = Paragraph('Design', styleB)
    hp_ethics = Paragraph('Social and Ethical Issues', styleB)
    
    det_headpara = Paragraph(' ', styleB)  
    val_theory = Paragraph(c.class_time_spent_theory, styleN)
    val_analysis = Paragraph(c.class_time_spent_analysis, styleN)
    val_design = Paragraph(c.class_time_spent_design, styleN)
    val_ethics = Paragraph(c.class_time_spent_ethics, styleN)
    
    datas = [[headpara, hp_theory, hp_analysis, hp_design, hp_ethics]]
    datas.append([det_headpara, val_theory, val_analysis, val_design, val_ethics])
    t = LongTable(datas, colWidths=[5 * cm, 2 * cm, 3 * cm, 3 * cm, 4 * cm])
    
    t.setStyle(TableStyle([
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('SPAN', (0, 0), (0, 1)),
                           # ('SPAN', (2, 0), (2, -1)),    
                           ]))
    elements.append(t)
    val_reports = c.communciation_details_num_reports
    val_pages = c.communciation_details_pages
    val_pres = c.communciation_details_num_pres
    val_mins = c.communciation_details_num_mins

    head_comm = Paragraph('Oral and Written Communication', styleB)
    val_comm = Paragraph("Every student is required to submit at least <u>" + str(val_reports) + 
                            "</u> written reports of typically <u>" + str(val_pages) + "</u> pages and to make <u>" + str(val_pres) 
                             + "</u> oral presentations of typically <u>" + str(val_mins) + "</u> minute's duration. Include only material that is graded for " 
                            + "grammar, spelling, style, and so forth, as well as for technical content, completeness and accuracy." , styleN)
    datas = [[head_comm, val_comm]]
    t = LongTable(datas, colWidths=[5 * cm, 12 * cm])
    
    t.setStyle(TableStyle([
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ]))
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
