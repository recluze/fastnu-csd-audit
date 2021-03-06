from reportlab.lib.pagesizes import letter, A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, LongTable, TableStyle
from reportlab.lib import colors

import datetime 

class Nceac: 

    def nceac_header_footer(obk, canvas, doc):
        canvas.saveState()
        now = datetime.datetime.now()
        
        width, height = A4
        titleoffset = 100
        
    
        canvas.line(50, height - 10, width - 50, height - 10)
        canvas.line(titleoffset, height - 80, width - 50, height - 80)
        
        
        canvas.setFontSize(18) #choose your font type and font size
        canvas.drawString(titleoffset, height - 40, "National Computer Education Accredication Council")
        canvas.drawString(titleoffset, height - 60, "NCEAC")
        
        
        canvas.setFontSize(10) #choose your font type and font size
        canvas.drawString(width - 130, height - 100, "NCEAC.DOC.008")
       
        
        #    P = Paragraph(str(now), styleN)
        # w, h = P.wrap(doc.width, doc.bottomMargin)
        #P.drawOn(canvas, doc.leftMargin, h)
        
        # footer 
        
        canvas.setFontSize(8) #choose your font type and font size
        canvas.line(50, 30, width - 50, 30)
        canvas.drawString(60, 20, "Page 2 of 2")
        nowdate = str(datetime.datetime.now().strftime("%B %d, %Y"))
        canvas.drawString(width - 120, 20, nowdate)
        canvas.restoreState()
        # END HEADER AND FOOTER --------------------------------------


    def get_header_footer(self): 
        return self.nceac_header_footer 
    
    def getTextStyles(self): 
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleB = styles['Normal']
        styleB.fontName = 'Helvetica-Bold'
        styleH = styles['Heading1']
        return styleN, styleB, styleH 
        
    def getFrame(self, doc):
        frame = Frame(doc.leftMargin - 20 , doc.bottomMargin - 20, doc.width + 40, doc.height - 30,
               id='normal')

        return frame 
    
    def getTableStyle(self):
        return [
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]