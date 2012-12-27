# required for PDF generation 
from __future__ import unicode_literals

from io import BytesIO

from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, LongTable, TableStyle, PageTemplate
from reportlab.platypus.flowables import PageBreak 
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from django.http import HttpResponse 

from cscm.views.FooterDocTemplate import FooterDocTemplate

import datetime 
from cscm.views.nceac_styles import *
from cscm.helpers.loadconfigs import get_config
from cscm.helpers.functions import * 

# models 

from cscm.models import CourseLogEntry
from cscm.models import Course, Instructor
from csip.models import InstructorProfile

# Forms imports 
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.template import RequestContext
  
from django.contrib.auth.decorators import login_required 

import copy 
# =============================================================================================
@login_required 
def report_nceac_faculty_profile(request):
    class NceacFacultyProfileForm(forms.Form):
        if request.user.is_superuser: 
            instructor = forms.ModelMultipleChoiceField(queryset=Instructor.objects.all())
        else: 
            instructor = forms.ModelMultipleChoiceField(queryset=Instructor.objects.filter(owner=request.user))
        
    
    c = RequestContext(request)  
    c.update(csrf(request))
    
    # if 'course_name' in request.GET and request.GET['course_name']:
    if request.method == 'POST':  
        # form submitted 
        form = NceacFacultyProfileForm(request.POST)
        form.is_valid()
        instructor = form.cleaned_data['instructor']
        instructor = instructor[0]
        inner_response = report_nceac_faculty_profile_pdf(request, instructor)
        http_response = HttpResponse(inner_response, c)  
        escaped_name = str(instructor.name).replace(' ', '_')
        this_year = datetime.datetime.now().strftime("%Y")
        filename = "faculty_profile_" + escaped_name + "-" + this_year + ".pdf"
        http_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
        return http_response  
        
    else:  
        # form not yet submitted ... display it 
        form = NceacFacultyProfileForm()
        return render_to_response('nceac_faculty_profile.html' , {
                'form': form
                }, c)
         





# ============= PDF GEN 

