# required for PDF generation 
from __future__ import unicode_literals

import os 

from io import BytesIO

from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, LongTable, TableStyle, PageTemplate, Image, Spacer
from reportlab.platypus.flowables import PageBreak 
from reportlab.lib import colors

from django.http import HttpResponse 

from cscm.views.FooterDocTemplate import FooterDocTemplate

import datetime 
from qec_styles import *
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
def report_qec_courselog(request):
    class QecCourseLogForm(forms.Form):
        WEEKRANGE = (
                (1, "Weeks 1 to 5"),
                (2, "Weeks 6 to 10"),
                (3, "Weeks 11 to End"),
                )
        # course_name = forms.ChoiceField(choices=TEMP)
        num_courses = Course.objects.count()
        if request.user.is_superuser: 
            course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.all().order_by('-year', 'semester'))
        else: 
            course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.filter(instructor__owner=request.user).order_by('-year', 'semester'))
        course_name.widget.attrs['size'] = num_courses if num_courses < 10 else 10 
        week_range = forms.MultipleChoiceField(choices=WEEKRANGE)
    
    c = RequestContext(request)  
    c.update(csrf(request))
    
    # if 'course_name' in request.GET and request.GET['course_name']:
    if request.method == 'POST':  
        # form submitted 
        form = QecCourseLogForm(request.POST)
        form.is_valid()
        try: 
            course_name = form.cleaned_data['course_name']
            course_name = course_name[0]
            week_range = form.cleaned_data['week_range']
            week_range = int(week_range[0]) 
            week_range = {
                          1: lambda: (1, 5),
                          2: lambda: (6, 10),
                          3: lambda: (11, 16)
                          }[week_range]()
        except Exception, err:
             raise RuntimeError("Invalid values selected in form.")
        
        inner_response = report_qec_courselog_pdf(request, course_name, week_range)
        http_response = HttpResponse(inner_response, c)  
        filename = "QEC_CourseExec_" + str(course_name.course_code) + "-" + str(course_name.semester) + str(course_name.year) +\
                                "_" + str(week_range[0]) + "-" + str(week_range[1]) +".pdf"
        http_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
        return http_response  
        
    else:  


        # form not yet submitted ... display it 
        form = QecCourseLogForm()
        return render_to_response('qec_courselog.html' , {
                'form': form
                }, c)
         





# ============= PDF GEN 

