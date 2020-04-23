# coding: utf-8

### TODO: make single connect/disconnect for all variables of BERCsys and BERCcomp
### TODO: find rows with token from .mif

import os
from base import *

login = 'root'
password = 'bercut'

#### DECORATORS ####

def list_components(ip, path='/', login=login, password=password):
    """
        Get list of components by ip
    """
    cmd = 'ssx2 -c "connect {ip} {login} {password};ls \'{path}\';disconnect"'.format(ip=ip, login=login, password = password, path=path)
    return [x.strip() for x in os.popen(cmd).readlines() if x.strip() not in ['', None]]

def get_description(ip, ident, login=login, password=password):
    """
        Get description of component
    """
    desc = get_var(ip, ident, "/About/Description", login, password)
    return desc

def get_version(ip, ident, login=login, password=password):
    """
        Get version of component
    """
    version = get_var(ip, ident, "/About/Version", login, password)
    return version

def get_type(ip, ident, login=login, password=password):
    """
       Define type of component
    """
    desc = get_description(ip, ident, login, password)
    if desc:
        if desc.lower().find('slr') > -1:
            return 'SLR'
        if desc.lower().find('web') > -1:
            return 'WEB'
        if desc.lower().find('agent') > -1:
            return 'AGENT'
        if desc.lower().find('monitor') > -1:
            return 'MONITOR'
        if desc.lower().find('sysinfo') > -1:
            return 'INFO'
        if desc.lower().find('start') > -1:
            return 'SSM'
        else:
            return None
    return None

def get_status(ip, ident, login=login, password=password):
    """
        Get status
    """
    status = get_var(ip, ident, "/Status & Control/Active", login, password)
    if not status == None:
        status = int(status)
        if status == 1:
            return 'Active'
        else:
            if status == 0:
                return 'Stopped'
            else:
                return ''
    return None

if __name__ == "__main__":
    pass
    # print(get_var(ip='192.168.16.206',ident='UPSSMPServer', path='About/Solution/Version'))
    # print(get_status('192.168.6.147', '/UPSGenLoadSLR'))