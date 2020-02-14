# coding: utf-8

"""
    Executor of program
"""

from berc import BercSys, Comp, SLR

ip = '192.168.16.206'

def run():
    b = SLR('192.168.6.147', 'UPSGenLoadMP')
    b.get_profile_source()


if __name__ == "__main__":
    run()