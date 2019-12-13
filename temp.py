# coding: utf-8

"""
    Work with template file 
    Use as buffer with ssx2 results
"""

f_temp = 'temp2.txt'
import os

def get_list():
    """
        Get list of data from temp-file
    """
    global f_temp
    with open(f_temp, 'r') as f:
        l = [x.strip() for x in f.readlines() if x.strip() not in ['']]
    return l

def get_var():
    """
        Get variable of data from temp-file
    """
    global f_temp
    with open(f_temp, 'r') as f:
        res = f.readline().strip()
    os.remove(f_temp)
    return res
    

if __name__ == "__main__":
    print(get_var())
