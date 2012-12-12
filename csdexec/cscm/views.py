from reportlab.pdfgen import canvas 
from django.http import HttpResponse 
import datetime 
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib import colors
from django.utils import timezone

from cscm.models import CourseLogEntry

def current_datetime(request):
    response = HttpResponse(mimetype='application/pdf')
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    
    titleoffset = 100
    
    
    def coord(x, y, unit=1):
        x, y = x * unit, height - y * unit
        return x, y
    
    # Headers
    hdescrpcion = Paragraph('''<b>Date</b>''', styleBH)
    hpartida = Paragraph('''<b>Duration</b>''', styleBH)
    hcandidad = Paragraph('''<b>Topics Covered</b>''', styleBH)
    hprecio_unitario = Paragraph('''<b>Evaluation Instruments Used</b>''', styleBH)
    hprecio_total = Paragraph('''<b>Signature</b>''', styleBH)
    
    # Texts
    descrpcion = Paragraph(' ', styleN)
    partida = Paragraph(' ', styleN)
    candidad = Paragraph(' ', styleN)
    precio_unitario = Paragraph(' ', styleN)
    precio_total = Paragraph(' ', styleN)
    
    data = [[hdescrpcion, hpartida, hcandidad, hprecio_unitario, hprecio_total]]
    
    entered_logs = 0 
    courselogentry_data = CourseLogEntry.objects.all()
    for i in courselogentry_data: 
        entered_logs += 1
        topics_covered = Paragraph(str(i.topics_covered).replace('\n', '<br />'), styleN)
        data.append([partida, candidad, topics_covered, precio_unitario, precio_total])
    
    for i in range(entered_logs, 16): 
        data.append([[partida, candidad, descrpcion, precio_unitario, precio_total]])

    
    
    table = Table(data, colWidths=[1.5 * cm, 2 * cm, 8 * cm,
                                   3 * cm, 3 * cm])
    
    table.setStyle(TableStyle([
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ]))
    
    c = canvas.Canvas(response, pagesize=A4)
    
    
    # HEADER 
    c.line(50, height - 10, width - 50, height - 10)
    c.line(titleoffset, height - 80, width - 50, height - 80)
    
    
    c.setFont("Helvetica", 18) #choose your font type and font size
    c.drawString(titleoffset, height - 40, "National Computer Education Accredication Council")
    c.drawString(titleoffset, height - 60, "NCEAC")
    
    
    c.setFont("Helvetica", 10) #choose your font type and font size
    c.drawString(width - 130, height - 100, "NCEAC.DOC.008")
    
    # TABLE DATA 
    
    table.wrapOn(c, width, height)
    table.drawOn(c, *coord(1.8, 22, cm))
    
    # FOOTER 
    c.setFont("Helvetica", 8) #choose your font type and font size
    c.line(60, 30, width - 40, 30)
    c.drawString(60, 20, "Page 2 of 2")
    nowdate = str(datetime.datetime.now().strftime("%B %d, %Y"))
    c.drawString(width - 120, 20, nowdate)
    
    # OUTPUT FILE 
    c.save()
    return response
