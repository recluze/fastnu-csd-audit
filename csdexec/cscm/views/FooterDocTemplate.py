from reportlab.platypus import BaseDocTemplate


class FooterDocTemplate(BaseDocTemplate):
    
    def _endBuild(self):
        self.canv.beginForm("pageCount")
        self.canv.setFont("Helvetica", 8)
        self.canv.drawString(100, 20, u"%s" % (self.canv.getPageNumber(),))
        self.canv.endForm()
        BaseDocTemplate._endBuild(self)