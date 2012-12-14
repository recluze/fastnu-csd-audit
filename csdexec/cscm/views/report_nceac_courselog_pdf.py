from __future__ import unicode_literals

from io import BytesIO

from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, LongTable, TableStyle, PageTemplate
from reportlab.lib import colors

from django.http import HttpResponse 

import datetime 
from nceac_styles import *

from cscm.models import CourseLogEntry
from cscm.models import Course


def report_nceac_courselog_pdf(request, course_name):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefile.pdf"' 
    
    buffer = BytesIO() 
    
    org = Nceac()
    styleN, styleB, styleH, styleSmaller = org.getTextStyles()
    doc = BaseDocTemplate(buffer, pagesize=A4)
    frame = org.getFrame(doc)
    template = PageTemplate(id='test', frames=frame, onPage=org.get_header_footer())
    doc.addPageTemplates([template])
    
    #text = []
    #for i in range(111):
    #    text.append(Paragraph("This is line %d." % i,
    #                          styleN))
    #doc.build(text)
    
    # =================== TABLE DATA 
    elements = []
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
        l_date = Paragraph(str(i.lecture_date.strftime("%d-%m, %Y")).replace('\n', '<br />'), styleSmaller)
        l_duration = Paragraph(str(i.duration).replace('\n', '<br />'), styleSmaller)
        l_topics_covered = Paragraph(i.topics_covered.replace('\n', '<br />').replace('&', '&amp;'), styleSmaller)
        l_eval = Paragraph(str(i.evaluation_instruments).replace('\n', '<br />'), styleSmaller)
        
        datas.append([l_date, l_duration, l_topics_covered, l_eval, emptypara])
    
    #for i in range(entered_logs, 16): 
    #    data.append([[emptypara, emptypara, emptypara, emptypara, emptypara]])
        
    t = LongTable(datas, colWidths=[1.5 * cm, 2 * cm, 8 * cm, 3 * cm, 3 * cm])
    
    t.setStyle(TableStyle(org.getTableStyle()))
    elements.append(t)
    doc.build(elements)
    
    
    # OUTPUT FILE 
    # doc.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
