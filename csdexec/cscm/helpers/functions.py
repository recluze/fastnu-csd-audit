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


def get_standard_grade(marks):
    if marks >= 90: return 'A+' 
    if marks >= 86: return 'A'
    if marks >= 82: return 'A-'
    if marks >= 78: return 'B+'
    if marks >= 74: return 'B'
    if marks >= 70: return 'B-'
    if marks >= 66: return 'C+'
    if marks >= 62: return 'C'
    if marks >= 58: return 'C-'
    if marks >= 54: return 'D+'
    if marks >= 50: return 'D'
    return 'F' 