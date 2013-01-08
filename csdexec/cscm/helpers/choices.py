DESIGNATION_CHOICES = (
                ('Lecturer', 'Lecturer'),
                ('Assistant Professor', 'Assistant Professor'),
                ('Associate Professor', 'Associate Professor'),
                ('Professor', 'Professor'),
                )

CREDITS_CHOICES = (
                    (1, '1'), (2, '2'), (3, '3'), (4, '4')
                    )
 
SEMESTER_CHOICES = (
                    ('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')
                    )
COURSE_TYPE_CHOICES = (
                   ('Core', 'Core'), ('Elective', 'Elective'), ('No Credit', 'No Credit')
                   ) 


PUB_STATUS_CHOICES = (
                      ('Published', 'Published'), ('Submitted', 'Submitted'), ('Accepted', 'Accepted'), ('In Preparation', 'In Preparation'),
                    )

PUB_TYPE_CHOICES = (
                    ('Journal', 'Journal'), ('Conference', 'Conference'), ('Book' , 'Book'), ('Book Chapter', 'Book Chapter'),
                    )



EVENT_TYPE_CHOICES = (
                      ('Conference', 'Conference'), ('Workshop', 'Workshop'), ('Training', 'Training'), ('Project', 'Project'), ('Seminar', 'Seminar')
                      )


STUDENT_PROJECT_TYPES = (
                         ('FYP-I', 'FYP-I'), ('FYP-II', 'FYP-II'), ('Thesis-I', 'Thesis-I'), ('Thesis-II', 'Thesis-II')     
                         )


PROJECT_MILESTONES_CHOICES = (
                              ('Proposal and SWOT', 'Proposal and SWOT'),
                              ('Feasibility Plan', 'Feasibility Plan'),
                              ('Presentation 1', 'Presentation 1'),
                              ('Presentation 2', 'Presentation 2'),
                              ('Presentation 3', 'Presentation 3'),
                              ('Report', 'Report'),
                              ('Final Presentation', 'Final Presentation'),
                              ('Supervisor Evaluation', 'Supervisor Evaluation'),
                              )


PROJECT_MILESTONES_TYPE_CHOICES = (
                              ('Presentation', 'Presentation'), ('Document', 'Document'), ('Interaction', 'Interaction'),
                              )
