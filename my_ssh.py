# coding: utf-8

"""
    Work with ssh
"""


import paramiko


def exec_ssh_command(ip, command, login='bercut', password='Rebus#7777'):
    """
        Execute command by ssh
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=login, password=password, port=22)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    client.close()
    return data