def report_nceac_faculty_profile_pdf(request, instructor):
    def make_table(data, widths, style=[]):
        table = LongTable(data, colWidths=widths)
        table.setStyle(TableStyle(style))
        return table 
        
    response = HttpResponse(mimetype='application/pdf')
    
    buffer = BytesIO() 
    
    org = Nceac()
    styleN, styleB, styleH, styleSmaller = org.getTextStyles()
    styleBC = copy.copy(styleB)
    styleBC.alignment = TA_CENTER 
    
    width, height = A4
    doc = FooterDocTemplate(buffer, pagesize=(height, width))
    
    frame = org.getFrame(doc)
    template = PageTemplate(id='test', frames=frame, onPage=org.get_header_footer(doccode="NCEAC.DOC.008", pagesize=(height, width)))
    doc.addPageTemplates([template])
    
    # Our main content holder 
    
    elements = []
    
    i = instructor 
    ip = i.instructorprofile
    percent_time_teaching = ip.percent_time_teaching
    
    # title page 
    data = [[Paragraph('Name', styleB), i.name],
            [Paragraph('Academic Rank', styleB), ip.designation],
            [Paragraph('Administrative Responsibility', styleB), ip.admin_responsibility],
            [Paragraph('Date of Original Appointment', styleB), ip.joining_date],
            ]
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]    
    elements.append(make_table(data, widths=[6 * cm, 20 * cm], style=ts))    
    # elements.append(PageBreak())
    
    # Education 
    ieds = i.instructoreducation_set.all().order_by('-year')
    data = [[Paragraph('Degrees', styleB),
             Paragraph('Degree', styleB),
             Paragraph('Field', styleB),
             Paragraph('Institution', styleB),
             Paragraph('Date', styleB),
            ]]
    for ied in ieds: 
        data.append(['',
             Paragraph(ied.degree, styleN),
             Paragraph(ied.field, styleN),
             Paragraph(ied.university, styleN),
             Paragraph(ied.year, styleN),
            ])
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('SPAN', (0, 0), (0, -1))
            ]    
    elements.append(make_table(data, widths=[6 * cm, 4.5 * cm, 4.5 * cm, 7 * cm, 4 * cm], style=ts))    
    
    # events 
    ievs = i.instructoreventparticpation_set.all().order_by('-start_date')
    counter = 1
    cat_header = Paragraph('Conferences, workshops, and professional development programs participated during the past five years', styleB)
    data = []
    for iev in ievs: 
        iev_string = str(counter) + '. ' + iev.title + '. Role: ' + iev.role + ' (' + str(iev.duration) + ' at ' + str(iev.venue) + ')'  
        data.append([cat_header,
             Paragraph(iev_string, styleN),
             Paragraph(str(iev.start_date.year), styleN),
            ])
        cat_header = ''
        counter += 1
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('SPAN', (0, 0), (0, -1))
            ]    
    if len(data) < 1: 
        data.append([cat_header, 'None' , '-'])
    elements.append(make_table(data, widths=[6 * cm, 16 * cm, 4 * cm], style=ts))    
    
    
    # Consultancies 
    icons = i.instructorconsultancy_set.all().order_by('-date')
    counter = 1
    cat_header = Paragraph('Consulting activities during the last five years', styleB)
    data = []
    for icon in icons: 
        icon_string = str(counter) + '. <b>' + icon.organization + '</b>. ' + icon.description   
        data.append([cat_header,
             Paragraph(icon_string, styleN),
             Paragraph(str(icon.date.year), styleN),
            ])
        cat_header = ''
        counter += 1
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('SPAN', (0, 0), (0, -1))
            ]    
    if len(data) < 1: 
        data.append([cat_header, 'None' , '-'])
    elements.append(make_table(data, widths=[6 * cm, 16 * cm, 4 * cm], style=ts))
    
    # Publications 
    ipbs = i.instructorpublication_set.all().order_by('-pub_date')
    counter = 1
    cat_header = Paragraph('Principal publications during the last five years (give in standard bibliogrpahic format)', styleB)
    data = []
    for ipb in ipbs: 
        pub_string = ipb.get_citation()
        data.append([cat_header,
             Paragraph(pub_string, styleN),
             Paragraph(str(ipb.pub_date.year), styleN),
            ])
        cat_header = ''
        counter = counter + 1
        
    ts = [  ('INNERGRID', (1, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (0, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # ('SPAN', (0, 0), (0, -1)) # gives error for some reason 
            ]    
    if len(data) < 1: 
        data.append([cat_header, 'None' , '-'])
    elements.append(make_table(data, widths=[6 * cm, 16 * cm, 4 * cm], style=ts)) 

    # Other activities 
    ioas = i.instructorotheractivity_set.all().order_by('-date')
    counter = 1
    cat_header = Paragraph('Other scholarly activities during the last five years (grants, sabbaticals, software development, etc.)', styleB)
    data = []
    for ioa in ioas: 
        pub_string = str(counter) + '. ' + str(ioa.title) + '. ' + str(ioa.description)
        data.append([cat_header,
             Paragraph(pub_string, styleN),
             Paragraph(str(ioa.date), styleN),
            ])
        cat_header = ''
        counter += 1
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('SPAN', (0, 0), (0, -1))
            ]    
    if len(data) < 1: 
        data.append([cat_header, 'None' , '-'])
        
    elements.append(make_table(data, widths=[6 * cm, 16 * cm, 4 * cm], style=ts)) 
    
    # courses during last two years 
    ics = i.course_set.all().order_by('-year')
    data = [[Paragraph('Courses taught during this and last academic year', styleB),
             Paragraph('Year', styleB),
             Paragraph('Semester', styleB),
             Paragraph('Course Code', styleB),
             Paragraph('Course Title', styleB),
            ]]
    for ic in ics: 
        data.append(['',
                     str(ic.year),
                     str(ic.semester),
                     str(ic.course_code),
                     str(ic.course_name)
                     ])
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # ('SPAN', (0, 0), (0, -1))
            ]    
    elements.append(make_table(data, widths=[6 * cm, 3 * cm, 3 * cm, 3 * cm, 11 * cm], style=ts)) 


    # Percentage of time given to teaching
    data = [[Paragraph('State percentage of your full-time work dedicated to teaching in the computing program under evaluation', styleB)
             , str(percent_time_teaching) + '%']]
    ts = [  ('INNERGRID', (0, 0), (-1, -1), 0.15, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
    elements.append(make_table(data, widths=[6 * cm, 20 * cm], style=ts))

    # END OF REPORT. NOW BUILD 

    doc.build(elements)
    # OUTPUT FILE 
    # doc.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


