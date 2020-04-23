# coding: utf-8

"""
    Executor of program
"""

from berc import Host, Comp, SLR, Web
from base import *

ip = '192.168.16.206'

def run():
    b = SLR('192.168.16.206', 'UPSSMPServer')
    b.get_profile_source()
    print(b.profile_src)
    print(b.desc)
    b.ls('/ESM_PROFILE/')
    print(b.ls_dir)

def run_host():
    h = Host(ip='192.168.6.145')
    h.find_web(ip='192.168.6.146', port='7797')

def run_slr():
    slr = SLR('192.168.16.206', 'UPSSMPServer')
    slr.backup_group('About')

def test_get_var():
    res = get_var(ip='192.168.6.145', ident='/UPSTerminalSMP', path='/UPSTerminalSMP/Security/Providers/SLR/LBGroup000/FTGroup000/Server000/Configuration/Address')
    print(res)

def run_web():
    w = Web('192.168.6.145', 'UPSTerminalSMP')
    w.find_slr()

if __name__ == "__main__":
    run_slr()
    # make_dir()