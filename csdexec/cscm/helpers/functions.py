def clean_string(instr):
    '''
    Clean string: change \n to <br /> and escape ampersand 
    ''' 
    return instr.replace('\n', '<br />').replace('&', '&amp;')
