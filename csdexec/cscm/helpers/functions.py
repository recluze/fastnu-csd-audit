from tl.rename.case import transform_sentence_case
from loadconfigs import *

def clean_string(instr):
    '''
    Clean string: change \n to <br /> and escape ampersand 
    ''' 
    cleaned_string = instr.replace('\n', '<br />').replace('&', '&amp;')
    if(get_config('clean_string_sentence_case') == 'True'): 
        cleaned_string = transform_sentence_case([cleaned_string])[0]
    
    return cleaned_string
