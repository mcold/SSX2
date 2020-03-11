# coding: utf-8


### TODO: decorator get data from temp-fiel + delete temp-file
### TODO: make single connect/disconnect for all variables of BERCsys and BERCcomp
### TODO: find rows with token from .mif


import os
import temp

f_temp = 'temp2.txt'
login = 'root'
password = 'bercut'

#### DECORATORS ####

def del_temp_file(func):
    def wrapper(*args):
        func(*args)
        # os.remove(f_temp)
    return wrapper



def get_var(ip, ident, path, login=login, password=password):
    """
        Get variable by path
    """
    var = None
    try:
        l_cmd = list()
        l_cmd.append('connect {ip} {login} {password}'.format(ip=ip, login=login, password = password)) 
        # l_cmd.append("varget '{identifier}{path}'".format(identifier=ident,path=path))
        l_cmd.append("varget '{identifier}{path}'".format(identifier=ident,path=path))
        l_cmd.append('disconnect')
        cmd =  ";".join(l_cmd)
        cmd = 'ssx2 -c "' + cmd + '"'
        var = temp.get_var(cmd)
    except:
        pass
    return var.strip()


def get_description(ip, ident, login=login, password=password):
    """
        Get description of component
    """
    desc = get_var(ip, ident, "About/Description", login, password)
    return desc


def get_type(ip, ident, login=login, password=password):
    """
       Define type of component
    """
    desc = get_description(ip, ident, login, password)
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

def get_status(ip, ident, login=login, password=password):
    """
        Get status
    """

    status = int(get_var(ip, ident, "/Status & Control/Active", login, password))
    if status == 1:
        return 'Active'
    else:
        if status == 0:
            return 'Stopped'
        else:
            return ''


# @del_temp_file
def list_components(ip, path='/'):
    """
        Get list of components by ip
    """
    ### TODO: change root & bercut on global variables
    cmd = 'ssx2 -c "connect {ip} root bercut;ls {path};disconnect"'.format(ip=ip, path=path)
    # os.system('ssx2 -c "connect {ip} root bercut;ls {path};disconnect" > {res_file}'.format(ip=ip, path=path, res_file = f_temp))
    l = temp.get_list(cmd)
    # os.remove(f_temp)
    return l

if __name__ == "__main__":
    # res = get_description('192.168.6.147', '/UPSGenLoadSLR/')    
    # print('Description: ' + res)
    # l = list_components('192.168.6.147', '/')
    # print(l)
    print(get_status('192.168.6.147', '/UPSGenLoadSLR'))