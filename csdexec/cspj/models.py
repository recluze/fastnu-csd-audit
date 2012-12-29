from cscm.models import Instructor
from cscm.helpers.choices import * 
from django.db import models

class StudentProject(models.Model):
    instructor = models.ForeignKey(Instructor)
    year = models.PositiveIntegerField()
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    project_type = models.CharField(max_length=20, choices=STUDENT_PROJECT_TYPES)
    title = models.CharField(max_length=500)
    co_supervisors = models.TextField(blank=True)
    team_members = models.TextField()
    achievements = models.TextField(blank=True)

    def __unicode__(self): 
        fields = [self.title, "(" + str(self.semester) + " " + str(self.year) + ")"]
        desc_name = ' '.join(fields)
        return desc_name


class StudentProjectLogEntry(models.Model):
    project = models.ForeignKey(StudentProject)
    session_date = models.DateField()
    issues_discussed = models.TextField()
    issue_originator = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    evaluation_instruments = models.TextField(blank=True)
    score = models.IntegerField()


    def session_no(self):
        ents = self.project.studentprojectlogentry_set.all().order_by('session_date')
        s_no = 0
        for e in ents:
             s_no += 1 
             if e == self: 
                 break 
        return s_no
    #session_no.admin_order_field = 'session_date'
    
    
    def __unicode__(self): 
        fields = ['Session ' + str(self.session_no()) + ' on ' + str(self.session_date), "(" + str(self.project.title) + " " + str(self.project.year) + ")"]
        desc_name = ' '.join(fields)
        return desc_name
