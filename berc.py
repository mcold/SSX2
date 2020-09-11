# coding: utf-8

"""
   Contain components for work with components BERCunica
"""

import my_ssx2
import os
import temp
import definit
import time
from base import *

login = 'root'
password = 'bercut'
sep_print = ': '
sep = '/'

class Stend:
    """
        Stend connected components
    """
    obj_list = []

    def __init__(self):
        pass

    def add(self, obj):
        """
            Add object in stend
        """
        self.obj_list.append(obj)

    def load(self, name):
        """
            Load stend
        """
    
    def restart(self):
        """
            Restart stend's components
        """
        for comp in self.obj_list: comp.restart()
        
    
    def save(self, name):
        """
            Save stend
        """

    def start(self):
        for comp in self.obj_list: comp.start()


    def stop(self):
        for comp in self.obj_list: comp.stop()

class Comp:
    """
        BERCunica component
    """
    ls_dir = list()
    start_time = None
    stop_time = None
    status = None

    def __init__(self, ident):
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
        self.version = my_ssx2.get_version(ip, ident)
    
    def __repr__(self):
        return "{ip} {type} {ident}".format(ip=self.ip, type=self.__type__, ident=self.ident)

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
            cmd = 'ssx2 -c "' + cmd + '"'
            var = os.popen(cmd).readline().strip()
        except:
            pass

    def stop(self, path='/Startup/Activity'):
        """
            Stop component
        """
        try:
            l_cmd = list()
            l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
            l_cmd.append("set '/{identifier}{path}' False".format(identifier=self.ident,path=path))
            l_cmd.append('disconnect')
            cmd =  ";".join(l_cmd)
            cmd = 'ssx2 -c "' + cmd + '"'
            var = os.popen(cmd).readline().strip()
        except:
            pass

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
            cmd = 'ssx2 -c "' + cmd + '"'
            var = temp.get_var()
        except:
            pass
        return var


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
            cmd = 'ssx2 -c "' + cmd + '"'
            res = os.popen(cmd)
        except:
            pass
        return var
    
    def backup(self):
        """
            Make .mif-backup of component
        """
        dir_name = self.ident + '__' + self.ip
        cur_time = definit.get_cur_time()
        make_backup_dir()
        try:
            l_cmd = list()
            l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
            l_cmd.append("export -s '{comp_name}' {dir}{backup_name}.mif".format(comp_name=self.ident, dir=backup_dir_name + sep, backup_name=self.ident + '_' + cur_time))
            l_cmd.append('disconnect')
            cmd =  ";".join(l_cmd)
            cmd = 'ssx2 -c "' + cmd + '"'
            os.popen(cmd)
        except:
            pass
    
    def backup_group(self, path):
        """
            Make .mif-backup of group
        """
        dir_name = self.ident + make_var(path)
        cur_time = definit.get_cur_time()
        make_backup_dir()
        
        l_cmd = list()
        l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
        l_cmd.append("export -s '{comp_name}' {dir}{backup_name}.mif".format(comp_name=dir_name, dir=backup_dir_name + sep, backup_name=dir_name.replace(sep, '_') + '_' + cur_time))
        l_cmd.append('disconnect')
        cmd =  ";".join(l_cmd)
        cmd = 'ssx2 -c "' + cmd + '"'
        os.popen(cmd)

    def ls(self, path='/'):
        """
            Get content of directory
        """
        d = dict()
        
        path = '/{ident}/{path}'.format(ident=self.ident, path=path.strip('/'))
        self.ls_dir = [x for x in my_ssx2.list_components(self.ip, path) if x.strip() not in ['', None]]
    
    def get_var(self, path, login=login, password=password):
        """
            Get variable by path
        """
        path = unmake_ident(self.ident, path)
        l_path = [unmake_slash(self.ident)] + [x for x in path.split('/')[:-1] if x.strip() not in ['', None]]
        prove_path = ""
        l_elems = list()
        for sub_path in l_path:
            if not sub_path.upper() in l_elems and not len(l_elems) == 0: 
                return None
            
            prove_path = '/' + unmake_slash(prove_path + '/' + sub_path)
            l_elems = [x.upper().strip() for x in my_ssx2.list_components(ip=self.ip, path=prove_path)]
            if len(l_elems) == 0:
                return None
        
        if not path.split('/')[-1].upper() in [x.split(' ')[0] for x in l_elems]:
            return None

        l_cmd = list()
        l_cmd.append('connect {ip} {login} {password}'.format(ip=self.ip, login=login, password = password)) 
        path = unmake_ident(self.ident, path)
        l_cmd.append("varget '{identifier}{path}'".format(identifier=self.ident,path=make_var(path)))
        l_cmd.append('disconnect')
        cmd =  ";".join(l_cmd)
        cmd = 'ssx2 -c "' + cmd + '"'
        return os.popen(cmd).readline().strip()

