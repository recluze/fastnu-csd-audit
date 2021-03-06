from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, LongTable, TableStyle, Spacer
from reportlab.lib import colors

from cscm.helpers.loadconfigs import get_config

import datetime 

import copy 

class Internal: 

    def get_header_footer(self, doccode, pagesize=A4):
        width, height = pagesize
            
        def nceac_header_footer(canvas, doc):
            canvas.saveState()
            now = datetime.datetime.now()

            #            titleoffset = 100
            #            
            #        
            #            canvas.line(50, height - 10, width - 50, height - 10)
            #            canvas.line(titleoffset, height - 80, width - 50, height - 80)
            #            
            #            
            #            canvas.setFontSize(18) #choose your font type and font size
            #            canvas.drawString(titleoffset, height - 40, get_config('inst_name'))
            #            canvas.drawString(titleoffset, height - 60, get_config('dept_name') + ' ' + get_config('campus_name'))
            #            
            #            
            #            canvas.setFontSize(10) #choose your font type and font size
            #            canvas.drawString((width - 80) - (len(doccode) * 5), height - 100, doccode)
           
            
            #    P = Paragraph(str(now), styleN)
            # w, h = P.wrap(doc.width, doc.bottomMargin)
            #P.drawOn(canvas, doc.leftMargin, h)
            
            # footer 
            
            canvas.setFontSize(8) #choose your font type and font size
            canvas.line(50, 30, width - 50, 30)
            canvas.drawString(60, 20, "Page %s of " % doc.page)
            canvas.doForm("pageCount") 
            nowdate = str(datetime.datetime.now().strftime("%B %d, %Y"))
            canvas.drawString(width - 120, 20, nowdate) 
            canvas.restoreState()
            # END HEADER AND FOOTER --------------------------------------

        return nceac_header_footer 
    
    
         
    def getTextStyles(self): 
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleB = copy.copy(styles['Normal'])
        styleSmaller = copy.copy(styles['Normal'])
        styleSmaller.fontSize = 8
        styleB.fontName = 'Helvetica-Bold'
        styleH = styles['Heading1']
        styleH.leading = 24
        styleH.fontSize = 12
        
        return styleN, styleB, styleH, styleSmaller 
        
    def getFrame(self, doc):
        frame = Frame(doc.leftMargin - 20 , doc.bottomMargin - 20, doc.width + 40, doc.height + 40,
               id='normal')

        return frame 
    
    def getTableStyle(self):
        return [
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]
