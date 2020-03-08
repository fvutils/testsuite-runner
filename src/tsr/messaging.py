'''
Created on Mar 7, 2020

@author: ballance
'''

_verbosity = 0

def set_verbosity(verbosity):
    _verbosity = verbosity
    
def get_verbosity():
    return _verbosity

def note(msg):
    print("Note: " + msg)
    
def verbose_note(msg, verbosity=1):
    if verbosity >= _verbosity:
        print("Note: " + msg)
        
def warn(msg):
    print("Warning: " + msg)
    
def verbose_warn(msg, verbosity=1):
    if verbosity >= _verbosity:
        print("Warning: " + msg)
        
def error(msg):
    print("Error: " + msg)
    
def fatal(msg):
    print("Fatal: " + msg)
    
    