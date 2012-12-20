from django.db import models
from cscm.models import Instructor 
from cscm.helpers.choices import * 
from cscm.helpers.functions import get_pub_string

from datetime import timedelta
from dateutil import relativedelta as rdelta


class InstructorProfile(models.Model):
    instructor = models.OneToOneField(Instructor)
    date_of_birth = models.DateField(blank=True)
    department = models.CharField(max_length=100)
    
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    current_position_appointment_date = models.DateField()
    joining_date = models.DateField()
    admin_responsibility = models.CharField(max_length=200, blank=True)
    pay_grade = models.CharField(max_length=50, blank=True)
    pay_step = models.CharField(max_length=50, blank=True)
    gross_pay = models.CharField(max_length=50, blank=True)
    percent_time_teaching = models.CharField(max_length=4, blank=True, help_text='Percentage of time given to teaching in organization. Please do not suffix the \'%\' symbol ')
    awards = models.TextField('Academic Awards/Distinctions', blank=True)
    memberships = models.TextField('Professional Memberships', blank=True, help_text='e.g. editor of journal, academic bodies')
    
    
    def __unicode__(self): 
        fields = [str(self.instructor)]
        desc_name = ' '.join(fields)
        return desc_name 
    
    
    
class InstructorEducation(models.Model):
    instructor = models.ForeignKey(Instructor)
    degree = models.CharField(max_length=100)
    field = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    university = models.CharField('University/Board', max_length=100, blank=True)
    year = models.CharField(max_length=10, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    
    def __unicode__(self): 
        fields = [str(self.instructor), '(' + str(self.degree) + ')']
        desc_name = ' '.join(fields)
        return desc_name 
    
    
class InstructorPublication(models.Model):
    instructor = models.ForeignKey(Instructor)
    pub_bib = models.TextField('BibTex', blank=True, help_text='DEPRECATED. LEAVE BLANK!')
    author_list = models.CharField('List of Authors', max_length=500, help_text='In "first name last name" format. Separate multiple authors with a comma.')
    title = models.CharField(max_length=500, blank=True, help_text='In case of book, leave this field blank.')
    journal = models.CharField('Journal/Book/Conference', max_length=500, blank=True)
    journal_address = models.CharField('Address of Journal', max_length=500, blank=True)
    volume = models.CharField(max_length=25, blank=True)
    number = models.CharField(max_length=25, blank=True)
    pages = models.CharField(max_length=25, blank=True, help_text='Page numbers in format starting--ending')
    publisher = models.CharField(max_length=500, blank=True)
    pub_date = models.DateField('Publication Date', help_text='If unpublished, set to today')
    hec_cat = models.CharField('HEC Category', max_length=10, blank=True, help_text='In case of local journals')
    
    pub_type = models.CharField('Type', max_length=10, choices=PUB_TYPE_CHOICES)
    impact_factor = models.CharField(max_length=10, blank=True, help_text='Please leave blank in case of books/conferences/non-impact factor journals')
    status = models.CharField(max_length=20, choices=PUB_STATUS_CHOICES, blank=True)
    
    def get_conf_citation(self, html=False):
        cit = self.author_list + '. ' + self.title + '. ' + self.journal + '. (' + self.publisher + ' ' + str(self.pub_date.year) + ')' + self.journal_address 
        return cit 
    
    def pub_string(self):
        return self.title + ' ' + self.journal
    
    def __unicode__(self): 
        return self.title + ' ' + self.journal 




class InstructorConsultancy(models.Model):
    instructor = models.ForeignKey(Instructor)
    date = models.DateField()
    description = models.TextField(blank=True, help_text='Include project title, funding agency, date of award and duration and total amount of award; please specify whether you were principal investigator (PI) or co-Investigator')
    organization = models.CharField(max_length=200)
    
    
    def __unicode__(self): 
        fields = [str(self.organization), '(' + str(self.date) + ')']
        desc_name = ' '.join(fields)
        return desc_name        
               
class InstructorEventParticpation(models.Model):
    instructor = models.ForeignKey(Instructor)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateField()
    duration = models.CharField(max_length=50)
    role = models.TextField(blank=True)
    venue = models.TextField(blank=True)
    
    def __unicode__(self): 
        fields = [str(self.title), '(' + str(self.type) + ')']
        desc_name = ' '.join(fields)
        return desc_name  
    
    
class InstructorEmployment(models.Model):
    instructor = models.ForeignKey(Instructor)
    position = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    job_desc = models.TextField(blank=True) 
    
    def duration_days(self):
        return str((self.end_date - self.start_date).days) + " days"
    
    def duration(self):
        rd = rdelta.relativedelta(self.end_date + timedelta(days=1), self.start_date)
        if rd.months == 0:
            return ("{0} years".format(rd.years)) 
        else: 
            return ("{0.years} years and {0.months} months".format(rd))
    
    def __unicode__(self): 
        fields = [str(self.position), 'at' + str(self.organization) + '(' + str(self.start_date) + '-' + str(self.end_date) + ')']
        desc_name = ' '.join(fields)
        return desc_name  
    
    
    
class InstructorOtherActivity(models.Model):
    instructor = models.ForeignKey(Instructor)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    
    def __unicode__(self): 
        fields = [str(self.title)]
        desc_name = ' '.join(fields)
        return desc_name  













