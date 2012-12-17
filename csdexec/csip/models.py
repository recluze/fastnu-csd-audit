from django.db import models
from cscm.models import Instructor 
from cscm.helpers.choices import * 
from cscm.helpers.functions import get_pub_string

from datetime import timedelta
from dateutil import relativedelta as rdelta


class InstructorProfile(models.Model):
    instructor = models.ForeignKey(Instructor)
    date_of_birth = models.DateField(blank=True)
    department = models.CharField(max_length=100)
    
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    current_position_appointment_date = models.DateField()
    joining_date = models.DateField()
    admin_responsibility = models.CharField(max_length=200, blank=True)
    pay_grade = models.CharField(max_length=50, blank=True)
    pay_step = models.CharField(max_length=50, blank=True)
    gross_pay = models.CharField(max_length=50, blank=True)
    awards = models.TextField('Academic Awards/Distinctions',blank=True)
    memberships = models.TextField('Professional Memberships',blank=True, help_text='e.g. editor of journal, academic bodies')
    
    
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
    pub_bib = models.TextField('BibTex', blank=True)
    pub_type = models.CharField(max_length=10, choices=PUB_TYPE_CHOICES)
    impact_factor = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=10, choices=PUB_STATUS_CHOICES, blank=True)
    
    def __unicode__(self): 
        return get_pub_string(self.pub_bib)




class InstructorConsultancy(models.Model):
    instructor = models.ForeignKey(Instructor)
    date = models.DateField()
    description = models.TextField(blank=True)
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
    







