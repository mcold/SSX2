"""
    Additional functionality
"""
import os
import sys
import my_ssx2
from contextlib import redirect_stdout


login = 'root'
password = 'bercut'
backup_dir_name = 'MIF'

def unmake_slash(path):
    return path.strip('/')

def make_slash(path):
    return '/{path}/'.format(path=unmake_slash(path))

def make_var(path):
    return '/{path}'.format(path=unmake_slash(path))

def unmake_ident(ident, path):
    ident = unmake_slash(ident)
    path = unmake_slash(path)
    if path[:len(ident)].upper() ==  ident.upper():
        path = path.lstrip(ident)
    return path

def get_var(ip, ident, path, login=login, password=password):
    """
        Get variable by path
    """
    
    path = unmake_ident(ident, path)
    l_path = [unmake_slash(ident)] + [x for x in path.split('/')[:-1] if x.strip() not in ['', None]]
    prove_path = ""
    l_elems = list()
    for sub_path in l_path:
        if not sub_path.upper() in l_elems and not len(l_elems) == 0: 
            return None
        
        prove_path = '/' + unmake_slash(prove_path + '/' + sub_path)
        l_elems = [x.upper().strip() for x in my_ssx2.list_components(ip=ip, path=prove_path)]
        if len(l_elems) == 0:
            return None
    
    if not path.split('/')[-1].upper() in [x.split(' ')[0] for x in l_elems]:
        return None

    l_cmd = list()
    l_cmd.append('connect {ip} {login} {password}'.format(ip=ip, login=login, password = password)) 
    path = unmake_ident(ident, path)
    l_cmd.append("varget '{identifier}{path}'".format(identifier=ident,path=make_var(path)))
    l_cmd.append('disconnect')
    cmd =  ";".join(l_cmd)
    cmd = 'ssx2 -c "' + cmd + '"'
    return os.popen(cmd).readline().strip()


def make_backup_dir():
    """
        Backup dir
    """
    if not os.path.exists(backup_dir_name):
        os.makedirs(backup_dir_name)

if __name__ == "__main__":
    print(unmake_ident('CMP_LWSAContainer_v3', '/CMP_LWSAContainer_v3/About/Description'))
    print(unmake_ident('CMP_LWSAContainer_v3', 'CMP_LWSAContainer_v3/About/Description'))
    print(unmake_ident('/CMP_LWSAContainer_v3/', 'CMP_LWSAContainer_v3/About/Description'))