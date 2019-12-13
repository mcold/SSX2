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
    try:
        os.mkdir(dir_name)
    except:
        pass

def get_cur_time():
    """
        Get current time
    """
    t = time.localtime()
    t_str = "_".join([str(x) for x in [t.tm_min, t.tm_hour, t.tm_mday, t.tm_mon, t.tm_year]])
    return t_str