def report_qec_courselog_pdf(request, course_name, week_range):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefile.pdf"' 
    
    buffer = BytesIO() 
    
    org = Qec()
    styleN, styleB, styleH, styleSmaller = org.getTextStyles()
    doc = FooterDocTemplate(buffer, pagesize=A4)
    frame = org.getFrame(doc)
    
    logo_filename = os.path.join(os.path.dirname(__file__), 'images', get_config('logo_filename'))

    template = PageTemplate(id='test', frames=frame, onPage=org.get_header_footer())
    doc.addPageTemplates([template])
    
    # Our main content holder 
    
    elements = []
    
    # title page 
    # SYMBOLS FOR CHECKED/UNCHECKED: \u2713 \u26aa  or x 
    inst_name = Paragraph(get_config('inst_name'), styleH)
    dept_name = Paragraph(get_config('dept_name') + ", " + get_config('campus_name'), styleB)
    report_title = Paragraph('Weekly Progress Report (Performa 11)', styleB)
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
    
    # doc._draw_header_logo('/home/nam/documents/exps/django-tut/fastnu-csd-audit/csdexec/cscm/views/images/fastlogo.png', 10, 10)
    
    elements.append(Spacer(1, 0.5 * cm))
    
    course_name_label = Paragraph(course_name.course_name, styleB)
    inst_name_label = Paragraph(str(course_name.instructor), styleB)
    from_week_label = Paragraph(str(week_range[0]), styleB)
    to_week_label = Paragraph(str(week_range[1]), styleB)
    metainfo = [['Course Name', course_name_label,
                 'Instructor', inst_name_label],
                ['From Week', from_week_label,
                 'To Week', to_week_label],
                ]
    metainfo_tablestyle = []
    t1 = LongTable(metainfo, colWidths=[3 * cm, 6 * cm, 3 * cm, 6 * cm])
    t1.setStyle(TableStyle(metainfo_tablestyle))
    elements.append(t1)
    
    elements.append(Spacer(1, 0.5 * cm))
    
    # elements.append(PageBreak())

    
    # =================== TABLE DATA 
    datas = []
    headLNo = Paragraph('Lec.', styleB)
    headWNo = Paragraph('Wk.', styleB)
    headDate = Paragraph('Date', styleB)
    headDuration = Paragraph('Duration', styleB)
    headTopics = Paragraph('Topics Covered', styleB)
    headEval = Paragraph('Evaluation Instruments Used', styleB)
    headRead = Paragraph('Reading Materials', styleB)
    headSign = Paragraph('Signature', styleB)
    emptypara = Paragraph(' ', styleN)
    
    datas = [[headLNo, headWNo, headDate, headDuration, headTopics, headEval, headRead]]
    
    # courselogentry_data = CourseLogEntry.objects.all()
    courselogentry_data = course_name.courselogentry_set.all().order_by('lecture_date')
    
    start_week = int(week_range[0])
    end_week = int(week_range[1])
    num_assignments = 0 
    num_quizzes = 0 
    gross_contents_covered = ''
    all_contents_covered = True 
    
    l_no = 1 # start
    w_no = 1
    starting_week_of_year = 0
    other_activities = []    
    for i in courselogentry_data:
        l_no = i.lecture_no() 
        w_no = i.week_no() 
         
        if w_no < start_week or w_no > end_week:
            continue 
        
        # entered_logs += 1
        l_date = Paragraph(str(i.lecture_date.strftime("%d-%m, %Y")), styleSmaller)
        l_duration = Paragraph(str(i.duration), styleSmaller)
        l_topics_covered = Paragraph(clean_string(i.topics_covered), styleSmaller)
        l_eval = Paragraph(clean_string(i.evaluation_instruments), styleSmaller)
        l_reading = Paragraph(clean_string(i.reading_materials), styleSmaller)
        emptypara = Paragraph(str(l_no) + ' ' + str(w_no), styleSmaller)
        datas.append([str(l_no), str(w_no), l_date, l_duration, l_topics_covered, l_eval, l_reading])
        
        # logic for calculating meta data 
        num_assignments += i.evaluation_instruments.lower().count('assignment')
        num_quizzes += i.evaluation_instruments.lower().count('quiz')
        gross_contents_covered += i.contents_covered.strip() + '\n'
        if i.contents_covered.strip() != '': 
            all_contents_covered = False
            
        other_activities.append(i.other_activities)
    
        
    if len(datas) < 2: # 2 because we do have a header in any case  
        raise Exception("No Course Log Entries found!") 
        
        
    t = LongTable(datas, colWidths=[1 * cm, 1 * cm, 1.5 * cm, 2 * cm, 6 * cm, 3 * cm, 3 * cm], repeatRows=1)
    
    t.setStyle(TableStyle(org.getTableStyle()))
    elements.append(t)
    elements.append(Spacer(1, 0.5 * cm))
    
    # lower metadata
    metainfo = [[Paragraph('<b>Number of Assignments</b>', styleN), str(num_assignments)],
                 [Paragraph('<b>Number of Quizzes', styleN), str(num_quizzes)],
                ]
    t1 = LongTable(metainfo, colWidths=[6 * cm, 12 * cm])
    t1.setStyle(TableStyle())
    elements.append(t1)
    elements.append(Spacer(1, 1 * cm))
    
    
    metainfo = [[Paragraph('Other activities (if any)', styleB)]]
    
    for oa in other_activities: 
        metainfo.append([Paragraph(str(oa), styleN)])
        
    t1 = LongTable(metainfo, colWidths=[18 * cm])
    t1.setStyle(TableStyle())
    elements.append(t1)
    elements.append(Spacer(1, 0.5 * cm))
        
    
    # elements.append(Spacer(1, 0.5 * cm))
    if all_contents_covered:
         is_covered_yes = '\u2713'
         is_covered_no = 'x'
    else: 
         is_covered_yes = 'x'
         is_covered_no = '\u2713'
    gross_contents_covered = 'NA' if all_contents_covered == '' else gross_contents_covered 
    metainfo = [ [is_covered_yes, 'All contents planned for this period were covered.'],
                 [is_covered_no, 'Some contens planned for this period were not covered. Details below:'],
                 ['', ''],
                 [Paragraph(clean_string(gross_contents_covered), styleN), '']
                ]
    metainfo_tablestyle = [('SPAN', (0, 2), (1, 2)),
                           ('BOX', (0, 3), (1, 3), 0.25, colors.black),
                           ('BOX', (0, 0), (0, 0), 0.25, colors.black),
                           ('BOX', (0, 1), (0, 1), 0.25, colors.black)]
    t1 = LongTable(metainfo, colWidths=[0.6 * cm, 16 * cm])
    t1.setStyle(TableStyle(metainfo_tablestyle))
    elements.append(t1)    
    
    # signature area 
    elements.append(Spacer(1, 1 * cm))
    metainfo = [ [Paragraph('Date', styleB), datetime.datetime.now().strftime('%d-%B-%Y'),
                 Paragraph('Signature', styleB), '', ''],
                ]
    metainfo_tablestyle = [('LINEBELOW', (3, 0), (3, 0), 0.25, colors.black)]
    t1 = LongTable(metainfo, colWidths=[2 * cm, 4 * cm, 2 * cm , 4 * cm, 5 * cm])
    t1.setStyle(TableStyle(metainfo_tablestyle))
    elements.append(t1)    
    
    
    # finalize document 
    doc.build(elements)
    
    
    # OUTPUT FILE 
    # doc.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
