#!/usr/bin/python
from subprocess import Popen, PIPE
from re import search


def GetUsers(host):
    """SSH to host and retrieve all users with a valid shell"""
    monitored_users = []
    user_list = str(Popen(['ssh', host, 'cat', '/etc/passwd'], stdout=PIPE
                          ).stdout.read().strip('\n').split('\n'))
    no_shell = (r'/bin/false$|/sbin/nologin$|/bin/sync$|/sbin/halt$' +
                '|/sbin/shutdown$')
    for user in user_list:
        if not search(no_shell, user):
            monitored_users.append(user.split(':')[0])
    return monitored_users


def GetGroups(host):
    """SSH to host and retrieve desired groups"""
    groups = []
    monitored_groups = []
    m_groups = open('monitored_groups.list', 'r+b')
    host_groups = str(Popen(['ssh', host, 'cat', '/etc/groups'], stdout=PIPE
                            ).stdout.read().strip('\n').split('\n'))
    for line in m_groups:
        groups.append(str(line).strip('\n'))
    for group in groups:
        r_exp = '^' + group + '.+\d{4,6}:'
        for host_group in host_groups:
            if search(r_exp, host_group):
                monitored_groups.append(host_group)
    return monitored_groups
