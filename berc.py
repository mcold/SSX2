# coding: utf-8

#### TODO: decorator - connect / disconnect
#### TODO: fix last time of actualization and periodically look to
#### TODO: write configuration of BERCsys (and read) into file
#### TODO: backup configuration (.mif and current OOP-structure)
# /UPS_MA_MP/Status & Control/StopTime 
#### TODO: if StopTime > at component -> recheck parameters, else don't do anything

"""
   Contain components for work with components BERCunica
"""

import my_ssx2
from temp import f_temp
import os
import temp
import definit
import time

login = 'root'
password = 'bercut'
sep = ': '

class Comp:
    """
        BERCunica component
    """

    def __init__(self):
        """
            Initialize object
        """
        self.ident = ident
    
    def __init__(self, ip, ident):
        """
            Initialize by ip and identification
        """
        self.ip = ip
        self.ident = ident
        self.desc = my_ssx2.get_description(ip, ident)
        self.status = my_ssx2.get_status(ip, ident)
    
    def get_type(self):
        return self.__type__

    def restart(self):
        """
            Restart component
        """
        self.stop()
        self.start()

    def start(self, path='/Startup/Activity'):
        """
            Start component
        """
        try:
            l_cmd = list()
            l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
            l_cmd.append("set '/{identifier}{path}' True".format(identifier=self.ident,path=path))
            l_cmd.append('disconnect')
            cmd =  ";".join(l_cmd)
            print(cmd)
            res = os.system('ssx2 -c "' + cmd + '"' + '> {res_file}'.format(res_file=f_temp))
            var = temp.get_var()
        except:
            pass

    def stop(self, path='/Startup/Activity'):
        """
            Stop component
        """
        # try:
        l_cmd = list()
        l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
        l_cmd.append("set '/{identifier}{path}' False".format(identifier=self.ident,path=path))
        l_cmd.append('disconnect')
        cmd =  ";".join(l_cmd)
        print(cmd)
        res = os.system('ssx2 -c "' + cmd + '"' + '> {res_file}'.format(res_file=f_temp))
        # var = temp.get_var()
        # except:
        #     pass
    
    def get_var(self, path):
        """
            Get variable by path
        """
        var = None
        try:
            l_cmd = list()
            l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
            l_cmd.append("varget '/{identifier}{path}'".format(identifier=self.ident,path=path))
            l_cmd.append('disconnect')
            cmd =  ";".join(l_cmd)
            print(cmd)
            res = os.system('ssx2 -c "' + cmd + '"' + '> {res_file}'.format(res_file=f_temp))
            var = temp.get_var()
        except:
            pass
        return var
    
    def get_var_list(self, path):
        """
            Get variables by path
        """
        # TODO: to write
    
    def get_list(self, path):
        """
           Get variables + groups by path
        """
        # TODO: to write

    def set_var(self, path, value):
        """
            Get variable by path
        """
        var = None
        try:
            l_cmd = list()
            l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
            l_cmd.append("set '/{identifier}{path}' {value}".format(identifier=self.ident,path=path, value=value))
            l_cmd.append('disconnect')
            cmd =  ";".join(l_cmd)
            print(cmd)
            res = os.system('ssx2 -c "' + cmd + '"' + '> {res_file}'.format(res_file=f_temp))
            var = temp.get_var()
        except:
            pass
        return var
    
    def backup():
        """
            Make .mif-backup of component
        """
        # make dir by identifier + ip -- if not exists
        dir_name = self.ident + '__' + self.ip
        cur_time = definit.get_cur_time()
        

        try:
            l_cmd = list()
            l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
            l_cmd.append("export -s '{comp_name}' {backup_name}.mif".format(comp_name=self.ident, backup_name=self.ident+'_' + cur_time))
            l_cmd.append('disconnect')
            cmd =  ";".join(l_cmd)
            print(cmd)
            res = os.system('ssx2 -c "' + cmd + '"' + '> {res_file}'.format(res_file=f_temp))
            var = temp.get_var()
        except:
            pass
        return var


class SLR(Comp):
    """
        SLR
    """
    __type__ = 'SLR'
    profile_type = None
    profile_src = None
    
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
    
    def get_profile_type(self):
        """
            Get profile type
        """
        # TODO: why doesn't work???
        # self.profile_type = self.get_var("/ProfileLoader/Configuration/LoaderType")
        self.profile_type = my_ssx2.get_var(self.ip, self.ident, "/ProfileLoader/Configuration/LoaderType")

    def get_profile_source(self):
        self.get_profile_type()
        if self.profile_type == 'XML':
            # TODO: why doesn't work???
            # self.profile_src = self.get_var("/ProfileLoader/XML/Configuration/ProfileSources")
            self.profile_src = my_ssx2.get_var(self.ip, self.ident, "/ProfileLoader/XML/Configuration/ProfileSources")
        if self.profile_type == 'DB':
            # TODO: why doesn't work???
            self.profile_src = self.get_var("/ProfileLoader/DB/Configuration/ConnectionString")
            # self.profile_src = my_ssx2.get_var(self.ip, self.ident, "/ProfileLoader/DB/Configuration/ConnectionString")
        else:
            pass
    
    def set_log_level(self, level):
        """
           Set log level
        """
        self.set_var('/Configuration/Log', level)
    

class Web(Comp):
    """
        Agent
    """
    __type__ = 'Agent'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
    
    def __init__(self):
        Comp.__init__(self)


class Agent(Comp):
    """
        Agent
    """
    __type__ = 'Agent'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
    
    def __init__(self):
        Comp.__init__(self)

class SSM(Comp):
    """
        StartStop Manager
    """
    __type__ = 'SSM'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
    
    def __init__(self):
        Comp.__init__(self)


class SysInfo(Comp):
    """
        SysInfo
    """
    __type__ = 'SysInfo'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
    
    def __init__(self):
        Comp.__init__(self)

class Monitor(Comp):
    """
        Monitor
    """
    __type__ = 'Monitor'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
    
    def __init__(self):
        Comp.__init__(self)

class BercSys:
    """
        BERCunica system
    """
    comps = list()
    name = ""

    def __init__(self, ip):
        """
            Define objects by ip
        """
        l = my_ssx2.list_components(ip)
        for comp in l:
            try:
                c = Comp(ip, comp)
                self.comps.append(c)
            except:
                pass

    def add(self, comp):
        """
            Add component to system
        """
        self.comps.append(comp)
    
    def add(self, ip, ident):
        type = my_ssx2.get_type(ip, ident)
        if type == 'SLR':
            b = SLR(ip, ident)
        if type == 'WEB':
            b = Web(ip, ident)
        if type == 'AGENT':
            b = Agent(ip, ident)
        if type == 'MONITOR':
            b = Monitor(ip, ident)
        if type == 'INFO':
            b = SysInfo(ip, ident)
        if type == 'SSM':
            b = SSM(ip, ident)
    
    def get_comp(self, num):
        """
            Get component by number
        """
        num = num + 1
        return self.comps[num]

    
    def comp_desc(self):
        """
            Print components description
        """
        for c in self.comps:
            print(': '.join([c.ident, c.__type__, c.desc]))
    
    def comp_status(self):
        """
            Print components status
        """
        for c in self.comps:
            print(sep.join([c.ident, c.__type__, c.desc, c.status]))
    
    def comp_full(self):
        """
            Full components info
        """
        for c in self.comps:
            l = list()
            l.append(c.ip)
            l.append(c.ident)
            l.append(c.__type__)
            l.append(c.desc)
            l.append(c.status)
            print(sep.join([l]))
