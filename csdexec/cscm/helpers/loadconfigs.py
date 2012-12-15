import json
import os 

def get_config(varname):
    filepath = os.path.dirname(__file__)
    f = open(filepath + '/csdexec.settings.json')
    confs = json.load(f)
    return confs[varname]
