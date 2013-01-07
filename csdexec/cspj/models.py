from cscm.models import Instructor
from cscm.helpers.choices import * 
from django.db import models
from django.db.models import Q

class Student(models.Model):
    name = models.CharField(max_length=50)
    uid = models.CharField(max_length=20, blank=True)
    
    def __unicode__(self):
        return self.name + ' (' + self.uid + ')' 

    class Meta: 
        ordering = ['name']

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
        

class StudentProjectMilestoneCategory(models.Model):
    milestone_name = models.CharField(max_length=100, choices=PROJECT_MILESTONES_CHOICES)
    weight = models.IntegerField(default=0)
    project_type = models.CharField(max_length=100, choices=(('FYP', 'FYP'), ('Thesis', 'Thesis')))
    milestone_type = models.CharField(max_length=100, choices=PROJECT_MILESTONES_TYPE_CHOICES)

    def __unicode__(self):
        fields = [str(self.project_type) + ' - ' + str(self.milestone_name) + ' (' + str(self.weight) + ')']
        desc_name = ' '.join(fields)
        return desc_name
        
class StudentProjectMilestone(models.Model):   
    project = models.ForeignKey(StudentProject)     
    milestone_category = models.ForeignKey(StudentProjectMilestoneCategory)
    milestone_deadline = models.DateField(blank=True, null=True)

    def __unicode__(self):
        fields = [str(self.project) + ' - ' + str(self.milestone_category)]
        desc_name = ' '.join(fields)
        return desc_name


class StudentProjectMilestoneEvaluation(models.Model):
    milestone = models.ForeignKey(StudentProjectMilestone)
    instructor = models.ForeignKey(Instructor, verbose_name='evaluator')
    student = models.ForeignKey(Student)
    evaluator_confidence = models.FloatField(help_text='Confidence you have in your evaluation (x/10)')
    problem_difficulty = models.FloatField(help_text='Difficulty of the problem targeted by the project (Thesis: x/10, FYP: x/5)', blank=True)
    solution_strength = models.FloatField(help_text='Quality of proposed solution and student\'s contribution to it (Thesis: x/15, FYP: x/10)', blank=True)
    execution = models.FloatField(help_text='Quality of implementation and student\'s contribution to it (x/10)')
    issue_resolution = models.FloatField(help_text='Resolution of issues faced/raised in last presentation (Thesis: x/10, FYP: x/5)', blank=True)
    presentation = models.FloatField(help_text='Presentation skills (x/5)', blank=True)
    comments = models.TextField(help_text='Suggestions made to the student, questions to be answered in next session', blank=True)

    # limit students 
    student.limit_choices_to = {'student__name__startswith': 'N'}

    def __unicode__(self):
        fields = [str(self.milestone) + ' - ' + str(self.instructor) + 'for' + str(self.student)]
        desc_name = ' '.join(fields)
        return desc_name
    
