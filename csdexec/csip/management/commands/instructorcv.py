from django.core.management.base import BaseCommand, CommandError

from cscm.models import Instructor
from cscm.helpers.loadconfigs import get_config


from docx import *


htmlCodes = (
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    ("'", '&#39;'),
)
def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))

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

def add_section_header(docbody, counter, header):
    docbody.append(paragraph(' '))
    docbody.append(paragraph(int_to_roman(counter) + '. ' + header))
    return counter + 1

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
    
        s_c = add_section_header(docbody, s_c, 'PERSONAL INFORMATION')
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
    
    
    
        # education 
        s_c = add_section_header(docbody, s_c, 'ACADEMIC RECORD (in reverse chronological order, highest degree first')
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
    
        # Employment record 
        s_c = add_section_header(docbody, s_c, 'EMPLOYMENT RECORD (starting from most recent one')
        iems = i.instructoremployment_set.filter(instructor=i).order_by('-start_date')
        tbdataem = [['Position/Job Title',
                               'Department',
                               'Years of Experience',
                               '',
                               'Nature of Duties/Experience',
                               ]] # Can't merge right now :( 
        
        for iem in iems: 
            tbdataem.append([iem.position,
                       iem.organization,
                       str(iem.start_date),
                       str(iem.end_date),
                       str(iem.job_desc).replace('\n', ' ').replace('\r', ' ')])
        tbem = table(tbdataem)
        docbody.append(tbem)

        s_c = add_section_header(docbody, s_c, 'ACADEMIC AWARDS/DISTINCTIONS/HONOURS')
        tbem = table([[ip.awards]])
        docbody.append(tbem)

        s_c = add_section_header(docbody, s_c, 'PROFESSIONAL MEMBERSHIP/AFFILIATIONS & ACTIVITIES (e.g. editor of journal, academic bodies)')
        tbem = table([[ip.memberships]])
        docbody.append(tbem)

        # research and consultancy projects
        s_c = add_section_header(docbody, s_c, 'RESEARCH/CONSULTANCY PROJECTS (Include project title, funding agency, date of award and duration and total amount of award; please specify whether you were principal investigator (PI) or co-Investigator)')
        ics = i.instructorconsultancy_set.filter(instructor=i).order_by('-date')
        
        c_str = '' 
        inner_counter = 1
        tbdataem = []
        for ic in ics: 
            c_str = str(inner_counter) + '. ' + ic.description + '. ' + ic.organization 
            inner_counter += 1
            tbdataem.append([c_str.replace('\n', ' ').replace('\r', ' ')])
            
        tbem = table(tbdataem)
        docbody.append(tbem)

        # publications with impact factor 
        s_c = add_section_header(docbody, s_c, 'RESEARCH PUBLICATIONS, BOOKS AND BOOK CHAPTERS (Starting from the most recent one including publication during the past 5 years')
        docbody.append(paragraph(' '))
        docbody.append(paragraph('A. List of Publications in journals having IF (Impact Factor)'))
        ipwis = i.instructorpublication_set.exclude(pub_type='Conference').exclude(impact_factor='').filter(status='Published').order_by('-pub_date')
        tbdataem = [['S.No.',
                               'Name of Author(s)',
                               'Complete Name. Address of Journal',
                               'Title of Publication',
                               'Vol and Page No.',
                               'Year Published',
                               'Impact Factor' 
                               ]]  
        inner_counter = 1
        for ipwi in ipwis: 
            
            ipwi_vol = ipwi.volume            
            if ipwi.pages != '':
                ipwi_vol += ' pp.' + ipwi.pages
                
            ipwi_journal = ipwi.journal
            if ipwi.journal_address != '':
                ipwi_journal += '. (' + ipwi.journal_address + ')'
                
            tbdataem.append([str(inner_counter),
                       ipwi.author_list,
                       ipwi_journal,
                       ipwi.title,
                       ipwi_vol,
                       str(ipwi.pub_date.year),
                       str(ipwi.impact_factor)
                       ])
            inner_counter += 1
            
        tbem = table(tbdataem)
        docbody.append(tbem)
        
        
        # journals with no impact factor 
        docbody.append(paragraph(' '))
        docbody.append(paragraph('B. List of Publications in journals having no IF (Impact Factor)'))
        ipwis = i.instructorpublication_set.exclude(pub_type='Conference').filter(impact_factor='').filter(status='Published').order_by('-pub_date')
        tbdataem = [['S.No.',
                               'Name of Author(s)',
                               'Name of Journal',
                               'Categorized by HEC as W/X/Y/Z**',
                               'Vol. No.',
                               'Title of Publication',
                               'Year Published' 
                               ]]  
        inner_counter = 1
        for ipwi in ipwis: 
            
            ipwi_vol = ipwi.volume            
            if ipwi.pages != '':
                ipwi_vol += ' pp.' + ipwi.pages
                
            ipwi_journal = ipwi.journal
            if ipwi.journal_address != '':
                ipwi_journal += '. (' + ipwi.journal_address + ')'
                
            tbdataem.append([str(inner_counter),
                       ipwi.author_list,
                       ipwi_journal,
                       ipwi.hec_cat,
                       ipwi_vol,
                       ipwi.title,
                       str(ipwi.pub_date.year),
                       ])
            inner_counter += 1
            
        tbem = table(tbdataem)
        docbody.append(tbem)
        
        # submitted papers but not yet accepted
        docbody.append(paragraph(' '))
        docbody.append(paragraph('C. Papers submitted but not yet published (Submitted/pending acceptance/accepted)'))
        ipwis = i.instructorpublication_set.exclude(pub_type='Conference').exclude(impact_factor='').exclude(status='Published').order_by('-pub_date')
        tbdataem = [['S.No.',
                               'Name of Author(s)',
                               'Complete Name. Address of Journal',
                               'Title of Publication',
                               'Impact Factor',
                               'Comments' 
                               ]]  
        inner_counter = 1
        for ipwi in ipwis: 
            
            ipwi_journal = ipwi.journal
            if ipwi.journal_address != '':
                ipwi_journal += '. (' + ipwi.journal_address + ')'
                
            tbdataem.append([str(inner_counter),
                       ipwi.author_list,
                       ipwi_journal,
                       ipwi.title,
                       str(ipwi.impact_factor),
                       str(ipwi.status) 
                       ])
            inner_counter += 1
            
        tbem = table(tbdataem)
        docbody.append(tbem)
        
        
        # conference
        docbody.append(paragraph(' '))
        docbody.append(paragraph('C. Papers submitted but not yet published (Submitted/pending acceptance/accepted)'))
        ipcs = i.instructorpublication_set.filter(pub_type='Conference').order_by('-pub_date')
        c_str = '' 
        inner_counter = 1
        tbdataem = []
        for ipc in ipcs:    
            c_str = str(inner_counter) + '. ' + ipc.get_conf_citation() 
            inner_counter += 1
            tbdataem.append([c_str.replace('\n', ' ').replace('\r', ' ')])
                
        tbem = table(tbdataem)
        docbody.append(tbem)
            
        # FINALZE DOCUMENT 
        
        # Create our properties, contenttypes, and other support files
        coreprops = coreproperties(title='Instructor CV', subject='A practical example of making docx from Python', creator='Mike MacCana', keywords=['python', 'Office Open XML', 'Word'])
        appprops = appproperties()
        _contenttypes = contenttypes()
        _websettings = websettings()
        _wordrelationships = wordrelationships(relationships)
        
        # Save our document
        savedocx(document, coreprops, appprops, _contenttypes, _websettings, _wordrelationships, 'instructor-cv.docx')
        self.stdout.write('Done\n')
