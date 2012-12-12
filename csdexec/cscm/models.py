from django.db import models


class Instructor(models.Model):
    DESIGNATION_CHOICES = (
                ('1', 'Lecturer'),
                ('2', 'Assistant Professor'),
                ('3', 'Associate Professor'),
                ('4', 'Professor'),
                )
    
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=200, default=25)
    designation = models.CharField(max_length=1, choices=DESIGNATION_CHOICES)
    joining_date = models.DateField()
    
    def __unicode__(self): 
        return self.name 
    
    
# Course  Stuff  --------------------------------------------------    
class Course(models.Model):
    CREDITS_CHOICES = (
                       (1, '1'), (2, '2'), (3, '3'), (4, '4')
                       ) 
    SEMESTER_CHOICES = (
                        ('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')
                        )
    COURSE_TYPE_CHOICES = (
                       ('Core', 'Core'), ('Elective', 'Elective'), ('No Credit', 'No Credit')
                       ) 
    course_code = models.CharField(max_length=10, default='CS')
    instructor = models.ForeignKey(Instructor)
    course_name = models.CharField(max_length=200)
    credits = models.IntegerField()
    year = models.PositiveIntegerField()
    batch = models.CharField(max_length=10, default='BS11')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    grade_distribution = models.TextField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)
    pre_reqs = models.TextField()
    course_url = models.CharField('Course URL', max_length=256)
    lab_projects = models.TextField('Laboratory Projects/Experiments', blank=True)
    prog_assignments = models.TextField('Programming Assignments', blank=True)
    class_time_spent = models.CharField(max_length=50, help_text="Please use time spent on each section in terms of credit hours: theory,problem analysis,solution design,ethical issues", default=',,,')
    oral_written_details =  models.CharField('Oral/Written Comm.', max_length=20, help_text="Fill for this statement: <emph>Every student is required to submit at least __ written reports of __ pages and to make __ presentations of __ minutes.</emph> Please use the format: number of reports,pages, number of presentations, minutes", default=',,,')

    def __unicode__(self): 
        fields = [self.course_name, "(" + str(self.semester) + " " + str(self.year) + ")"]
        desc_name = ' '.join(fields)
        return desc_name
    

class CourseOutline(models.Model):
    course = models.OneToOneField(Course)
    objectives = models.TextField()
    text_books = models.TextField()
    recommended_books = models.TextField()
    course_policies = models.TextField()
    other_information = models.TextField()
    
    def __unicode__(self): 
        fields = [str(self.course)]
        desc_name = ' '.join(fields)
        return desc_name


class WeekPlan(models.Model):
    WEEK_NUM_CHOICES = tuple([(str(x), str(x)) for x in range(1, 17)])

    course_outline = models.ForeignKey(CourseOutline)
    week_no = models.CharField(max_length=2, choices=WEEK_NUM_CHOICES)
    topics = models.TextField(default='Please insert topics here')
    
    def __unicode__(self): 
        fields = ['Week', self.week_no, str(self.course_outline)]
        desc_name = ' '.join(fields)
        return desc_name


class CourseLogEntry(models.Model):    
    LECTURE_NUM_CHOICES = tuple([(str(x), str(x)) for x in range(1, 60)])
    WEEK_NUM_CHOICES = tuple([(str(x), str(x)) for x in range(1, 17)])

    course = models.ForeignKey(Course)
    lecture_no = models.CharField(max_length=2, choices=LECTURE_NUM_CHOICES)
    week_no = models.CharField(max_length=2, choices=WEEK_NUM_CHOICES)

    lecture_date = models.DateField()
    
    # widget=forms.Textarea(attrs={'size', 30})
    duration = models.CharField(max_length=5)
    topics_covered = models.TextField()
    evaluation_instruments = models.TextField()
    
    def __unicode__(self): 
        fields = ['Lecture ', self.lecture_no, str(self.course)]
        desc_name = ' '.join(fields)
        return desc_name
# END Course  Stuff  ----------------------------------------------    


