from cscm.models import Instructor
from cscm.helpers.choices import * 
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    uid = models.CharField(max_length=20, blank=True)
    
    def __unicode__(self):
        return self.name + ' (' + self.uid + ')' 


class StudentProject(models.Model):
    instructor = models.ForeignKey(Instructor)
    year = models.PositiveIntegerField()
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    project_type = models.CharField(max_length=20, choices=STUDENT_PROJECT_TYPES)
    title = models.CharField(max_length=500)
    co_supervisors = models.TextField(blank=True)
    team_members = models.TextField()
    achievements = models.TextField(blank=True)
    students = models.ManyToManyField(Student)

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
    score = models.IntegerField(help_text='Out of 10')


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

    class Meta:
        # verbose_name = "Student Project Log Entry"
        verbose_name_plural = "Student Project Log Entries"
        
        
class StudentProjectMilestone(models.Model):   
    project = models.ForeignKey(StudentProject)     
    milestone_name = models.CharField(max_length=100, choices=PROJECT_MILESTONES_CHOICES)
    weight = models.IntegerField()
    milestone_type = models.CharField(max_length=100, choices=PROJECT_MILESTONES_TYPE_CHOICES)
    milestone_deadline = models.DateField(blank=True, null=True)


    def __unicode__(self):
        fields = [str(self.project) + ' - ' + str(self.milestone_name)]
        desc_name = ' '.join(fields)
        return desc_name
    
    