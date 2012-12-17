from tl.rename.case import transform_sentence_case
from loadconfigs import *

# for parsing bibtex
from zs.bibtex.parser import parse_string


def clean_string(instr, change_case=True):
    '''
    Clean string: change \n to <br /> and escape ampersand 
    ''' 
    cleaned_string = instr.replace('\n', '<br />').replace('&', '&amp;')
    if(get_config('clean_string_sentence_case') == 'True' and change_case): 
        cleaned_string = transform_sentence_case([cleaned_string])[0]
    
    return cleaned_string




def get_pub_string(biblio):
    biblio = parse_string(biblio)
    for i in biblio: 
        art = biblio[i]
        break 
    
    author_list = ''
    for auth in art['author']: 
        author_list += str(auth) + ', '
        
    author_list.rstrip(', ')
    str_rep = author_list + '. "' + str(art['title']) + '". ' + str(art['journal']) + '. ' + str(art['year']) 
    return str_rep
