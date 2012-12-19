from django.core.management.base import BaseCommand, CommandError

from cscm.models import Instructor
from cscm.helpers.loadconfigs import get_config


from docx import *

def int_to_roman(input):
   """
   Convert an integer to Roman numerals.
   Source: http://code.activestate.com/recipes/81611-roman-numerals/
   """
   
   if type(input) != type(1):
      raise TypeError, "expected integer, got %s" % type(input)
   if not 0 < input < 4000:
      raise ValueError, "Argument must be between 1 and 3999"   
   ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
   nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
   result = ""
   for i in range(len(ints)):
      count = int(input / ints[i])
      result += nums[i] * count
      input -= ints[i] * count
   return result

class Command(BaseCommand): 
    def handle(self, *args, **options):
        s_c = 1
        all_borders = {'all': 
                       {
                        'color': 'auto', 'space' : '0', 'sz' : '1', 'val' : '' 
                         }
                       }
        # if __name__ == '__main__':        
        # Default set of relationshipships - these are the minimum components of a document
        relationships = relationshiplist()
    
        # Make a new document tree - this is the main part of a Word document
        document = newdocument()
        
        # This xpath location is where most interesting content lives 
        docbody = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
        
        # Append two headings and a paragraph
        docbody.append(heading('''Standard Format CV''', 1))   
    
        docbody.append(paragraph(int_to_roman(s_c) + '. PERSONAL INFORMATION'))
        s_c += 1
        # Append a table
        # get instructor information 
        i = Instructor.objects.all()[0]
        ip = i.instructorprofile
        
        docbody.append(table([['Name & Campus',
                               'DOB & Age',
                               'Designation',
                               'Date of appointment in the present position',
                               'Induction date in NU',
                               'Present scale and pay'
                               ],
                              [str(i.name) + ' (' + get_config('campus_name') + ')',
                               str(ip.date_of_birth),
                               ip.designation,
                               str(ip.current_position_appointment_date),
                               str(ip.joining_date),
                               str(ip.gross_pay)]
                              ], borders=all_borders))
    
    
    
        # Create our properties, contenttypes, and other support files
        coreprops = coreproperties(title='Instructor CV', subject='A practical example of making docx from Python', creator='Mike MacCana', keywords=['python', 'Office Open XML', 'Word'])

        docbody.append(paragraph(int_to_roman(s_c) + '. ACADEMIC RECORD (in reverse chronological order, highest degree first'))
        s_c += 1
        ies = i.instructoreducation_set.filter(instructor=i).order_by('-year')
        
        tbdata = [['Degree',
                               'Year Passed',
                               'University/Board',
                               'Institution',
                               'Division/Grade',
                               'Area of Specialization/Main Subject(s)'
                               ]]
        
        for ie in ies: 
            tbdata.append([ie.degree, 
                       ie.year, 
                       ie.university, 
                       ie.institution,
                       ie.grade, 
                       ie.field])
        
        tb = table(tbdata)
        docbody.append(tb)
    
        
        
        # FINALZE DOCUMENT 
        
        appprops = appproperties()
        _contenttypes = contenttypes()
        _websettings = websettings()
        _wordrelationships = wordrelationships(relationships)
        
        # Save our document
        savedocx(document, coreprops, appprops, _contenttypes, _websettings, _wordrelationships, 'instructor-cv.docx')
        self.stdout.write('Done\n')
