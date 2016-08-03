#!/usr/bin/env/python

## 除了以下使用到的标准库模组，还有很多其它有用的标准模组：subprocess、ConfigParser、readline和curses。

from __future__ import print_function
from collections import OrderedDict
import pprint
import platform
from collections import namedtuple
import os
import glob
import re
import pwd
import argparse

platform.uname() # linux uname cmd

platform.system() # linux
 
platform.release() # linux release info

platform.linux_distribution() # linux release detail info

platform.architecture() # system architecture bit and及python can execute format tuple

""" print out the /proc/cpuinfo
    file
"""
with open('/proc/cpuinfo') as f:
    for line in f:
        print(line.rstrip('\n'))
        
""" Print the model of your 
    processing units
"""
with open('/proc/cpuinfo') as f:
    for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
        if line.strip():
            if line.rstrip('\n').startswith('model name'):
                model_name = line.rstrip('\n').split(':')[1]
                print(model_name)

""" Find the real bit architecture
"""
with open('/proc/cpuinfo') as f:
    for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
        if line.strip():
            if line.rstrip('\n').startswith('flags') \
                    or line.rstrip('\n').startswith('Features'):
                if 'lm' in line.rstrip('\n').split():
                    print('64-bit')
                else:
                    print('32-bit')
                    
"""
/proc/cpuinfo as a Python dict
"""
def cpuinfo():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}
 
    '''
 
    cpuinfo=OrderedDict()
    procinfo=OrderedDict()
 
    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
                # Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
 
    return cpuinfo
"""
get memory info
"""
def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()
 
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo
    
"""
get network devices
"""
def netdevs(iface=None):
    ''' RX and TX bytes for each of the network devices '''
 
    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
 
    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if not iface:
            if line[0].strip() != 'lo':
                device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0), 
                                                    float(line[1].split()[8])/(1024.0*1024.0))
        else:
            if line[0].strip() == iface:
                device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0), 
                                                    float(line[1].split()[8])/(1024.0*1024.0))    
    return device_data
"""
get process info
"""
def process_list():
 
    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)
 
    return pids
    
# Add any other device pattern to read from
dev_pattern = ['sd.*','mmcblk*']
 
def size(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')
 
    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

"""
get all block devices
"""
def detect_devs():
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                print('Device:: {0}, Size:: {1} GiB'.format(device, size(device)))

def read_login_defs():
 
    uid_min = None
    uid_max = None
 
    if os.path.exists('/etc/login.defs'):
        with open('/etc/login.defs') as f:
            login_data = f.readlines()
 
        for line in login_data:
            if line.startswith('UID_MIN'):
                uid_min = int(line.split()[1].strip())
 
            if line.startswith('UID_MAX'):
                uid_max = int(line.split()[1].strip())
 
    return uid_min, uid_max
 
# Get the users from /etc/passwd
def getusers(no_system=False):
 
    uid_min, uid_max = read_login_defs()
 
    if uid_min is None:
        uid_min = 1000
    if uid_max is None:
        uid_max = 60000
 
    users = pwd.getpwall()
    for user in users:
        if no_system:
            if user.pw_uid >= uid_min and user.pw_uid <= uid_max:
                print('{0}:{1}'.format(user.pw_name, user.pw_shell))
        else:
            print('{0}:{1}'.format(user.pw_name, user.pw_shell))
    
if __name__=='__main__':
    cpuinfo = cpuinfo()
    for processor in cpuinfo.keys():
        print(cpuinfo[processor]['model name'])
        
    meminfo = meminfo()
    print('Total memory: {0}'.format(meminfo['MemTotal']))
    print('Free memory: {0}'.format(meminfo['MemFree']))
    
    netdevs = netdevs()
    for dev in netdevs.keys():
        print('{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))<span style="font-family:'sans serif', tahoma, verdana, helvetica;font-size:10pt;line-height:1.5;"> </span>
        
    pids = process_list()
    print('Total number of running processes:: {0}'.format(len(pids)))
    
    detect_devs()
    
    parser = argparse.ArgumentParser(description='User/Password Utility')
 
    parser.add_argument('--no-system', action='store_true',dest='no_system',
                        default = False, help='Specify to omit system users')
 
    args = parser.parse_args()
    getusers(args.no_system)
    
    parser = argparse.ArgumentParser(description='Network Interface Usage Monitor')
    parser.add_argument('-i','--interface', dest='iface',
                        help='Network interface')
 
    args = parser.parse_args()
 
    netdevs = netdevs(iface = args.iface)
    for dev in netdevs.keys():
        print('{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))
