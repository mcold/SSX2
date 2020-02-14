# coding: utf-8

"""
    Work with template file 
    Use as buffer with ssx2 results
"""

import os

def get_list(cmd):
    """
        Get list of data from temp-file
    """
    return [x.rstrip() for x in os.popen(cmd).readlines()]

def get_var(cmd):
    """
        Get variable of data from temp-file
    """
    return os.popen(cmd).read()
    

if __name__ == "__main__":
    cmd = r'ECHO %GOPATH%'
    print(get_var(cmd))
