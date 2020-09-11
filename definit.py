# coding: utf-8

"""
    Functionality module for bercut-components
"""

import os
import sys
import time


def make_dir(dir_name):
    """
        Make directory
    """
    if not os.path.exists(dir_name): os.mkdir(dir_name)

def get_cur_time():
    """
        Get current time
    """
    t = time.localtime()
    t_str = "_".join([str(x) for x in [t.tm_min, t.tm_hour, t.tm_mday, t.tm_mon, t.tm_year]])
    return t_str

def def_dir_var(l_args):
    """
        Define if element is directory or variable
    """
    l_gr = list()
    l_var = list()
    cat = ''
    for arg in l_args:
        if arg.find(' ') > 0:
            l_var.append(arg)
        else:
            l_gr.append(arg)
    return l_gr, l_var


if __name__ == "__main__":
    pass