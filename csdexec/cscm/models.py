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
    grade_distribution = models.TextField(blank=True)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)
    pre_reqs = models.TextField(blank=True)
    course_url = models.CharField('Course URL', max_length=256, blank=True)
    lab_projects = models.TextField('Laboratory Projects/Experiments', blank=True)
    prog_assignments = models.TextField('Programming Assignments', blank=True)
    class_time_spent_theory = models.CharField('Theory', max_length=50, blank=True) 
    class_time_spent_analysis = models.CharField('Analysis', max_length=50, blank=True)
    class_time_spent_design = models.CharField('Design', max_length=50, blank=True)
    class_time_spent_ethics = models.CharField('Ethics', max_length=50, blank=True)
    communciation_details_num_reports = models.CharField('Reports', help_text='Oral communication number of reports', max_length=20, blank=True)
    communciation_details_pages = models.CharField('Pages', help_text='Oral communication number of pages per report', max_length=20, blank=True)
    communciation_details_num_pres = models.CharField('Presentations', help_text='Oral communication number of presentations', max_length=20, blank=True)
    communciation_details_num_mins = models.CharField('Minutes', help_text='Oral communication minutes per presentation', max_length=20, blank=True)
    

    def __unicode__(self): 
        fields = [self.course_name, "(" + str(self.semester) + " " + str(self.year) + ")"]
        desc_name = ' '.join(fields)
        return desc_name
    

class CourseOutline(models.Model):
    course = models.OneToOneField(Course)
    objectives = models.TextField(blank=True)
    text_books = models.TextField(blank=True)
    recommended_books = models.TextField(blank=True)
    course_policies = models.TextField(blank=True)
    other_information = models.TextField(blank=True)
    
    def __unicode__(self): 
        fields = [str(self.course)]
        desc_name = ' '.join(fields)
        return desc_name


class WeekPlan(models.Model):
    WEEK_NUM_CHOICES = tuple([(str(x), str(x)) for x in range(1, 17)])

    course_outline = models.ForeignKey(CourseOutline)
    week_no = models.CharField(max_length=2)
    topics = models.TextField(default='Please insert topics here', blank=True)
    
    def __unicode__(self): 
        fields = ['Week', self.week_no, str(self.course_outline)]
        desc_name = ' '.join(fields)
        return desc_name


class CourseLogEntry(models.Model):    
    LECTURE_NUM_CHOICES = tuple([(str(x), str(x)) for x in range(1, 60)])
    WEEK_NUM_CHOICES = tuple([(str(x), str(x)) for x in range(1, 17)])

    course = models.ForeignKey(Course)
    lecture_no = models.CharField(max_length=2)
    week_no = models.CharField(max_length=2)

    lecture_date = models.DateField()
    
    # widget=forms.Textarea(attrs={'size', 30})
    duration = models.CharField(max_length=5, default=1.5)
    topics_covered = models.TextField()
    evaluation_instruments = models.TextField(blank=True)
    reading_materials = models.TextField(blank=True)
    other_activities = models.TextField(blank=True)
    contents_covered = models.TextField('Contents Covered?', blank=True, help_text='Leave blank for Yes; enter reason if not.')
        
    def __unicode__(self): 
        fields = ['Lecture ', self.lecture_no, str(self.course)]
        desc_name = ' '.join(fields)
        return desc_name
# END Course  Stuff  ----------------------------------------------    


