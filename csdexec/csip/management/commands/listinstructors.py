from django.core.management.base import BaseCommand, CommandError

from cscm.models import Instructor
from cscm.helpers.loadconfigs import get_config


from docx import *

import datetime 

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
    args = '<instructor_id>'
    help = 'Generate instructor cv for the specified instructor'
    def handle(self, *args, **options):
        ins = Instructor.objects.all().order_by('name') 
        for i in ins: 
            self.stdout.write(str (str(i.id) + '\t ' + str(i.name) + '\n'))
