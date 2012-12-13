from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, LongTable, TableStyle, PageTemplate
from reportlab.lib import colors

import datetime 
from nceac_styles import *

org = Nceac()
styleN, styleB, styleH = org.getTextStyles()
doc = BaseDocTemplate('test.pdf', pagesize=A4)
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
headDuration = Paragraph('Duration', styleN)
headTopics = Paragraph('Topics Covered', styleN)
headEval = Paragraph('Evaluation Instruments Used', styleN)
headSign = Paragraph('Signature', styleN)

datas = [[headDate, headDuration, headTopics, headEval, headSign]]
for x in range(1, 50):
    datas.append(
        [x, x + 1, x + 2, x + 4, x + 5]
    )
t = LongTable(datas, colWidths=[1.5 * cm, 2 * cm, 8 * cm, 3 * cm, 3 * cm])

t.setStyle(TableStyle(org.getTableStyle()))
elements.append(t)
doc.build(elements)