class SLR(Comp):
    """
        SLR
    """
    __type__ = 'SLR'
    log = None
    profile_type = None
    profile_src = None
    port = None
    status = None
    
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
        self.get_port()
        self.get_status()
    
    def get_profile_type(self):
        """
            Get profile type
        """
        self.profile_type = my_ssx2.get_var(self.ip, self.ident, "/ProfileLoader/Configuration/LoaderType")

    def get_profile_source(self):
        self.get_profile_type()
        if self.profile_type == 'XML':
            self.profile_src = my_ssx2.get_var(self.ip, self.ident, "/ProfileLoader/XML/Configuration/ProfileSources")
        if self.profile_type == 'DB':
            self.profile_src = self.get_var("/ProfileLoader/DB/Configuration/ConnectionString")
        
    def get_port(self):
        self.port = my_ssx2.get_var(self.ip, self.ident, "/Security/Users/Agent-Gateway/Port")

    def get_webs(self):
        con_path = make_slash(self.ident + '/Statistics/AG/')
        l_connects = my_ssx2.list_components(ip=self.ip, path=con_path)
        l_ips = []
        l_webs = []
        for con_name in l_connects:
            try:
                c_path = con_path + con_name + '/' + 'Address'
                address = self.get_var(path=c_path).split(':')[0]
                l_ips.append(address)
            except AttributeError:
                pass
        l_ips = list(set(l_ips))
        l_agents = []
        for ip in l_ips:
            h = Host(ip=ip)
            l_new_agents = h.find(ip=self.ip, port=self.port, type="WEB")
            l_agents = l_agents + l_new_agents
        self.agents = l_agents
        for agent in self.agents:
            print(agent)

    def find_web(self, ip):
        h = Host(ip=ip)
        h.find(ip=self.ip, port=self.port, type="WEB")

    def get_log(self):
        self.log = my_ssx2.get_var(self.ip, self.ident, "/Configuration/Log")

    def set_log(self, log_number):
        """
           Set log level
        """
        self.set_var('/Configuration/Log', log_number)
        self.log = log_number
    
    def get_start_time(self):
        self.start_time = my_ssx2.get_var(self.ip, self.ident, "/Status & Control/StartTime")
        print('START TIME: ' + str(self.start_time))
    
    def get_stop_time(self):
        self.stop_time = my_ssx2.get_var(self.ip, self.ident, "/Status & Control/StopTime")
        print('STOP TIME: ' + str(self.stop_time))

    def get_pid(self):
        self.pid = my_ssx2.get_var(self.ip, self.ident, "/Status & Control/PID")
    
    def get_status(self):
        if my_ssx2.get_var(self.ip, self.ident, "/Status & Control/Active")=='1':
            self.status = 'Active'
        else:
            self.status = 'Not active'
        
    def exec(self, command):
        """
            Execute command
        """
        self.set_var('/Status & Control/Console-Command', command)

    def restart(self):
        """
            Restart server
        """
        self.set_log(3)
        super().restart()
        self.set_log(6)

class Web(Comp):
    """
        Agent
    """
    __type__ = 'WEB'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)
        self.get_slr_ip()
        self.get_slr_port()
        self.get_agent_id()
        self.get_agent_type()

    def get_slr_ip(self):
        self.slr_ip = my_ssx2.get_var(self.ip, self.ident, "/Security/Providers/SLR/LBGroup000/FTGroup000/Server000/Configuration/Address")
    
    def get_slr_port(self):
        self.slr_port = my_ssx2.get_var(self.ip, self.ident, "/Security/Providers/SLR/LBGroup000/FTGroup000/Server000/Configuration/Port")

    def get_agent_id(self):
        self.agent_id = my_ssx2.get_var(self.ip, self.ident, "/Security/Providers/SLR/LBGroup000/FTGroup000/Server000/Configuration/AgentID")
    
    def get_agent_type(self):
        self.agent_type = my_ssx2.get_var(self.ip, self.ident, "/Security/Providers/SLR/LBGroup000/FTGroup000/Server000/Configuration/AgentID")

    def find_slr(self):
        h = Host(ip=self.slr_ip)
        h.find(ip=self.slr_ip, port=self.slr_port, type="SLR")

class Agent(Comp):
    """
        Agent
    """
    __type__ = 'Agent'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)


class SSM(Comp):
    """
        StartStop Manager
    """
    __type__ = 'SSM'
    def __init__(self, ip, ident):
        Comp.__init__(self, ip, ident)

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

class Host:
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
            self.add(ip=ip,ident=comp)
            

    def add(self, comp):
        """
            Add component to system
        """
        self.comps.append(comp)
    
    def add(self, ip, ident):
        try:
            type = my_ssx2.get_type(ip, ident)
            if type == 'SLR':
                self.comps.append(SLR(ip, ident))
            if type == 'WEB':
                self.comps.append(Web(ip, ident))
            if type == 'AGENT':
                self.comps.append(Agent(ip, ident))
            if type == 'MONITOR':
                self.comps.append(Monitor(ip, ident))
            if type == 'INFO':
                self.comps.append(SysInfo(ip, ident))
            if type == 'SSM':
                self.comps.append(SSM(ip, ident))
        except:
            pass

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
            print(sep_print.join([c.ident, c.__type__, c.desc, c.status]))
    
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
            print(sep_print.join([l]))

    def find(self, ip, port, type):
        l = []
        if type == 'WEB':
            for comp in self.comps:
                if comp.__type__ == "WEB":
                    if comp.slr_ip == ip and comp.slr_port == port:
                        l.append(comp)
            return l
        if type == "SLR":
            if comp.__type__ == "WEB":
                if comp.ip == ip and comp.port == port:
                    pass